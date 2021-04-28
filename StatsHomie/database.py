import os.path, copy, json

class Database:
    __database = None
    def __init__ (self, *, intent: str, file_name: str, default: dict):
        self.intent = intent
        self.file_name = file_name
        self.default = default
        if not os.path.exists (self.file_name):
            self.__database = copy.deepcopy (self.default)
            self.save ()
        else:
            with open (self.file_name, "r") as in_file:
                self.__database = json.load (in_file)
    def __getitem__ (self, key):
        if key not in self.__database:
            if key not in self.default: raise Exception (f"Invalid {self.intent} key {key}")
            self.__setitem__ (key, copy.deepcopy (self.default [key]))
        if self.__database.get (key, None) is None: raise Exception (f"Key {key} is set to null; assign a value in your {self.intent} file")
        return self.__database [key]
    def __setitem__ (self, key, value):
        self.__database [key] = value
        self.save ()
    def __delitem__ (self, key):
        del self.__database [key]
        self.save ()
    def save (self):
        with open (self.file_name, "w+") as out_file:
            json.dump (self.__database, out_file)
