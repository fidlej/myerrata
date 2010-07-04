
from src.model import Fix

def save_fix(url, orig_text, new_text, pos, page_order):
    fix = Fix.prepare(url, orig_text, new_text, pos, page_order)
    if orig_text.rstrip() == new_text:
        fix.delete()
    else:
        fix.put()

    return fix
