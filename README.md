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
2. Navigate to the cloned directory.
3. Run the setup script: `./setup.sh`
4. Install the required packages in environment.yml
5. Configure the conda environments path in .env

## Usage

Once installed and completed the setup, you can start using py2bin with the following commands:

1. Convert a Python file to an Executable:

    ```
    py2bin [path/to/python_file.py] -d <optional description>
    ```

2. List Added Scripts:

    ```
    cmd
    ```

### demo screenshot ...

3. Add other customized shell functions to the list:

    ```
    cmd-add -n <name> -f <the script location> -d <description>
    ```

## Contributing

Contributions to py2bin are welcome! If you encounter any issues or have suggestions for improvements, please feel free to submit a pull request or open an issue on the GitHub repository.

## License

This project is licensed under the MIT License

## Acknowledgments

-   [List any acknowledgments or references to external libraries/frameworks used in your project]
