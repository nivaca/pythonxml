from io import StringIO, BytesIO
from bs4 import BeautifulSoup
import re


soup = BeautifulSoup(open("data/sorb.xml"), "lxml-xml")


# Checks whether tag has 'xml:id'
def has_attr(tag):
    return tag.has_attr('xml:id')


paragraphs = soup.find_all(has_attr)


# This gives us a list of all and only all <p> whose xml:id
# contains "b1d3qun":
parag_list = [p for p in paragraphs if "b1d3qun" in p["xml:id"]]

# This gives us a list of all and only all <p> whose xml:id
# contains "b1d3qun":
pa_cont_list = [p.contents for p in parag_list]

# This gives us a list of all and only all @xml:ids containing "b1d3qun":
xml_ids = [p["xml:id"] for p in parag_list]


# for p in pa_cont_list:
#     print('\n', pa_cont_list.index(p), ' ===> ', p)

text = (pa_cont_list[186])
newtext = " ".join(str(x) for x in text)
newtext = '<p>' + newtext + '</p>'
textsoup = BeautifulSoup(newtext, "lxml-xml")
# for desc in textsoup.descendants:
#     print(desc)

# print(textsoup.prettify(), '\n')

strcont = textsoup.choice.reg.contents

textsoup.choice.replace_with(strcont)
print(textsoup.prettify())
