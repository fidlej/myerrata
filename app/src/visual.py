
def group_by_url(sorted_fixes):
    """Returns a list of (url, fixes) pairs.
    The fixes are assumed to be already sorted by URL.
    Their order is preserved within a group.
    """
    url_fixes = []
    last_url = None
    last_group = None
    for fix in sorted_fixes:
        if fix.url == last_url:
            last_group.append(fix)
        else:
            last_url = fix.url
            last_group = [fix]
            url_fixes.append((last_url, last_group))

    return url_fixes

