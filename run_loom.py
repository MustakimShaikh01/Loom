# convenience launcher
import sys
from loom import cli
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage: python run_loom.py <script-path>')
    else:
        cli.run(sys.argv[1])
