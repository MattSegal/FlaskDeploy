import os
from fabric.api import sudo
import fabric.contrib.files as files

script_dir  = os.path.dirname(os.path.realpath(__file__))
wsgi_file   = os.path.join(script_dir,"wsgi_template.py")

with open(wsgi_file,"r") as f:
    wsgi_content = f.read()

class WSGI:

    @staticmethod
    def upload_wgsi_file(app):
        target_wsgi_path = WSGI.get_file_path(app)
        sudo("touch {0}".format(target_wsgi_path))
        files.append(target_wsgi_path,wsgi_content, use_sudo=True)

    @staticmethod
    def get_file_path(app):
        return os.path.join(app["path"],"wsgi.py").replace("\\","/")
   