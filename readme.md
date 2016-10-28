**Flask Deploy**

This is a set of script that I use to deploy my Flask apps to their host webservers.

**Functionality**

Sets up a fresh Linux box to use apache2 and mod-wsgi, then deploys a set of Flask apps to the server, handling configuration and SFTP. The goal is for deployment from source code to a brand new server to be a single command task.

Eg.
> .\deploy.ps1 -ProjectName test -HostName test

**Features**

Files named *.prod will be transformed to * and stomp existing files.
Possible to deploy specific branches (applied to whole project)

**Goals**

Setup webwalrus and deploy it to vagrant server

**To Do**
  
* Remove security holes - it is probably a dumb idea to list IPs in source
* Add support for MYSQL
* Add MYSQL database backup and restore functionality
* Add SSH setup