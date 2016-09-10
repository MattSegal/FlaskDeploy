import os.path
import shutil
import json
from fabric.api import local

def config_for_deployment(path):
    app_name = os.path.basename(path)

    staged_app = StagedApp(path)
    staged_app.prune()

    configure_git(app_name)

def configure_git(app_name):
    local("git init")
    local("git add *")
    local("git commit -m \"ready for deployment\"")

class StagedApp:

    def __init__(self,path):
        self.app_name = os.path.basename(path)
        self.path = path

        deployment_config  = self._get_deployment_config()
        self.file_config   = deployment_config['files']
        self.dir_config    = deployment_config['dirs']

    def _get_deployment_config(self):
        """ Get deploy.json config file from the app source path
        """
        config_file = os.path.join(self.path,"deploy.json")
        with open(config_file) as f:
            config = json.load(f)
        return config

    def prune(self):
        """ Removes unwanted files and folders from the application.
        """
        print "Pruning non deployables from {app}".format(app=self.app_name)
        self._remove_invalid_files(self.path)

    def _remove_invalid_files(self,path):
        """ Recursively removes invalid files and folders
        """
        for _file in self._get_invalid_files(path):
            file_path = os.path.join(path,_file)
            os.remove(file_path)

        for _dir in self._get_invalid_dirs(path):
            dir_path = os.path.join(path,_dir)
            shutil.rmtree(dir_path)

        for _dir in self._get_dirs(path):
            dir_path = os.path.join(path,_dir)
            self._remove_invalid_files(dir_path)

    def _get_invalid_dirs(self,path):
        for el in self._get_dirs(path):
            is_deployable = os.path.basename(el) in self.dir_config["deployable"]
            if not is_deployable:
                yield el

    def _get_dirs(self,path):
        return (x for x in os.listdir(path) if os.path.isdir(os.path.join(path,x)))

    def _get_invalid_files(self,path):
        files = (x for x in os.listdir(path) if os.path.isfile(os.path.join(path,x)))
        for el in files:
            is_correct_file_type    = el.split(".")[-1] in self.file_config["file_types"]
            is_deployable           = el in self.file_config["deployable"]
            is_non_deployable       = el in self.file_config["non-deployable"]
            if is_non_deployable or not (is_correct_file_type or is_deployable):
                yield el