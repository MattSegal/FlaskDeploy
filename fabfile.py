import sys
import json
from fabric.api import env, task

import pre_deploy
import server
host = ""

def deploy(proj):
    project_file = "projects\\{0}.json".format(proj)

    with open(project_file,"r") as f:
        apps = json.load(f)

    for app in apps:
        pre_deploy.stage_app(app["name"])

    server.setup(apps,host)

# This is a hack because fabric is being a dick
def pi():
    host_name = "pi"
    set_host(host_name)

def test():
    host_name = "test"
    set_host(host_name)
    
def set_host(host_name):
    host_file = "hosts\\{0}.json".format(host_name)
    with open(host_file,"r") as f:
        global host
        host = json.load(f) 
    env.hosts = ["{username}@{url}:{port}".format(**host)]
    env.reject_unknown_hosts = False # default
    if "password" in host.keys():
        env.password = host["password"]