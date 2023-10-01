"""
Add a bash function to a file to run a python file (*For anaconda/miniconda users only)

How to use this command:
1. Activate the desired conda virtual environment.
2. Run "py2bin <full_path/script.py> -d <optional-description>"

Note: 
1. The exec file will assume the activated conda environment as the default interpreter.
2. Do not run the command in the "base" conda environment as it has a different python interpreter path/

Configuring .env:
    CONDA_ENVS: the path storing venv 
    BASH_SCRIPT_PATH: the path of the bash script storing all commands
    CSV_SOURCE: the csv path of the list of bash functions
    BASH_SOURCE: the bash source file path
"""

import argparse
import os
from dotenv import load_dotenv
import sys
import subprocess
import tempfile


def configure_and_run_arg_parser():
    parser = argparse.ArgumentParser(
        description="Create a exec file for python file to run in CLI as a command"
    )
    parser.add_argument("file", type=str, help="The target python file")
    parser.add_argument(
        "-d", "--desc", type=str, help="Optional description argument", required=False
    )

    args = parser.parse_args()

    # Raise error for non-python file
    if not args.file.endswith(".py"):
        sys.exit("Please select a python file!")

    # Add '# ' to description
    if args.desc:
        args.desc = f"# {args.desc}\n"

    return args


def add_shebang_line_to_file_top(file: str, shebang_line: str):
    with open(file, "r") as f:
        file_content = f.read()
    if file_content[: file_content.index("\n")] != shebang_line:
        with open(file, "w") as f:
            f.write(f"{shebang_line}\n{file_content}")


def create_dirs_and_file_if_not_exists(file: str):
    dirname = os.path.dirname(file)
    if not os.path.exists(dirname):
        print(f"\nDirectory {dirname} does not exist, created one successfully.")
        os.makedirs(dirname)

    if not os.path.exists(file):
        with open(file, "w") as f:
            pass
        print(f"\nFile {file} does not exist, created one successfully.")


def create_exec_copy(py_file: str, shebang_line: str):
    # Create file copy and insert the shebang line to the beginning of it
    with open(py_file, "r") as f:
        file_content = f.read()

    with tempfile.NamedTemporaryFile("w") as f:
        f.write(f"{shebang_line}\n{file_content}")
        f.flush()

        # Create a exec copy of the input file
        process = subprocess.run(
            ["sudo", os.path.join(PWD, "create_exec_copy.sh"), py_file, f.name]
        )

    return process.returncode


def update_bash_function_and_description(
    bash_script, bash_lines, cmd_idx, command_name, new_desc, new_function_line
):
    desc_change_consent = "n"
    if new_desc and bash_lines[cmd_idx - 1] != new_desc:
        desc_change_consent = input(
            f"\nUpdating from\n{bash_lines[cmd_idx - 1]}\nto\n{new_desc}\n"
            + "Please confirm the change y/[n]: "
        )
        if desc_change_consent != "y":
            print("Description remains unchanged.")
        else:
            old_desc = bash_lines[cmd_idx - 1]
            bash_lines[cmd_idx - 1] = new_desc
            print("Description will be changed")

    # Update current command if the user consents
    cmd_change_consent = "n"
    if bash_lines[cmd_idx] != new_function_line:
        cmd_change_consent = input(
            f"\nUpdating from\n{bash_lines[cmd_idx]}\nto\n{new_function_line}\n"
            + "\nPlease confirm the change y/[n]: "
        )
        if cmd_change_consent != "y":
            print("Exiting without updating the function")
        else:
            old_function_line = bash_lines[cmd_idx]
            bash_lines[cmd_idx] = new_function_line
            print("Command will be updated")

    with open(bash_script, "w") as f:
        f.write("".join(bash_lines))
    print(
        f"\nCommand <{command_name}> udpated:\nDescription changed? {'No' if desc_change_consent != 'y' else (old_desc + ' -> ' + new_desc)}\
            \nCommand updated? {'No' if cmd_change_consent != 'y' else (old_function_line + ' -> ' + new_function_line)}"
    )


def insert_new_bash_function_and_description(
    bash_script, bash_lines, command_name, new_desc, new_function_line
):
    bash_lines.append("\n")
    bash_lines.append(
        "# Please add command description\n" if not new_desc else new_desc
    )
    bash_lines.append(new_function_line)

    with open(bash_script, "w") as f:
        f.write("".join(bash_lines))

    print(
        f"\nNew command <{command_name}> added successfully!"
        + f"\nDescription: {new_desc}"
        + f"\nCommand: {new_function_line}"
    )

    if not new_desc:
        print('\nPlease add the new command to track list via "cmd-add"')


def main():
    # Project directory and .env setup
    global PWD
    PWD = os.path.dirname(__file__)
    load_dotenv(os.path.join(PWD, ".env"))

    # Cli argument parser
    args = configure_and_run_arg_parser()

    # Check the activated conda environment
    if conda_env := os.getenv("CONDA_DEFAULT_ENV"):
        print(f"The command will be run in:\n{conda_env}\n")
    else:
        print("This program is only compatible to Anaconda users!")
        sys.exit(1)

    # Construct the shebang line
    conda_envs_path = os.path.expanduser(os.getenv("CONDA_ENVS"))
    shebang_line = "#!" + os.path.join(
        conda_envs_path,
        conda_env,
        f"bin/python{sys.version_info.major}.{sys.version_info.minor}",
    )

    # Create exec copy in target directory
    process_return_code = create_exec_copy(args.file, shebang_line)
    if process_return_code == 0:
        exec_file_path = args.file[:-3]
        print(f"Exec file created at {exec_file_path} successfully!")
    else:
        sys.exit("The exec file is not created. Exiting without any changes made")

    # Update the bash function script
    bash_script = os.path.expanduser(os.getenv("BASH_SCRIPT_PATH"))
    create_dirs_and_file_if_not_exists(bash_script)

    # Get bash script content
    with open(bash_script, "r") as f:
        bash_lines = f.readlines()

    command_name = os.path.basename(args.file)
    command_name = command_name[: command_name.index(".py")]

    new_function_line = f"function {command_name}() {{{exec_file_path} $@}}\n"

    cmd_bools = [
        f"{command_name}()" in i for i in bash_lines
    ]  # True if the new function already exists

    if True in cmd_bools:
        cmd_idx = cmd_bools.index(True)  # index of the command in the bash script

        update_bash_function_and_description(
            bash_script=bash_script,
            bash_lines=bash_lines,
            cmd_idx=cmd_idx,
            command_name=command_name,
            new_desc=args.desc,
            new_function_line=new_function_line,
        )

    else:
        # Insert new command if it does not exist
        insert_new_bash_function_and_description(
            bash_script=bash_script,
            bash_lines=bash_lines,
            command_name=command_name,
            new_desc=args.desc,
            new_function_line=new_function_line,
        )

    # Update the command csv
    subprocess.run(
        [
            os.path.join(PWD, "cmd-add"),
            "-n",
            command_name,
            "-f",
            args.file,
            "-d",
            args.desc[2:-2]
            if args.desc
            else "NO_UPDATE",  # [2:] to escape the '# ' at the beginning and '\n' at the end
        ]
    )

    # Source the bash source file to refresh env
    subprocess.run(
        [os.path.join(PWD, "source.sh"), os.path.expanduser(os.getenv("BASH_SOURCE"))]
    )


if __name__ == "__main__":
    main()
