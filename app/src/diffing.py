
from difflib import SequenceMatcher
from markupsafe import escape, Markup
import re

NON_WORD_PATTERN = re.compile(r'(\w+)', re.UNICODE)

def mark_changes(orig, new):
    return _mark_sequence_changes(NON_WORD_PATTERN.split(orig),
            NON_WORD_PATTERN.split(new))

def _mark_sequence_changes(orig, new):
    matcher = SequenceMatcher(_is_junk, orig, new)
    result = ""
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "replace":
            result += _mark_delete(orig[i1:i2])
            result += _mark_insert(new[j1:j2])
        elif tag == "delete":
            result += _mark_delete(orig[i1:i2])
        elif tag == "insert":
            result += _mark_insert(new[j1:j2])
        elif tag == "equal":
            result += _mark_equal(orig[i1:i2])
        else:
            raise Exception("Unknown diff opcode: %s" % tag)

    return result

def _is_junk(x):
    """Spaces are considered to be junk.
    They should not be marked as preserved
    when the words around them are different.
    """
    return x in " \t\n\r"

def _mark_delete(seq):
    return Markup(u"<del>%s</del>") % escape("".join(seq))

def _mark_insert(seq):
    return Markup(u"<ins>%s</ins>") % escape("".join(seq))

def _mark_equal(seq):
    return escape("".join(seq))


