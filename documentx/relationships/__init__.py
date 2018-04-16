class Relationship:
    def __init__(self, root):
        self._root = root

    def __repr__(self):
        return "<Relationship id='%s' target='%s'>" % (self.id, self.target)

    @property
    def id(self):
        return self._root.attrib.get('Id', None)

    @property
    def target(self):
        return self._root.attrib.get('Target', None)

    @property
    def type(self):
        return self._root.attrib.get('Type', None)
