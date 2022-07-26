"""Get Configuration Items."""
import configparser
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
configFilename = os.path.join(dir_path, "..", "config.ini")

config = configparser.RawConfigParser()
config.read(configFilename)

dbString = config["DATABASE"]["ConnectionString"]
dbParams = dict(entry.split("=") for entry in dbString.split(";"))

boxViewUrl = config["APP_SETTINGS"]["ViewBoxUrl"]
