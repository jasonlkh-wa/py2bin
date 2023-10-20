# Py2bin

## Description

Py2bin is a tool designed to assist in running Python scripts seamlessly in command line interface (cli).

It offers a smooth deployment workflow for python scripts to run as shell functions in cli, which you **no longer need to type the lengthy .py file path to call your script.**

_The tool currently only supports Anaconda user._

## Features

1. Convert the Python file to executable and shell function
2. Display all added scripts in a CLI Table View

## Installation and Initial setup

To install py2bin, you can follow these steps:

1. Clone the py2bin repository from GitHub

```shell
git clone <github-repo-link>
```

2. Navigate to the cloned directory.
3. Run the setup script: `./setup.sh`
4. Configure the conda environments path in .env

```shell
# Example
CONDA_ENVS="~/opt/miniconda3/envs"
```

5. Create a conda venv with the required packages in environment.yml

```shell
conda env create --file environment.yml
```

6. Run the following command to initiate py2bin, cmd and cmd-add

```shell
# Initiate py2bin
# example path of py2bin: ~/python-project/py2bin/py2bin.py
python py2bin.py <full path of py2bin.py> -d "Convert py file to exec with py2bin"

# Initiate cmd-add (py2bin is set up)
# example path of cmd-add: ~/python-project/py2bin/cmd-add.py
py2bin <full path of cmd-add.py> -d "Add new function to py2bin's command list"
```

Lastly, add this line to py2bin/shell-scripts/custom-command.sh

```shell
# View all commands
function cmd() {<conda venv path>/bin/csvlook <py2bin path>/resources/cmd.csv}
```

## Usage

Once installed and completed the setup, you can start using py2bin with the following commands:

1. Convert a Python file to an Executable:

    ```shell
    py2bin [path/to/python_file.py] -d <optional description>
    ```

2. List Added Scripts:

    ```
    cmd
    ```

3. Manually add non-python function to the py2bin's track list

    ```
    cmd-add -n <name of function> -f <reference file path> -d <description>
    ```

## Contributing

Contributions to py2bin are welcome! If you encounter any issues or have suggestions for improvements, please feel free to submit a pull request or open an issue on the GitHub repository.

## License

This project is licensed under the MIT License
