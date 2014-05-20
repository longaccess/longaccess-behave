from .boto_init import start_moto, stop_moto
import requests
from mock import patch


class PatchedSession(requests.Session):
    def __init__(self, *args, **kwargs):
        super(PatchedSession, self).__init__(*args, **kwargs)
        self.headers['connection'] = 'Close'


def maybe_teardown(context):
    if hasattr(context, 'moto') and context.moto is not None:
        teardown(context)


def setup(context):
    context.patcher = patch('requests.Session', PatchedSession)
    context.patcher.start()
    start_moto(context)
    context.buckets = []


def teardown(context):
    stop_moto(context)
    context.patcher.stop()
