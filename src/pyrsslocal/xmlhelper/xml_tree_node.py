"""
@file
@brief  parsing XML
"""

import copy

from pyquickhelper.loghelper.flog import guess_type_list, guess_type_value_type
from .xml_utils import escape
from .xml_exceptions import XmlException


class XMLHandlerDictNode(dict):
    """
    Defines a node containing a dictionary.

    @var        father      ancestor
    @var        name        name of the section (tag)
    @var        buffer      value or content of the section
    @var        level       level in the hierarchy
    @var        other       included sections
    """

    def __init__(self, father, name, level, root=False):
        """
        @param      father      father
        @param      name        node name
        @param      level       could be infered but still
        @param      root        is it the root
        """
        dict.__init__(self)
        self.father = father
        self.name = name
        self.buffer = ""
        self.level = level
        if father is None and not root:
            raise XmlException(
                "father is None and root is False, name = %s level = %d" %
                (name, level))
        self.other = []

    def __cmp__(self, other):
        a, b = id(self), id(other)
        if a < b:
            return -1
        elif a == b:
            return 0
        else:
            return 1

    def __lt__(self, other):
        return self.__cmp__(other) == -1

    def enumerate_on_tag(self, tag, recursive=False):
        """
        Enumerates all nodes sharing the same name: tag.

        @param  tag         node name to enumerate on
        @param  recursive   if True, looks into node (name == tag) if there are
                            sub-node with the same name
        @return             enumeration on node
        """
        if self.name == tag:
            yield self
        for o in self.other:
            if isinstance(o, tuple):
                if recursive:
                    for _ in o[1].enumerate_on_tag(tag):
                        yield _
                else:
                    yield o[1]
            else:
                for _ in o.enumerate_on_tag(tag):
                    yield _

    def add_xml_content(self, content):
        """
        Adds the content of the node itself (and all included nodes).
        """
        self.xmlcontent = content

    def get_xml_content(self):
        """
        @return self.xmlcontent
        """
        return self.xmlcontent if "xmlcontent" in self.__dict__ else None

    def __str__(self):
        """
        usual
        """
        mx = 0
        for k in self:
            mx = max(len(k), mx)
        head = self.level * "  "
        pile = [head + "*" + self.name]

        try:
            buf = str(self.buffer) \
                if self.buffer[0] in guess_type_value_type() \
                else self.buffer
        except IndexError:
            buf = str(self.buffer)

        if len(buf) > 0:
            t = " " * (mx - len("lst") + 1)
            ty = self.__dict__.get("conversion_table", {}).get(self.name, "")
            if ty != "":
                ty = "      \t(%s)" % str(ty)
            if isinstance(buf, (list, tuple)):
                pile.append(head + "  lst" + t + ": " + str(repr(buf) + ty))
            else:
                pile.append(head + "  val" + t + ": " + buf + ty)

        for k in sorted(self):
            v = self[k]
            vs = str(v) if v in guess_type_value_type() or isinstance(
                v,
                tuple) else v
            ty = self.__dict__.get("conversion_table", {}).get(k, "")
            if ty != "":
                ty = "         \t(%s)" % str(ty)
            if isinstance(vs, str):
                t = " " * (mx - len(k) + 1)
                pile.append(head + "  " + k + t + ": " + vs + ty)
            elif isinstance(vs, list):
                t = " " * (mx - len(k) + 1)
                pile.append(head + "  " + k + t + ": " + str(repr(vs)) + ty)
            elif isinstance(vs, tuple):
                pile.append("-" + str(vs) + ty)
            else:
                pile.append(str(vs) + ty)

        if len(self.other) > 0:
            pile.append(head + "  ----")
        soro = sorted(copy.copy(self.other))
        for k, v in soro:
            temp = str(v)
            star = temp.find("*")
            if star != -1 and "_othercount" in self.__dict__:
                temp = "%s*(%d) %s" % (temp[:star],
                                       self._othercount.get(k, -1), temp[star + 1:])
            pile.append(temp)

        return "\n".join(pile)

    def strip(self):
        """
        Strips the buffer.
        """
        self.buffer = self.buffer.strip()

    def copy(self):
        """
        Gets a copy.
        """
        u = XMLHandlerDictNode(self, self.father, self.name, self.level)
        u.buffer = self.buffer
        u.level = self.level
        return u

    def set(self, i, v):
        """
        Changes the value of a field.
        @param      i       field
        @param      v       new value
        """
        if i in self:
            if isinstance(v, XMLHandlerDictNode):
                self.other.append((i, v))
                return v
            else:
                raise XmlException(
                    "unable to append a new string value for an existing field %s:%s" %
                    (i, v))
        else:
            self[i] = v
        return self

    def is_text_only(self):
        """
        Returns True if it only contains text.
        """
        if len(self.other) > 0:
            return False
        if len(self) > 1:
            return False
        for k, v in self.items():
            if k != self.name:
                return False
            if not isinstance(v, str):
                return False
        return True

    def rearrange(self, debug=False):
        """
        Moves all objects to other.
        """

        # check level
        if self.father is not None:
            self.level = self.father.level + 1

        # is is_text_only --> fill buffer, clean the rest
        if self.is_text_only() and len(self) == 1:
            k = self.keys()[0]
            self.buffer = self[k]
            self.clear()
            return

        # values in self.keys also in other --> all in other
        # unique values in other and if text --> self
        count = {}
        for k, v in self.other:
            count[k] = 0
            v.rearrange()

        for k, v in self.other:
            count[k] += 1
        move = [k for k, v in count.items() if v == 1]
        keys = {}
        for m in move:
            keys[m] = None
        mult = []
        rem = []
        i = 0
        for k, v in self.other:
            if k in keys and v.is_text_only():
                if k in self:
                    if k not in mult:
                        tempv = self[k]
                        if isinstance(tempv, str):
                            tempv = XMLHandlerDictNode(self, k, self.level + 1)
                            tempv.buffer = self[k]
                        mult.append((k, tempv))
                else:
                    self[k] = v.buffer
                    rem.append(i)
            i += 1

        mult.reverse()
        for m in mult:
            self.other.insert(0, m)
            del self[m[0]]
        rem.reverse()
        for e in rem:
            del self.other[e]

        # in case of self contains object --> other
        rem = []
        for k, v in self.items():
            if not isinstance(v, str) and not isinstance(v, list):
                v.rearrange(debug=True)
                if not v.is_text_only():
                    self.other.append((k, v))
                    rem.append(k)
                else:
                    self[k] = v.buffer

        for k in rem:
            del self[k]

        # in case other already contains some objects of the same kind
        rem = []
        count = {}
        for k, v in self.other:
            count[k] = 1
        for k, v in self.items():
            if k in count:
                if isinstance(v, str):
                    node = XMLHandlerDictNode(self, k, self.level + 1, False)
                    node.buffer = v
                    self.other.append((k, node))
                else:
                    self.other.append((k, v))
                rem.append(k)

        for k in rem:
            del self[k]

        # last check
        if len(self) == 1:
            # self.popitem(), strange it works in version 2
            k, _ = list(self.items())[0]
            if k == self.name:
                self.buffer = self[k]
                del self[k]

    def get_xml_output(self):
        """
        @return      an XML output (all lines terminated by end_of_line
        """
        att = [""] + ["%s=\"%s\"" %
                      (k, escape(self[k])) for k in sorted(self) if len(self[k]) <= 20]
        att = " ".join(att)
        lev = max(self.level - 1, 0)
        lev = "  " * lev

        if len(self.other) == 0:
            if len(self.buffer) == 0:
                return "%s<%s%s />\n" % (lev, self.name, att)
            else:
                return "%s<%s%s>%s</%s>\n" % (lev,
                                              self.name, att, self.buffer, self.name)
        else:
            res = ["%s<%s%s>\n" % (lev, self.name, att)]
            if len(self.buffer) > 0:
                res.append("%s%s\n" % (lev, escape(self.buffer)))
            for k in sorted(self):
                v = self[k]
                if len(v) <= 20:
                    continue
                res.append("%s<%s>\n" % (lev, k))
                res.append("%s%s\n" % (lev, escape(v)))
                res.append("%s</%s>\n" % (lev, k))

            other = sorted(copy.copy(self.other))

            for k, v in other:
                res.append(v.get_xml_output())
            res.append("%s</%s>\n" % (lev, self.name))
            return "".join(res)

    def get_values(self, field):
        """
        Gets all values associated to a given field name.
        @param      field       field name
        @return                 list of  [  key, value ]
        """
        res = []
        if self.name == field:
            res.append((("", -1), self.buffer))

        for k, v in self.items():
            if k == field:
                res.append(((k, -1), v))

        i = 0
        for k, v in self.other:
            temp = v.get_values(field)
            for a, b in temp:
                res.append(((k, i) + a, b))
            i += 1

        return res

    def get_values_group(self, fields, nb=1):
        """
        Gets all values associated to a list of fields
        (must come together in a single node, not in *self.other*).
        @param      fields      fields name (list or dictionary)
        @param      nb          at least nb fields must be filled
        @return                 list of  dictionaries
        """
        res = []
        if self.name in fields:
            res.append((self.name, self.buffer))

        for k, v in self.items():
            if k in fields:
                res.append((k, v))

        if len(res) >= nb:
            temp = {}
            for k, v in res:
                if k in temp:
                    raise XmlException("field %s already present in '%s' (full name '%s')" % (
                        k, ", ".join(temp.keys()), "/".join(self.get_full_name())))
                temp[k] = v
            for f in fields:
                if f not in temp:
                    temp[f] = None
            res = [((self.name, -1), temp)]
        else:
            res = []

        i = 0
        for k, v in self.other:
            temp = v.get_values_group(fields, nb)
            for a, b in temp:
                res.append(((k, i) + a, b))
            i += 1

        return res

    def _convert_into_list(self):
        """
        Converts all types into lists.
        """
        if isinstance(self.buffer, str):
            self.buffer = [self.buffer]

        for k in self:
            v = self[k]
            if isinstance(v, str):
                self[k] = [v]

        for k, v in self.other:
            v._convert_into_list()

    def __iadd__(self, other):
        """
        Concatenates every information.
        @param      other       other value to concatenate
        @return                 self
        """
        self.iadd(other, False, False)
        return self

    def iadd(self, other, use_list, collapse):
        """
        Concatenates every information.
        @param      other       other value to concatenate
        @param      use_list    use a list or not
        @param      collapse    collapse all information
        @return                 self
        """
        if self.name != other.name:
            raise XmlException("the two names should be equal %s != %s full names (%s != %s)" % (
                self.name, other.name, "/".join(self.get_full_name()), "/".join(other.get_full_name())))

        # _othercount
        if "_othercount" not in self.__dict__:
            self._othercount = {}

        # next
        if use_list:
            self._convert_into_list()

        if use_list:
            if isinstance(other.buffer, list):
                self.buffer.extend(other.buffer)
            else:
                self.buffer.append(other.buffer)
        else:
            self.buffer += other.buffer

        for k, v in other.items():
            if k not in self:
                if use_list:
                    if isinstance(v, list):
                        self[k] = v
                    else:
                        self[k] = [v]
                else:
                    self[k] = v
            else:
                if use_list:
                    if isinstance(v, list):
                        self[k].extend(v)
                    else:
                        self[k].append(v)
                else:
                    self[k] += v

        # count the number
        selfcount = {}
        othcount = {}
        for k, v in self.other:
            if k in selfcount:
                selfcount[k] += 1
            else:
                selfcount[k] = 1
            self._othercount[k] = max(self._othercount.get(k, 0), selfcount[k])

        for k, v in other.other:
            if k in othcount:
                othcount[k] += 1
            else:
                othcount[k] = 1
            self._othercount[k] = max(self._othercount.get(k, 0), othcount[k])

        if "_othercount" in other.__dict__:
            for k, v in other._othercount.items():
                self._othercount[k] = max(self._othercount.get(k, 0), v)

        # iadd single elements + append other from others
        for node in other.other:
            ok = False
            for n in self.other:
                if node[0] != n[0]:
                    continue
                key = node[0]
                if selfcount.get(key, 0) == othcount.get(key, 0) == 1:
                    n[1].iadd(node[1], use_list=use_list, collapse=collapse)
                    ok = True
                    break

            if not ok:
                nt = copy.deepcopy(node)
                nt[1].parent = self
                nt[1]._build_othercount()
                if use_list:
                    nt[1]._convert_into_list()
                if collapse:
                    nt[1]._collapse(use_list)
                self.other.append(nt)
                k = node[0]

        # count
        count = {}
        for k, v in self.other:
            count[k] = count.get(k, 0) + 1

        # transfert from dict self if a key is present in self.other
        rem = []
        for k, v in self.items():
            if k in count:
                tn = XMLHandlerDictNode(self, k, self.level + 1, False)
                tn._build_othercount()
                if use_list:
                    tn._convert_into_list()
                tn.buffer = [v] if use_list and not isinstance(v, list) else v
                self.other.append((k, tn))
                rem.append(k)
                self._othercount[k] = self._othercount.get(k, 0) + 1
        for k in rem:
            del self[k]

        # count again
        count = {}
        for k, v in self.other:
            if isinstance(v, str):
                count[k, 0] = count.get((k, 0), 0) + 1
            else:
                count[k, 1] = count.get((k, 1), 0) + 1

        # string to object
        for i, tu in enumerate(self.other):
            k, v = tu
            if isinstance(v, str) and count.get((k, 1), 0) > 0:
                tn = XMLHandlerDictNode(self, k, self.level + 1, False)
                tn._build_othercount()
                tn.buffer = [v] if use_list else v
                self.other[i] = (k, tn)

        # collapsing
        if collapse:
            self._collapse(use_list)

    def _build_othercount(self):
        """
        Builds *_othercount* when not present.
        """
        if "_othercount" not in self.__dict__:
            self._othercount = {}
        for k, v in self.other:
            self._othercount[k] = self._othercount.get(k, 0) + 1
            v._build_othercount()

    def _collapse(self, use_list):
        """
        Collapses together all fields having the same name
        in the member other.
        @warning                it should be called after iadd
        """
        names = {}
        for k, v in self.other:
            if k in names:
                names[k].append(v)
            else:
                names[k] = [v]

        del self.other[:]
        for k, lv in names.items():
            if len(lv) > 1:
                self._othercount[k] = max(self._othercount.get(k, 0), len(lv))
                for i in range(1, len(lv)):
                    lv[0].iadd(lv[i], use_list=use_list, collapse=True)
                self.other.append((k, lv[0]))
            else:
                lv[0]._collapse(use_list)
                self.other.append((k, lv[0]))
        #self._check_ (False)

    def _check_(self, add_root_id):
        """some checking
        """
        count = {}
        # if add_root_id and "add_root_id" not in self.__dict__ :
        #    fLOG (self)
        #    raise Exception ("unable to find add_root_id in '%s'" % self.get_full_name ())
        if "_othercount" not in self.__dict__:
            raise XmlException("unable to find _othercount in '%s'" %
                               "/".join(self.get_full_name()))
        for k, v in self.other:
            count[k] = count.get(k, 0) + 1
        if len(count) > 0:
            if max(count.values()) > 1:
                raise XmlException("max (count.values ()) > 1 in '%s' \nexp: %s" % (
                    "/".join(self.get_full_name()), str(count)))
        for k, v in self.other:
            if isinstance(v, list):
                for _ in v:
                    _._check_(add_root_id)
            else:
                v._check_(add_root_id)

    def _guess_type(self, tolerance=0.01, utf8=False):
        """
        Replaces all values in the object.
        @param      tolerance       @see fn guess_type_list
        @param      utf8            if True, all types are str
        @warning                    it should be called after _collapse
        """
        self.buffer = (str, 10) if utf8 else guess_type_list(self.buffer)
        for k in self:
            self[k] = (str, 10) if utf8 else guess_type_list(self[k])
        for k, v in self.other:
            v._guess_type(utf8)

    def find_node(self, li):
        """
        @param      li      list of names
        @return             a list of nodes which correspond to the list of names
        """
        node = [self]
        for l in li:
            temp = []
            for n in node:
                for k, v in n.other:
                    if k == l:
                        temp.append(v)
            node = temp

        return node

    def find_node_value(self, li):
        """
        @param      li      list of names
        @return             a list of values
        """
        path = li if isinstance(li, list) else li.split("/")
        way, last = path[:-1], path[-1]

        if len(way) > 0 and way[0] == self.name:
            del way[0]

        res = []
        node = self.find_node(way)
        for n in node:
            if last == "_":
                res.append(n.buffer)
            else:
                res.append(n.get(last, None))
        return res

    def get_full_name(self):
        """
        @return         the list of self.name from all parents
        """
        li = [self.name]
        node = self
        while node.father is not None:
            node = node.father
            li.append(node.name)
        li.reverse()
        return li

    def _log_error(self):
        """
        logs an object from the root if not already done
        """
        root = self.get_root()
        if "_logged" in root.__dict__:
            return
        root._logged = True

    def _adopt_table(self, tbl, exception):
        """
        Adopts a table built on anoher object.
        @param      tbl         same kind of node but including members:
                                    - table
                                    - conversion_table
        @param      exception   if True, raises an exception, log otherwise

        @warning  The method could change the object itself if it does not fit.

        @warning  The method adds members 'conversion_table', 'add_root_id'
        """
        self.conversion_table = tbl.conversion_table  # field conversion
        self.add_root_id = tbl.add_root_id

        memo = {}
        for k, v in tbl.other:
            memo[k] = v

        rem = []
        for k in self:
            if k not in tbl.conversion_table:
                if len(self[k]) == 0:
                    continue
                if k not in memo:
                    self._log_error()
                    if exception:
                        raise XmlException(
                            "a field '%s' is not provided by the reference (path: %s)\nmemo.keys(): %s" %
                            (k, "/".join(
                                self.get_full_name()), str(
                                memo.keys())))
                tn = XMLHandlerDictNode(self, k, self.level + 1, False)
                v = self[k]
                tn.buffer = v
                self.other.append((k, tn))
                rem.append(k)

        for k in rem:
            del self[k]

        count = {}
        for k, v in self.other:
            if k in count:
                count[k] += 1
            else:
                count[k] = 1

        # checking if relation 11 are ok with this object
        if "_othercount" not in tbl.__dict__:
            raise XmlException("we expect _othercount to be here")
        for k, v in count.items():
            if k not in tbl._othercount:
                self._log_error()
                if exception:
                    raise XmlException("unable to find field '%s' (1:n) in path '%s'" % (
                        k, "/".join(self.get_full_name())))
            elif v > 1 and tbl._othercount[k] <= 1:  # pylint: disable=R1716
                self._log_error()
                if exception:
                    raise XmlException("we expect a relation 1:1 for field '%s' in path '%s'" % (
                        k, "/".join(self.get_full_name())))

        # next
        for k, v in self.other:
            if k not in memo:
                # fLOG("ERROR: unable to find field '%s' (1:n) in path '%s'" %
                #    (k, "/".join(self.get_full_name())))
                self._log_error()
            else:
                v._adopt_table(memo[k], exception=exception)

    def _transfer_to_object(self, root=True, exception=True):
        """
        Transfers values to the object *self.table*.
        @param      root            if True, it is the root
        @param      exception       if True, raise Exception
        @return                     the value, dictionary of dictionary of list sometimes...

        @warning    We assume fid is the key.

        @warning    If root.add_root_id is True, is assumes column root_id is root.add_root_id
        """
        attr = {}
        try:
            v = self.conversion_table[self.name](self.buffer)
        except Exception as ex:
            if "conversion_table" not in self.__dict__:
                # fLOG("ERROR: unable to find conversion_table for field ",
                #     self.name,
                #     " in node " + "/".join(self.get_full_name()))
                self._log_error()
                #if exception : raise Exception ("fail to convert value for field " + k)
            elif len(self.buffer) > 0:
                # fLOG("ERROR: fail to convert value '",
                #     self.buffer,
                #     "' into ",
                #     self.conversion_table.get(self.name,
                #                               "not found"),
                #     " for field ",
                #     self.name,
                #     " --- ",
                #     repr(self.buffer),
                #     " path: ",
                #     "/".join(self.get_full_name()))
                self._log_error()
                if exception:
                    raise XmlException(
                        "Fail to convert value for field '{}'".format(self.name)) from ex
            v = ""

        if not isinstance(v, str) or len(v) > 0:
            attr[self.name] = v

        for k, v in self.items():
            try:
                v = self.conversion_table[k](v)
            except Exception as ex:
                if "conversion_table" not in self.__dict__:
                    # fLOG("ERROR: unable to find conversion_table field " +
                    #     k +
                    # " in node " +
                    #     "/".join(self.get_full_name()))
                    self._log_error()
                    #if exception : raise Exception ("fail to convert value for field " + k)
                    continue
                elif len(v) > 0:
                    # fLOG("ERROR: fail to convert value ",
                    #     v,
                    #     " field ",
                    #     k,
                    #     " into ",
                    #     self.conversion_table.get(k,
                    #                               "not found"),
                    #     " for field ",
                    #     "/".join(self.get_full_name()))
                    self._log_error()
                    if exception:  # pylint: disable=R1720
                        raise XmlException("fail to convert value for field '%s' in node '%s'" % (
                            k, "/".join(self.get_full_name()))) from ex
                    else:
                        continue
                else:
                    continue

            if not isinstance(v, str) or len(v) > 0:
                attr[k] = v

        if "add_root_id" not in self.__dict__:
            raise XmlException("unable to find add_root_id in '%s' (name '%s')" % (
                "/".join(self.get_full_name()), self.name))
        if self.add_root_id is not None:
            attr[self.add_root_id] = ("mapto", self.get_root().name, "fid")

        # other attributes
        for k, v in self.other:
            kn = "$" + k
            if kn not in attr:
                attr[kn] = []
            r = v._transfer_to_object(root=False, exception=exception)
            attr[kn].append(r)

        return attr

    def apply_change_names(self, change_names):
        """
        private: change names attributes.
        @param      change_names      { oldname : newname }
        """
        if self.name in change_names:
            self.name = change_names[self.name]

        if "_othercount" in self.__dict__:
            rem = []
            upd = {}
            for k, v in self._othercount.items():
                if k in change_names:
                    rem.append(k)
                    upd[change_names[k]] = v
            for r in rem:
                del self._othercount[r]
            self._othercount.update(upd)

        rem = []
        upd = {}
        for k, v in self.items():
            if k in change_names:
                rem.append(k)
                upd[change_names[k]] = v
        for r in rem:
            del self[r]
        self.update(upd)

        old = self.other
        self.other = []
        for k, v in old:
            if k in change_names:
                self.other.append((change_names[k], v))
            else:
                self.other.append((k, v))
            v.apply_change_names(change_names)

    def get_root(self):
        """
        @return the root of the node
        """
        node = self
        while node.father is not None:
            node = node.father
        return node

    def iterfields(self):
        """
        Iterator on the nodes.
        """
        root = "/".join(self.get_full_name())
        if self.name is not None:
            yield (root + "/_", self.buffer)
        for k, v in self.items():
            yield (root + "/" + k, v)

        for k, v in self.other:
            for a, b in v.iterfields():
                yield (a, b)

    def find_node_regex(self, regex):
        """
        Finds all nodes depending on a regular expression.
        @param     regex    regular expression
        @return             list of ``[ (node, value) ]``
        """
        res = []
        for node, value in self.iterfields():
            if regex.search(node) is not None:
                res.append((node, value))
        return res
