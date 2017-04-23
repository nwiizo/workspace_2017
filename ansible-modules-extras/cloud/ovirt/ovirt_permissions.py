#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Red Hat, Inc.
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#

try:
    import ovirtsdk4.types as otypes
except ImportError:
    pass

import traceback

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.ovirt import (
    BaseModule,
    check_sdk,
    create_connection,
    equal,
    follow_link,
    get_link_name,
    ovirt_full_argument_spec,
    search_by_attributes,
    search_by_name,
)


ANSIBLE_METADATA = {'status': 'preview',
                    'supported_by': 'community',
                    'version': '1.0'}

DOCUMENTATION = '''
---
module: ovirt_permissions
short_description: "Module to manage permissions of users/groups in oVirt"
version_added: "2.3"
author: "Ondra Machacek (@machacekondra)"
description:
    - "Module to manage permissions of users/groups in oVirt"
options:
    role:
        description:
            - "Name of the the role to be assigned to user/group on specific object."
        default: UserRole
    state:
        description:
            - "Should the permission be present/absent."
        choices: ['present', 'absent']
        default: present
    object_id:
        description:
            - "ID of the object where the permissions should be managed."
    object_name:
        description:
            - "Name of the object where the permissions should be managed."
    object_type:
        description:
            - "The object where the permissions should be managed."
        default: 'virtual_machine'
        choices: [
            'data_center',
            'cluster',
            'host',
            'storage_domain',
            'network',
            'disk',
            'vm',
            'vm_pool',
            'template',
        ]
    user_name:
        description:
            - "Username of the the user to manage. In most LDAPs it's I(uid) of the user, but in Active Directory you must specify I(UPN) of the user."
    group_name:
        description:
            - "Name of the the group to manage."
    authz_name:
        description:
            - "Authorization provider of the user/group. In previous versions of oVirt known as domain."
        required: true
        aliases: ['domain']
    namespace:
        description:
            - "Namespace of the authorization provider, where user/group resides."
        required: false
extends_documentation_fragment: ovirt
'''

EXAMPLES = '''
# Examples don't contain auth parameter for simplicity,
# look at ovirt_auth module to see how to reuse authentication:

# Add user user1 from authorization provider example.com-authz
- ovirt_permissions:
    user_name: user1
    authz_name: example.com-authz
    object_type: vm
    object_name: myvm
    role: UserVmManager

# Remove permission from user
- ovirt_permissions:
    state: absent
    user_name: user1
    authz_name: example.com-authz
    object_type: cluster
    object_name: mycluster
    role: ClusterAdmin
'''

RETURN = '''
id:
    description: ID of the permission which is managed
    returned: On success if permission is found.
    type: str
    sample: 7de90f31-222c-436c-a1ca-7e655bd5b60c
permission:
    description: "Dictionary of all the permission attributes. Permission attributes can be found on your oVirt instance
                  at following url: https://ovirt.example.com/ovirt-engine/api/model#types/permission."
    returned: On success if permission is found.
'''


def _objects_service(connection, object_type):
    return getattr(
        connection.system_service(),
        '%ss_service' % object_type,
        None,
    )()


def _object_service(connection, module):
    object_type = module.params['object_type']
    objects_service = _objects_service(connection, object_type)

    object_id = module.params['object_id']
    if object_id is None:
        sdk_object = search_by_name(objects_service, module.params['object_name'])
        if sdk_object is None:
            raise Exception(
                "'%s' object '%s' was not found." % (
                    module.params['object_type'],
                    module.params['object_name']
                )
            )
        object_id = sdk_object.id

    return objects_service.service(object_id)


def _permission(module, permissions_service, connection):
    for permission in permissions_service.list():
        user = follow_link(connection, permission.user)
        if (
            equal(module.params['user_name'], user.principal if user else None) and
            equal(module.params['group_name'], get_link_name(connection, permission.group)) and
            equal(module.params['role'], get_link_name(connection, permission.role))
        ):
            return permission


class PermissionsModule(BaseModule):

    def _user(self):
        user = search_by_attributes(
            self._connection.system_service().users_service(),
            usrname="{name}@{authz_name}".format(
                name=self._module.params['user_name'],
                authz_name=self._module.params['authz_name'],
            ),
        )
        if user is None:
            raise Exception("User '%s' was not found." % self._module.params['user_name'])
        return user

    def _group(self):
        groups = self._connection.system_service().groups_service().list(
            search="name={name}".format(
                name=self._module.params['group_name'],
            )
        )

        # If found more groups, filter them by namespace and authz name:
        # (filtering here, as oVirt backend doesn't support it)
        if len(groups) > 1:
            groups = [
                g for g in groups if (
                    equal(self._module.params['namespace'], g.namespace) and
                    equal(self._module.params['authz_name'], g.domain.name)
                )
            ]
        if not groups:
            raise Exception("Group '%s' was not found." % self._module.params['group_name'])
        return groups[0]

    def build_entity(self):
        entity = self._group() if self._module.params['group_name'] else self._user()

        return otypes.Permission(
            user=otypes.User(
                id=entity.id
            ) if self._module.params['user_name'] else None,
            group=otypes.Group(
                id=entity.id
            ) if self._module.params['group_name'] else None,
            role=otypes.Role(
                name=self._module.params['role']
            ),
        )


def main():
    argument_spec = ovirt_full_argument_spec(
        state=dict(
            choices=['present', 'absent'],
            default='present',
        ),
        role=dict(default='UserRole'),
        object_type=dict(
            default='virtual_machine',
            choices=[
                'data_center',
                'cluster',
                'host',
                'storage_domain',
                'network',
                'disk',
                'vm',
                'vm_pool',
                'template',
            ]
        ),
        authz_name=dict(required=True, aliases=['domain']),
        object_id=dict(default=None),
        object_name=dict(default=None),
        user_name=dict(rdefault=None),
        group_name=dict(default=None),
        namespace=dict(default=None),
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )
    check_sdk(module)

    if module.params['object_name'] is None and module.params['object_id'] is None:
        module.fail_json(msg='"object_name" or "object_id" is required')

    if module.params['user_name'] is None and module.params['group_name'] is None:
        module.fail_json(msg='"user_name" or "group_name" is required')

    try:
        connection = create_connection(module.params.pop('auth'))
        permissions_service = _object_service(connection, module).permissions_service()
        permissions_module = PermissionsModule(
            connection=connection,
            module=module,
            service=permissions_service,
        )

        permission = _permission(module, permissions_service, connection)
        state = module.params['state']
        if state == 'present':
            ret = permissions_module.create(entity=permission)
        elif state == 'absent':
            ret = permissions_module.remove(entity=permission)

        module.exit_json(**ret)
    except Exception as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())
    finally:
        connection.close(logout=False)


if __name__ == "__main__":
    main()
