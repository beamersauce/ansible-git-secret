#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'beamersauce'
}

DOCUMENTATION = '''
---
module: git-secret

short_description: Wrapper for git-secret https://git-secret.io/ functionality

version_added: "2.4"

description:
    - "Wraps some of the functionality of git-secret https://git-secret.io/.  Requires git secrets to be installed on host system."

options:
    action:
        description:
            - Which action to perform, encrypt or decrypt
        required: true
    private_key:
        description:
            - Path to private GPG key to import to keychain, if not specified will just use keychain as is.
        required: false

author:
    - Caleb Burch (@beamersauce)
'''

EXAMPLES = '''
# Pass in a message
- name: Test with a message
  my_test:
    name: hello world

# pass in a message and have changed true
- name: Test with a message and changed output
  my_test:
    name: hello world
    new: true

# fail the module
- name: Test failure of the module
  my_test:
    name: fail me
'''

RETURN = '''
original_message:
    description: The original name param that was passed in
    type: str
    returned: always
message:
    description: The output message that the test module generates
    type: str
    returned: always
'''

from ansible.module_utils.basic import AnsibleModule

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        action=dict(type='str', required=True),
        dir=dict(type='str', required=True),
        private_key=dict(type='str', required=False),
        passphrase=dict(type='str', required=False)
    )

    result = dict(
        changed=False,
        message=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    #checkmode just responds with git secret whoknows
    if module.check_mode:
        r = module.run_command('git secret whoknows', cwd=module.params['dir'])
        result['message'] = r
        module.exit_json(**result)

    #validate inputs
    #TODO can we do this in a more elegant way (an enum of potential values or something?)
    #TODO should this happen before the above checkmode logic?
    if module.params['action'] != 'encrypt' and module.params['action'] != 'decrypt':
        module.fail_json(msg="action must be 'encrypt' or 'decrypt'", **result)

    # was not check mode, attempt to encrypt or decrypt based on action
    result['changed'] = True
    if module.params['action'] == 'encrypt':
        r = module.run_command('git secret hide', cwd=module.params['dir'])
        result['message'] = r 
    if module.params['action'] == 'decrypt':
        cmd = 'git secret reveal -f'
        if module.params['passphrase']:
            cmd += ' -p ' + module.params['passphrase']
        r = module.run_command(cmd, cwd=module.params['dir'])
        result['message'] = r      
    
    # return results (success)
    module.exit_json(**result)

    #TODO - update the docs
    #TODO - how to handle verbosity
    #TODO - how to hide passphrase from any output (can I mark it as a secure value or something in the input dict)

def main():
    run_module()

if __name__ == '__main__':
    main()