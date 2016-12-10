import os
from bs4 import BeautifulSoup
from xmlcleaners import meta_cleanup, clean_str
import simplediff
from pprint import pprint
import pyprind
import sys

xml_prefix = 'b1d3qun'
data_path = 'data/'
files = ['sorb', 'maz', 'vat', 'tara']
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
        self.parse_me()

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


def compare_witnesses(fromwit, towit):
    """ Compares two witnesses.
    Returns a list like so:
    [[xml:id, (deletions, additions)], etc.] """

    # Creates a global list of all XML:IDs (using the first file only)
    xml_ids = fromwit.xml_ids

    # totals is a list containing the xml_id of the p
    # and a tuple containing deletions and additions
    totals = []

    # message = '\nComparing ' + fromwit.short_file_name \
    #           + ' vs. ' + towit.short_file_name
    message = "\nComparing %s & %s" % \
              (fromwit.short_file_name, towit.short_file_name)
    bar = pyprind.ProgBar(len(fromwit), title=message,
                          stream=sys.stdout, track_time=False)

    for xid in xml_ids:
        from_data = fromwit.get_par_by_xmlid(xid).lower()
        to_data = towit.get_par_by_xmlid(xid).lower()
        delta = simplediff.diff(from_data, to_data)

        for d in delta:
            additions = ''
            deletions = ''
            if d[0] == '+':
                additions = d[1].strip()
                # print('ADD: ', additions)
            if d[0] == '-':
                deletions = d[1].strip()
                # print('DEL: ', deletions)
        totals.append([xid, (deletions, additions)])
        bar.update()

    # totals is a list structured thus:
    # [[xml:id, (deletions, additions)], etc.]
    return totals


def check_files(witness):
    """ Checks that all files have the same number of <p> """
    file_num = len(files)
    bar = pyprind.ProgBar(file_num, title='\nChecking files...',
                          stream=sys.stdout, track_time=False)
    for i in range(1, file_num):
        if len(witness[0]) != len(witness[i]):
            print('\nError! Files do not have the same number of <p xml:id="..."> tags!')
            print('Aborting...')
            exit(0)
        bar.update()
    bar.update()
    print('OK!')


def main():
    bar = pyprind.ProgBar(file_num, title='Parsing files...',
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

    c1 = compare_witnesses(witness[0], witness[1])
    # c2 = compare_witnesses(witness[0], witness[2])
    # c3 = compare_witnesses(witness[0], witness[3])

    print(c1)



if __name__ == "__main__":
    main()