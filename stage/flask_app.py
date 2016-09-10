import sys
import os.path
import os
import json
import shutil

class FlaskApp:
    
    def __init__(self,source_path,target_path):
        self.app_name = os.path.basename(source_path)
        self.source_path = source_path
        self.target_path = target_path

        deployment_config  = self._get_deployment_config()
        self.file_config   = deployment_config['files']
        self.dir_config    = deployment_config['dirs']

    def _get_deployment_config(self):
        """ Get deploy.json config file from the app source path
        """
        config_file = os.path.join(self.source_path,"deploy.json")
        with open(config_file) as f:
            config = json.load(f)
        return config

    def deploy(self):
        """ Deploys the app to the target_path directory
        """
        print "\nDeploying app %s ..." % self.app_name
        self._cleanse_target_path()
        self._copy_valid_files(self.source_path,self.target_path)
        print "... done.\n"

    def _cleanse_target_path(self):
        if os.path.isdir(self.target_path):
            shutil.rmtree(self.target_path)
        os.mkdir(self.target_path)

    def _copy_valid_files(self,source_path,target_path):
        """ Recursively copies files and folders
        """
        for _file in self._get_valid_files(source_path):
            src = os.path.join(source_path,_file)
            dst = os.path.join(target_path,_file)
            shutil.copy2(src,dst)

        for _dir in self._get_valid_dirs(source_path):
            dir_source_path = os.path.join(source_path,_dir)
            dir_target_path = os.path.join(target_path,_dir)

            os.mkdir(dir_target_path)
            self._copy_valid_files(dir_source_path,dir_target_path)

    def _get_valid_dirs(self,path):
        dirs = [x for x in os.listdir(path) if os.path.isdir(os.path.join(path,x))]
        for el in dirs:
            is_deployable = os.path.basename(el) in self.dir_config["deployable"]
            if is_deployable:
                yield el

    def _get_valid_files(self,path):
        files = [x for x in os.listdir(path) if os.path.isfile(os.path.join(path,x))]
        for el in files:
            is_correct_file_type    = el.split(".")[-1] in self.file_config["file_types"]
            is_deployable           = el in self.file_config["deployable"]
            is_non_deployable       = el in self.file_config["non-deployable"]
            if (is_correct_file_type or is_deployable) and not is_non_deployable:
                yield el
   