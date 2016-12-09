import os
from bs4 import BeautifulSoup
from xmlcleaners import meta_cleanup, clean_str
import simplediff
from pprint import pprint


xml_prefix = 'b1d3qun'


def parse_file(file):
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

    # Returns a list of the parsed XML, like so:
    # [('b1d3qun-cdtvet': 'Circa ...'), etc.]
    # This is useful because it indexes each pair of xml:id and p-content,
    # since the xml:ids are not sorted in themselves.
    return [(xml_ids[i], pa_cont_list[i]) for i in range(len(pa_cont_list))]


def main():
    data_path = 'data/'
    files = ['sorb', 'maz', 'vat', 'tara']
    extension = '.xml'

    # Creates a list of the files, like so:
    # ['data/sorb.xml', etc.]
    file_list = \
        [os.path.join(data_path, ''.join([file, extension])) for file in files]

    # Creates a list of the dictionaries, like so:
    # [{'b1d3qun-cdtvet': 'Circa...'}, etc.]
    # This is required to index each xml:id => p
    # as the xml:ids are not sorted out.
    dictionaries = [parse_file(file) for file in file_list]


    texta = dictionaries[0][1][1]
    textb = dictionaries[1][1][1]

    print(texta, '\n', textb)

    delta = simplediff.diff(texta, textb)
    for d in delta:
        print(d)



if __name__ == "__main__":
    main()