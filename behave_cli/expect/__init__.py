from pexpect import EOF, TIMEOUT

import os
import signal


def expected_text(child, pattern, timeout):
    if child is None:
        raise RuntimeError("expected_text called without having previously "
                           "run a child process to interact with")
    return 0 == child.expect([pattern, TIMEOUT, EOF], timeout)


def setup(context):
    context.environ = {}
    context.child = None
    context.children = {}
    context.cwd = os.getcwd()
    context._cwd = context.cwd
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
    os.chdir(context._cwd)
