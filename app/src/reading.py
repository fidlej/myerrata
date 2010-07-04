
from src import model
from src.model import Fix

def find_fixes(url, limit=1000):
    url = model.normalize_url(url)
    q = Fix.gql("where url = :url", url=url)
    return q.fetch(limit)

def search(url_prefix, limit=1000):
    q = Fix.gql("where url > :url_prefix order by url, page_order", url_prefix=url_prefix)
    return q.fetch(limit)

