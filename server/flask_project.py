import os
from fabric.api import sudo, put

script_dir  = os.path.dirname(os.path.realpath(__file__))
staged_apps_dir = os.path.join(script_dir,"..\staged_apps")

class FlaskProject:
    
    @staticmethod
    def upload_app(app):
        assert "path" in app.keys()
        assert "name" in app.keys()
        src = FlaskProject.get_app_path(app["name"])
        dst = app["path"]
        sudo("rm -rf {0}".format(dst))
        put(local_path=src,remote_path=os.path.dirname(dst),use_sudo=True)

    @staticmethod
    def get_app_requirements(apps):
        deployable_apps = FlaskProject.get_deployable_apps(apps)
        app_staging_paths = [FlaskProject.get_app_path(app["name"]) for app in deployable_apps]
        print app_staging_paths
        get_filename = lambda path : os.path.join(path,'requirements.txt')
        file_exists  = lambda path : os.path.exists(get_filename(path))
        requirement_files = [get_filename(path) for path in app_staging_paths if file_exists(path)]
        return requirement_files

    @staticmethod
    def get_deployable_apps(apps):
        required_app_keys = [u'name',u'sub_url',u'path','deploy']

        for app in apps:
            # Validate application JSON fields
            error_message = "Application definition must only contain {0}".format(required_app_keys)
            assert app.keys().sort() == required_app_keys.sort(), error_message
            
            is_deployable_app = app["deploy"]
            if is_deployable_app:
                yield app

    @staticmethod
    def clean_deployment_folder():
        sudo("rm -rf /var/www/*")

    @staticmethod
    def get_app_path(name):
        return os.path.join(staged_apps_dir,name)

