**Flask Deploy**

This is a set of scripts that I use to deploy my Flask apps to their host webservers. The goal is for deployment from source code to a brand new server to be a simple, repeatable, single command task.

Eg.
> .\deploy.ps1 -ProjectName test -HostName test (-BranchName dev)

**Functionality**

The app works as follows:
* Reads host metadata from .\hosts and app config data from .\projects
* Clones apps from parent directory (Eg. ..\my_flask_app) into .\staged_apps
* Prunes unwanted files
* Installs required debian packages on target host
* Installs required python packages on target host
* Configures Apache2 to host the installed Flask apps

**Flask App Project Structure**

This is the assumed project structure of Flask apps that this tool deploys
See [this repository](https://github.com/MattSegal/ChrisRoddWebsite) for an example of a compatible app.
```
.
├── app
│   └── __init__.py     (required)
│
├── wsgi.py             (required)
├── deploy.json         determines which files are pruned/deployed (required)
├── requirements.txt    python packages installed (required)
├── debian.txt          debian packages installed (required) 
├── config.py.prod      will be transformed to config.py
└── config.py           will be deleted
```

These scripts also assume the following relationship:
```
.
├── flask_deploy
│   ├── hosts
│   ├── pre_deploy
│   └── etc ... 
│
└── target_flask_app
    ├── app
    ├── wsgi.py
    └── etc ... 
```

**Goals**

Setup webwalrus and deploy it to vagrant server

**To Do**

* Remove security holes - it is probably a dumb idea to list IPs in source
* Add support for MYSQL
* Add MYSQL database backup and restore functionality
* Add SSH setup
* Add zip and transfer step to reduce deploy time

**Branching**

All new work should be done on dev and then merged into master when it seems to work ok. This is done so that there is always an easily accesible working instance of the app.

* master    - last working iteration, should work
* dev       - add new features, might not work
