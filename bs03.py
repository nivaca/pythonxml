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


class Witness:
    """This is the class of witnesses."""
    def __init__(self, name):
        self.name = name
        self.file_name =\
            os.path.join(data_path, ''.join([self.name, extension]))
        self.xml_list = []
        self.xml_ids = []
        self.paragraphs = []
        self.len = 0
        self.parse_me()

    def parse_me(self):
        """Parses the file to obtain XML data."""
        self.xml_list = list(parse_file(self.file_name))
        self.xml_ids = [id[0] for id in self.xml_list]
        self.paragraphs = [id[1] for id in self.xml_list]
        self.len = len(self.xml_ids)

    def get_par_by_index(self, index):
        """Returns the contents of a certain paragraph
        depending on its numbered index (0-len)."""
        return self.paragraphs[index]

    def get_par_by_xmlid(self, xmlid):
        """Returns the contents of a certain paragraph
        depending on its xml:id."""
        return self.paragraphs[self.xml_ids.index(xmlid)]

    def __len__(self):
        """Returns the number of paragraphs in the witness."""
        return self.len


def parse_file(file):
    """Parses a given TEI-XML file.
    Returns a list of couples, like so:
    [('b1d3qun-cdtvet', 'Circa ...'), etc.]"""
    soup = BeautifulSoup(open(file), "lxml-xml")
    soup = meta_cleanup(soup)

    # Checks whether tag has 'xml:id'
    def has_attr(tag): return tag.has_attr('xml:id')

    paragraphs = soup.find_all(has_attr)

    # This creates a list of all and only all <p> whose xml:id
    # contains "b1d3qun":
    parag_list = [p for p in paragraphs if xml_prefix in p["xml:id"]]

    # This creates a list of all and only all <p> whose xml:id
    # contains "b1d3qun":
    pa_cont_list = []
    for parag in parag_list:
        buf = ''
        for pa in parag:
            buf += pa
        buf = clean_str(buf)
        pa_cont_list.append(buf)

    # This gives us a list of all and only all @xml:ids containing "b1d3qun":
    xml_ids = [p["xml:id"] for p in parag_list]

    # Returns a list of couples of the parsed XML, like so:
    # [('b1d3qun-cdtvet', 'Circa ...'), etc.]
    datalist = list(zip(xml_ids, pa_cont_list))
    return datalist


def compare_witnesses(fromwit, towit):
    """Compares two witnesses."""
    print('From:', fromwit.name)
    print('To:', towit.name)


def main():
    file_num = len(files)
    bar = pyprind.ProgBar(file_num, title='Parsing files...', stream=sys.stdout)

    # Creates a lists of Witness objects.
    # E.g. wit[0] is a Witness object whose name is contained in file[0].
    # witness = [Witness(files[i]) for i in range(len(files))]
    witness = []
    for i in range(file_num):
        witness.append(Witness(files[i]))
        bar.update()

    # Creates a global list of all XML:IDs (using the first file only)
    xml_ids = witness[0].xml_ids


    compare_witnesses(witness[0], witness[1])

    # texta = dictionaries[0][1][1]
    # textb = dictionaries[1][1][1]
    #
    # print(texta, '\n', textb)
    #
    # delta = simplediff.diff(texta, textb)
    # for d in delta:
    #     print(d)



if __name__ == "__main__":
    main()