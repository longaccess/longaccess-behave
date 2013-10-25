from pexpect import EOF, TIMEOUT

import os
import signal


def expected_text(child, text, timeout):
    return 0 == child.expect_exact([text, TIMEOUT, EOF], timeout)


def setup(context):
    context.environ = {}
    context.child = None
    context.children = {}
    context.cwd = os.getcwd()
    context.args = None
    context.timeout = 2


def teardown(context):
    for child in context.children.values():
        if hasattr(child, '__proc'):
            os.write(child.__io, chr(4))
            os.kill(child.__proc.pid, signal.SIGHUP)
            child.__proc.join(1)
            try:
                os.kill(child.__proc.pid, signal.SIGTERM)
                child.__proc.join(5)
            except:
                pass
        child.close()
    context.child = None
    context.children = {}
    context.args = None
