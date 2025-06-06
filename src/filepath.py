import os
from pathlib import Path
from src.args import Args

VIDEO_EXTENSIONS = {
    '.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm',
    '.m2ts', '.vob'
}

class FilePathInfo:
    def __init__(self):
        self.meta = Args().gmeta()
        self.file_path = Path(self.meta.get("filepath", "")).resolve()
        self.file_name = None
        self.file_name_no_ext = None
        self.video_path = None
        self.video_file_name = None
        self.upload_folder = None
        self.torrent_path = None

    def _find_largest_video(self, start_path: Path) -> Path | None:
        largest_video = None
        largest_size = -1

        for file in start_path.rglob("*"):
            if file.is_file() and file.suffix.lower() in VIDEO_EXTENSIONS:
                try:
                    size = file.stat().st_size
                    if size > largest_size:
                        largest_size = size
                        largest_video = file
                except OSError:
                    continue

        return largest_video

    def process(self):
        if self.file_path.is_file():
            self.file_name = self.file_path.name
            self.file_name_no_ext = self.file_path.stem
            self.video_path = self.file_path

        elif self.file_path.is_dir():
            self.file_name = self.file_path.name
            self.file_name_no_ext = self.file_path.name

            # Check for Blu-ray
            bdmv_path = self.file_path / "BDMV" / "STREAM"
            if bdmv_path.is_dir():
                self.video_path = self._find_largest_video(bdmv_path)

            # Check for DVD
            elif (self.file_path / "VIDEO_TS").is_dir():
                self.video_path = self._find_largest_video(self.file_path / "VIDEO_TS")

            # Normal folder
            else:
                self.video_path = self._find_largest_video(self.file_path)

        if self.video_path:
            self.video_file_name = self.video_path.name

        self.upload_folder = Path("uploads") / self.file_name_no_ext
        self.upload_folder.mkdir(parents=True, exist_ok=True)

        self.torrent_path = self.upload_folder / f"{self.file_name_no_ext}.torrent"

        self.meta.update({
            "filename": self.file_name,
            "filename_noext": self.file_name_no_ext,
            "videopath": str(self.video_path) if self.video_path else None,
            "video_filename": self.video_file_name,
            "filepath": str(self.file_path),
            "upload_folder": str(self.upload_folder),
            "torrent_path": str(self.torrent_path),
        })

        return self.meta
