import requests
import re
from packaging import version
from pathlib import Path
from src.ia import console

class VersionChecker:
    def __init__(self, local_path="src/version.py", remote_url=None):
        self.local_version_file = Path(local_path)
        self.remote_version_url = remote_url or \
            "https://raw.githubusercontent.com/xDE3PM/BWT-Uploader/main/src/version.py"

    def get_local_version(self):
        """Extract the local version from src/version.py."""
        try:
            content = self.local_version_file.read_text(encoding='utf-8')
            match = re.search(r'version\s*=\s*"([^"]+)"', content)
            if match:
                return match.group(1)
        except FileNotFoundError:
            console.print("[bold red]Local version file not found.[/bold red]")
        return None

    def get_remote_version(self):
        """Fetch the latest version from the remote version.py file."""
        try:
            response = requests.get(self.remote_version_url, timeout=5)
            response.raise_for_status()
            content = response.text
            match = re.search(r'version\s*=\s*"([^"]+)"', content)
            if match:
                return match.group(1)
        except requests.RequestException:
            console.print("[bold red]Failed to fetch remote version.[/bold red]")
        return None

    def check_for_updates(self):
        """Compare local and remote version and print update info."""
        local_version = self.get_local_version()
        remote_version = self.get_remote_version()

        if not local_version:
            self.console.print("[bold red]Could not determine local version.[/bold red]")
            return False

        if not remote_version:
            self.console.print("[bold yellow]Could not check for updates. Using current version.[/bold yellow]")
            return False

        if version.parse(remote_version) > version.parse(local_version):
            console.print(f"[red][NOTICE] [green]Update available: v[/green][yellow]{remote_version}")
            console.print(f"[red][NOTICE] [green]Current version: v[/green][yellow]{local_version}\n")
            return True

        return False
