import os.path
import shutil
import subprocess

def stage_app(app_name):
    if not test_app_exists(app_name):
        print "Flask app {app} was not found".format(app=app_name)
        return False
    print "Found flask app {app}".format(app=app_name)

    clean_staging_dir(app_name)
    clone_app(app_name)

    staging_path = get_staging_path(app_name)
    config_for_deployment(staging_path)
    return True

def config_for_deployment(staging_path):
    fab_src = ".\\fabfile.py" 
    fab_dst = os.path.join(staging_path,"fabfile.py")
    shutil.copy2(fab_src,fab_dst)
    fabfile_args = "config_for_deployment:path={0}".format(staging_path)
    subprocess.call(["fab",fabfile_args],cwd=staging_path)


def clone_app(app_name):
    src = get_app_path(app_name)
    dst = get_staging_path(app_name)
    subprocess.call(["git","clone",src,dst])

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

def test_app_exists(app_name):
    app_path = get_app_path(app_name)
    has_git_dir = os.path.isdir(os.path.join(app_path,".git"))
    is_project = os.path.isfile(os.path.join(app_path,"__init__.py"))
    is_deployable = os.path.isfile(os.path.join(app_path,"deploy.json"))
    return has_git_dir and is_project and is_deployable

def get_staging_path(app_name):
    return os.path.join(get_fabric_path(),"staging",app_name)

def get_app_path(app_name):
    return os.path.join(get_fabric_path(),"..",app_name)

def get_fabric_path():
    return os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":
    stage_app("chris_profile")