import os
import subprocess
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

    def create(self):
        if os.path.exists(self.output_torrent):
            console.print("[bold green]\n ✔ Torrent file already exists. Skipping creation.\n")
            return
            
        console.print("[bold yellow]\n ➥ Createing Torrent file...\n")
        command = f'py3createtorrent -P -c DE3PM -t {self.tracker} "{self.input_filepath}" -o "{self.output_torrent}"'
        process = subprocess.run(command, shell=True, capture_output=True, text=True)
        console.print(f"[bold green] ✔ {process.stdout}")
        console.print(f"[bold red] ✘ {process.stderr}")        
        if os.path.exists(self.output_torrent):
            self.modify_torrent(self.output_torrent)

    def modify_torrent(self, torrent_file):
        try:
            with open(torrent_file, "rb") as f:
                torrent_data = bencode.bdecode(f.read())

            torrent_data["comment"] = "-=DE3PM=-"
            torrent_data["created by"] = "-=DE3PM=-"
            torrent_data["info"]["source"] = "-=DE3PM=-"
            torrent_data["source"] = "-=DE3PM=-"
            torrent_data["source.utf-8"] = "-=DE3PM=-"

            with open(torrent_file, "wb") as f:
                f.write(bencode.bencode(torrent_data))
        except Exception as e:
            console.print(f"[bold red] Error modifying torrent file: {e}")
 
