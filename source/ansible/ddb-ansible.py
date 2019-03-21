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
        query="",
        affected_rows=0,
        data_lenght=0,
        column_length=0,
        data=None,
        error=None,
        success=False
    )


    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )
    e=engine()
    results=e.query(module.params['query'])
    result['success']=results.success
    result['affected_rows']=results.affected_rows
    result['data_lenght']=results.data_lenght
    result['column_length']=results.column_length
    result['data']=results.data
    result['error']=results.error
    result['success']=results.success

    if module.check_mode:
        return result


    if results.affected_rows>0:
        result['changed'] = True

    if results.error:
        module.fail_json(msg='Query failed', **result)

    module.exit_json(**result)

