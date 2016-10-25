import os
import getpass
from fabric.api import sudo

class PackageManager:
    """ Handles installation of Debian packages
    """
    @staticmethod
    def get_required_packages(apps):
        packages = [
            "apache2",
            "libapache2-mod-wsgi",
            "python-pip",
            "curl"
        ]

        optional_packages = [
            "mysql-server"
        ]

        for app in apps:
            if "packages" not in app.keys():
                continue

            selected_packages = [p for p in app["packages"] if p in optional_packages]
            packages += selected_packages
        return packages

    @staticmethod
    def ensure_installed(requested_packages):
        packages = set(requested_packages)

        required_packages = []
        for package in packages:
            if PackageManager.is_package_installed(package):
                print "{0} is already installed".format(package)
            else:
                print "{0} will need to be installed".format(package)
                required_packages.append(package)

        if required_packages:
            sudo("apt-get -qq update")
            for package_name in required_packages:
                if package_name == "mysql-server":
                    PackageManager._install_mysql()
                else:
                    sudo("apt-get -qq install {0} -y".format(package_name))
        else:
            print "All packages have already been installed."

    @staticmethod
    def _install_mysql():
        sudo("export DEBIAN_FRONTEND=noninteractive apt-get -qq -y install mysql-server")

        # Set password
        print "\n ===== TEMPOARY WORKAROUND ====="
        print "This is bad and you should feel bad"
        password_1 = True
        password_2 = False

        while password_1 != password_2:
            password_1 = getpass.getpass("MYSQL Password: ")
            password_2 = getpass.getpass("Confirm MYSQL Password: ")
            if password_1 == password_2:
                run("mysqladmin -u root password {0}".format(password_1))

    @staticmethod
    def is_package_installed(name):
        """ Use Debian Package Manager output to check for package
        """
        package_info = sudo("dpkg --status {0}".format(name),quiet=True)
        return "Status: install ok installed" in package_info