class Element:
    def __init__(self, root):
        self._root = root

    @property
    def tag(self):
        return self._root.tag

    def getchildren(self):
        return [child for child in self._root.getchildren()]

    def get_plain_text(self):
        """Returns a str of the text within the Paragraph including only raw text"""
        t = ''

        for text in self._root.xpath('.//w:t', namespaces=self._root.nsmap):
            t += text.text

        return t

    def element_is_type(self, element, tag):
        return element.tag == "{%s}%s" % (self._root.nsmap['w'], tag)

    @staticmethod
    def create_element(root):
        """Returns the object corresponding to the tag type

        Paragraph and Table are the 2 currently supported types with each bringing unique interactions with each type.
        """
        from re import findall

        from paragraph import Paragraph
        from table import Table
        from table import TableRow
        from table import TableColumn
        from paragraph.run import Run
        from paragraph.object import Object
        from style import Style

        # Add new supported types here as they are added
        group_map = {
            'p': Paragraph,
            'tbl': Table,
            'tr': TableRow,
            'tc': TableColumn,
            'r': Run,
            'pPr': Style,
            'object': Object
        }

        tag = findall(r'{.*}(.*)', root.tag)[0]

        if tag in group_map.keys():
            return group_map[tag](root)
        return Element(root)
