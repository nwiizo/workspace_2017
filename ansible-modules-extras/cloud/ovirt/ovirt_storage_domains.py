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

    from ovirtsdk4.types import StorageDomainStatus as sdstate
except ImportError:
    pass

import traceback

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.ovirt import (
    BaseModule,
    check_sdk,
    create_connection,
    ovirt_full_argument_spec,
    search_by_name,
    wait,
)


ANSIBLE_METADATA = {'status': 'preview',
                    'supported_by': 'community',
                    'version': '1.0'}

DOCUMENTATION = '''
---
module: ovirt_storage_domains
short_description: Module to manage storage domains in oVirt
version_added: "2.3"
author: "Ondra Machacek (@machacekondra)"
description:
    - "Module to manage storage domains in oVirt"
options:
    name:
        description:
            - "Name of the the storage domain to manage."
    state:
        description:
            - "Should the storage domain be present/absent/maintenance/unattached"
        choices: ['present', 'absent', 'maintenance', 'unattached']
        default: present
    description:
        description:
            - "Description of the storage domain."
    comment:
        description:
            - "Comment of the storage domain."
    data_center:
        description:
            - "Data center name where storage domain should be attached."
    domain_function:
        description:
            - "Function of the storage domain."
        choices: ['data', 'iso', 'export']
        default: 'data'
        aliases:  ['type']
    host:
        description:
            - "Host to be used to mount storage."
    nfs:
        description:
            - "Dictionary with values for NFS storage type:"
            - "C(address) - Address of the NFS server. E.g.: myserver.mydomain.com"
            - "C(path) - Path of the mount point. E.g.: /path/to/my/data"
    iscsi:
        description:
            - "Dictionary with values for iSCSI storage type:"
            - "C(address) - Address of the iSCSI storage server."
            - "C(port) - Port of the iSCSI storage server."
            - "C(target) - iSCSI target."
            - "C(lun_id) - LUN id."
            - "C(username) - Username to be used to access storage server."
            - "C(password) - Password of the user to be used to access storage server."
    posixfs:
        description:
            - "Dictionary with values for PosixFS storage type:"
            - "C(path) - Path of the mount point. E.g.: /path/to/my/data"
            - "C(vfs_type) - Virtual File System type."
            - "C(mount_options) - Option which will be passed when mounting storage."
    glusterfs:
        description:
            - "Dictionary with values for GlusterFS storage type:"
            - "C(address) - Address of the NFS server. E.g.: myserver.mydomain.com"
            - "C(path) - Path of the mount point. E.g.: /path/to/my/data"
            - "C(mount_options) - Option which will be passed when mounting storage."
    fcp:
        description:
            - "Dictionary with values for fibre channel storage type:"
            - "C(address) - Address of the fibre channel storage server."
            - "C(port) - Port of the fibre channel storage server."
            - "C(lun_id) - LUN id."
    destroy:
        description:
            - "If I(True) storage domain metadata won't be cleaned, and user have to clean them manually."
            - "This parameter is relevant only when C(state) is I(absent)."
    format:
        description:
            - "If I(True) storage domain will be removed after removing it from oVirt."
            - "This parameter is relevant only when C(state) is I(absent)."
extends_documentation_fragment: ovirt
'''

EXAMPLES = '''
# Examples don't contain auth parameter for simplicity,
# look at ovirt_auth module to see how to reuse authentication:

# Add data NFS storage domain
- ovirt_storage_domains:
    name: data_nfs
    host: myhost
    data_center: mydatacenter
    nfs:
      address: 10.34.63.199
      path: /path/data

# Add data iSCSI storage domain:
- ovirt_storage_domains:
    name: data_iscsi
    host: myhost
    data_center: mydatacenter
    iscsi:
      target: iqn.2016-08-09.domain-01:nickname
      lun_id: 1IET_000d0002
      address: 10.34.63.204

# Import export NFS storage domain:
- ovirt_storage_domains:
    domain_function: export
    host: myhost
    data_center: mydatacenter
    nfs:
      address: 10.34.63.199
      path: /path/export

# Create ISO NFS storage domain
- ovirt_storage_domains:
    name: myiso
    domain_function: iso
    host: myhost
    data_center: mydatacenter
    nfs:
      address: 10.34.63.199
      path: /path/iso

# Remove storage domain
- ovirt_storage_domains:
    state: absent
    name: mystorage_domain
    format: true
'''

RETURN = '''
id:
    description: ID of the storage domain which is managed
    returned: On success if storage domain is found.
    type: str
    sample: 7de90f31-222c-436c-a1ca-7e655bd5b60c
storage domain:
    description: "Dictionary of all the storage domain attributes. Storage domain attributes can be found on your oVirt instance
                  at following url: https://ovirt.example.com/ovirt-engine/api/model#types/storage_domain."
    returned: On success if storage domain is found.
'''


class StorageDomainModule(BaseModule):

    def _get_storage_type(self):
        for sd_type in ['nfs', 'iscsi', 'posixfs', 'glusterfs', 'fcp']:
            if self._module.params.get(sd_type) is not None:
                return sd_type

    def _get_storage(self):
        for sd_type in ['nfs', 'iscsi', 'posixfs', 'glusterfs', 'fcp']:
            if self._module.params.get(sd_type) is not None:
                return self._module.params.get(sd_type)

    def _login(self, storage_type, storage):
        if storage_type == 'iscsi':
            hosts_service = self._connection.system_service().hosts_service()
            host = search_by_name(hosts_service, self._module.params['host'])
            hosts_service.host_service(host.id).iscsi_login(
                iscsi=otypes.IscsiDetails(
                    username=storage.get('username'),
                    password=storage.get('password'),
                    address=storage.get('address'),
                    target=storage.get('target'),
                ),
            )

    def build_entity(self):
        storage_type = self._get_storage_type()
        storage = self._get_storage()
        self._login(storage_type, storage)

        return otypes.StorageDomain(
            name=self._module.params['name'],
            description=self._module.params['description'],
            comment=self._module.params['comment'],
            type=otypes.StorageDomainType(
                self._module.params['domain_function']
            ),
            host=otypes.Host(
                name=self._module.params['host'],
            ),
            storage=otypes.HostStorage(
                type=otypes.StorageType(storage_type),
                logical_units=[
                    otypes.LogicalUnit(
                        id=storage.get('lun_id'),
                        address=storage.get('address'),
                        port=storage.get('port', 3260),
                        target=storage.get('target'),
                        username=storage.get('username'),
                        password=storage.get('password'),
                    ),
                ] if storage_type in ['iscsi', 'fcp'] else None,
                mount_options=storage.get('mount_options'),
                vfs_type=storage.get('vfs_type'),
                address=storage.get('address'),
                path=storage.get('path'),
            )
        )

    def _attached_sds_service(self):
        # Get data center object of the storage domain:
        dcs_service = self._connection.system_service().data_centers_service()
        dc = search_by_name(dcs_service, self._module.params['data_center'])
        if dc is None:
            return

        dc_service = dcs_service.data_center_service(dc.id)
        return dc_service.storage_domains_service()

    def _maintenance(self, storage_domain):
        attached_sds_service = self._attached_sds_service()
        if attached_sds_service is None:
            return

        attached_sd_service = attached_sds_service.storage_domain_service(storage_domain.id)
        attached_sd = attached_sd_service.get()

        if attached_sd and attached_sd.status != sdstate.MAINTENANCE:
            if not self._module.check_mode:
                attached_sd_service.deactivate()
            self.changed = True

            wait(
                service=attached_sd_service,
                condition=lambda sd: sd.status == sdstate.MAINTENANCE,
                wait=self._module.params['wait'],
                timeout=self._module.params['timeout'],
            )

    def _unattach(self, storage_domain):
        attached_sds_service = self._attached_sds_service()
        if attached_sds_service is None:
            return

        attached_sd_service = attached_sds_service.storage_domain_service(storage_domain.id)
        attached_sd = attached_sd_service.get()

        if attached_sd and attached_sd.status == sdstate.MAINTENANCE:
            if not self._module.check_mode:
                # Detach the storage domain:
                attached_sd_service.remove()
            self.changed = True
            # Wait until storage domain is detached:
            wait(
                service=attached_sd_service,
                condition=lambda sd: sd is None,
                wait=self._module.params['wait'],
                timeout=self._module.params['timeout'],
            )

    def pre_remove(self, storage_domain):
        # Before removing storage domain we need to put it into maintenance state:
        self._maintenance(storage_domain)

        # Before removing storage domain we need to detach it from data center:
        self._unattach(storage_domain)

    def post_create_check(self, sd_id):
        storage_domain = self._service.service(sd_id).get()
        self._service = self._attached_sds_service()

        # If storage domain isn't attached, attach it:
        attached_sd_service = self._service.service(storage_domain.id)
        if attached_sd_service.get() is None:
            self._service.add(
                otypes.StorageDomain(
                    id=storage_domain.id,
                ),
            )
            self.changed = True
            # Wait until storage domain is in maintenance:
            wait(
                service=attached_sd_service,
                condition=lambda sd: sd.status == sdstate.ACTIVE,
                wait=self._module.params['wait'],
                timeout=self._module.params['timeout'],
            )

    def unattached_pre_action(self, storage_domain):
        self._service = self._attached_sds_service(storage_domain)
        self._maintenance(self._service, storage_domain)


def failed_state(sd):
    return sd.status in [sdstate.UNKNOWN, sdstate.INACTIVE]


def control_state(sd_module):
    sd = sd_module.search_entity()
    if sd is None:
        return

    sd_service = sd_module._service.service(sd.id)
    if sd.status == sdstate.LOCKED:
        wait(
            service=sd_service,
            condition=lambda sd: sd.status != sdstate.LOCKED,
            fail_condition=failed_state,
        )

    if failed_state(sd):
        raise Exception("Not possible to manage storage domain '%s'." % sd.name)
    elif sd.status == sdstate.ACTIVATING:
        wait(
            service=sd_service,
            condition=lambda sd: sd.status == sdstate.ACTIVE,
            fail_condition=failed_state,
        )
    elif sd.status == sdstate.DETACHING:
        wait(
            service=sd_service,
            condition=lambda sd: sd.status == sdstate.UNATTACHED,
            fail_condition=failed_state,
        )
    elif sd.status == sdstate.PREPARING_FOR_MAINTENANCE:
        wait(
            service=sd_service,
            condition=lambda sd: sd.status == sdstate.MAINTENANCE,
            fail_condition=failed_state,
        )


def main():
    argument_spec = ovirt_full_argument_spec(
        state=dict(
            choices=['present', 'absent', 'maintenance', 'unattached'],
            default='present',
        ),
        name=dict(required=True),
        description=dict(default=None),
        comment=dict(default=None),
        data_center=dict(required=True),
        domain_function=dict(choices=['data', 'iso', 'export'], default='data', aliases=['type']),
        host=dict(default=None),
        nfs=dict(default=None, type='dict'),
        iscsi=dict(default=None, type='dict'),
        posixfs=dict(default=None, type='dict'),
        glusterfs=dict(default=None, type='dict'),
        fcp=dict(default=None, type='dict'),
        destroy=dict(type='bool', default=False),
        format=dict(type='bool', default=False),
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )
    check_sdk(module)

    try:
        connection = create_connection(module.params.pop('auth'))
        storage_domains_service = connection.system_service().storage_domains_service()
        storage_domains_module = StorageDomainModule(
            connection=connection,
            module=module,
            service=storage_domains_service,
        )

        state = module.params['state']
        control_state(storage_domains_module)
        if state == 'absent':
            ret = storage_domains_module.remove(
                destroy=module.params['destroy'],
                format=module.params['format'],
                host=module.params['host'],
            )
        elif state == 'present':
            sd_id = storage_domains_module.create()['id']
            storage_domains_module.post_create_check(sd_id)
            ret = storage_domains_module.action(
                action='activate',
                action_condition=lambda s: s.status == sdstate.MAINTENANCE,
                wait_condition=lambda s: s.status == sdstate.ACTIVE,
                fail_condition=failed_state,
            )
        elif state == 'maintenance':
            sd_id = storage_domains_module.create()['id']
            storage_domains_module.post_create_check(sd_id)
            ret = storage_domains_module.action(
                action='deactivate',
                action_condition=lambda s: s.status == sdstate.ACTIVE,
                wait_condition=lambda s: s.status == sdstate.MAINTENANCE,
                fail_condition=failed_state,
            )
        elif state == 'unattached':
            ret = storage_domains_module.create()
            storage_domains_module.pre_remove(
                storage_domain=storage_domains_service.service(ret['id']).get()
            )
            ret['changed'] = storage_domains_module.changed

        module.exit_json(**ret)
    except Exception as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())
    finally:
        connection.close(logout=False)


if __name__ == "__main__":
    main()
