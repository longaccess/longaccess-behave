import os

from behave_cli import environment as clienv

from distutils.util import strtobool as _bool
BEHAVE_DEBUG_ON_ERROR = _bool(os.environ.get("BEHAVE_DEBUG_ON_ERROR", "no"))


def after_step(context, step):
    if BEHAVE_DEBUG_ON_ERROR and step.status == "failed":
        import ipdb
        ipdb.post_mortem(step.exc_traceback)


def before_all(context):
    clienv.before_all(context)


def after_all(context):
    clienv.after_all(context)


def before_feature(context, feature):
    clienv.before_feature(context, feature)


def after_feature(context, feature):
    clienv.after_feature(context, feature)


def before_scenario(context, scenario):
    clienv.before_scenario(context, scenario)


def after_scenario(context, scenario):
    clienv.after_scenario(context, scenario)
