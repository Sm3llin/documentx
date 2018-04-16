from lxml import etree


class Document:
    """An adapter into interacting with the *.docx file format

    Helper functions are supplied to enable the user to implement fast gathering solutions to meet the document scraping
    requirements that they have. Also attempted implementation of ways to locate and pull embedded documents indexing of
    known previous keywords or table columns.
    """
    __parser = etree.XMLParser(encoding='utf-8')

    def __init__(self, docx_zipfile, mode='r'):
        """Opens the required lxml file streams for locating and building document layout

        :param docx_zipfile: valid open ZipFile object
        :param mode: read (r) or write (w) modes (only r implemented)
        """
        from zipfile import ZipFile
        from io import BytesIO

        if not isinstance(docx_zipfile, ZipFile) and not docx_zipfile.fp:
            raise AttributeError('docx_zipfile is required to be a valid ZipFile object')

        self.__zipfile = docx_zipfile
        self._document = etree.parse(BytesIO(self.zipfile.open('word/document.xml').read()))
        self._relationships = etree.parse(BytesIO(self.zipfile.open('word/_rels/document.xml.rels').read()))

    def getchildren(self):
        """Returns the children of the document.body XML tag (usually p and tbl tags)"""
        from element import Element

        body = self._document.getroot().getchildren()[0]
        return [Element.create_element(child) for child in body.getchildren()]

    def getchildrenoftag(self, tag):
        return [child for child in self.getchildren() if child.tag == "{%s}%s" % (doc.namespaces['w'], tag)]

    def get_relation_id(self, id):
        """Returns a Relationship object representing the matching XML tag from the _rels group"""
        for rel in self.relationships:
            if rel.id == id:
                return rel

    def get_object_io(self, target):
        """Returns a BytesIO of the target file"""
        from io import BytesIO
        return BytesIO(self.zipfile.open(target, 'r').read())

    @property
    def relationships(self):
        """Returns a list of document.xml.rels relationship XML tags"""
        from relationships import Relationship
        return [Relationship(root) for root in self._relationships.getroot().getchildren()]

    @property
    def namespaces(self):
        """Returns the namespace mapping for the etree root object"""
        return self.root.nsmap

    @property
    def root(self):
        """Returns the etree document root etree.Element"""
        return self._document.getroot()

    @property
    def zipfile(self):
        return self.__zipfile


if __name__ == '__main__':
    from zipfile import ZipFile
    doc = Document(ZipFile(r'../documents/deception.docx', 'r'))

    print(doc.namespaces)
    r = doc.root

    rels = doc.relationships
    print(rels)
    print(doc.get_relation_id('rId3'))
    children = doc.getchildren()
    print(doc.get_object_io('word/' + 'styles.xml'))

    for child in doc.getchildren():
        print(child.get_plain_text())
