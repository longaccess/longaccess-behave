import sys


def main(args=sys.argv):
    print "FOOBAR"


def main_input(args=sys.argv):
    print sys.stdin.readline().upper()


def main_forever_read(args=sys.argv):
    while True:
        print sys.stdin.readline().upper()

if __name__ == "__main__":
    main()
