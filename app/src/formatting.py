
from markupsafe import Markup

def attr_class(fix):
    if fix.gone:
        return Markup(' class="fix gone"')
    else:
        return Markup(' class="fix"')

def attr_gone_checked(fix):
    if fix.gone:
        return Markup(' checked="checked"')
    else:
        return ''

