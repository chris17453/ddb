#!/usr/bin/python

# Copyright: (c) 2018, Charles Watkins <chris17453@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: ddb

short_description: SQL interface for flat files

version_added: "2.7"

description:
    - "A serviceless SQL interface for crud operations on flat files"

options:
    query:
        description:
            - the database query to run 
            - select, update, insert, delete are all valid queries
            
        required: true
        
    query: 'SELECT id from test WHERE id=1'


extends_documentation_fragment:
    - 

author:
    - Charles Watkins (@chris17453)
'''

EXAMPLES = '''
- name: Update csv with data
  query: 'SELECT id from test WHERE id=1'
'''

EXAMPLES = '''
- name: Update csv with data
  query: 'SELECT id from test WHERE id=1'
'''


RETURN = '''
original_message:
    description: The original name param that was passed in
    type: str
message:
    description: The output message that the sample module generates
'''

from ansible.module_utils.basic import AnsibleModule

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        query=dict(type='str', required=True),
    )

    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        return result

    result['original_message'] = module.params['name']
    result['message'] = 'goodbye'

    if module.params['new']:
        result['changed'] = True

    if module.params['name'] == 'fail me':
        module.fail_json(msg='You requested this to fail', **result)

    module.exit_json(**result)

