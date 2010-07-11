
from markupsafe import Markup

def style_fix(fix):
    if fix.gone:
        return Markup(' class="gone"')
    else:
        return ''

