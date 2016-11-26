import os
from fabric.api import sudo

class Pip():

    @staticmethod
    def ensure_installed(requirements_files):
        packages = []

        # Load all requirements
        for req_file in requirements_files:
            with open(req_file,'r') as f:
                requirements = f.read()
            packages+= requirements.split('\n')
            os.remove(req_file)

        # Get rid of duplicates, ignore version numbers
        format_name = lambda name : name.split('==')[0].lower()
        packages = set([format_name(p) for p in packages])

        assert "flask" in packages, "Flask must be in requirements.txt"

        sudo("pip install --upgrade pip")
        freeze = sudo("pip freeze").lower()
        for package in packages:
            if package.lower() not in freeze:
                sudo("pip install {0}".format(package))