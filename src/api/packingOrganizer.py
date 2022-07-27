"""Main API entrypoint."""
import configparser
import os

import connexion
from encoder import Encoder
from flask_cors import CORS

dir_path = os.path.dirname(os.path.realpath(__file__))
configFilename = os.path.join(dir_path, "config.ini")

config = configparser.RawConfigParser()
config.read(configFilename)

dbString = config["DATABASE"]["DbFile"]

if dbString is None:
    raise ValueError("DATABASE/DbFile cannot be empty.")

# Create the application instance
app = connexion.App(__name__, specification_dir="./")

CORS(app.app, origins="*")

app.app.json_encoder = Encoder

# Read the swagger.yml file to configure the routes
app.add_api("swagger.yml")

# If we're running in stand alone mode, run the application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
