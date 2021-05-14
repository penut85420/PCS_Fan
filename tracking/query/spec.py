import argparse

from ..trackingthepros import get_spec_list

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--focus', '-f', type=str, default='')
    parser.add_argument('--important', '-i', type=str, default='')

    args = parser.parse_args()
    focus, important = map(
        lambda x: x.split(','),
        (args.focus, args.important)
    )

    get_spec_list(focus, important)

if __name__ == '__main__':
    main()
