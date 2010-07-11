
from google.appengine.ext import db

from src import model
from src.model import Fix

def save_fix(url, orig_text, new_text, pos, page_order):
    fix = Fix.prepare(url, orig_text, new_text, pos, page_order)
    if orig_text == new_text:
        fix.delete()
    else:
        fix.put()

    return fix


def update_gone(url, gone, ungone):
    _set_gone(url, gone, True)
    _set_gone(url, ungone, False)


def _set_gone(url, fix_ids, value):
    keynames = []
    for id in fix_ids:
        keyname = model.compute_fix_key_name(url, id["pos"], id["orig"])
        keynames.append(keyname)

    fixes = Fix.get_by_key_name(keynames)
    for fix in fixes:
        fix.gone = value
    db.put(fixes)

