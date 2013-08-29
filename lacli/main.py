#!/home/kouk/code/bototest/bin/python
"""Upload a file to S3

Usage: laput.py [-d <sec>] [-D <level>] [-u <user>]
            [-b <bucket> ] [-p <np>] [<filename>...]
       laput.py -h, --help

Options:
    -u <user>, --user <user>       use a federated user token
    -d <sec>, --duration <sec>     duration of token in seconds [default: 3600]
    -D <level>, --debug <level>    debugging level, from 0 to 2 [default: 0]
    -b <bucket>, --bucket <bucket> bucket to upload to [default: lastage]
    -p <np>, --procs <np>          number of processes [default: auto]

"""


import sys
from docopt import docopt
from lacli.upload import *
from lacli.command import LaCommand
from latvm.session import UploadSession, NoCredentialsException
from lacli import __version__
from lacli.log import setupLogging, getLogger


def main(args=sys.argv[1:]):
    """Main function called by `laput` command.
    """
    options = docopt(__doc__, version='laput {}'.format(__version__))
    setupLogging(int(options['--debug']))
    try:
        session = UploadSession(
            uid=options['--user'],
            secs=options['--duration'],
            bucket=options['--bucket'],
            debug=int(options['--debug']),
            nprocs=options['--procs'])
        getLogger().debug("Using TVM: %s", session.tvm)
        cli = LaCommand(session, debug=int(options['--debug']))
        if len(options['<filename>']) > 0:
            for fname in options['<filename>']:
                cli.onecmd('put {}'.format(fname))
        else:
            cli.cmdloop()
    except NoCredentialsException:
        print "Error: no AWS credentials have been configured."
        print "Either setup a Boto configuration or run 'lacreds init'."
        sys.exit(1)

if __name__ == "__main__":
    main()
