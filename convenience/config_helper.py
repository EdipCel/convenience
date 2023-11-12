"""
This module is a convenience module and configparser wrapper.

It provides a convenient way to access the settings in the config.ini
or specified configuration file.
Follows python's configparser library.
"""

import configparser
from os.path import exists


class Config:
    """
    The instance reads the default config values from the config_ini_file file.

    These config_ini_file sections are later available using the Config objects.
    The default file is convenience/config.ini.
    """

    def __init__(self, config_ini_file="convenience/config.ini") -> None:
        self._config = configparser.ConfigParser()

        try:
            if exists(config_ini_file):
                self._config.read(config_ini_file)
            else:
                raise FileNotFoundError

        except FileNotFoundError as exc:
            print(
                f"FileNotFoundError occured in Config class while reading and parsing the {config_ini_file} file."
            )
            print("Exception details:")
            print(exc.message)

        except configparser.MissingSectionHeaderError as exc:
            print(
                f"MissingSectionHeaderError occured in Config class while reading and parsing the {config_ini_file} file."
            )
            print("Exception details:")
            print(exc.message)

    def get_config(self) -> configparser.ConfigParser:
        """Gets the ConfigParser already populated with the settings from the ini file.
        This will contain all the sections. You can loop over the settings using two 
        indices like: config['database']['schema']"""
        return self._config

    def get_setting_value(self, section: str, setting: str) -> str:
        """Provided with section and setting names returns the current value from the ini file."""
        return self._config[section][setting]
