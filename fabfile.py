import sys
import json
import re
from StringIO import StringIO
from fabric.api import env, task, sudo

import pre_deploy
import server


assert env.host_name, "host_name value must be set."

# Load host data
host_file = "hosts\\{0}.json".format(env.host_name)
with open(host_file,"r") as f:
    host = json.load(f)
env.hosts = ["{username}@{url}:{port}".format(**host)]
env.reject_unknown_hosts = False # Default setting
if "password" in host.keys():
    env.password = host["password"]

def deploy():
    assert env.project_name, "project_name value must be set."
    assert env.branch_name, "branch_name value must be set." # Currently unused

    # Load application data
    project_file = "projects\\{0}.json".format(env.project_name)
    with open(project_file,"r") as f:
        apps = json.load(f)

    # Stage applications
    for app in apps:
        # use branch_name here
        pre_deploy.stage_app(app["name"])

    # Deploy
    server.setup(apps,host)

def get_error_logs(num_lines=10):
    error_log_path = "/var/log/apache2/error.log"
    outputIO = StringIO()
    sudo("tail {0} --lines={1} --verbose".format(error_log_path,num_lines),stdout=outputIO)
    fabric_output_regex = '(\[\S+\]) out: '
    output = outputIO.getvalue()
    outputIO.close()
    output = re.sub(fabric_output_regex,'',output)
    print output