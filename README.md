# to setup dev env

1. follow setup in https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html
    1. to get it working I had to remove the ansible/venv/lib/python3.6/site-package/MarkupSafe-* dir during the step `pip isntall -r requirements.txt` and then rerun that command
2. from then on you only need to run
    1. `. venv/bin/activate`
    2. `. hacking/env-setup`
3. I may need to adapt these instructions when I move the module out of the ansible proj
4. To run a test you can run `ansible-playbook test.yaml -v`
