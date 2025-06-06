from src.filepath import FilePathInfo

class MetaPath:
    def __init__(self):
        file_info = FilePathInfo()
        self.meta = file_info.process()
        self.metapath = f"{self.meta.get('upload_folder')}/metadata.json"

    def get_metapath(self):
        return self.metapath
