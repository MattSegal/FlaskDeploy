import re
from StringIO import StringIO
from fabric.api import sudo

def restart_apache():
    sudo("service apache2 restart")

def print_error_logs(num_lines):
    error_log_path = "/var/log/apache2/error.log"
    _print_logs(error_log_path,num_lines)

def print_access_logs(num_lines):
    access_log_path = "/var/log/apache2/access.log"
    _print_logs(access_log_path,num_lines)

def _print_logs(logfile,num_lines):
    outputIO = StringIO()
    sudo("tail {0} --lines={1} --verbose".format(logfile,num_lines),stdout=outputIO)
    fabric_output_regex = '(\[\S+\]) out: '
    output = outputIO.getvalue()
    outputIO.close()
    output = re.sub(fabric_output_regex,'',output)
    print output