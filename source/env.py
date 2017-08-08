import optparse
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
PY_VERSION = "python%s.%s" % (sys.version_info[0], sys.version_info[1])


def run_command_with_code(cmd, redirect_output=True, check_exit_code=True):
    """Runs a command in an out-of-process shell.
    Runs a command in an out-of-process shell, returning the
    output of that command.  Working directory is ROOT.
    """
    if redirect_output:
        stdout = subprocess.PIPE
    else:
        stdout = None

    proc = subprocess.Popen(cmd, cwd=ROOT, stdout=stdout)
    output = proc.communicate()[0]
    if check_exit_code and proc.returncode != 0:
        die('Command "%s" failed.\n%s', ' '.join(cmd), output)
    return (output, proc.returncode)


def run_command(cmd, redirect_output=True, check_exit_code=True):
    return run_command_with_code(cmd, redirect_output, check_exit_code)[0]


def print_help():
    help = """
    Setup is complete. 
    In case the arguments do not match contact support.
    """
    print(help)


def pip_install(*args):
    run_command(['pip', 'install', '--upgrade'] + list(args),
                redirect_output=False)


def install_dependencies(venv=VENV):
    print('Installing dependencies with pip (this can take a while)...')

    # First things first, make sure our venv has the latest pip and distribute.
    pip_install('pip')
    pip_install('distribute')

   # pip_install('-r', PIP_REQUIRES)

def die(message, *args):
    print(message % args, file=sys.stderr)
    sys.exit(1)


def check_python_version():
    if sys.version_info < (2, 6):
        die("Need Python Version >= 2.6")

def parse_args():
    """Parse command-line arguments."""
    parser = optparse.OptionParser()
    return parser.parse_args()


def main(argv):
    (options, args) = parse_args()
    check_python_version()
    install_dependencies()
    post_process()
    print_help()

if __name__ == '__main__':
    main(sys.argv)