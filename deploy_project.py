import json
import sys
import os
import os.path
import shutil
from flask_app import FlaskApp

def main(project_name,debug=False):
    """ Deploys Flask projects to flask_deploy directory
    """
    script_root = os.path.dirname(os.path.realpath(__file__))

    target_path = os.path.join(script_root,"deployables",project_name)
    modules  = get_project_modules(script_root, project_name)

    print "Deploying project %s ..." % project_name

    # Cleanse target directory
    if os.path.isdir(target_path):
        shutil.rmtree(target_path)
    os.mkdir(target_path)

    # Write project init file
    init_script = build_init_script(modules,debug)
    init_file = os.path.join(target_path,"__init__.py")
    with open(init_file,'w') as f:
        f.write(init_script)

    # Deploy project modules
    for module in modules:
        module_source_path = os.path.join(script_root,"..",module)
        module_target_path =  os.path.join(target_path,module)
        flask_app = FlaskApp(module_source_path, module_target_path)
        flask_app.deploy()

    print "... project done."


def build_init_script(modules,debug):
    # This is some fully sick metaprogramming right here.
    module_imports = "\n".join(["from {0} import *".format(module) for module in modules])
    module_register = "\n".join(["app.register_blueprint({0})".format(module) for module in modules])

    script = """
from flask import Flask
app = Flask(__name__)

{imports}
{register}

if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug={debug})
    """.format(imports=module_imports, register=module_register, debug=debug)
    return script

def get_project_modules(root,project_name):
    project_file = os.path.join(root, project_name + ".project")
    with open(project_file) as f:
        modules = json.load(f)
    return modules

if __name__ == '__main__':
    project_name = sys.argv[1] 
    is_debug = sys.argv[2] == "--debug" if len(sys.argv) > 2 else False
    main(project_name,debug=is_debug)