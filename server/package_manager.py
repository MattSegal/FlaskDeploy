import os
import getpass
from fabric.api import sudo

class PackageManager:
    """ Handles installation of Debian packages
    """
    @staticmethod
    def ensure_installed(debian_package_files):
        supported_packages = [
            "apache2",
            "libapache2-mod-wsgi",
            "python-pip",
            "curl",
            "mysql-server"
        ]

        packages = []

       # Load all requirements
        for req_file in debian_package_files:
            with open(req_file,'r') as f:
                requirements = f.read()
            packages += requirements.split('\n')
            os.remove(req_file)

        # Get rid of duplicates
        packages = set(packages)
        assert "apache2" in packages, "You need to have apache2 in at least one debian.txt file"
        assert "libapache2-mod-wsgi" in packages, "You need to have libapache2-mod-wsgi in at least one debian.txt file"

        required_packages = []
        for package in packages:
            assert package in supported_packages, "package %s must be added to supported_packages" % package

            if PackageManager.is_package_installed(package):
                print "{0} is already installed".format(package)
            else:
                print "{0} will need to be installed".format(package)
                required_packages.append(package)

        if required_packages:
            sudo("apt-get -qq update")
            for package_name in required_packages:
                    sudo("apt-get -qq install {0} -y".format(package_name))
        else:
            print "All packages have already been installed."

    @staticmethod
    def is_package_installed(name):
        """ Use Debian Package Manager output to check for package
        """
        package_info = sudo("dpkg --status {0}".format(name),quiet=True)
        return "Status: install ok installed" in package_info