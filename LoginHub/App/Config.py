import os
import configparser


class Config:
    def __init__(self, path: str = None):
        if path is None:
            self.__defaults_path = os.path.normpath(os.getcwd() + '/Config/defaults.ini')
        else:
            self.__defaults_path = os.path.normpath(path)
        self.__config = configparser.ConfigParser()
        if not os.path.isfile(self.__defaults_path):
            open(self.__defaults_path, 'a').close()
        self.__config.read(self.__defaults_path)

    def get(self, var: str, default_value: str = None):
        var = var.upper()
        section = var.split('_')[0]
        option = "_".join(var.split('_')[1:])
        if option == "":
            raise AttributeError("Invalid config var")
        else:
            if self.__config.has_section(section):
                if self.__config.has_option(section, option):
                    default = self.__config.get(section, option)
                else:
                    default = None
            else:
                self.__config.add_section(section)
                default = None
            env = os.getenv(var, default)
            if env is None:
                if default_value is not None:
                    self.__config.set(section, option, default_value)
                    with open(self.__defaults_path, 'w') as confighandler:
                        self.__config.write(confighandler)
                return default_value
            else:
                if env == "":
                    env = None
                    self.__config.remove_option(section, option)
                else:
                    self.__config.set(section, option, env)
                with open(self.__defaults_path, 'w') as confighandler:
                    self.__config.write(confighandler)
                return env

    def getbool(self, var: str, default_value: bool = None):
        value = self.get(var, str(default_value).lower())
        if value == 'true':
            return True
        elif value == 'false':
            return False
        else:
            return default_value

    def getint(self, var: str, default_value: int = None):
        value = self.get(var, default_value)
        try:
            value = int(value)
        except ValueError:
            value = None
        if value is not None:
            return value
        elif default_value is not None:
            try:
                default_value = int(default_value)
            except ValueError:
                default_value = None
            return default_value
        else:
            return None