**Flask Deploy**

This is a set of script that I use to deploy my Flask apps to their host webservers.

**Functionality**

Sets up a fresh Linux box to use apache2 and mod-wsgi, then deploys a set of Flask apps to the server, handling configuration and SFTP. The goal is for deployment from source code to the server to be a single command proccess.

**Goals**

Setup webwalrus and deploy it to vagrant server

**To Do**

Support config.prod transforms
Add post deployment scripts
Add support for MYSQL
Seperate setup and deploy actions
