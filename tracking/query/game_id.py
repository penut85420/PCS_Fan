import sys
from ..trackingthepros import get_game_id

def main():
    print(get_game_id(sys.argv[1]))

if __name__ == '__main__':
    main()
