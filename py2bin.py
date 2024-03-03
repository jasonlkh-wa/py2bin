"""
Add a shell function to a file to run a python file (*For anaconda/miniconda users only)

How to use this command:
1. Activate the desired conda virtual environment.
2. Run "py2bin <full_path/script.py> -d <optional-description>"

Note: 
1. The exec file will assume the activated conda environment as the default interpreter.
2. Do not run the command in the "base" conda environment as it has a different python interpreter path/

Configuring .env:
    CONDA_ENVS: the path storing venv 
    SHELL_SCRIPT_PATH: the path of the shell script storing all commands
    CSV_SOURCE: the csv path of the list of shell functions
"""
# CR: solve the weird insert in csv, one possbile solution would be reading the whole csv in list
# do any changes and join with "\n" 
# CR-soon: review the shell script insert to see if there is a better way to change the command
import whelper
import os
from dotenv import load_dotenv
import sys
import subprocess
import tempfile
import re
import main_arg_parser


def configure_and_run_arg_parser():
    # parser = argparse.ArgumentParser(
    #     description="Create a exec file for python file to run in CLI as a command"
    # )

    parser = main_arg_parser.MainArgParser(
        prog="py2bin", subparser_description="py2bin actions"
    )

    subparser_add = parser.subparsers.add_parser(
        "add",
        help="add a new python-based command",
        description="Add a new python-based command",
    )

    subparser_update = parser.subparsers.add_parser(
        "update",
        help="update an existing py2bin command by regenerating the exec file",
        description="Update an existing py2bin command by regenerating the exec file",
    )

    subparser_add.add_argument("file", type=str, help="The target python file")
    subparser_add.add_argument(
        "-d",
        "--desc",
        type=str,
        help="<Optional> description argument",
        required=False,
    )

    subparser_add.add_argument(
        "--dotenv",
        type=str,
        help="<Optional> custom .env file path, for testing only",
        required=False,
    )

    subparser_update.add_argument("command", type=str, help="the command to be updated")

    return parser.parse_args()


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


def create_exec_name(x: str) -> str:
    x = x.replace("_", "-").replace(" ", "-")
    return x[:-3]  # rempve .py


def create_exec_copy(
    py_file: str,
    conda_env: str,
):
    # Construct the shebang line
    conda_envs_path = os.path.expanduser(os.getenv("CONDA_ENVS"))
    shebang_line = "#!" + os.path.join(
        conda_envs_path,
        conda_env,
        f"bin/python{sys.version_info.major}.{sys.version_info.minor}",
    )

    # Create file copy and insert the shebang line to the beginning of it
    with open(py_file, "r") as f:
        file_content = f.read()

    with tempfile.NamedTemporaryFile("w") as f:
        f.write(f"{shebang_line}\n{file_content}")
        f.flush()

        # Create a exec copy of the input file
        # CR-soon use shutil to copy instead for stability and flexibility
        process = subprocess.run(
            [
                "sudo",
                os.path.join(PWD, "create_exec_copy.sh"),
                py_file,
                f.name,
                create_exec_name(py_file),
            ]
        )

    # Create exec copy in target directory
    if process.returncode == 0:
        exec_file_path = create_exec_name(py_file)
        print(f"Exec file created at {exec_file_path} successfully!")
    else:
        sys.exit("The exec file is not created. Exiting without any changes made")

    return exec_file_path


def update_shell_function_and_description(
    SHELL_SCRIPT, shell_lines, cmd_idx, command_name, new_desc, new_function_line
):
    desc_change_consent = "n"
    if new_desc and shell_lines[cmd_idx - 1] != new_desc:
        desc_change_consent = input(
            f"\nUpdating from\n{shell_lines[cmd_idx - 1]}\nto\n{new_desc}\n"
            + "Please confirm the change y/[n]: "
        )
        if desc_change_consent != "y":
            print("Description remains unchanged.")
        else:
            old_desc = shell_lines[cmd_idx - 1]
            shell_lines[cmd_idx - 1] = new_desc
            print("Description will be changed")

    # Update current command if the user consents
    cmd_change_consent = "n"
    if shell_lines[cmd_idx] != new_function_line:
        cmd_change_consent = input(
            f"\nUpdating from\n{shell_lines[cmd_idx]}\nto\n{new_function_line}\n"
            + "\nPlease confirm the change y/[n]: "
        )
        if cmd_change_consent != "y":
            print("Exiting without updating the function")
        else:
            old_function_line = shell_lines[cmd_idx]
            shell_lines[cmd_idx] = new_function_line
            print("Command will be updated")

    with open(SHELL_SCRIPT, "w") as f:
        f.write("".join(shell_lines))
    print(
        f"\nCommand <{command_name}> udpated:\nDescription changed? {'No' if desc_change_consent != 'y' else (old_desc + ' -> ' + new_desc)}\
            \nCommand updated? {'No' if cmd_change_consent != 'y' else (old_function_line + ' -> ' + new_function_line)}"
    )


def insert_new_shell_function_and_description(
    SHELL_SCRIPT, shell_lines, command_name, new_desc, new_function_line
):
    shell_lines.append("\n")
    shell_lines.append(
        "# Please add command description\n" if not new_desc else new_desc
    )
    shell_lines.append(new_function_line)

    with open(SHELL_SCRIPT, "w") as f:
        f.write("".join(shell_lines))

    print(
        f"\nNew command <{command_name}> added successfully!"
        + f"\nDescription: {new_desc}"
        + f"\nCommand: {new_function_line}"
    )

    if not new_desc:
        print('\nPlease add the new command to track list via "cmd-add"')


def update_command(command: str):
    command = command.strip()
    load_dotenv(os.path.join(PWD, ".env"))
    with open(os.path.expanduser(os.getenv("CSV_SOURCE")), "r") as f:
        csv_lines = f.readlines()
        for line in csv_lines:
            line = line.split(",")

            if line[0].strip('"') == command:
                py_file_location = line[1].strip('"')

                conda_env = os.getenv("CONDA_DEFAULT_ENV")
                create_exec_copy(py_file_location, conda_env)
                print(
                    f"Exec file regenerated at <{create_exec_name(py_file_location)}> with <{conda_env}> env"
                )
                return None

    raise ValueError(f"Command {command} not found in {os.getenv('CSV_SOURCE')}")


def main():
    global PWD
    PWD = os.path.dirname(__file__)
    # Cli argument parser
    args = configure_and_run_arg_parser()

    match args.action:
        case "add":
            # Raise error for non-python file
            if not args.file.endswith(".py"):
                sys.exit("Please select a python file!")
            # Add '# ' to description
            if args.desc:
                args.desc = f"# {args.desc}\n"
            if os.path.basename(create_exec_name(args.file)) == "cmd":
                raise ValueError("Please do not use cmd as command name")

        case "update":
            update_command(command=args.command)
            return None
        case _:
            raise ValueError(f"Invalid action: {args.action}, run with -h for help.")

    # Load .env setup
    if args.dotenv:
        load_dotenv(args.dotenv)
    else:
        load_dotenv(os.path.join(PWD, ".env"))

    # Check the activated conda environment
    if conda_env := os.getenv("CONDA_DEFAULT_ENV"):
        print(f"The command will be run in:\n{conda_env}\n")
    else:
        print("This program is only compatible to Anaconda users!")
        sys.exit(1)

    # Create exec copy in target directory
    exec_file_path = create_exec_copy(args.file, conda_env)

    # Update the shell function script
    SHELL_SCRIPT = os.path.expanduser(os.getenv("SHELL_SCRIPT_PATH"))
    create_dirs_and_file_if_not_exists(SHELL_SCRIPT)

    # Backup shell script directory
    shell_script_dir = os.path.dirname(SHELL_SCRIPT)
    whelper.backup_directory_with_timestamp(shell_script_dir, ignore_hidden=True)

    # Get shell script content
    with open(SHELL_SCRIPT, "r") as f:
        shell_lines = f.readlines()

    command_name = os.path.basename(create_exec_name(args.file))

    new_function_line = f"function {command_name}() {{{exec_file_path} $@}}\n"

    cmd_bools = [
        bool(re.search(rf"\b{command_name}\(\)", i)) for i in shell_lines
    ]  # True if the new function already exists

    if True in cmd_bools:
        cmd_idx = cmd_bools.index(True)  # index of the command in the shell script

        update_shell_function_and_description(
            SHELL_SCRIPT=SHELL_SCRIPT,
            shell_lines=shell_lines,
            cmd_idx=cmd_idx,
            command_name=command_name,
            new_desc=args.desc,
            new_function_line=new_function_line,
        )

    else:
        # Insert new command if it does not exist
        insert_new_shell_function_and_description(
            SHELL_SCRIPT=SHELL_SCRIPT,
            shell_lines=shell_lines,
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
            (
                args.desc[2:-1] if args.desc else "NO_UPDATE"
            ),  # [2:] to escape the '# ' at the beginning and '\n' at the end
        ]
    )


if __name__ == "__main__":
    main()
