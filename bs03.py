""" collator.py
A Simple Python Collator v.0.1
© 2016 Nicolas Vaughan
nivaca@fastmail.com
Runs on Python 3.5+
Requires: BeautifulSoup 4, diff_match_patch """

import os
from bs4 import BeautifulSoup
from xmlcleaners import meta_cleanup, clean_str
import diff_match_patch
import pyprind
import sys
# import logging
import re

# logging.basicConfig(filename='logfile.txt', level=logging.INFO, filemode='w')

xml_prefix = 'b1d3qun'
data_path = 'data/'
files = ['sorb', 'maz', 'vat', 'tara']
# files = ['s', 'm', 'v', 't']
extension = '.xml'
file_num = len(files)


class Witness:
    """ This is the class of witnesses. """
    def __init__(self, name):
        self.name = name
        self.short_file_name = self.name + extension
        self.file_name =\
            os.path.join(data_path, ''.join([self.name, extension]))
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
        self.run()


    def run(self):
        """ Calls diff_witnesses() over the two wits. """
        self.data = diff_witnesses(self.from_wit, self.to_wit)


# =========================================================



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




def check_files(witness):
    """ Checks that all files have the same number of <p> """
    bar = pyprind.ProgBar(file_num,
                          title=f'\nChecking {file_num} files...',
                          stream=sys.stdout,
                          track_time=False)
    for i in range(1, file_num):
        if len(witness[0]) != len(witness[i]):
            print('\nError! Files do not have the same number of <p xml:id="..."> tags!')
            print('Aborting...')
            exit(0)
        bar.update()
    bar.update()
    print('OK!')
    return




def diff_witnesses(fromwit, towit):
    """ Compares two witnesses.
    Returns a list like so:
    [[xml:id, (deletions, additions)], etc.] """

    # Creates a global list of all XML:IDs (using the first file only)
    xml_ids = fromwit.xml_ids

    # totals is a list containing the xml_id of the p
    # and a tuple containing deletions and additions
    totals = []

    message = f"\nComparing {fromwit.id} and {towit.id}"
    bar = pyprind.ProgBar(len(fromwit), title=message,
                          stream=sys.stdout, track_time=False)

    for xid in xml_ids:
        from_data = \
            fromwit.get_par_by_xmlid(xid).lower()
        to_data = \
            towit.get_par_by_xmlid(xid).lower()


        # create a diff_match_patch object
        dmp = diff_match_patch.diff_match_patch()

        dmp.Diff_Timeout = 0

        delta = dmp.diff_main(from_data, to_data)
        dmp.diff_cleanupSemantic(delta)

        additions = '|'
        deletions = '|'

        for d in delta:
            change = d[1].strip()
            if d[0] == 0 or len(change) == 0:
                continue
            if d[0] == 1:
                additions = additions + change + '|'
            if d[0] == -1:
                deletions = deletions + change + '|'

        totals.append((additions, deletions))
        bar.update()

    print('OK!')

    # totals is a list structured thus:
    # [(deletions, additions), etc.]
    return totals




def collate(witness):
    """ Performs collation between all witnesses.
    Takes the Witness list as argument. """

    # This list will hold the Collation objects.
    # Only (file_num - 1) collations will be created.
    collation = \
        [Collation(i, witness[0], witness[i + 1]) for i in range(file_num - 1)]

    out_file = open('output.txt', 'w')

    xml_ids = witness[0].xml_ids

    bar = pyprind.ProgBar(len(witness[0]), title='\nWriting output.txt',
                          stream=sys.stdout, track_time=False)

    last_id = ''

    # This first loop will be repeated the number of
    # XML-IDs.
    # It will collate each <p>.
    for i in range(len(witness[0])):

        xid = xml_ids[i]

        # This second loop will be repeated the number of
        # collations done before (file_num - 1)

        for coll in collation:
            # coll.data[i] is the data with index i
            (deletions, additions) = coll.data[i]

            # this is the id of the from-witness
            to_wit_id = coll.to_wit_id

            if xid != last_id:
                out_file.write('\n\n--------------\n')
                out_file.write(f'{xid} (¶{i+1})')
                out_file.write('\n--------------\n')
                out_file.write(coll.from_wit_id + '\n')
                out_file.write(witness[0].get_par_by_index(i) + '\n')
            out_file.write('\n' + to_wit_id + '\n')
            # out_file.write(coll.to_wit.get_par_by_index(i) + '\n')
            if len(deletions) > 1:
                out_file.write('˜˜˜ ' + deletions + '\n')
            if len(additions) > 1:
                out_file.write('+++ ' + additions + '\n')

            last_id = xid

        bar.update()

    out_file.close()
    return




def main():
    """ Main function. """
    bar = pyprind.ProgBar(file_num, title=f'Parsing {file_num} files...',
                          stream=sys.stdout, track_time=False)

    # Creates a lists of Witness objects.
    # E.g. wit[0] is a Witness object whose name is contained in file[0].
    # These witnesses are parsed upon creation.
    witness = []
    for file_name in files:
        witness.append(Witness(file_name))
        bar.update()
    print("OK!")

    check_files(witness)

    collate(witness)

if __name__ == "__main__":
    main()