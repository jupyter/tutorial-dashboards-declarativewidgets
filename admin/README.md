Notes for setting up and running the tutorial talk.

## Setup environment

Git clone this repo.

```
git clone https://github.com/ibm-et/pydata2016.git
cd pydata2016/admin
```

Build the admin Docker image, which runs a notebook server to host the Slack VM
assignment bot notebook.

```
docker-compose build
```

Run the `pydata2016-notebook` container.

```
export SOFTLAYER_USER=<user>
export SOFTLAYER_API_KEY=<api_key>
export SLACK_TOKEN=<token>
docker-compose up -d
```

## Pre-Session

0. Enter python environment to be able to run the `vms.py` admin script.

  If you have conda installed:

  ```
  conda env create --file environment.yml
  source activate pydata
  ```

  OR, you can run the `vms.py` script from within the `pydata2016-notebook` container:

  ```
  docker exec -it pydata2016-notebook /bin/bash
  ```

1. Use `vms.py` script to start `N` VMs and enable DNS for each VM. (They're separate commands!)

  ```
  ./vms.py create -s 2 -n 10
  ./vms.py dns add -s 2 -n 10
  ```

2. Get a list of the credentials for all of the VMs and save it off somewhere locally.

  ```
  ./vms.py list --creds
  ```

3. Use the `vms.py` script to assign a VM to each of the session leaders.
4. Make sure the `notebooks/inspection/inspection_dashboard_complete.ipynb` notebook works on each of the leader VMs.
5. Run `pydata2016-notebook` container for VM assignment bot.
6. Open the `slack_vmbot.ipynb` in the notebook server.
7. Run the notebook top to bottom.
8. Flip to dashboard mode to watch messages and assignment.
9. Try requesting a VM from the bot to make sure it works.

## During Session

1. Open the `slack_vmbot.ipynb` in the notebook server.
2. Flip `DEV` to false so that VMs are permanently assigned.
3. Change the `TRIGGER` keyword to something only people in the room will hear.
3. Run the notebook top to bottom.
4. Flip to dashboard mode to watch messages and assignment.
5. Once everyone has a VM, close and halt the bot notebook.

If anyone gets a bunk VM, use the `vms.py` script to manually assign them to another and get the creds. (Or, use the backup list of creds from step #2 in the pre-session section.)

## Post-Session

1. Wait a week.
2. Use the `vms.py` script to cancel all of the VMs.
3. Revoke the Slack bot API key for good measure.
