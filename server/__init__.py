from server_utility import ServerUtils
from flask_project import FlaskProject
from apache import Apache
from pip_manager import Pip
from package_manager import PackageManager

def setup(apps,host):

    # Convenience configurations
    ServerUtils.set_bash_rc()
    ServerUtils.set_timezone()
    
    # Install Debian packages
    debian_package_files = FlaskProject.get_debian_requirements(apps)
    PackageManager.ensure_installed(debian_package_files)

    # Install Python packages
    requirements_files = FlaskProject.get_pip_requirements(apps)
    Pip.ensure_installed(requirements_files)

    # Setup Flask applications on Apache
    apache = Apache()
    apache.disable_sites()

    apache.clean_config()
    FlaskProject.clean_deployment_folder()

    for app in FlaskProject.get_deployable_apps(apps):
        
        FlaskProject.upload_app(app)
        apache.add(app)

    apache.write_config(host)
    apache.enable_wsgi()
    apache.start_website()
    apache.restart()

    # TODO: Setup SSH key + PuTTY for easy remote access