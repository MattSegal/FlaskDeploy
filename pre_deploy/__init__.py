import os
import shutil
import subprocess

from staged_app import StagedApp

def stage_app(app_name,branch_name):
    assert_app_is_valid(app_name)
    print "Found flask app {app}".format(app=app_name)

    clean_staging_dir(app_name)
    clone_app(app_name,branch_name)
    
    staging_path = get_staging_path(app_name)
    staged_app = StagedApp(staging_path)
    staged_app.prune()

def clone_app(app_name,branch_name):
    # Clone repo
    src = get_app_path(app_name)
    dst = get_staging_path(app_name)
    subprocess.call(["git","clone",src,dst])

    # Copy production config file (config.prod) files in base
    config_file = 'config.py.prod'
    config_file_src = os.path.join(src,config_file)
    config_file_dst = os.path.join(dst,config_file)

    if os.path.exists(config_file_src):
        shutil.copyfile(config_file_src,config_file_dst)

    # Checkout branch name if available
    working_directory = get_staging_path(app_name)
    print "working dir " + working_directory
    process = subprocess.Popen("git branch -a",stdout=subprocess.PIPE,cwd=working_directory)
    out, err = process.communicate()
    print "git branches:\n" + out
    if branch_name in out:
        subprocess.call(["git","checkout",branch_name], cwd=working_directory)
    else:
        print "Git branch {0} was not found.".format(branch_name)
        assert "master" in out, "Repository {0} must have a 'master' branch.".format(app_name)
        subprocess.call(["git","checkout","master"],cwd=working_directory)
        
def clean_staging_dir(app_name):
    path = get_staging_path(app_name)
    if os.path.isdir(path):
        print "Cleaning staging area for {app}".format(app=app_name)

        # Remove the .git dir using command-prompt 'remove directory' tool to avoid
        # 'Access Denied' issues
        git_path = os.path.join(path,".git")
        if os.path.isdir(git_path):
            subprocess.call("RD /S /Q {0}".format(git_path),shell=True)

        shutil.rmtree(path)

def assert_app_is_valid(app_name):
    app_path = get_app_path(app_name)
    
    has_git_dir = os.path.isdir(os.path.join(app_path,".git"))
    assert has_git_dir, "Flask app {app} has no .git dir".format(app=app_name)

    has_wsgi = os.path.isfile(os.path.join(app_path,"wsgi.py"))
    assert has_wsgi, "Flask app {app} has no wsgi.py file".format(app=app_name)

    is_project = os.path.isfile(os.path.join(app_path,"app\__init__.py"))
    assert is_project, "Flask app {app} has no app\\__init__.py file".format(app=app_name)

    is_deployable = os.path.isfile(os.path.join(app_path,"deploy.json"))
    assert is_deployable, "Flask app {app} has no deploy.json file".format(app=app_name)

    has_pip_requirements = os.path.isfile(os.path.join(app_path,"requirements.txt"))
    assert is_deployable, "Flask app {app} has no requirements.txt file".format(app=app_name)

    has_debian_packages = os.path.isfile(os.path.join(app_path,"debian.txt"))
    assert is_deployable, "Flask app {app} has no debian.txt debian packages file".format(app=app_name)

def get_staging_path(app_name):
    return os.path.join(get_fabric_path(),"staged_apps",app_name)

def get_app_path(app_name):
    return os.path.abspath(os.path.join(get_fabric_path(),"..",app_name))

def get_fabric_path():
    return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))