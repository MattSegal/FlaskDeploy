import sys
import os.path
import os
import json

class AppDeployer:
    """
    Deploys Flask apps to flask_deploy directory
    """
    def __init__(self,app_name,project_name=None):
        self.root = os.path.dirname(os.path.realpath(__file__))
        self.app_name = app_name

        if project_name == None:
            self.source_dir = self.build_path([self.root,app_name])
            self.target_dir = self.build_path([self.root,"flask_deploy",app_name])
        else:
            self.source_dir = self.build_path([self.root,app_name])
            self.target_dir = self.build_path([self.root,"flask_deploy",project_name,app_name])

        deployment_config  = self.get_deployment_config()
        self.file_config   = deployment_config['files']
        self.dir_config    = deployment_config['dirs']
    
    def deploy_app(self):
        """
        Deploys a stand alone Flask app
        to the flask_deploy directory
        """
        print "\nDeploying app %s ..." % self.app_name
        self.cleanse_target_dir()
        self.deploy(self.source_dir,self.target_dir)
        print "... app done.\n"

    def deploy(self,source_path,target_path):
        """
        Recursively copies files and folders
        """
        files = self.get_valid_files(source_path)
        for _file in files:
            file_source_path = self.build_path([source_path,_file])
            file_target_path = self.build_path([target_path,_file])
            self.deploy_file(file_source_path,file_target_path)

        dirs = self.get_valid_dirs(source_path)
        for _dir in dirs:
            dir_source_path = self.build_path([source_path,_dir])
            dir_target_path = self.build_path([target_path,_dir])

            self.deploy_dir(dir_target_path)
            self.deploy(dir_source_path,dir_target_path)

    def cleanse_target_dir(self):
        if os.path.isdir(self.target_dir):
            cmd = "rmdir %s /S /Q" % self.target_dir
            os.system(cmd)
        cmd = "mkdir %s" % self.target_dir
        os.system(cmd)

    def deploy_file(self,file_source_path,file_target_path):
        cmd = "copy %s %s > NUL" % (file_source_path,file_target_path)
        os.system(cmd) 

    def deploy_dir(self,dir_target_path):
        cmd = "mkdir %s" %  dir_target_path
        os.system(cmd)

    def get_valid_dirs(self,path):
        dirs = self.list_dirs(path)
        valid_dirs = [el for el in dirs if el.split("\\")[-1] in self.dir_config["deployable"]]
        valid_dirs = [el for el in valid_dirs if el.split("\\")[-1] not in self.dir_config["non-deployable"]]
        return valid_dirs

    def get_valid_files(self,path):
        files = self.list_files(path)
        valid_files =  [el for el in files if el.split(".")[-1] in self.file_config["file_types"]]
        [valid_files.append(el) for el in files if el in self.file_config["deployable"]]
        valid_files =  [el for el in valid_files if el not in self.file_config["non-deployable"]]
        return valid_files

    def list_files(self,path):
        assert path[-1] != "\\"
        return [x for x in os.listdir(path) if os.path.isfile(path+"\\"+x)]

    def list_dirs(self,path):
        assert path[-1] != "\\"
        dirs = []
        for _dir in os.listdir(path):
            if os.path.isdir(path+"\\"+_dir):
                dirs.append(_dir)
        return dirs

    def get_deployment_config(self):
        """
        Get deploy.json config from app directory
        """
        config_file = self.build_path([self.source_dir,"deploy.json"])
        try:
            with open(config_file) as config_data:
                config = json.load(config_data)
        except IOError:
            raise IOError("App '%s' does not have a config file named 'deploy.json'" % self.app_name)
        except:
            raise Exception("There was an issue reading 'deploy.json' for app '%s'" % self.app_name)
        return config

    def build_path(self,dirs):
        """
        Builds a window file path from a list of directories
        """
        path = ""
        for _dir in dirs:
            path += _dir.strip("\\") + "\\"
        path = path.rstrip("\\")
        return path

if __name__ == "__main__":
    app_name = sys.argv[1]
    ad = AppDeployer(app_name)
    ad.deploy_app()