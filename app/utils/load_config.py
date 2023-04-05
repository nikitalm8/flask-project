import yaml


class AutoConfig(dict):

    def __init__(self, recursive: bool=False, **kwargs):
        """
        Base class for config entity. Generates "magic" object from dict.

        :param bool recursive: Set attributes recursively, defaults to False
        """

        for key, value in kwargs.items():

            if recursive and isinstance(value, dict):

                setattr(self, key, AutoConfig(**value))

            else:

                setattr(self, key, value)

    def __repr__(self):

        return str(self.__dict__)


def load_config(path: str, recursive: bool=True) -> AutoConfig:
    """
    Load config from yaml file

    :param str path: Path to file
    :return AutoConfig: AutoConfig object
    """

    with open(path, "r") as file:

        config_as_json = yaml.safe_load(file)

    return AutoConfig(recursive=recursive, **config_as_json)
