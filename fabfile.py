import sys
import json
from fabric.api import env, task

import pre_deploy
import server

assert env.branch_name, "branch_name value must be set." # Currently unused
assert env.project_name, "project_name value must be set."
assert env.host_name, "host_name value must be set."

# Load host data
host_file = "hosts\\{0}.json".format(env.host_name)
with open(host_file,"r") as f:
    host = json.load(f)
env.hosts = ["{username}@{url}:{port}".format(**host)]
env.reject_unknown_hosts = False # Default setting
if "password" in host.keys():
    env.password = host["password"]

# Load application data
project_file = "projects\\{0}.json".format(env.project_name)
with open(project_file,"r") as f:
    apps = json.load(f)


def deploy():
    # Stage applications
    for app in apps:
        # use branch_name here
        pre_deploy.stage_app(app["name"])

    # Deploy
    server.setup(apps,host)