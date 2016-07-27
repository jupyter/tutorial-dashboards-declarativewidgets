Notes for setting up and running the tutorial talk.

## Pre-Session

1. Use `admin/vms.py` script to start X VMs and enable DNS for each VM. (They're separate commands!)
2. Get a list of the credentials for all of the VMs and save it off somewhere locally.
3. Use the `admin/vms.py` script to assign a VM to each of the session leaders.
4. Make sure the completed notebook works on each of the leader VMs.
5. Git clone this repo locally.
6. Run (TODO: conda or docker or something) locally to create the environment needed to run the VM assignment bot.
7. Run `jupyter notebook --notebook-path admin` in that environment from the root of the git sandbox.
8. Open the `admin/slack_vmbot.ipynb` in the notebook server.
9. Put in the secret Slack key, SoftLayer username, and SoftLayer password.
10. Run the notebook top to bottom.
11. Flip to dashboard mode to watch messages and assignment.
12. Try requesting a VM from the bot to make sure it works.

## During Session

1. Open the `admin/slack_vmbot.ipynb` in the notebook server.
2. Flip `DEV` to false so that VMs are permanently assigned.
3. Change the `TRIGGER` keyword to something only people in the room will hear.
3. Run the notebook top to bottom.
4. Flip to dashboard mode to watch messages and assignment.
5. Once everyone has a VM, close and halt the bot notebook.

If anyone gets a bunk VM, use the `admin/vms.py` script to manually assign them to another and get the creds. (Or, use the backup list of creds from step #2 in the pre-session section.)

## Post-Session

1. Wait a week.
2. Use the `admin/vms.py` script to cancel all of the VMs.
3. Revoke the Slack bot API key for good measure.
