from bs4 import BeautifulSoup, Comment


soup = BeautifulSoup(open("data/vat.xml"), "lxml-xml")


# <mentioned>xxx</mentioned> -> ‘xxx’
def mentioned_tag_cleanup(insoup):
    for match in insoup.find_all('mentioned'):
        match.insert_before('‘')
        match.insert_after('’')
        match.unwrap()
    return insoup


# <quote>xxx</quote> -> ”xxx”
def quote_tag_cleanup(insoup):
    for match in insoup.find_all('quote'):
        match.insert_before('“')
        match.insert_after('”')
        match.unwrap()
    return insoup


# <unclear>xxx</unclear>  =>  ¿xxx¿
def unclear_tag_cleanup(insoup):
    for match in insoup.find_all('unclear'):
        match.insert_before('¿')
        match.insert_after('¿')
        match.unwrap()
    return insoup


# <add>xxx</add>  =>  +xxx+
def add_tag_cleanup(insoup):
    for match in insoup.find_all('add'):
        match.insert_before('+')
        match.insert_after('+')
        match.unwrap()
    return insoup


# <del>xxx</del>  =>  _xxx_
def del_tag_cleanup(insoup):
    for match in insoup.find_all('del'):
        match.insert_before('_')
        match.insert_after('_')
        match.unwrap()
    return insoup


# <gap/>  =>  ¿…¿
def gap_tag_cleanup(insoup):
    for match in insoup.find_all('gap'):
        match.insert_before('¿…¿')
        match.decompose()
    return insoup


# Unwraps selected tags leaving their contents
def simple_tag_cleanup(insoup):
    wrapped_tags = ['lb', 'cb', 'pb', 'title', 'name',
                    'g', 'c', 'corr', 'sic', 'ref', 'pc',
                    'hi', 'subst', 'seg', 'cit',]
                    # 'p', 'head', 'div', 'body', 'TEI', 'text']
    for tag in wrapped_tags:
        for match in insoup.find_all(tag):
            match.unwrap()
    return insoup


# Completely deletes selected tags and their contents
def delete_tags(insoup):
    invalid_tags = ['note', 'space', 'bibl']
    for tag in invalid_tags:
        for match in insoup.find_all(tag):
            match.decompose()
    return insoup


# Unwraps <choice>...</choice> depending on its contents
def clean_choice(insoup):
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


# Removes all comments from the soup
def clean_comments(insoup):
    comments = insoup.find_all(text=lambda text: isinstance(text, Comment))
    [comment.extract() for comment in comments]
    return insoup


# Performs all defined cleanups
def meta_cleanup(insoup):
    cleaners = [clean_comments, clean_choice, simple_tag_cleanup, del_tag_cleanup,
                add_tag_cleanup, unclear_tag_cleanup, delete_tags, gap_tag_cleanup,
                quote_tag_cleanup, mentioned_tag_cleanup]
    for cleaner in cleaners:
        cleaner(insoup)
    return insoup


soup = meta_cleanup(soup)

print(soup)