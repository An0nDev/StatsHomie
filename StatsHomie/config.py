import os.path, copy, json

class Config:
    default_config = {
        "discord_bot_token": None,
        "discord_is_bot": True,
        "hypixel_api_key": None,
        "prefix": "sh"
    }
    __config = None
    def __init__ (self, *, file_name):
        self.file_name = file_name
        if not os.path.exists (self.file_name):
            self.__config = copy.deepcopy (self.default_config)
            self.__save ()
        else:
            with open (self.file_name, "r") as in_file:
                self.__config = json.load (in_file)
    def __getitem__ (self, key):
        if key not in self.__config:
            if key not in self.default_config: raise Exception (f"Invalid config key {key}")
            self.__setitem__ (key, copy.deepcopy (self.default_config [key]))
        if self.__config.get (key, None) is None: raise Exception (f"Key {key} is set to null; assign a value in your config file")
        return self.__config [key]
    def __setitem__ (self, key, value):
        self.__config [key] = value
        self.__save ()
    def __delitem__ (self, key):
        del self.__config [key]
        self.__save ()
    def __save (self):
        with open (self.file_name, "w+") as out_file:
            json.dump (self.__config, out_file)
