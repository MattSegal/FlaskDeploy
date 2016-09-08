import json
import sys
import os
import os.path

from flask_deploy_app import AppDeployer

class ProjectDeployer(AppDeployer):
    """
    Deploys Flask projects to flask_deploy directory
    """
    def __init__(self,project_name,debug=False):
        self.root = os.path.dirname(os.path.realpath(__file__))
        self.debug = debug
        self.project_name = project_name
        self.target_dir = self.build_path([self.root,"flask_deploy",project_name])

        self.modules  = self.get_deployment_config()

    def deploy_project(self):
        print "Deploying project %s ..." % self.project_name
        self.cleanse_target_dir()
        self.build_init_script()
        for module in self.modules:
            module_deployer = AppDeployer(module,project_name=self.project_name)
            module_deployer.deploy_app()
        print "... project done."

    def build_init_script(self):
        # This is some fully sick metaprogramming right here.
        script = "from flask import Flask\n"

        script+= "app = Flask(__name__)\n"

        for module in self.modules:
            script+= "from %s import *\n" % (module)

        for module in self.modules:
            script+= "app.register_blueprint(%s)\n" % module
        
        script+= "if __name__ == '__main__':\n"
        script+= "    app.run(host= '0.0.0.0',debug=%s)" % self.debug

        init_file = self.build_path([self.target_dir,"__init__.py"])

        cmd = "copy NUL %s > NUL" % (init_file)
        os.system(cmd)
        with open(init_file,'w') as init:
            init.write(script)

    def get_deployment_config(self):
        file_name = self.project_name + "_project.json"
        config_file = self.build_path([self.root,file_name])
        try:
            with open(config_file) as config_data:
                config = json.load(config_data)
        except IOError:
            raise IOError("Project '{0}' does not have a config file at '{1}'".format(self.project_name,config_file))
        return config

if __name__ == '__main__':
    project_name = sys.argv[1] 
    is_debug = sys.argv[2] == "--debug" if len(sys.argv) > 2 else False
    pd = ProjectDeployer(project_name,debug=is_debug)
    pd.deploy_project()