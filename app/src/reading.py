
from src import model
from src.model import Fix

def find_fixes(url, limit=1000):
    url = model.normalize_url(url)
    q = Fix.gql("where url = :url", url=url)
    return q.fetch(limit)

def search(url_prefix, limit=1000):
    range_end = url_prefix + unichr(0x10ffff)
    q = Fix.gql("where url >= :url_prefix and url < :range_end order by url, page_order", url_prefix=url_prefix, range_end=range_end)
    return q.fetch(limit)

