import os
import json
import shutil
from subprocess import PIPE, run
import sys


GAME_DIR_PATTERN = "game"


def find_games_path(source):
    game_paths = []

    for root, dirs, files, in os.walk(source):
        for directory in dirs:
            if GAME_DIR_PATTERN in directory.lower():
                path = os.path.join(source, directory)
                game_paths.append(path)


        break
    return game_paths


def main(source, earmark):
    pwd = os.getcwd()
    source_path = os.path.join(pwd, source)
    earmark_path = os.path.join(pwd, earmark)

    game_paths = find_games_path(source_path)
    print(game_paths)





if __name__ == "__main__":
    args = sys.argv
    if len(args) != 3:
        raise Exception ("You must - only - pass a primary and target directory.")

    source, earmark = args[1:]
    main(source, earmark)