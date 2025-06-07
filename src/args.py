import argparse
import sys
from pathlib import Path

class ShortHelpFormatter(argparse.HelpFormatter):
    def __init__(self, *args, **kwargs):
        kwargs['max_help_position'] = 40
        kwargs['width'] = 100
        super().__init__(*args, **kwargs)

class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_help(sys.stderr)
        self.exit(2, f"\nError: {message}\n")

class Args:
    def __init__(self):
        self.parser = CustomArgumentParser(
            prog="BWT-Uploader",
            description="BWT-Uploader: Torrent Upload Assistant for BWTorrents",
            formatter_class=ShortHelpFormatter
        )
        self.add_arguments()
        self.args = self.parser.parse_args()
        self.metadata = self.gmeta()

    def add_arguments(self):
        self.parser.add_argument("filepath", nargs="?", help="Enter your Filepath of the file you want to upload...")
        self.parser.add_argument("--version", "-v", action="version", version="BWT-Uploader 1.0.0")
        self.parser.add_argument("--imdb", "-i", help="Enter your IMDb ID Number (e.g., 1234567)")
        self.parser.add_argument("--tmdb", "-t", help="Enter your TMDb ID Number (e.g., 123456)")
        self.parser.add_argument("--request", "-r", action="store_true", help="Mark torrent as fulfilling a request")
        self.parser.add_argument("--recomanded", "-rm", action="store_true", help="Mark torrent as a recommended upload")
        self.parser.add_argument("--doubleupload", "-du", action="store_true", help="Enable double upload option")
        self.parser.add_argument("--catagory", "-c", type=int, help="Category ID number for the upload")

    def get_args(self):
        return self.args

    def gmeta(self):
        if not self.args.filepath:
            print("No filepath provided.")
            return None

        meta = {
            "filepath": str(self.args.filepath),
            "imdb_id": self.args.imdb,
            "tmdb_id": self.args.tmdb,
            "request": self.args.request,
            "recomanded": self.args.recomanded,
            "doubleupload": self.args.doubleupload,
            "catagory_id": self.args.catagory,
        }
        
        return meta 
