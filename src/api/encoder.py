"""Custom JSON Encoder for Date Time."""
from json import JSONEncoder


class Encoder(JSONEncoder):
    """Custom JSON Encoder for Date Time."""

    def default(self, o):
        """Encode object."""
        return o.__dict__
