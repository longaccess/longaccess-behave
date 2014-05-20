import os
import signal
from moto.server import main as moto_main
from multiprocessing import Process
from pkg_resources import resource_filename

env_stack = []


def push_env(var, val):
    env_stack.append((var, os.environ.get(var, None)))
    os.environ[var] = val


def pop_env():
    var, val = env_stack.pop()
    if val is not None:
        os.environ[var] = val
    else:
        del os.environ[var]


config = resource_filename("behave_cli", "boto.cfg")


def start_moto(context):
    context.moto = Process(target=moto_main,
                           kwargs={'argv': ['s3bucket_path']})
    context.moto.start()
    if config is not None:
        push_env('BOTO_CONFIG', config)
        import boto
        import boto.connection
        import boto.provider
        from boto.pyami.config import Config
        boto.config = Config(config)  # reread configuration
        boto.connection.config = boto.provider.config = boto.config


def get_s3_connection():
    from boto import connect_s3
    return connect_s3(
        host='localhost', port=5000, is_secure=False,
        calling_format='boto.s3.connection.OrdinaryCallingFormat')


def stop_moto(context):
    os.kill(context.moto.pid, signal.SIGTERM)
    context.moto.join(5)
    context.moto = None
    while len(env_stack) > 0:
        pop_env()
