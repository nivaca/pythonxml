from bs4 import BeautifulSoup

content = '''
<p xml:id="myid2312">
quod non videtur quia secundum <name ref="#Augustine">augustinum</name> in <title>sermone
                <lb ed="#S"/>communi de uno martyre</title> si servasset in se
                <lb ed="#S"/>homo bonum quod in illo <corr><add place="marginBottom">creavit deus id est <choice><orig>ymaginem</orig><reg>imaginem</reg></choice> suam semper laudaret deum non solum lingua sed et vita</add></corr> etc igitur ex opposito non sic laudat
                <cb n="79va"/><lb ed="#S"/>igitur non servavit in se bonum illud secundum <choice><orig>ymaginem</orig><reg>imaginem</reg></choice> dei et tamen servat
                men<lb ed="#S"/>tem suam igitur mens humana non est <choice><orig>ymago</orig><reg>imago</reg></choice> dei
</p>'''


soup = BeautifulSoup(content, "lxml-xml")

# print(soup.choice)
# print(soup.name)
# print(soup.get_text())
# for child in soup.p.stripped_strings:
#     print(child)

# for tag in soup.find_all(True):
#     print(tag.name)

print(soup.find_all(id="myid2312"))