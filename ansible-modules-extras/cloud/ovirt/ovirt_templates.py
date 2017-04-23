#!/usr/bin/pythonapi/
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

import time
import traceback

try:
    import ovirtsdk4.types as otypes
except ImportError:
    pass

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.ovirt import (
    BaseModule,
    check_sdk,
    create_connection,
    equal,
    get_dict_of_struct,
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
module: ovirt_templates
short_description: Module to manage virtual machine templates in oVirt
version_added: "2.3"
author: "Ondra Machacek (@machacekondra)"
description:
    - "Module to manage virtual machine templates in oVirt."
options:
    name:
        description:
            - "Name of the the template to manage."
        required: true
    state:
        description:
            - "Should the template be present/absent/exported/imported"
        choices: ['present', 'absent', 'exported', 'imported']
        default: present
    vm:
        description:
            - "Name of the VM, which will be used to create template."
    description:
        description:
            - "Description of the template."
    cpu_profile:
        description:
            - "CPU profile to be set to template."
    cluster:
        description:
            - "Name of the cluster, where template should be created/imported."
    exclusive:
        description:
            - "When C(state) is I(exported) this parameter indicates if the existing templates with the
               same name should be overwritten."
    export_domain:
        description:
            - "When C(state) is I(exported) or I(imported) this parameter specifies the name of the
               export storage domain."
    image_provider:
        description:
            - "When C(state) is I(imported) this parameter specifies the name of the image provider to be used."
    image_disk:
        description:
            - "When C(state) is I(imported) and C(image_provider) is used this parameter specifies the name of disk
               to be imported as template."
    storage_domain:
        description:
            - "When C(state) is I(imported) this parameter specifies the name of the destination data storage domain."
    clone_permissions:
        description:
            - "If I(True) then the permissions of the VM (only the direct ones, not the inherited ones)
            will be copied to the created template."
            - "This parameter is used only when C(state) I(present)."
        default: False
extends_documentation_fragment: ovirt
'''

EXAMPLES = '''
# Examples don't contain auth parameter for simplicity,
# look at ovirt_auth module to see how to reuse authentication:

# Create template from vm
- ovirt_templates:
    cluster: Default
    name: mytemplate
    vm: rhel7
    cpu_profile: Default
    description: Test

# Import template
- ovirt_templates:
  state: imported
  name: mytemplate
  export_domain: myexport
  storage_domain: mystorage
  cluster: mycluster

# Remove template
- ovirt_templates:
    state: absent
    name: mytemplate
'''

RETURN = '''
id:
    description: ID of the template which is managed
    returned: On success if template is found.
    type: str
    sample: 7de90f31-222c-436c-a1ca-7e655bd5b60c
template:
    description: "Dictionary of all the template attributes. Template attributes can be found on your oVirt instance
                  at following url: https://ovirt.example.com/ovirt-engine/api/model#types/template."
    returned: On success if template is found.
'''


class TemplatesModule(BaseModule):

    def build_entity(self):
        return otypes.Template(
            name=self._module.params['name'],
            cluster=otypes.Cluster(
                name=self._module.params['cluster']
            ) if self._module.params['cluster'] else None,
            vm=otypes.Vm(
                name=self._module.params['vm']
            ) if self._module.params['vm'] else None,
            description=self._module.params['description'],
            cpu_profile=otypes.CpuProfile(
                id=search_by_name(
                    self._connection.system_service().cpu_profiles_service(),
                    self._module.params['cpu_profile'],
                ).id
            ) if self._module.params['cpu_profile'] else None,
        )

    def update_check(self, entity):
        return (
            equal(self._module.params.get('cluster'), get_link_name(self._connection, entity.cluster)) and
            equal(self._module.params.get('description'), entity.description) and
            equal(self._module.params.get('cpu_profile'), get_link_name(self._connection, entity.cpu_profile))
        )

    def _get_export_domain_service(self):
        provider_name = self._module.params['export_domain'] or self._module.params['image_provider']
        export_sds_service = self._connection.system_service().storage_domains_service()
        export_sd = search_by_name(export_sds_service, provider_name)
        if export_sd is None:
            raise ValueError(
                "Export storage domain/Image Provider '%s' wasn't found." % provider_name
            )

        return export_sds_service.service(export_sd.id)

    def post_export_action(self, entity):
        self._service = self._get_export_domain_service().templates_service()

    def post_import_action(self, entity):
        self._service = self._connection.system_service().templates_service()


def wait_for_import(module, templates_service):
    if module.params['wait']:
        start = time.time()
        timeout = module.params['timeout']
        poll_interval = module.params['poll_interval']
        while time.time() < start + timeout:
            template = search_by_name(templates_service, module.params['name'])
            if template:
                return template
            time.sleep(poll_interval)


def main():
    argument_spec = ovirt_full_argument_spec(
        state=dict(
            choices=['present', 'absent', 'exported', 'imported'],
            default='present',
        ),
        name=dict(default=None, required=True),
        vm=dict(default=None),
        description=dict(default=None),
        cluster=dict(default=None),
        cpu_profile=dict(default=None),
        disks=dict(default=[], type='list'),
        clone_permissions=dict(type='bool'),
        export_domain=dict(default=None),
        storage_domain=dict(default=None),
        exclusive=dict(type='bool'),
        image_provider=dict(default=None),
        image_disk=dict(default=None),
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )
    check_sdk(module)

    try:
        connection = create_connection(module.params.pop('auth'))
        templates_service = connection.system_service().templates_service()
        templates_module = TemplatesModule(
            connection=connection,
            module=module,
            service=templates_service,
        )

        state = module.params['state']
        if state == 'present':
            ret = templates_module.create(
                result_state=otypes.TemplateStatus.OK,
                clone_permissions=module.params['clone_permissions'],
            )
        elif state == 'absent':
            ret = templates_module.remove()
        elif state == 'exported':
            template = templates_module.search_entity()
            export_service = templates_module._get_export_domain_service()
            export_template = search_by_attributes(export_service.templates_service(), id=template.id)

            ret = templates_module.action(
                entity=template,
                action='export',
                action_condition=lambda t: export_template is None,
                wait_condition=lambda t: t is not None,
                post_action=templates_module.post_export_action,
                storage_domain=otypes.StorageDomain(id=export_service.get().id),
                exclusive=module.params['exclusive'],
            )
        elif state == 'imported':
            template = templates_module.search_entity()
            if template:
                ret = templates_module.create(
                    result_state=otypes.TemplateStatus.OK,
                )
            else:
                kwargs = {}
                if module.params['image_provider']:
                    kwargs.update(
                        disk=otypes.Disk(
                            name=module.params['image_disk']
                        ),
                        template=otypes.Template(
                            name=module.params['name'],
                        ),
                        import_as_template=True,
                    )

                if module.params['image_disk']:
                    # We need to refresh storage domain to get list of images:
                    templates_module._get_export_domain_service().images_service().list()

                    glance_service = connection.system_service().openstack_image_providers_service()
                    image_provider = search_by_name(glance_service, module.params['image_provider'])
                    images_service = glance_service.service(image_provider.id).images_service()
                else:
                    images_service = templates_module._get_export_domain_service().templates_service()
                template_name = module.params['image_disk'] or module.params['name']
                entity = search_by_name(images_service, template_name)
                if entity is None:
                    raise Exception("Image/template '%s' was not found." % template_name)

                images_service.service(entity.id).import_(
                    storage_domain=otypes.StorageDomain(
                        name=module.params['storage_domain']
                    ) if module.params['storage_domain'] else None,
                    cluster=otypes.Cluster(
                        name=module.params['cluster']
                    ) if module.params['cluster'] else None,
                    **kwargs
                )
                template = wait_for_import(module, templates_service)
                ret = {
                    'changed': True,
                    'id': template.id,
                    'template': get_dict_of_struct(template),
                }

        module.exit_json(**ret)
    except Exception as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())
    finally:
        connection.close(logout=False)


if __name__ == "__main__":
    main()
