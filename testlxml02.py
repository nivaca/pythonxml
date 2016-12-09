import re
import os
from io import StringIO, BytesIO
from lxml import etree

def clean_str(thetext):
    # thetext = re.sub("<.*?>", "", thetext)
    # thetext = re.sub("<.*?/>", "", thetext)
    thetext = re.sub("\n", " ", thetext)
    thetext = re.sub("\t{1,8}", " ", thetext)
    thetext = re.sub("[ ]{1,8}", " ", thetext)
    thetext = re.sub("[ ]{1,8}", " ", thetext)
    return thetext

content = '''
<p>
quod non videtur quia secundum <name ref="#Augustine">augustinum</name> in <title>sermone
                <lb ed="#S"/>communi de uno martyre</title> si servasset in se
                <lb ed="#S"/>homo bonum quod in illo <corr><add place="marginBottom">creavit deus id est <choice><orig>ymaginem</orig><reg>imaginem</reg></choice> suam semper laudaret deum non solum lingua sed et vita</add></corr> etc igitur ex opposito non sic laudat
                <cb n="79va"/><lb ed="#S"/>igitur non servavit in se bonum illud secundum <choice><orig>ymaginem</orig><reg>imaginem</reg></choice> dei et tamen servat
                men<lb ed="#S"/>tem suam igitur mens humana non est <choice><orig>ymago</orig><reg>imago</reg></choice> dei
</p>'''

content = clean_str(content)
print(content)
exit(0)

tree = etree.parse(StringIO(content))

root = tree.getroot()

for child in root.iterchildren():
    print(etree.tostring(child))

