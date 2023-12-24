import os
import subprocess
import pytest
import whelper
import tempfile

PWD = os.path.dirname(whelper.dirname(__file__))


def test_py2bin_add_new_command():
    # Call the main function with sample.py and -d flag

    # Create the temporary dir and files for config app
    temp_path = os.path.join(PWD, "tmp")
    os.makedirs(temp_path, exist_ok=True)

    temp_py_file = os.path.join(temp_path, "sample.py")
    conda_env_path = os.path.expanduser("~/opt/miniconda3/envs")
    dotenv_path = os.path.join(temp_path, ".env")
    shell_script_path = os.path.join(temp_path, "custom-commands.sh")
    csv_path = os.path.join(temp_path, "cmd.csv")

    with open(temp_py_file, "w") as file:
        file.write('print("Hello world!")')

    with open(dotenv_path, "w") as file:
        file.write(
            f"""CONDA_ENVS={conda_env_path}
SHELL_SCRIPT_PATH={shell_script_path}
CSV_SOURCE={csv_path}"""
        )

    with open(shell_script_path, "w") as file:
        file.write("")
    with open(csv_path, "w") as file:
        file.write("cmd,file,description")

    try:
        subprocess.run(
            [
                "python",
                f"{PWD}/py2bin.py",
                "add",
                str(temp_py_file),
                "-d",
                "sample description",
                "--dotenv",
                dotenv_path,
            ]
        )
        print("")
        with open(shell_script_path, "r") as file:
            assert (
                file.read()
                == """
# sample description
function sample() {/Users/jason/python-project/cli-tools/py2bin/tmp/sample $@}
"""
            )
        with open(csv_path, "r") as file:
            assert (
                file.read()
                == '''cmd,file,description
"sample","/Users/jason/python-project/cli-tools/py2bin/tmp/sample.py","sample description"'''
            )
    finally:
        subprocess.run(["rm", "-rf", temp_path])
