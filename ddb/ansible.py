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
    src:
        description:
            - The location of the flat file you wish to modify
        required: true
    
    name:
        description:
            - The name of this table as used in the sql interface
        required: true

    columns:
        description:
            - An ordered list of columns present in the flat file
        required: optional

    header_on:
        description:
            - columns names are populated from this line in the file
        required: optional
        default: None

    data_on:
        description:
            - the line of the file to start reading data
        required: optional
        default: 1

    delimiter:
        description:
            - the seperator used for columns
        required: optional
        default: ','


    quoted:
        description:
            - the quoted identifier used for columns
        required: optional
        default: None

    query:
        description:
            - the query to run agains the table
            - select, update, insert, delete are all valid queries
            - if an action is taken, exit is true
            - if an action is not taken exit is false
            - such as select from test where id=1
            - if results are present, then exit is true
            - if results are not present, then exit is false
        required: true
        
    query: 'SELECT id from test WHERE id=1'


extends_documentation_fragment:
    - 

author:
    - Charles Watkins (@chris17453)
'''

EXAMPLES = '''
- name: Update csv with data
  ddb:
    - src: /home/nd/repos/chris17453/ddb/ddb/test/MOCK_DATA.csv
    name: test
    columns:
        - id
        - first_name
        - last_name
        - email
        - gender
        - ip_address
    header_on: 1
    data_on: 1
    delimiter: ':'
    quoted: '"'

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
        name=dict(type='str', required=True),
        new=dict(type='bool', required=False, default=False)
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

def main():
    run_module()

if __name__ == '__main__':
    main()