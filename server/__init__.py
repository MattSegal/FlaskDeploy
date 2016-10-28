from server_utility import ServerUtils
from flask_project import FlaskProject
from apache import Apache
from wsgi import WSGI
from pip_manager import Pip
from package_manager import PackageManager

def setup(apps,host):

    # Convenience configurations
    ServerUtils.set_bash_rc()
    ServerUtils.set_timezone()
    
    # Install Debian packages
    packages = PackageManager.get_required_packages(apps)
    PackageManager.ensure_installed(packages)

    # Install Python packages
    requirements_files = FlaskProject.get_app_requirements(apps)
    Pip.ensure_installed(requirements_files)

    # Setup Flask applications on Apache
    apache = Apache()
    apache.disable_sites()

    apache.clean_config()
    FlaskProject.clean_deployment_folder()

    for app in FlaskProject.get_deployable_apps(apps):
        
        FlaskProject.upload_app(app)
        WSGI.upload_wgsi_file(app)

        apache.add(app)

    apache.write_config(host)
    apache.enable_wsgi()
    apache.start_website()
    apache.restart()

    # TODO: Setup SSH key + PuTTY for easy remote access