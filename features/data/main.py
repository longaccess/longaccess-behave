import sys


def main(args=sys.argv):
    print "FOOBAR"


def main_input(args=sys.argv):
    print sys.stdin.readline().upper()


def main_forever_read(args=sys.argv):
    while True:
        print sys.stdin.readline().upper()


def main_delay_print(args=sys.argv):
    import time
    line = sys.stdin.readline().upper()
    time.sleep(2)
    print line

if __name__ == "__main__":
    main()
