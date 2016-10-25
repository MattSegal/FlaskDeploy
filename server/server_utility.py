import os
import re
from StringIO import StringIO
from fabric.api import sudo, put

script_dir  = os.path.dirname(os.path.realpath(__file__))
bashrc_file = os.path.join(script_dir,os.path.normpath("./.bashrc"))

class ServerUtils():
    @staticmethod
    def set_bash_rc():
        """ Upload shell preferences
        """
        src = bashrc_file
        dst = "/etc/bash.bashrc"
        put(local_path=src,remote_path=dst,use_sudo=True)
        dst = "~/.bashrc"
        put(local_path=src,remote_path=dst,use_sudo=True)

    @staticmethod
    def set_timezone():
        """ Set timezone of server to AEST
        """
        localtime_path = "/etc/localtime"
        AEST_path = "/usr/share/zoneinfo/Australia/Victoria"
        sudo("rm {0}".format(localtime_path))
        sudo("ln -s {0} {1}".format(AEST_path,localtime_path))

    @staticmethod
    def restart_apache():
        sudo("service apache2 restart")

    @staticmethod
    def print_error_logs(num_lines):
        error_log_path = "/var/log/apache2/error.log"
        ServerUtils._print_logs(error_log_path,num_lines)

    @staticmethod
    def print_access_logs(num_lines):
        access_log_path = "/var/log/apache2/access.log"
        ServerUtils._print_logs(access_log_path,num_lines)

    @staticmethod
    def _print_logs(logfile,num_lines):
        outputIO = StringIO()
        sudo("tail {0} --lines={1} --verbose".format(logfile,num_lines),stdout=outputIO)
        fabric_output_regex = '(\[\S+\]) out: '
        output = outputIO.getvalue()
        outputIO.close()
        output = re.sub(fabric_output_regex,'',output)
        print output