
from src import model
from src.model import Fix

def find_fixes(url, limit=1000):
    url = model.normalize_url(url)
    q = Fix.gql("where url = :url", url=url)
    return q.fetch(limit)

