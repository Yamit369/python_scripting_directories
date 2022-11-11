import os
import json
import shutil
from subprocess import PIPE, run
import sys


GAME_DIR_PATTERN = "game"
GAME_CODE_EXTENSION = ".go"
GAME_COMPILE_COMMAND = ["go", "build"]

def find_games_path(source):
    game_paths = []

    for root, dirs, files, in os.walk(source):
        for directory in dirs:
            if GAME_DIR_PATTERN in directory.lower():
                path = os.path.join(source, directory)
                game_paths.append(path)


        break
    return game_paths

def get_name_from_paths(paths, to_simplify):
    new_name = []
    for path in paths:
        _, dir_name = os.path.split(path)
        new_dir_name = dir_name.replace(to_simplify, "")
        new_name.append(new_dir_name)

    return new_name 


def create_directory(path):
    if not os.path.exists(path):
        os.mkdir(path)

def copy_and_overwrite(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    shutil.copytree(source, destination)


def json_file_metadata(path, game_dirs):
    data = {
        "gamesNames": game_dirs,
        "numberOfGames": len(game_dirs)
    }
    with open(path, "w") as f:
        json.dump(data, f)


def compile_game_code(path):
    code_file_name = None
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(GAME_CODE_EXTENSION):
                code_file_name = file
                break


        break

    if code_file_name is None:
        return
    
    command = GAME_COMPILE_COMMAND + [code_file_name]
    run_command(command, path)

def run_command(command, path):
    pwd = os.getcwd()
    os.chdir(path)

    result = run(command, stdout=PIPE, stdin=PIPE, universal_newlines=True)
    print(f'Compile Result: {result}')

    os.chdir(pwd)

def main(source, earmark):
    pwd = os.getcwd()
    source_path = os.path.join(pwd, source)
    earmark_path = os.path.join(pwd, earmark)

    game_paths = find_games_path(source_path)
    new_game_dirs = get_name_from_paths(game_paths, "_game")
    

    for src, destination in zip(game_paths, new_game_dirs):
        destination = os.path.join(earmark, destination)
        copy_and_overwrite(src, destination)
        compile_game_code(destination)

    create_directory(earmark_path)

    json_path = os.path.join(earmark_path, "metadata.json")
    json_file_metadata(json_path, new_game_dirs)


if __name__ == "__main__":
    args = sys.argv
    if len(args) != 3:
        raise Exception ("You must - only - pass a primary and target directory.")

    source, earmark = args[1:]
    main(source, earmark)