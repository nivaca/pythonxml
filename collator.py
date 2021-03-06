#!/usr/bin/env python3

""" collator.py
A Simple Python Collator v.0.4
© 2018 Nicolas Vaughan
n.vaughan@uniandes.edu.co
Universidad de los Andes, Colombia
Runs on Python 3.7+
Requires: BeautifulSoup 4, diff_match_patch """

import os
import functools
from multiprocessing import Pool

try:
    from bs4 import BeautifulSoup
except ImportError:
    print('BeautifulSoup 4 module not available')
    print('Aborting...')
    exit(0)

try:
    import diff_match_patch as gdmp
except ImportError:
    print('diff_match_patch module not available')
    print('Aborting...')
    exit(0)

try:
    from xmlcleaners import meta_cleanup, clean_str
except ImportError:
    print('xmlcleaners module not available')
    print('Aborting...')
    exit(0)


# +++++++++++++++++++ GLOBAL VARIABLES +++++++++++++++++++++

# Name of the main witness against which all other
# witnesses will be compared.
# If left empty, the script selects the first alphabetically.
main_wit = 'sorb'

xml_prefix = 'b1d3qun'


default_ext = '.xml'
directory = 'data/'                   # leave empty for CWD

# collation_type can have: 'html', 'textual', or 'both'
# default is 'both'
collation_type = 'both'

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



class Witness:
    """ This is the class of witnesses. """

    def __init__(self, name):
        self.name = name
        self.short_file_name = self.name + default_ext
        self.file_name =\
            os.path.join(directory, ''.join([self.name, default_ext]))
        self.xml_list = []
        self.xml_ids = []
        self.paragraphs = []
        self.len = 0
        self.id = ''
        self.get_my_id()
        self.parse_me()

    def get_my_id(self):
        """ Returns the witness id. """
        self.id = get_wit_id(self.file_name)

    def parse_me(self):
        """ Parses the file to obtain XML data. """
        self.xml_list = list(parse_file(self.file_name))
        self.xml_ids = [xid[0] for xid in self.xml_list]
        self.paragraphs = [xid[1] for xid in self.xml_list]
        self.len = len(self.xml_ids)

    def get_par_by_index(self, index):
        """ Returns the contents of a certain paragraph
        depending on its numbered index (0-len). """
        return self.paragraphs[index]

    def get_par_by_xmlid(self, xmlid):
        """ Returns the contents of a certain paragraph
        depending on its xml:id. """
        return self.paragraphs[self.xml_ids.index(xmlid)]

    def __len__(self):
        """ Returns the number of paragraphs in the witness. """
        return self.len




class Collation:
    """ This is the class of collations. """

    def __init__(self, c_id, from_wit, to_wit):
        self.c_id = c_id
        # from-Witness
        self.from_wit = from_wit
        self.from_wit_id = from_wit.id
        # to-Witness
        self.to_wit = to_wit
        self.to_wit_id = to_wit.id
        self.data = []


class TCollation(Collation):
    """ This is the class of textual collations. """

    def run(self):
        """ Calls diff_witnesses() over the two wits. """
        self.data = textual_diff_witnesses(self.from_wit, self.to_wit)


class HCollation(Collation):
    """ This is the class of HTML collations. """

    def run(self):
        """ Calls diff_witnesses() over the two wits. """
        self.data = html_diff_witnesses(self.from_wit, self.to_wit)


# =========================================================
# =========================================================


def get_files():
    """ Returns the list of names of the xml files
    in the data directory. """

    fnames = os.listdir(directory + '.')
    file_list = []

    for file in fnames:
        fname = os.path.splitext(file)[0]
        fext = os.path.splitext(file)[1]
        # check whether file has required extension
        if fext == default_ext:
            file_list += [fname]

    file_list = sorted(file_list)

    if len(file_list) == 0:
        print("Error: No XML files to process")
        exit(0)
    return file_list


def sort_witnesses(witnesses):
    """ Makes witnesses[0] be the main witness,
    according to the value of main_wit. """

    main_wit_id = 0

    for wit in witnesses:
        if main_wit == wit.name:
            main_wit_id = witnesses.index(wit)

    if main_wit_id != 0:
        temp = witnesses[0]
        witnesses[0] = witnesses[main_wit_id]
        witnesses[main_wit_id] = temp

    return witnesses


def get_wit_id(file):
    """ Returns the witness id. """
    soup = BeautifulSoup(open(file), "lxml-xml")
    witdesc = soup.find('witness')
    wit = '#' + witdesc["xml:id"]
    return wit


def parse_file(file):
    """ Parses a given TEI-XML file.
    Returns a list of couples, like so:
    [('b1d3qun-cdtvet', 'Circa ...'), etc.] """
    soup = BeautifulSoup(open(file), "lxml-xml")
    soup = meta_cleanup(soup)

    # Checks whether tag has 'xml:id'
    def has_attr(tag):
        return tag.has_attr('xml:id')

    # Creates a soup of all <p> tags
    p_soup = soup.find_all(has_attr)

    # Creates a list of all and only all <p>
    # whose xml:id contain "b1d3qun"
    paragraphs = [p for p in p_soup if xml_prefix in p["xml:id"]]

    # Creates a list of all and only all <p> whose @xml:id
    # contains "b1d3qun"
    p_tags = []
    for parag in paragraphs:
        buf = ''
        for pa in parag:
            buf += pa
        buf = clean_str(buf)
        p_tags.append(buf)

    # Provides a list of all @xml:ids containing "b1d3qun":
    xml_ids = [p["xml:id"] for p in paragraphs]

    # Returns a list of tuples of the parsed XML, like so:
    # [('b1d3qun-cdtvet', 'Circa ...'), etc.]
    return list(zip(xml_ids, p_tags))




def check_files(witnesses):
    """ Checks that all files have the same number of <p> """

    message = f'\nChecking {file_num} files... '
    print(message, end='')

    for i in range(1, file_num):
        if len(witnesses[0]) != len(witnesses[i]):
            print('\nError! Files do not have the same number of <p xml:id="..."> tags!')
            print('Aborting...')
            exit(0)

    print('OK!')
    return


def textual_diff_subroutine(fromwit, towit, xid):
    """ Textual diff subroutine needed for multiprocessing. """
    from_data = \
        fromwit.get_par_by_xmlid(xid).lower()
    to_data = \
        towit.get_par_by_xmlid(xid).lower()

    # create a diff_match_patch object
    dmp = gdmp.diff_match_patch()

    dmp.Diff_Timeout = 0

    delta = dmp.diff_main(from_data, to_data)
    dmp.diff_cleanupSemantic(delta)

    additions = '|'
    deletions = '|'

    for d in delta:
        change = d[1].strip()

        # Skip one for loop if no changes found.
        if d[0] == 0 or len(change) == 0:
            continue

        # Checks if any changes were found and
        # thus need to be written. The value
        # of 1 takes into account the initial '|'.
        if d[0] == 1:
            additions = additions + change + '|'
        if d[0] == -1:
            deletions = deletions + change + '|'
    return additions, deletions


def textual_diff_witnesses(fromwit, towit):
    """ Compares two witnesses.
    Returns a list like so:
    [[xml:id, (deletions, additions)], etc.]. """

    # Creates a global list of all XML:IDs (using the first file only)
    xml_ids = fromwit.xml_ids

    message = f"Comparing {fromwit.id} and {towit.id}... "
    print(message, end='')

    # Multiprocessing
    pool = Pool()
    partial_fun = \
        functools.partial(textual_diff_subroutine, fromwit, towit)
    totals = pool.map(partial_fun, xml_ids)
    pool.close()
    pool.join()

    print('OK!')

    # totals is a list structured thus:
    # [(deletions, additions), etc.]
    return totals


def textual_collate(witnesses):
    """ Performs collation between all witnesses.
    Takes the Witness list as argument. """

    # This list will hold the Collation objects.
    # Only (file_num - 1) collations will be created.
    collations = \
        [TCollation(i, witnesses[0], witnesses[i + 1])
         for i in range(file_num - 1)]

    for coll in collations:
        coll.run()

    out_file = open('output.txt', 'w')

    xml_ids = witnesses[0].xml_ids

    message = '\nWriting output.txt... '
    print(message, end='')

    # This first loop will be repeated the number of
    # XML-IDs.
    # It will collate each <p>.
    for i in range(len(witnesses[0])):

        xid = xml_ids[i]

        # This second loop will be repeated the number of
        # collations done before (file_num - 1)

        for coll in collations:
            # coll.data[i] is the data with index i
            (deletions, additions) = coll.data[i]

            # this is the id of the from-witness
            to_wit_id = coll.to_wit_id

            if collations.index(coll) == 0:
                out_file.write('\n\n--------------\n')
                out_file.write(f'{xid} (¶{i+1})')
                out_file.write('\n--------------\n')
                out_file.write(coll.from_wit_id + '\n')
                out_file.write(witnesses[0].get_par_by_index(i) + '\n')
            out_file.write('\n' + to_wit_id + '\n')
            if len(deletions) > 1:
                out_file.write('˜˜˜ ' + deletions + '\n')
            if len(additions) > 1:
                out_file.write('+++ ' + additions + '\n')

    out_file.close()
    print('OK!')
    return



def html_diff_subroutine(fromwit, towit, xid):
    """" HTML diff subroutine needed for multiprocessing. """
    from_data = \
        fromwit.get_par_by_xmlid(xid).lower()
    to_data = \
        towit.get_par_by_xmlid(xid).lower()

    # create a diff_match_patch object
    dmp = gdmp.diff_match_patch()

    dmp.Diff_Timeout = 0

    diffs = dmp.diff_main(from_data, to_data)
    dmp.diff_cleanupSemantic(diffs)

    html_snippet = dmp.diff_prettyHtml(diffs)

    return html_snippet



def html_diff_witnesses(fromwit, towit):
    """ Compares two witnesses.
    Returns a list like so: """

    # Creates a global list of all XML:IDs (using the first file only)
    xml_ids = fromwit.xml_ids

    message = f"Comparing {fromwit.id} and {towit.id}... "
    print(message, end='')

    # Multiprocessing
    pool = Pool()
    partial_fun = \
        functools.partial(html_diff_subroutine, fromwit, towit)
    totals = pool.map(partial_fun, xml_ids)
    pool.close()
    pool.join()

    print('OK!')

    # totals is a list structured thus:
    # [(deletions, additions), etc.]
    return totals


def html_collate(witnesses):
    """ Performs collation between all witnesses.
    Takes the Witness list as argument.
    Returns a list containing html items."""

    # This list will hold the Collation objects.
    # Only (file_num - 1) collations will be created.
    collations = \
        [HCollation(i, witnesses[0], witnesses[i + 1])
         for i in range(file_num - 1)]

    for coll in collations:
        coll.run()

    out_file = open('output.html', 'w')

    out_file.write("""
    <!DOCTYPE html>
    <meta charset="UTF-8">
    <html>
    <body>
    """)

    xml_ids = witnesses[0].xml_ids

    message = '\nWriting output.html...'
    print(message, end='')

    # This first loop will be repeated the number of
    # XML-IDs.
    # It will collate each <p>.
    for i in range(len(witnesses[0])):

        xid = xml_ids[i]

        # This second loop will be repeated the number of
        # collations done before (file_num - 1)

        for coll in collations:
            # coll.data[i] is the data with index i
            data = coll.data[i]

            # this is the id of the from-witness
            to_wit_id = coll.to_wit_id

            if collations.index(coll) == 0:
                out_file.write(f'<h1>{xid} (¶{i+1})</h1>\n')
            # out_file.write(f'<h2>{coll.from_wit_id}</h2>\n')
            # out_file.write(witnesses[0].get_par_by_index(i) + '\n')
            out_file.write(f'<h2>{to_wit_id}</h2>')
            # out_file.write(coll.to_wit.get_par_by_index(i) + '\n')
            out_file.write(f'{data}')

    out_file.write("</body>\n</html>")
    out_file.close()
    print('OK!')
    return


def main():
    """ Main function. """

    # Creates a list of xml files from the data dir
    files = get_files()
    global file_num
    file_num = len(files)

    message = f'Parsing {file_num} files... '
    print(message, end='')


    # Creates a lists of Witness objects.
    # E.g. wit[0] is a Witness object whose name is contained in file[0].
    # These witnesses are parsed upon creation.
    witnesses = []
    for file_name in files:
        witnesses.append(Witness(file_name))

    witnesses = sort_witnesses(witnesses)

    print("OK!")

    check_files(witnesses)

    if collation_type == 'textual':
        print('\nStarting textual collation')
        textual_collate(witnesses)
    elif collation_type == 'html':
        print('\nStarting HTML collation')
        html_collate(witnesses)
    else:
        print('\nStarting textual collation')
        textual_collate(witnesses)
        print('\nStarting html collation')
        html_collate(witnesses)

    print('Finished!')


if __name__ == "__main__":
    main()
