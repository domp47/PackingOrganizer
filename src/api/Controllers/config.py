"""Get Configuration Items."""
import configparser
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
configFilename = os.path.join(dir_path, "..", "config.ini")

config = configparser.RawConfigParser()
config.read(configFilename)

dbFile = config["DATABASE"]["DbFile"]
boxViewUrl = config["APP_SETTINGS"]["ViewBoxUrl"]
