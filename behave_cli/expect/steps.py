from . import expected_text
from behave import step
from behave_cli import format_vars
from multiprocessing import Process
from importlib import import_module
from shutil import rmtree

import os
import pty
import pexpect
import fdpexpect
import pkg_resources
import sys
import shlex


@step(u'the environment variable "{name}" is "{value}"')
@format_vars
def env_var(context, name, value):
    context.environ[name] = value


@step(u'the home directory is "{directory}"')
def home_directory(context, directory):
    context.environ['HOME'] = directory
    if os.path.exists(directory):
        if not os.path.isdir(directory):
            os.remove(directory)
        else:
            rmtree(directory)
        os.mkdir(directory)
    else:
        os.makedirs(directory)
    assert os.path.isdir(directory), "Home directory doesn't exist"
    context.dirs['home'] = directory


@step(u'the command line arguments "{args}"')
@format_vars
def cli_args(context, args):
    context.args = args


@step(u'I run console script "{entry}"')
def run_console_script(context, entry):

    e = None
    for p in pkg_resources.iter_entry_points(group='console_scripts'):
        if p.name == entry:
            e = p
    assert e, "Console script has entry point in setup.py"
    module = e.module_name
    target = e.attrs[0]
    run_python_module(context, module, target)


@step(u'I run module "{module}" target "{target}"')
def run_python_module(context, module, target):
    logfile = None
    if hasattr(context, 'stdout_capture'):
        logfile = context.stdout_capture

    fullname = "{}.{}".format(module, target)

    _io, pipeio = pty.openpty()

    def run_script(_pipe, _io, ctx):
        sys.stdout = os.fdopen(_pipe, "w")
        sys.stderr = os.fdopen(_pipe, "w")
        sys.stdin = os.fdopen(_pipe, "r")
        # Explicitly open the tty to make it become a controlling tty.
        tmp_fd = os.open(os.ttyname(_pipe), os.O_RDWR)
        os.close(tmp_fd)
        os.setsid()

        try:
            from features.steps import mp_setup
            mp_setup(ctx)
        except ImportError:
            pass
        try:
            from setproctitle import setproctitle
            setproctitle("python process: {}".format(fullname))
        except ImportError:
            pass
        for name, value in ctx.environ.iteritems():
            os.environ[name] = value
        os.chdir(ctx.cwd)
        sys.argv = ['-']
        if ctx.args:
            sys.argv += shlex.split(ctx.args)
        else:
            sys.argv = ['me']
        getattr(import_module(module), target)()

    proc = Process(target=run_script, args=(pipeio, _io,  context))
    proc.start()

    os.close(pipeio)

    context.child = fdpexpect.fdspawn(_io, logfile=logfile)
    context.child.__proc = proc
    context.child.__io = _io
    context.children[fullname] = context.child


@step(u'I run "{command}"')
def run_command(context, command):
    run_named_command(context, command, '')


@step(u'I spawn "{command}" named "{name}"')
def run_named_command(context, command, name):
    logfile = None
    if hasattr(context, 'stdout_capture'):
        logfile = context.stdout_capture
    args = []
    if context.args:
        args = shlex.split(context.args)
    context.children[name] = pexpect.spawn(
        command, cwd=context.cwd, env=context.environ,
        logfile=logfile, args=args)
    context.child = context.children[name]


@step(u'I see "{text}"')
@format_vars
def i_see_text(context, text):
    txt = "Expected '{}'".format(text)
    assert expected_text(context.child, text, context.timeout), txt


@step(u'I wait until I don\'t see "{text}" anymore')
def wait_for_text_to_dissapear(context, text):
    while expected_text(context.child, text, context.timeout):
        pass


@step(u'I wait {timeout} seconds to see "{text}"')
def wait_for_text(context, timeout, text):
    assert expected_text(context.child, text, int(timeout))


@step(u'the timeout is {seconds} seconds')
def set_timeout(context, seconds):
    context.timeout = int(seconds)


@step(u'I type "{text}"')
def i_type_text(context, text):
    context.child.sendline(text)


@step(u'I type the lines')
def i_type_lines(context):
    for row in context.table:
        i_type_text(context, row['line'])


@step(u'I send end of file')
def i_send_eof(context):
    i_type_text(context, chr(4))


@step(u'I change to the "{d}" directory')
@format_vars
def i_chdir(context, d):
    assert os.path.isdir(d)
    if context.cwd != d:
        os.chdir(d)
        context.cwd = os.getcwd()
