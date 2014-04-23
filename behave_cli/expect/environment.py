from . import setup, teardown


def expect_vars(context):
    vs = {
        'cwd': context.cwd,
        'homedir': None
    }
    if hasattr(context, 'environ'):
        if 'HOME' in context.environ:
            vs['homedir'] = context.environ['HOME']
    return vs


def before_all(context):
    setup(context)
    if not hasattr(context, 'format_vars'):
        context.format_vars = []
    context.format_vars.append(expect_vars)


def after_all(context):
    teardown(context)


def before_feature(context, feature):
    pass


def after_feature(context, feature):
    pass


def before_scenario(context, scenario):
    setup(context)


def after_scenario(context, scenario):
    teardown(context)
