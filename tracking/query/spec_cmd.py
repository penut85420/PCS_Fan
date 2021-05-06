import sys
from tracking.trackingthepros import get_spec_cmd

def main():
    print(get_spec_cmd(sys.argv[1]))

if __name__ == '__main__':
    main()
