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
```
.
├── app
│   └── __init__.py     _(required)_
│
├── wsgi.py             _(required)_
├── deploy.json         _determines which files are pruned/deployed (required)_
├── requirements.txt    _python packages installed (required)_
├── debian.txt          _debian packages installed (required)_ 
├── config.py.prod      _will be transformed to config.py_
└── config.py           _will be deleted_
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
