"""
@file

@brief      functions related to XML files representing objects
"""

from pyquickhelper.loghelper.flog import GetSepLine
from .xml_tree import XMLHandlerDict, XMLIterParser


def _iteration_values(values):
    """
    Iterators on all possible tuple of values taken into a list.
    Let's assume you have two rows:
    @code
    a1 a2 a3
    b1 b2
    @endcode

    The function will produce:
    @code
    a1 b1
    a1 b2
    a2 b1
    a2 b2
    a3 b1
    a3 b2
    @endcode

    The function is used by @see fn table_extraction_from_xml_files_iterator.

    @param      values      list of rows
    @return                 iterator on rows
    """
    co = []
    for v in values:
        if isinstance(v, list):
            co.append(v)
        else:
            co.append([v])

    ind = [0 for _ in co]
    while ind[0] < len(co[0]):
        line = [c[i] for c, i in zip(co, ind)]
        yield line

        ind[-1] += 1
        i = len(ind) - 1
        while i > 0:
            if ind[i] >= len(co[i]):
                ind[i] = 0
                ind[i - 1] += 1
            i -= 1


def table_extraction_from_xml_files_iterator(file, fields, log=False, fLOG=None, encoding="utf-8", errors=None):
    """
    Goes through a XML file, extract values and put them into an iterator.

    @param      file        a file
    @param      fields      list of fields to get from the XML files (see below)
    @param      log         do logs if True
    @param      fLOG        logging function
    @param      errors      sent to function :epkg:`*py:library:function`
    @param      encoding    encoding
    @return                 iterator on lines

    One example for fields:

    ::

        [   ("tag1/tag2",           "all"),
            ("tag1/tag2/tag3/_",    "one"),
            ...
        ]
    """

    fileh = open(file, "r", encoding=encoding, errors=errors) if isinstance(
        file, str) else file

    parser = XMLIterParser()
    handler = XMLHandlerDict(no_content=True)
    parser.setContentHandler(handler)

    fields = [(a.split("/"), b) for a, b in fields]
    if log:
        fLOG("table_extraction_from_xml_files: begin")

    for i_, o in enumerate(parser.parse(fileh)):

        values = []
        nb = 0
        for look, typ in fields:
            path = o.find_node_value(look)

            if typ == "one":
                if len(path) == 0:
                    if log:
                        fLOG(o.get_xml_content())
                    raise Exception(
                        "unable to find a value for path %s" %
                        "/".join(look))
                val = path[0]
                if val is None:
                    val = ""
            elif typ == "all":
                if len(path) == 1:
                    val = path[0]
                elif len(path) == 0:
                    val = ""
                else:
                    val = path
                    nb += 1
            else:
                raise Exception(
                    "the type must in (one, all) %s,%s" %
                    (look, typ))
            values.append(val)

        if nb == 0:
            line = "\t".join(values)
            yield line
        else:
            for v in _iteration_values(values):
                line = "\t".join(v)
                yield line

        if log and (i_ + 1) % 1000 == 0:
            fLOG("table_extraction_from_xml_files reading ", i_)

    if isinstance(file, str):
        fileh.close()
    if log:
        fLOG("table_extraction_from_xml_files: end")


def table_extraction_from_xml_files(file, output, fields, log=False, encoding="utf-8", errors=None):
    """
    Goes through a :epkg:`XML` file, extract values and put them into a flat file.

    @param      file        a file
    @param      output      output file, string or file object,
    @param      fields      list of fields to get from the XML files
    @param      log         do logs if True
    @param      errors      sent to function :epkg:`*py:library:function`
    @param      encoding    encoding

    One example for fields:

    ::

        [   ("tag1/tag2",           "all"),
            ("tag1/tag2/tag3/_",    "one"),
            ...
        ]
    """
    outputh = open(output, "w", encoding=encoding,
                   errors=errors) if isinstance(output, str) else output
    for line in table_extraction_from_xml_files_iterator(file, fields, log):
        outputh.write(line)
        outputh.write(GetSepLine())
    if isinstance(output, str):
        outputh.close()


def xml_filter_iterator(file, filter=None, log=False, xmlformat=True,
                        fLOG=None, encoding="utf-8", errors=None):
    """
    Goes through a :epkg:`XML` file,
    returns :epkg:`XML` content if a condition is verified,
    the result is an iterator.

    @param      file        a file
    @param      filter      a function which takes a node and returns a boolean, if None, accepts everything
    @param      log         do logs if True
    @param      xmlformat   if True, return the xml, otherwise return the node
    @param      fLOG        logging function
    @param      encoding    encoding
    @param      errors      sent to function :epkg:`*py:library:function`
    @return                 the xml format or a node depending on thevalue of xmlformat
    """
    if filter is None:
        def filter(node):
            return True

    fileh = open(file, "r", encoding=encoding, errors=errors) if isinstance(
        file, str) else file

    parser = XMLIterParser()
    handler = XMLHandlerDict()
    parser.setContentHandler(handler)

    for i_, o in enumerate(parser.parse(fileh)):

        res = filter(o)
        if res:
            if xmlformat:
                yield o.get_xml_content()
            else:
                yield o

        if log and (i_ + 1) % 1000 == 0:
            fLOG("table_extraction_from_xml_files reading ", i_)

    if isinstance(file, str):
        fileh.close()
    if log:
        fLOG("xml_filter_iterator: end")


def xml_filter(file, output, filter, log=False, xmlformat=True, encoding="utf-8", errors=None):
    """
    go through a XML file, return XML content if a condition is verified, the result is put into a stream

    @param      file        a file
    @param      output      output file, string or file object
    @param      filter      a function which takes a node and returns a boolean
    @param      xmlformat   if True, return the xml, otherwise return the node
    @param      encoding    encoding
    @param      errors      sent to function :epkg:`*py:library:function`
    @param      log         do logs if True
    """
    outputh = open(output, "r", encoding=encoding,
                   errors=errors) if isinstance(output, str) else output
    for line in xml_filter_iterator(file, filter, log, xmlformat):
        outputh.write(line)
        outputh.write(GetSepLine())
    if isinstance(output, str):
        outputh.close()
