# coding: latin-1
"""
@file

@brief  parsing XML
"""

import xml.sax.handler
import io
import xml.sax.expatreader
import xml.sax.saxutils as saxutils
from xml.parsers import expat

from .xml_tree_node import XMLHandlerDictNode


class XMLHandlerDict (xml.sax.handler.ContentHandler):

    """
    overload functions about XML, it produces objects at the end
    we assume the file contains a list of objects
    """

    def __init__(self, no_content=False):
        """
        constructor
        @param      no_content      avoid loading the content of every record
        """
        xml.sax.handler.ContentHandler.__init__(self)
        self._objs = []
        self._being = None
        self._level = 0
        self._tag = None
        self._tile = []
        self._pointer = None
        self._forget_root = True  # always True
        self._no_content = no_content
        self._prepare_stringio()

    def _prepare_stringio(self):
        """prepare the StringIO stream
        """

        if not self._no_content:
            self._xmlio = io.StringIO()
            self._xmlgen = saxutils.XMLGenerator(self._xmlio, "utf8")
            self._xmlgen.startDocument()
        else:
            self._xmlgen = None

    def startElement(self, name, attributes):
        """
        when enters a section
        """
        if self._level == 0 and self._forget_root:
            self._level = 1
            return

        if self._xmlgen is not None:
            self._xmlgen.startElement(name, attributes)

        self._tile.append(name)
        if self._being is None:
            self._tag = name
            self._being = XMLHandlerDictNode(
                None,
                name,
                self._level,
                root=True)
            self._pointer = self._being
        else:
            node = XMLHandlerDictNode(
                self._pointer,
                name,
                self._level,
                root=False)
            self._pointer.set(name, node)
            self._pointer = node

        for k in attributes.getNames():
            self._pointer.set(k, attributes[k].strip())
        self._level += 1

    def endElement(self, name):
        """
        after a tag
        """
        if len(self._tile) == 0:
            return

        if self._xmlgen is not None:
            self._xmlgen.endElement(name)

        self._pointer.strip()
        self._tile.pop()
        self._level -= 1
        if len(self._tile) == 0:
            self._being.rearrange()
            if self._xmlgen is not None:
                self._xmlgen.endDocument()
                self._xmlio.write("\n")
                content = self._xmlio.getvalue()
                if content.startswith("<?xml"):
                    end = content.find("\n") + 1
                    if len(content) > end and content[end] == "\n":
                        end += 1
                    content = content[end:]
            else:
                content = ""

            if isinstance(content, bytes):
                raise AssertionError("this should not happen")

            self._being.add_xml_content(content)
            self._objs.append(self._being)
            self._being = None
            self._pointer = None
            self._prepare_stringio()
        else:
            self._pointer = self._pointer.father

    def characters(self, data):
        """
        add characters
        """
        if self._xmlgen is not None:
            self._xmlgen.characters(data)

        if self._pointer is not None:
            self._pointer.buffer += data

# iteration version


class XMLIterParser (xml.sax.expatreader.ExpatParser):

    """
    to use a parser like an iterator

    example:
    @code
        print(__file__, self._testMethodName, OutputPrint = __name__ == "__main__")
        zxml = \"\"\"
                <mixed engine___="conf1" fid="3" grade___="Fair" query___="queryA" rank="3">
                  <urls>
                  <url___>http://www.shop.com/Soloxine_1_0mg_Tab-181378988-214010464-p!.shtml</url___>
                  <url___>http://fake</url___>
                  </urls>
                </mixed>
                <mixed engine___="conf1" fid="4" grade___="Good" query___="queryA" rank="4" url___="http%3A//www.lamars.com/products/nutrition.html" />
               \"\"\"

        zxml = "<root>%s</root>" % zxml
        f = StringIO.StringIO (zxml)
        assert len (f.getvalue ()) > 0

        parser  = XMLIterParser ()
        handler = XMLHandlerDict (no_content = False)
        parser.setContentHandler (handler)
        nb = 0
        for o in parser.parse(f) :
            assert o ["query___"] == "queryA"
            nb += 1
        assert nb > 0
    @endcode
    """

    def __init__(self, namespaceHandling=0, bufsize=2 ** 17):
        if bufsize is None:
            bufsize = 2 ** 17
        xml.sax.expatreader.ExpatParser.__init__(
            self,
            namespaceHandling=namespaceHandling,
            bufsize=bufsize)

    def parse(self, source, no_content=False):
        """
        Parse an XML document from a URL or an InputSource.
        @param      source          a file or a stream
        @param      no_content      avoid keeping the content into memory
        """
        source0 = source
        source = saxutils.prepare_input_source(source)

        self._source = source
        self.reset()
        self._cont_handler.setDocumentLocator(
            xml.sax.expatreader.ExpatLocator(self))

        # xmlreader.IncrementalParser.parse(self, source)
        # source = saxutils.prepare_input_source(source)

        self.prepareParser(source)
        file_char = source.getCharacterStream()
        if file_char is None:
            file_bytes = source.getByteStream()
            file = file_bytes
        else:
            file = file_char

        if file is None:
            raise FileNotFoundError(
                "file is None, it should not, source={0}\n{1}".format(source0, source0.name))

        buffer = file.read(self._bufsize)
        isFinal = 0
        while buffer != "" or isFinal == 0:
            # self.feed(buffer)
            data = buffer
            isFinal = 1 if len(buffer) == 0 else 0

            if not self._parsing:
                self.reset()
                self._parsing = 1
                self._cont_handler.startDocument()

            try:
                # The isFinal parameter is internal to the expat reader.
                # If it is set to true, expat will check validity of the entire
                # document. When feeding chunks, they are not normally final -
                # except when invoked from close.
                self._parser.Parse(data, isFinal)

                for o in self._cont_handler._objs:
                    yield o
                del self._cont_handler._objs[:]

            except expat.error as e:
                exc = xml.sax.SAXParseException(
                    expat.ErrorString(
                        e.code),
                    e,
                    self)
                # FIXME: when to invoke error()?
                # mes = "\n".join([str(e), str(exc)])
                self._err_handler.fatalError(exc)

            buffer = file.read(self._bufsize)

        # self.close()
        self._cont_handler.endDocument()
        self._parsing = 0
        # break cycle created by expat handlers pointing to our methods
        self._parser = None

        for o in self._cont_handler._objs:
            yield o
        del self._cont_handler._objs[:]
