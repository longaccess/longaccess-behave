from behave.log_capture import capture
from . import setup, maybe_teardown


@capture
def before_all(context):
    pass


@capture
def after_all(context):
    pass


def before_feature(context, feature):
    pass


def after_feature(context, feature):
    pass


@capture
def before_scenario(context, scenario):
    if 's3mock' in scenario.tags:
        setup(context)


@capture
def after_scenario(context, scenario):
    maybe_teardown(context)
