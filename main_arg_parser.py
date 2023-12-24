import argparse


class MainArgParser:
    def __init__(
        self,
        prog: str,
        subparser_description: str,
        subparser_name="action",
        description: str = "select the py2bin action",
    ):
        self.parser = argparse.ArgumentParser(prog=prog, description=description)
        self.subparsers = self.parser.add_subparsers(
            title=subparser_name,
            dest=subparser_name,
            description=subparser_description,
            required=True,
        )

    def parse_args(self):
        return self.parser.parse_args()
