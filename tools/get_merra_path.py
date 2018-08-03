from urllib.request import urlopen
import re

#connect to a URL
website = urlopen("https://disc.gsfc.nasa.gov/datasets/M2I3NPASM_V5.12.4/summary?keywords=M2I3NPASM_V5.12.4")

# read html code
html = website.read().decode('utf-8')

print(html)

#use re.findall to get the link
link = re.findall('"((http|ftp)s?://.*/data/MERRA2/M2I3NPASM.5.12.4/*)?"', html)

print(link)
