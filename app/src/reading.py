
from src.model import Fix

def find_fixes(url, limit=1000):
    q = Fix.gql("where url = :url", url=url)
    return q.fetch(limit)

def search(query, limit=1000):
    from src import urlbits
    url_prefix = urlbits.strip_www(query)

    range_end = url_prefix + unichr(0x10ffff)
    q = Fix.gql("where stripped_url >= :url_prefix and stripped_url < :range_end order by stripped_url, url, page_order", url_prefix=url_prefix, range_end=range_end)
    return q.fetch(limit)

