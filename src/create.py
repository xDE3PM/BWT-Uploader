import os
import time
import math
import shutil
import sys
import bencode
from src.ia import console
from src.filepath import FilePathInfo

class Torrent:
    def __init__(self):
        self.file_info = FilePathInfo()
        self.fmeta = self.file_info.process()
        self.output_torrent = self.fmeta.get('torrent_path')
        self.input_filepath = self.fmeta.get('filepath')
        self.tracker = "https://bwtorrents.tv/announce.php"
        self.debug = self.fmeta.get('debug', False)
        self.piece_size_length = self.fmeta.get('piece_length', None)

    def create(self):
        if os.path.exists(self.output_torrent):
            console.print("[bold green]\n ✔ Torrent file already exists. Skipping creation.\n")
            return

        if not shutil.which("mkbrr") and not shutil.which("py3createtorrent"):
            console.print("[bold red] ✘ Neither mkbrr nor py3createtorrent is installed.\n")
            return
        
        if not shutil.which("mkbrr"):
            self.create_with_py3()
        else:
            self.create_with_mkbrr()

    def piece_size(self):
        piece_size_map = {
            16: ("64KB", 64),
            17: ("128KB", 128),
            18: ("256KB", 256),
            19: ("512KB", 512),
            20: ("1MB", 1024),
            21: ("2MB", 2048),
            22: ("4MB", 4096),
            23: ("8MB", 8192),
            24: ("16MB", 16384),
            25: ("32MB", 32768),
            26: ("64MB", 65536),
            27: ("128MB", 131072)
        }
        return piece_size_map

    def create_with_mkbrr(self):
        console.print("[bold yellow]\n ➥ Creating torrent file with mkbrr...")
        cmd = [
            "mkbrr", "create",
            self.input_filepath,
            "--private",
            "-t", self.tracker,
            "-o", self.output_torrent
        ]
        if self.piece_size_length:
            if 16 <= self.piece_size_length <= 27:
                piece_size_map = self.piece_size()
                piece_info = piece_size_map.get(self.piece_size_length)
                if piece_info:
                    display_size, kib_size = piece_info
                    console.print(f"[bold] Using Piece Size Length : {display_size}")
                    cmd.extend(["--piece-length", str(self.piece_size_length)])
                else:
                    console.print("[bold red] Piece Size Length : Invalid size")
                    console.print("[bold yellow] Using Default Piece Size")
            else:
                console.print("[bold red] Piece Size Length : Invalid size")
                console.print("[bold yellow] Using Default Piece Size")
      
        command_str = " ".join(f'"{arg}"' if ' ' in arg else arg for arg in cmd)

        if self.debug:
            console.print(f"[cyan]mkbrr cmd: {command_str}")

        result = os.system(command_str)

        if result == 0 and os.path.exists(self.output_torrent):
            self.modify_torrent()
            console.print("[bold green] ✔ Torrent created successfully with mkbrr.\n")
        else:
            console.print("[bold red] ✘ Failed to create torrent with mkbrr\n")
            sys.exit(1)

    def create_with_py3(self):
        console.print("[bold yellow]\n ➥ Creating torrent file with py3createtorrent...")
        cmd = [
            "py3createtorrent",
            "-P",
            "-c", "DE3PM",
            "-t", self.tracker,
            self.input_filepath,
            "-o", self.output_torrent
        ]
        if self.piece_size_length:
            if 16 <= self.piece_size_length <= 27:
                piece_size_map = self.piece_size()
                piece_info = piece_size_map.get(self.piece_size_length)
                if piece_info:
                    display_size, kib_size = piece_info
                    console.print(f"[bold] Using Piece Size Length : {display_size}")
                    cmd.extend(["--piece-length", str(kib_size)])
                else:
                    console.print("[bold red] Piece Size Length : Invalid size")
                    console.print("[bold yellow] Using Default Piece Size")
            else:
                console.print("[bold red] Piece Size Length : Invalid size")
                console.print("[bold yellow] Using Default Piece Size")
      
        command_str = " ".join(f'"{arg}"' if ' ' in arg else arg for arg in cmd)

        if self.debug:
            console.print(f"[cyan]py3createtorrent cmd: {command_str}")

        result = os.system(command_str)

        if result == 0 and os.path.exists(self.output_torrent):
            self.modify_torrent()
            console.print("[bold green] ✔ Torrent created successfully with py3createtorrent.\n")
        else:
            console.print("[bold red] ✘ Failed to create torrent with py3createtorrent.")
            sys.exit(1)

    def modify_torrent(self):
        try:
            with open(self.output_torrent, "rb") as f:
                torrent_data = bencode.bdecode(f.read())

            torrent_data["comment"] = "-=DE3PM=-"
            torrent_data["created by"] = "-=DE3PM=-"
            torrent_data["info"]["source"] = "-=DE3PM=-"
            torrent_data["source"] = "-=DE3PM=-"
            torrent_data["source.utf-8"] = "-=DE3PM=-"

            with open(self.output_torrent, "wb") as f:
                f.write(bencode.bencode(torrent_data))
        except Exception as e:
            console.print(f"[bold red] Error modifying torrent file: {e}")
