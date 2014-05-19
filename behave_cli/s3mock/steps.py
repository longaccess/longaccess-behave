from behave import step
from boto import connect_s3
from boto import config as boto_config


@step(u'an S3 bucket named "{name}"')
def s3bucket_named(context, name):
    if not boto_config.has_section('Boto'):
        boto_config.add_section('Boto')
    boto_config.set('Boto', 'debug', '0')
    boto = connect_s3()
    boto.create_bucket(name)
    context.buckets.append(name)


@step(u'there are {num} keys in the bucket "{bucket}"')
def s3bucket_num_keys_bucket(context, num, bucket):
    bucket = connect_s3().get_bucket(bucket)
    assert len(bucket.get_all_keys()) == int(num), "{} keys in {}".format(
        num, bucket)


@step(u'there are {num} keys')
def s3bucket_num_keys(context, num):
    context.execute_steps(u"""
        Given there are {} keys in the bucket "{}"
        """.format(num, context.buckets[0]))


@step(u'the key "{key}" exists in the bucket "{bucket}"')
def s3bucket_key_bucket(context, key, bucket):
    bucket = connect_s3().get_bucket(bucket)
    assert bucket.get_key(key) is not None, "key {} exist in {}".format(
        key, bucket)


@step(u'the key "{key}" exists')
def s3bucket_key(context, key):
    context.execute_steps(u"""
        Given the key {} exists in the bucket "{}"
        """.format(key, context.buckets[0]))


@step(u'the following keys exists in the bucket "{bucket}"')
def s3bucket_keys_bucket(context, bucket):
    step = u"""
        Given the key "{}" exists in the bucket "{}"
    """
    for row in context.table:
        context.execute_steps(step.format(row['key'], bucket))


@step(u'the following keys exist')
def s3bucket_keys(context):
    s3bucket_keys_bucket(context, context.buckets[0])


@step(u'I set the contents of key "{key}" in bucket "{b}" to "{contents}"')
def s3bucket_set_key_bucket(context, key, b, contents):
    bucket = connect_s3().get_bucket(b)
    key = bucket.new_key(key)
    key.set_contents_from_string(contents)


@step(u'I set the contents of key "{key}" to "{contents}"')
def s3bucket_set_key(context, key, contents):
    context.execute_steps(u"""
        Given I set the contents of key "{}" in bucket "{}" to "{}"
        """.format(key, context.buckets[0], contents))


@step(u'I set the contents of the following keys in bucket "{b}"')
def s3bucket_set_keys_bucket(context, b):
    step = u"""
        Given I set the contents of key "{}" in bucket "{}" to "{}"
    """
    for row in context.table:
        context.execute_steps(step.format(row['key'], b, row['content']))


@step(u'I set the contents of the following keys')
def s3bucket_set_keys(context):
    s3bucket_set_keys_bucket(context, context.buckets[0])
