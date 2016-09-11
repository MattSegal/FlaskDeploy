import os
import json
from fabric.api import task, env, run, sudo, put
import fabric.contrib.files as files

script_dir  = os.path.dirname(os.path.realpath(__file__))
bashrc_file = os.path.join(script_dir,os.path.normpath("./.bashrc"))
wsgi_file   = os.path.join(script_dir,"wsgi.py")
apache_file = os.path.join(script_dir,"apache.conf")
staged_apps_dir = os.path.join(script_dir,"..\staged_apps")

def setup(apps,host):
    set_bash_rc()
    set_timezone()
    install_packages()
    install_flask_apps(apps,host)
    # ssh stuff

def set_bash_rc():
    """ Upload shell preferences
    """
    src = bashrc_file
    dst = "/etc/bash.bashrc"
    put(local_path=src,remote_path=dst,use_sudo=True)
    dst = "~/.bashrc"
    put(local_path=src,remote_path=dst,use_sudo=True)

def set_timezone():
    """ Set timezone of server to AEST
    """
    localtime_path = "/etc/localtime"
    AEST_path = "/usr/share/zoneinfo/Australia/Victoria"
    sudo("rm {0}".format(localtime_path))
    sudo("ln -s {0} {1}".format(AEST_path,localtime_path))

def install_packages():
    packages = [
        "apache2",
        "libapache2-mod-wsgi",
        "python-pip",
        "curl"
    ]
    manager = PackageManager (packages)
    manager.ensure_installed()

def install_flask_apps(apps,host):

    packages = ["flask"]
    pip = Pip(packages)
    pip.ensure_installed()

    flask = FlaskProject(apps)

    apache = Apache()
    apache.disable_sites()
    apache.clean_config()

    flask.clean_target()

    for app in flask.get_apps():
        flask.upload_app(app)

        wsgi = WSGI(app)
        wsgi.upload()

        apache.add(app)

    apache.write_config(host)
    apache.enable_wsgi()
    apache.start_website()
    apache.restart()

class FlaskProject:
    def __init__(self,apps):
        self.apps = [app for app in apps if app["deploy"]]
        for app in self.apps:
            assert app.keys().sort() == [u'name',u'sub_url',u'path','deploy'].sort()

    def clean_target(self):
        sudo("rm -rf /var/www/*")

    def upload_app(self,app):
        assert "path" in app.keys()
        assert "name" in app.keys()
        src = self.get_app_path(app["name"])
        dst = app["path"]
        sudo("rm -rf {0}".format(dst))
        put(local_path=src,remote_path=os.path.dirname(dst),use_sudo=True)
        # set debug to false

    def get_apps(self):
        return self.apps

    def get_app_path(self,name):
        return os.path.join(staged_apps_dir,name)

class Apache:
    def __init__(self):
        self.applications = []
        self.config_file = "/etc/apache2/sites-available/flask.conf"
        with open(apache_file,"r") as f:
            self.config_template = f.read()

    def restart(self):
        sudo("service apache2 restart")

    def start_website(self):
        sudo ("a2ensite flask.conf")

    def enable_wsgi(self):
        sudo("a2enmod wsgi")

    def add(self,app):
        self.applications.append(app)

    def write_config(self,server):
        for app in self.applications:
            app["wsgi_file"] = WSGI.get_file_path(app)

        alias_template = "WSGIScriptAlias {0} {1}"
        non_root_aliases = [app for app in self.applications if app["sub_url"] != "/"]
        root_aliases     = [app for app in self.applications if app["sub_url"] == "/"]
        assert len(root_aliases) < 2
        aliases = "\n    ".join([alias_template.format(app["sub_url"], app["wsgi_file"]) for app in non_root_aliases])
        if root_aliases:
            aliases+= "\n    " + alias_template.format(root_aliases[0]["sub_url"], root_aliases[0]["wsgi_file"])

        directory_template = """
    <Directory {path}>
        Order allow,deny
        Allow from all
    </Directory>
        """
        directories = "\n".join([directory_template.format(**app) for app in self.applications])

        config_content = self.config_template.format(url=server["url"],alias=server["alias"],directories=directories,aliases=aliases)
        files.append(self.config_file, config_content, use_sudo=True)

    def clean_config(self):
        if files.exists(self.config_file,use_sudo=True):
            sudo("rm -f {0}".format(self.config_file))
        sudo("touch {0}".format(self.config_file))

    def disable_sites(self):
        is_valid_site = lambda s: s not in ["000-default",""]
        sites = [s for s in self.get_enabled_sites() if is_valid_site(s)]
        for site in sites:
            sudo("a2dissite {0}".format(site))

    def get_enabled_sites(self):
        return sudo("ls /etc/apache2/sites-enabled").split(" ")

class WSGI:
    def __init__(self,app):
        with open(wsgi_file,"r") as f:
            self.content = f.read()
        self.path = WSGI.get_file_path(app)
   
    def upload(self):
        sudo("touch {0}".format(self.path))
        files.append(self.path,self.content, use_sudo=True)

    @staticmethod
    def get_file_path(app):
        return os.path.join(app["path"],"wsgi.py").replace("\\","/")
   
class Pip():
    def __init__(self,packages):
        self.packages = packages

    def ensure_installed(self):
        sudo("pip install --upgrade pip")
        freeze = sudo("pip freeze").lower()
        for package in self.packages:
            if package.lower() not in freeze:
                sudo("pip install {0}".format(package))

class PackageManager:
    def __init__(self,packages):
        self.packages = packages

    def ensure_installed(self):
        required_packages = []
        for package in self.packages:
            if self.is_package_installed(package):
                print "{0} is already installed".format(package)
            else:
                print "{0} will need to be installed".format(package)
                required_packages.append(package)

        if required_packages:
            sudo("apt-get -qq update")
            for p in required_packages:
                sudo("apt-get -qq install {0} -y".format(p))
        else:
            print "All packages have already been installed."

    def is_package_installed(self,name):
        """ Use Debian Package Manager output to check for package
        """
        package_info = sudo("dpkg --status {0}".format(name),quiet=True)
        return "Status: install ok installed" in package_info