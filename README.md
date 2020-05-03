# host machine requirements

1. git secret - https://git-secret.io/git-secret-reveal
2. gnupg2 (gpg) - https://gnupg.org/

# to install this module

1. create a directory on your computer for ansible modules: `mkdir -p ~/.ansible/plugins/modules`
2. copy the module code into that directory: `cp gitsecret.py ~/.ansible/plugins/modules/gitsecret.py`

# to setup dev env

There might be better ways to manage this, https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html goes into further detail but an easy way to just 'run your code live' is:

1. create a directory on your computer for modules: `mkdir -p ~/.ansible/plugins/modules`
2. create a symlink for the module code into that directory: `ln -s gitsecret.py ~/.ansible/plugins/modules/gitsecret.py`
3. To run a test you can run `ansible-playbook test.yaml -v`

