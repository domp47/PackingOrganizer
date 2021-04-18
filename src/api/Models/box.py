class Box():
    def __init__(self, body: dict = None):
        if body is None:
            return

        self.id = body['id'] if 'id' in body else None
        self.label = body['label'] if 'label' in body else None
        self.description = body['description'] if 'description' in body else None

    id: int = None
    label: str = None
    description: str = None