import json, re

class Config:
    
    def __init__(self, filepath) -> None:
        self.filepath = filepath
        print("Initialiazing config.json...")
        with open(filepath) as fd:
            self.json = json.load(fd)
        print("config.json successfully loaded.")
    
    def get(self, path: str):
        index, new_path = self._split_path(path)
        return self.json[index][new_path]
    
    def put(self, path: str, value):
        index, new_path = self._split_path(path)
        self.json[index][new_path] = value
        with open(self.filepath, 'w') as fd:
            json.dump(self.json, fd, indent = 4)
    
    def _split_path(self, path: str):
        return path.split(".")[0], re.sub("^[a-z]*.", '', path)