"""
@file
@brief  parsing HTML to convert it into JSON
"""
import html.parser


def iterate_on_json(json_structure, prefix="", keep_dictionaries=False,  # pylint: disable=W0102
                    skip=["__parent__"]):  # pylint: disable=W0102
    """
    Iterates on every field contains in the :epkg:`JSON` structure.

    @param      json_structure      json structure
    @param      prefix              prefix to add
    @param      keep_dictionaries   if True, add yield k,v where v is a JSON dictionary
    @param      skip                do not enter the following tag
    @return     iterator of (path, value)
    """
    for k, v in sorted(json_structure.items()):
        if k in skip:
            continue
        p = prefix + "/" + k
        if isinstance(v, str):
            yield (p, v)
        elif isinstance(v, dict):
            if keep_dictionaries:
                yield (p, v)
            for r in iterate_on_json(v, p, keep_dictionaries, skip):
                yield r
        elif isinstance(v, list):
            for el in v:
                if keep_dictionaries:
                    yield (p, el)
                for r in iterate_on_json(el, p, keep_dictionaries, skip):
                    yield r
        else:
            raise Exception(  # pragma: no cover
                "Unexpected type, the json was altered at path '{0}'".format(
                    p))


class HTMLtoJSONParser(html.parser.HTMLParser):

    """
    Parses :epkg:`HTML` and output a :epkg:`JSON` structure.
    Example:

    ::

        file = ...
        with open(file,"r",encoding="utf8") as f : content = f.read()
        parser = HTMLtoJSONParser()
        parser.feed(content)
        js = parser.json

    Or:

    ::

        js = HTMLtoJSONParser.to_json(content)

    To iterator on path:

    ::

        all = [ (k,v) for k,v in HTMLtoJSONParser.iterate(js) ]
    """

    def __init__(self, raise_exception=True):
        """
        @param      raise_exception     if True, raises an exception if the
                                        HTML is malformed, otherwise does what it can
        """
        html.parser.HTMLParser.__init__(self, convert_charrefs=True)
        self.doc = {}
        self.path = []
        self.cur = self.doc
        self.line = 0
        self.raise_exception = raise_exception

    @property
    def json(self):
        """
        Returns the :epkg:`JSON` strucure.
        @return     json
        """
        return self.doc

    @staticmethod
    def to_json(content, raise_exception=True):
        """
        Converts :epkg:`HTML` into :epkg:`JSON`.
        @param      content             :epkg:`HTML` content to parse
        @param      raise_exception     if True, raises an exception if the HTML is malformed, otherwise does what it can
        """
        parser = HTMLtoJSONParser(raise_exception=raise_exception)
        parser.feed(content)
        return parser.json

    @staticmethod
    def iterate(json_structure, prefix="", keep_dictionaries=False,  # pylint: disable=W0102
                skip=["__parent__"]):  # pylint: disable=W0102
        """
        Iterates on every field contains in the :epkg:`JSON` structure.

        @param      json_structure      json structure
        @param      prefix              prefix to add
        @param      keep_dictionaries   if True, add yield k,v where v is a JSON dictionary
        @param      skip                do not enter the following tag
        @return     iterator of (path, value)
        """
        for _ in iterate_on_json(
                json_structure, prefix, keep_dictionaries, skip):
            yield _

    def handle_starttag(self, tag, attrs):
        """
        What to do for a new tag.
        """
        self.path.append(tag)
        attrs = {k: v for k, v in attrs}  # pylint: disable=R1721
        if tag in self.cur:
            if isinstance(self.cur[tag], list):
                self.cur[tag].append({"__parent__": self.cur})
                self.cur = self.cur[tag][-1]
            else:
                self.cur[tag] = [self.cur[tag]]
                self.cur[tag].append({"__parent__": self.cur})
                self.cur = self.cur[tag][-1]
        else:
            self.cur[tag] = {"__parent__": self.cur}
            self.cur = self.cur[tag]

        for a, v in attrs.items():
            self.cur["#" + a] = v
        self.cur[""] = ""

    def handle_endtag(self, tag):
        """
        What to do for the end of a tag.
        """
        if tag != self.path[-1] and self.raise_exception:
            raise Exception(  # pragma: no cover
                "html is malformed around line: {0} (it might be because "
                "of a tag <br>, <hr>, <img .. > not closed)".format(
                    self.line))
        del self.path[-1]
        memo = self.cur
        self.cur = self.cur["__parent__"]
        self.clean(memo)

    def handle_data(self, data):
        """
        What to do with data.
        """
        self.line += data.count("\n")
        if "" in self.cur:
            self.cur[""] += data

    def clean(self, values):
        """
        Cleans a dictionary of value.
        """
        keys = list(values.keys())
        for k in keys:
            v = values[k]
            if isinstance(v, str):
                #print ("clean", k,[v])
                c = v.strip(" \n\r\t")
                if c != v:
                    if len(c) > 0:
                        values[k] = c
                    else:
                        del values[k]
                elif len(v) == 0:
                    del values[k]
        del values["__parent__"]
