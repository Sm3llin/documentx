from element import Element


class TableColumn(Element):
    pass


class TableRow(Element):
    def __init__(self, root):
        super(TableRow, self).__init__(root)

        self._cols = []

        for child in self.getchildren():
            if self.element_is_type(child, 'tc'):
                self._cols.append(TableColumn(child))

    def get_plain_text(self):
        t = []

        for col in self._cols:
            t.append(col.get_plain_text())

        return ' | '.join(t)


class Table(Element):
    def __init__(self, root):
        super(Table, self).__init__(root)

        self._rows = []

        for child in self.getchildren():
            if self.element_is_type(child, 'tr'):
                self._rows.append(TableRow(child))

    def get_plain_text(self):
        t = ''

        for row in self._rows:
            t += '| ' + row.get_plain_text() + ' |\n'

        return t
