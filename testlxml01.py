import re
import os
from lxml import etree


def clean_str(thetext):
    thetext = re.sub("\n", " ", thetext)
    thetext = re.sub("\t{1,8}", " ", thetext)
    thetext = re.sub("[ ]{1,8}", " ", thetext)
    thetext = re.sub("[ ]{1,8}", " ", thetext)
    return thetext


def parse_file(file):
    namespaces = {'tei': 'http://www.tei-c.org/ns/1.0'}
    # xp_bodytext = "//tei:body//text()"
    # xp_alltext = "//text()"
    # xp_seg = "//tei:body//tei:seg//text()"
    # xp_said = "//tei:body//tei:said//text()"
    # xp_p = "//tei:body//tei:p//text()"
    xp_p = "//tei:body//tei:p"
    xp_xmlid = "//tei:body//tei:p/@xml:id"
    tree = etree.parse(file)

    # This creates a list of all xml:ids of the <p>, like so:
    # ['b1d3qun-cdtvet', 'b1d3qun-aettwo', etc.]
    xml_ids = tree.xpath(xp_xmlid, namespaces=namespaces)

    paragraphs = tree.xpath(xp_p, namespaces=namespaces)
    parags = []
    for par in paragraphs:
        # text = ''
        # for x in par.xpath('.//text()'):
        #     text = text + x + ' '
        text = ' '.join(x for x in par.xpath('.//text()'))
        text = clean_str(text)
        parags.append(text)

    # Returns a list of the parsed XML, like so:
    # [('b1d3qun-cdtvet': 'Circa ...'), etc.]
    # This is useful because it indexes each pair of xml:id and p-content,
    # since the xml:ids are not sorted in themselves.
    return [(xml_ids[i], parags[i]) for i in range(len(parags))]


def main():
    data_path = 'data/'
    files = ['sorb', 'maz', 'vat', 'tara']
    extension = '.xml'

    # Creates a list of the files, like so:
    # ['data/sorb.xml', etc.]
    file_list =\
        [os.path.join(data_path, ''.join([file, extension])) for file in files]

    # Creates a list of the dictionaries, like so:
    # [{'b1d3qun-cdtvet': 'Circa...'}, etc.]
    # This is required to index each xml:id => p
    # as the xml:ids are not sorted out.
    dictionaries = [parse_file(file) for file in file_list]

    # dictionaries[0][0] contains the first pair (xml:id : p) of the first XML file.
    print(dictionaries[0][0])
    print(dictionaries[1][0])
    print(dictionaries[2][0])
    print(dictionaries[3][0])


if __name__ == "__main__":
    main()