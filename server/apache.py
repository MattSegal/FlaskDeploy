import os
from fabric.api import sudo
import fabric.contrib.files as files

from wsgi import WSGI

APACHE_CONFIG_FILE = "/etc/apache2/apache2.conf"
FLASK_CONFIG_FILE = "/etc/apache2/sites-available/flask.conf"

script_dir  = os.path.dirname(os.path.realpath(__file__))
apache_template_file = os.path.join(script_dir,"apache.conf")

class Apache:
    def __init__(self):
        self.applications = []
        with open(apache_template_file,"r") as f:
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
        # Write apache2.conf
        config_content = "\nServerName localhost"
        if not files.contains(APACHE_CONFIG_FILE,config_content,use_sudo=True):
            files.append(APACHE_CONFIG_FILE,config_content, use_sudo=True)

        # Write flask.conf
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
        files.append(FLASK_CONFIG_FILE, config_content, use_sudo=True)

    def clean_config(self):
        if files.exists(FLASK_CONFIG_FILE,use_sudo=True):
            sudo("rm -f {0}".format(FLASK_CONFIG_FILE))
        sudo("touch {0}".format(FLASK_CONFIG_FILE))

    def disable_sites(self):
        is_valid_site = lambda s: s not in ["000-default",""]
        sites = [s for s in self.get_enabled_sites() if is_valid_site(s)]
        for site in sites:
            sudo("a2dissite {0}".format(site))

    def get_enabled_sites(self):
        return sudo("ls /etc/apache2/sites-enabled").split(" ")