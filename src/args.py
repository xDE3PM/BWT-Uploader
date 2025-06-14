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
            description="BWT-Uploader: Torrent Upload Assistant for BWTorrents.Tv",
            formatter_class=ShortHelpFormatter
        )
        self.add_arguments()
        self.args = self.parser.parse_args()
        self.metadata = self.gmeta()

    def add_arguments(self):
        self.parser.add_argument(
            "filepath",
            nargs="?",
            help="Path to the file or directory to upload (required)"
        )
        self.parser.add_argument(
            "--version", "-v",
            action="version",
            version="BWT-Uploader 1.0.0 Beta",
            help="Show program version and exit"
        )
        self.parser.add_argument(
            "--imdb", "-i",
            help="IMDb ID Number for the content (e.g., 1234567)"
        )
        self.parser.add_argument(
            "--tmdb", "-t",
            help="TMDb ID Number for the content (e.g., 123456)"
        )
        self.parser.add_argument(
            "--no-tmdb", "-NT",
            action="store_true",
            help="Skip fetching TMDb metadata"
       )
        self.parser.add_argument(
            "--no-imdb-tmdb", "-NIT",
            action="store_true",
            help="Skip fetching IMDb and TMDb metadata"
        )
        self.parser.add_argument(
            "--request", "-r",
            action="store_true",
            help="Mark torrent as fulfilling a user request"
        )
        self.parser.add_argument(
            "--recommended", "-rm",
            action="store_true",
            help="Mark torrent as a recommended upload"
        )
        self.parser.add_argument(
            "--no-youtube", "-NY",
            action="store_true",
            help="Skip fetching a YouTube trailer"
        )
        self.parser.add_argument(
            "--double-upload", "-du",
            action="store_true",
            help="Enable double upload mode"
        )
        self.parser.add_argument(
            "--category", "-c",
            type=int,
            help="Category ID for the torrent (e.g., 119 for Bollywood-Untouched WEB-DLs, 145 for Bangla-Movies)"
        )
        self.parser.add_argument(
            "--piece-length", "-p",
            type=int,
            help="Piece length as 2^n bytes (16-27, default: automatic)"
        )

    def get_args(self):
        return self.args

    def gmeta(self):
        if not self.args.filepath:
            self.parser.print_help(sys.stderr)
            sys.exit(1, "\nError: filepath is required\n")
        
        if not Path(self.args.filepath).exists():
            self.parser.print_help(sys.stderr)
            sys.exit(1, f"\nError: filepath '{self.args.filepath}' does not exist\n")
         
        meta = {
            "filepath": str(self.args.filepath),
            "imdbID": self.args.imdb,
            "tmdbID": self.args.tmdb,
            "skip_tmdb": self.args.no_tmdb,
            "skip_imdb_tmdb": self.args.no_imdb_tmdb,
            "request": self.args.request,
            "recommended": self.args.recommended,
            "doubleupload": self.args.double_upload,
            "category_id": self.args.category,
            "skip_youtube": self.args.no_youtube,
            "piece_length": self.args.piece_length,
        }
        
        return meta
