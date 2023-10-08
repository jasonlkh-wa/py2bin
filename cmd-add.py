from dotenv import load_dotenv
import os
import argparse


def create_dirs_and_file_if_not_exists(file: str):
    dirname = os.path.dirname(file)
    if not os.path.exists(dirname):
        print(f"\nDirectory {dirname} does not exist, created one successfully.")
        os.makedirs(dirname)

    if not os.path.exists(file):
        with open(file, "w") as f:
            pass
        print(f"\nFile {file} does not exist, created one successfully.")


def update_item_if_exists(csv_path: str, new_cmd, new_file, new_description):
    with open(csv_path, "r") as f:
        csv_lines = f.readlines()

    for i in range(1, len(csv_lines)):
        line = csv_lines[i].split(",")
        cmd, file, description = (
            line[0].strip('"'),
            line[1].strip('"'),
            line[2].strip('"'),
        )

        # Check if command exists
        if new_cmd == cmd:
            if (
                new_description == "NO_UPDATE"
            ):  # Special token to escape description update
                new_description = description
            if file != new_file or description != new_description:
                print("Command exists in the list")
                if file != new_file:
                    print("\nold file -> new file:")
                    print(f"{file} -> {new_file}")
                if description != new_description:
                    print("\nold description -> new description:")
                    print(f"{description} -> {new_description}")

                if input("\nOverwrite the exists command y/[n]?") == "y":
                    csv_lines[i] = f'"{new_cmd}","{new_file}","{new_description}"'

                    # Write the csv with changes
                    with open(csv_path, "w") as f:
                        f.write("".join(csv_lines))

                    print(
                        "\nCommand list updated"
                        + f"\nold:\ncmd: {cmd}\nfile: {file}\ndescription:{description}\n"
                        + f"\nnew:\ncmd: {new_cmd}\nfile: {new_file}\ndescription: {new_description}"
                    )

                else:
                    print("\nAll changes discarded. Program exits.")
            else:
                print("\nCommand exists and no change is needed")
            return True
    return False


def main():
    # Load .env
    PWD = os.path.dirname(__file__)
    load_dotenv(os.path.join(PWD, ".env"))
    print(os.getenv("CSV_SOURCE"))
    cmd_csv = os.path.expanduser(os.getenv("CSV_SOURCE"))

    # Cli argument parser
    parser = argparse.ArgumentParser(description="Adding new item to command list csv")

    parser.add_argument(
        "-n", "--name", type=str, help="The command name", required=True
    )
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        help="The source file path of the command",
        required=True,
    )
    parser.add_argument("-d", "--desc", type=str, help="The description", required=True)

    args = parser.parse_args()

    # Initialize CSV file if it does not exist
    if not os.path.exists(cmd_csv):
        create_dirs_and_file_if_not_exists(cmd_csv)
        with open(cmd_csv, "a") as f:
            f.write("cmd,file,description")

    # Update item if exists
    is_item_exist = update_item_if_exists(
        csv_path=cmd_csv,
        new_cmd=args.name,
        new_file=args.file,
        new_description=args.desc,
    )

    # Insert new item to cmd.csv
    if not is_item_exist:
        with open(cmd_csv, "a") as f:
            f.write(f'\n"{args.name}","{args.file}","{args.desc}"')

        print("New command added successfully!")


if __name__ == "__main__":
    main()
