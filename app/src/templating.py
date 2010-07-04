
import logging
from mako.lookup import TemplateLookup

from src import config

TEMPLATE_LOOKUP = TemplateLookup(directories=["templates"],
        format_exceptions=config.DEBUG,
        filesystem_checks=config.DEBUG,
        input_encoding="utf-8",
        default_filters=["to_unicode", "h"],
        imports=["from src.templating import to_unicode"])

def render(template_name, **kw):
    template = TEMPLATE_LOOKUP.get_template(template_name)
    return template.render_unicode(**kw)

def to_unicode(value):
    """Converts everything to unicode.
    Invalid utf-8 chars are replaced with question marks.
    """
    logging.warn("unicode: %r", value)
    if isinstance(value, unicode):
        return value

    if value == "":
        return u""

    logging.warn("non-unicode: %r", value)
    if not isinstance(value, str):
        value = str(value)
    return unicode(value, encoding="utf-8", errors="replace")

