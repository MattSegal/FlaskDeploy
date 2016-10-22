**Flask Deploy**

This is a set of script that I use to deploy my Flask apps to their host webservers.

**Functionality**

Sets up a fresh Linux box to use apache2 and mod-wsgi, then deploys a set of Flask apps to the server, handling configuration and SFTP. The goal is for deployment from source code to a brand new server to be a single command task.

Eg.
> .\deploy.ps1 -ProjectName chris -HostName test

**Goals**

Setup webwalrus and deploy it to vagrant server

**To Do**
  
* Remove and change application secret keys, add to non commited *.prod config files. Add secret key to each Flask app.
* Remove security holes - is it a dumb idea to list IPs in source?
* Ability to target specific branches
* Support config.prod transforms
* Add post deployment scripts
* Add support for MYSQL
* Add SSH setup.