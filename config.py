import json, re

class Config:
    
    def __init__(self, filepath) -> None:
        print("Initialiazing config.json...")
        try: 
            with open(filepath) as fd:
                self.json = json.dumps(filepath)
            print("config.json successfully loaded.")
        except:
            raise FileNotFoundError("An error occured while trying to access config.json.")
    
    def get(self, path: str):
        index, new_path = self._split_path(path)
        print(index, new_path)
        #print(self.json[index][path])
    
    def _split_path(self, path: str):
        return path.split(".")[0], re.sub("^[a-z]*.", '', path)