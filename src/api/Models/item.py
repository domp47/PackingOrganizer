class Item():
    def __init__(self, body: dict = None):
        if body is None:
            return

        self.id = body['id'] if 'id' in body else None
        self.boxId = body['boxId'] if 'boxId' in body else None
        self.name = body['name'] if 'name' in body else None

    id: int = None
    boxId: int = None
    name: str = None