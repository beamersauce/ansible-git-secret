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
    dir:
        description:
            - Which directory to perform the git secret commands in, must be `git init` and `git secret init` prior to running this task
        required: true
    private_key:
        description:
            - Path to private GPG key to import to keychain, if not specified will just use keychain as is.
        required: false
    passphrase:
        description:
            - (decrypt only) Passphrase for the GPG used to decrypt, will be passed on the CLI to the git secret command
        required: false

author:
    - Caleb Burch (@beamersauce)
'''

EXAMPLES = '''
# Encrypt a directory
- name: encrypt w/ unused passphrase var filled in
  gitsecret:
    action: encrypt
    dir: /tmp/gitsectest
    private_key: caleb_pri.gpg

# Decrypt a directory with supplied passphrase
- name: decrypt (passphrase supplied via task)
  gitsecret:
    action: decrypt
    dir: /tmp/gitsectest
    private_key: caleb_pri.gpg
    passphrase: '123qwe'
'''

RETURN = '''
message:
    description: The output of the git secret command
    type: str
    returned: always
'''

from ansible.module_utils.basic import AnsibleModule

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        action=dict(type='str', required=True, choices=['encrypt','decrypt']),
        dir=dict(type='str', required=True),
        private_key=dict(type='str', required=False),
        passphrase=dict(type='str', required=False, no_log=True)
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

def main():
    run_module()

if __name__ == '__main__':
    main()