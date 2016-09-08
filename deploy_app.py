import sys
import os.path
from flask_app import FlaskApp

app_name = sys.argv[1]
script_root = os.path.dirname(os.path.realpath(__file__))

source_path = os.path.join(script_root,"..",app_name)
target_path =  os.path.join(script_root,"deployables",app_name)

flask_app = FlaskApp(source_path,target_path)
flask_app.deploy()