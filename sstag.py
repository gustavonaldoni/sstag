import argparse
import textwrap

from cli.args_validator import ArgsValidator
from core.simple_stag_inserter import SimpleStagInserter
from core.simple_stag_extractor import SimpleStagExtractor


class SStag:
    def __init__(self, args) -> None:
        self.args = args

        self.simple_stag_inserter = SimpleStagInserter()
        self.simple_stag_extractor = SimpleStagExtractor()
    
    def show_main_menu(self) -> None:
        with open("./cli/main_menu.txt", "r") as main_menu_file:
            print(main_menu_file.read())

    def run(self) -> None:
        self.show_main_menu()

        if self.args.extract != "":
            self.simple_stag_extractor.extract_file(self.args.extract)
            return
        
        if self.args.src != "" and self.args.dst != "":
            self.simple_stag_inserter.insert_file_at_the_end(self.args.src, self.args.dst)


def main():
    epilog = ""

    with open("./cli/epilog.txt", "r") as epilog_file:
        epilog = epilog_file.read()

    parser = argparse.ArgumentParser(
        description="Simple Steganography by Gustavo Naldoni",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(epilog),
    )

    args_validator = ArgsValidator()

    parser.add_argument(
        "-s",
        "--src",
        required=False,
        default="",
        help="source file path",
    )
    parser.add_argument(
        "-d",
        "--dst",
        required=False,
        default="",
        help="destination file path",
    )
    parser.add_argument(
        "-e",
        "--extract",
        required=False,
        default="",
        help="path to the file to extract",
    )

    args = parser.parse_args()
    sstag = SStag(args)

    sstag.run()


if __name__ == "__main__":
    main()
