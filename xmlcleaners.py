""" xmlcleaners.py
Part of A Simple Python Collator v.0.2
© 2016 Nicolas Vaughan
nivaca@fastmail.com
Runs on Python 3.5+
Requires: BeautifulSoup 4 """


from bs4 import Comment
import re


# def clean_before_diff(thetext):
#     thetext = re.sub(r'[¿.+-_?:]', '', thetext)
#     return thetext


def clean_str(thetext):
    thetext = re.sub(r"\n", " ", thetext)
    thetext = re.sub(r"[.,:;]", " ", thetext)
    thetext = re.sub(r"\t{1,8}", " ", thetext)
    thetext = re.sub(r"[ ]{2,8}", " ", thetext)
    thetext = re.sub(r"[ ]{2,8}", " ", thetext)
    # thetext = re.sub("\n", " ", thetext)
    return thetext


# # <mentioned>xxx</mentioned> -> ‘xxx’
# def mentioned_tag_cleanup(insoup):
#     for match in insoup.find_all('mentioned'):
#         match.insert_before('‘')
#         match.insert_after('’')
#         match.unwrap()
#     return insoup
#
#
# # <quote>xxx</quote> -> ”xxx”
# def quote_tag_cleanup(insoup):
#     for match in insoup.find_all('quote'):
#         match.insert_before('“')
#         match.insert_after('”')
#         match.unwrap()
#     return insoup


def unclear_tag_cleanup(insoup):
    """ <unclear>xxx</unclear>  =>  ¿xxx¿ """
    for match in insoup.find_all('unclear'):
        match.insert_before('¿')
        match.insert_after('¿')
        match.unwrap()
    return insoup


def add_tag_cleanup(insoup):
    """ <add>xxx</add>  =>  +xxx+ """
    for match in insoup.find_all('add'):
        match.insert_before('+')
        match.insert_after('+')
        match.unwrap()
    return insoup


def del_tag_cleanup(insoup):
    """ <del>xxx</del>  =>  _xxx_ """
    for match in insoup.find_all('del'):
        match.insert_before('-')
        match.insert_after('-')
        match.unwrap()
    return insoup


def gap_tag_cleanup(insoup):
    """ <gap/>  =>  ¿…¿ """
    for match in insoup.find_all('gap'):
        match.insert_before('¿…¿')
        match.decompose()
    return insoup


def simple_tag_cleanup(insoup):
    """ Unwraps selected tags leaving their contents. """
    wrapped_tags = ['lb', 'cb', 'pb', 'title', 'name',
                    'g', 'c', 'corr', 'sic', 'ref', 'pc',
                    'hi', 'subst', 'seg', 'cit',
                    'mentioned', 'quote',]
                    # 'p', 'head', 'div', 'body', 'TEI', 'text']
    for tag in wrapped_tags:
        for match in insoup.find_all(tag):
            match.unwrap()
    return insoup


def delete_tags(insoup):
    """ Completely deletes selected tags and their contents. """
    invalid_tags = ['note', 'space', 'bibl']
    for tag in invalid_tags:
        for match in insoup.find_all(tag):
            match.decompose()
    return insoup


def clean_choice(insoup):
    """ Unwraps <choice>...</choice> depending on its contents. """
    for match in insoup.find_all('choice'):
        #
        # first case: <orig> nad <reg>:
        if match.find('orig') is not None:
            match.orig.decompose()
            match.reg.unwrap()
            match.unwrap()
        #
        # second case: <abbr> and <expan>:
        if match.find('abbr') is not None:
            match.abbr.decompose()
            match.expan.unwrap()
            match.unwrap()
    return insoup


def clean_comments(insoup):
    """ Removes all comments from the soup. """
    comments = insoup.find_all(text=lambda text: isinstance(text, Comment))
    [comment.extract() for comment in comments]
    return insoup


def meta_cleanup(insoup):
    """ Performs all defined cleanups. """
    cleaners = [clean_comments, clean_choice, simple_tag_cleanup, del_tag_cleanup,
                add_tag_cleanup, unclear_tag_cleanup, delete_tags, gap_tag_cleanup, ]
    for cleaner in cleaners:
        cleaner(insoup)
    return insoup
