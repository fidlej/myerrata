# coding: utf-8
from nose.tools import eq_

from src import diffing

def test_mark_changes():
    tests = [
    (("buy big car", "buy small car"),
        "buy <del>big</del><ins>small</ins> car"),
    (("buy big car", "buy small red car"),
        "buy <del>big</del><ins>small red</ins> car"),
    (("buy big car", "buy small car and test it"),
        "buy <del>big</del><ins>small</ins> car<del></del><ins> and test it</ins>"),
    (("buy big expensive car", "buy small car"),
        "buy <del>big expensive</del><ins>small</ins> car"),
    (("come to visit me and buy me a new algorithm", "algorithm, come to visit me and buy milk"),
        "<ins>algorithm, </ins>come to visit me and buy <del>me a new algorithm</del><ins>milk</ins>"),
    (("buy milk", "buy me a new algorithm"),
        "buy <del>milk</del><ins>me a new algorithm</ins>"),
    (("say something to me", "do you have anything to say?"),
        "<ins>do you have anything to </ins>say<del> something to me</del><ins>?</ins>"),
    ((u"change vaše property", u"change naše property"),
        u"change <del>vaše</del><ins>naše</ins> property"),
    ]

    for args, expected in tests:
        eq_(diffing.mark_changes(*args), expected)



