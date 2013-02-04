import time
from os import remove
from os.path import abspath, join, dirname
from subprocess import Popen
from sys import path

# Imports and SALAD_PATH just for testing within salad.
SALAD_ROOT = abspath(join(dirname(__file__), "../", "../"))
path.insert(0, SALAD_ROOT)

from salad.tests import TEST_SERVER_PORT
from salad.logger import logger


def before_all(context):
    create_tempfile(context)
    setup_subprocesses(context)
    setup_test_server(context)


def after_all(context):
    teardown_test_server(context)
    remove_tempfile()

def setup_subprocesses(context):
    context.subprocesses = []


def setup_test_server(context):
    file_server_command = "python -m SimpleHTTPServer %s" % (TEST_SERVER_PORT)
    test_dir = abspath(join(SALAD_ROOT, "salad", "tests", "html"))
    context.silent_output = file('/dev/null', 'a+')
    context.tempfile = file('/dev/null', 'a+')

    context.subprocesses.append(Popen(file_server_command, shell=True,
                                    cwd=test_dir,
                                    stderr=context.silent_output,
                                    stdout=context.silent_output
                                ))
    time.sleep(3)  # Wait for server to spin up


def create_tempfile(context):
    context.tempfile = file('/tmp/temp_lettuce_test', 'a+')
    context.tempfile.close()


def teardown_test_server(context):
    context.silent_output.close()
    for s in context.subprocesses:
        try:
            s.terminate()
        except:
            try:
                s.kill()
            except OSError:
                # Ignore an exception for process already killed.
                pass


def remove_tempfile():
    remove("/tmp/temp_lettuce_test")
