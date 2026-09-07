# This script builds an xml CLDR keyboard for hieroglyphs for non-QWERTY/US keyboards
# Its main goals are:
#       - to take transform items with \m{C} and order them by decreasing lengths so that they work as intended
#       - to implement the "/" convention at the end of unicode control code abreviations in order to avoid ambiguities
#               (e.g. ss/ can be used along with ss and ss/ which may clash with other abreviations)
# Its inputs are:
# - an xml for QWERTY/US keyboards
# - a partial CLDR keyboard (LOCALIZEDKEYBOARD) with the info, version, keys and layers tags correctly filled (i.e. mostly the physical layout of the keyboard)
# - an arbitrary number of "extensions" xml files that contain transformGroup tags to be included
# - the location of the signs description from JSesh (as a source for the 'phonetic to Gardiner' conversions, as well as the JSesh 'cycles', like aA = O29 O29/R E7 O31 O29 ...
# - the location of the core java from mdc phonetic codes from JSesh
# - a dictionary for "JSESH fixes", converting for instance O29v to O29a
# - an arbitrary number of "extensions" tsv (tab-separated-values) files with two columns ("from" and "to") in order to implement extra abreviations, e.g. mdc phonetic abreviations)
# Its output is:
#  - a compliant keyboard that can be compiled in keyman (constant OUTPUTKEYBOARD)
# - a tsv with the implemented cycles
import xml.etree.ElementTree as ET
import os
import re
import pathlib
import collections
import urllib.request
import html

SOURCEQWERTYKEYBOARD = r".\sources\egyptian_hieroglyphic.xml"
LOCALIZEDKEYBOARD = r".\sources\localized.xml"
EXTENSIONSFOLDER = r".\sources\extensions\\"
OUTPUTKEYBOARD = r".\output\egyptian_hieroglyphic_modded.xml"
OUTPUTTSV = r".\output\cycles.tsv"
LOCALIZEDTAGS = ['info','version','keys','layers']
JSESHSIGNSDESCRIPTIONURL="https://raw.githubusercontent.com/rosmord/jsesh/refs/heads/master/jsesh/src/main/resources/jsesh/glyphs/resources/signs_description.xml"
JSESHMDCJAVAURL = "https://raw.githubusercontent.com/rosmord/jsesh/refs/heads/master/jsesh/src/main/java/jsesh/signcodes/ManuelDeCodage.java"
JSESHFIXES = { 'O29v' : 'O29a'}

script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(script_dir)
qwertyFilePath=os.path.join(base_dir,SOURCEQWERTYKEYBOARD)
mainET=ET.ElementTree(file=qwertyFilePath)
mainRoot=mainET.getroot()
#------------------------------------------------------------------------------------------
#First, we build the dGardiner dictionary which associates Gardiner codes with unicode codepoints, from Andrew Glass' original qwerty keyboard
with open(qwertyFilePath, 'r', encoding='utf-8') as f:
        lines=list(f)
curTitle=""
sXMLGardinerToUnicode=""
for line in lines:
        if line.strip().startswith("<!--"):
                curTitle=line.strip()
        if curTitle=="<!-- ✅Hieroglyphs from Gardiner-->" or curTitle=="<!-- Egyptian Hieroglyphs Extended-A -->":
                sXMLGardinerToUnicode+=line
t=ET.fromstring("<root>"+sXMLGardinerToUnicode+"</root>")
dGardiner={}
sg=t.findall('.//transform')
for g in sg:
        #only take those with \u in the "to"
        if "\\u" in g.get("to"):
                unichar=chr(int(re.findall(r'\\u{(.*)}',g.get("to"))[0],16))
                fromCode = g.get("from").replace(r'\m{C}','')
                dGardiner[fromCode]=unichar
                dGardiner[fromCode.upper()]=unichar
                if fromCode.startswith("AA"):
                        dGardiner["Aa"+fromCode[2:]]=unichar
#--------------------------------------------------------------------------------------------------------------------------------------------------------
# Compute the JSesh "cycles", i.e. the various Gardiner codes associated with a phonetic code
d = collections.defaultdict(list)
linesMDCJAVA = urllib.request.urlopen(JSESHMDCJAVAURL).read().decode("utf_8").splitlines()
for line in linesMDCJAVA:
        if not("//" in line) and "putCanon" in line:
                li=re.findall(r'"(.*?)"', line)
                if len(li)==2:
                        if li[1] in JSESHFIXES:
                                li[1]=JSESHFIXES[li[1]]
                                #print("fixed {}".format(li[1]))
                        li[0]=li[0].replace("-","")
                        if li[1] in dGardiner:
                                d[li[0]]=[li[1]]
signsET = ET.fromstring(urllib.request.urlopen(JSESHSIGNSDESCRIPTIONURL).read().decode('utf-8'))
ss=signsET.findall('.//hasTransliteration[@use="keyboard"]')

for s in ss:
        sign = s.attrib['sign']
        translit=s.attrib["transliteration"]
        translit=translit.replace("-","")
        if sign in JSESHFIXES:
                sign=JSESHFIXES[sign]
        if (not(sign in d[translit])) and (sign in dGardiner):
                d[translit].append(sign)
cycles = {k: v for k, v in sorted(d.items(), key=lambda item: item[0].upper())}     #classe en ordre croissant

#-------------------------------------------------------------------------------------------------------------------------
# Save the cycles .TSV
outputTSVFilePath=os.path.join(base_dir,OUTPUTTSV)
sOut=""
for a,dd in cycles.items():
        lDisplay=[a]
        for p in dd:
                if p in dGardiner:
                        lDisplay.append(p + " " + dGardiner[p])
                else:
                        lDisplay.append(p)
        sDisplay="\t".join(lDisplay)
        sOut+=sDisplay+"\n"
f = open(outputTSVFilePath, "w", encoding="utf-8")
f.write(sOut)
f.close()
with open(outputTSVFilePath, "r", encoding="utf-8") as f:
    rows = [line.rstrip("\n\r").split("\t") for line in f]

with open(outputTSVFilePath+".html", "w", encoding="utf-8") as f:
    f.write("""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
table { border-collapse: collapse; }
td { border: 1px solid #999; padding: 4px 8px; }
</style>
</head>
<body>
<table>
""")

    for row in rows:
        f.write("<tr>\n")
        for cell in row:
            f.write("<td>" + html.escape(cell) + "</td>\n")
        f.write("</tr>\n")

    f.write("""</table>
</body>
</html>
""")

#--------------------------------------------------------------------------------------------------------------------------------------------------------
#Merge localized xml with main qwerty xml
ns_url= re.match(r'\{(.*)\}', mainRoot.tag).group(1)
ns = {'k': ns_url}
for tagName in LOCALIZEDTAGS:
        mainRoot.remove(mainRoot.find('k:'+tagName, ns))

localizedET=ET.ElementTree(file=os.path.join(base_dir,LOCALIZEDKEYBOARD))
localizedRoot=localizedET.getroot()

#replace the tags info, version, keys and layers with those coming from the localized keyboard xml
for tagName in reversed(LOCALIZEDTAGS):
        tag=localizedRoot.find('k:'+tagName, ns)
        mainRoot.insert(0,tag)

#--------------------------------------------------------------------------------------------------------------------------------------------------------
#start computing all transforms
transformsToAdd={}

for t in mainET.findall(".//k:transform", ns):
        fromCode = t.get("from")
        #check all transforms with the "/xxx" convention, and add the "xxx/" convention )
        m=re.match(r'/(.*)\\m{C}',fromCode)
        if m:
                toCode = t.get("to")
                if not(m.group(1)=="0"):                #On ne permet pas l'abréviation 0/ sinon on ne peut pas faire 90/ ou 270/ par exemple
                        transformsToAdd[m.group(1)+r"/\m{C}"]=toCode
        #all other m{C} transforms have to be reordered
        m=re.match(r'(.*)\\m{C}',fromCode)
        if m:
                transformsToAdd[t.get("from")]=t.get("to")
                #add variants with upper case
                pattern = r"^[A-Z]\d{1,3}[a-z]$"
                if re.match(pattern,m.group(1)):
                        transformsToAdd[m.group(1).upper() +r"\m{C}"]=t.get('to')

#check the extras formatted as xml
for xml_file in pathlib.Path(os.path.join(base_dir,EXTENSIONSFOLDER)).glob('*.xml'):
        extensionET=ET.ElementTree(file=xml_file)
        for t in extensionET.findall(".//k:transform", ns):
                #transformsToAdd.append({'from': t.get("from"), 'to': t.get("to")})
                transformsToAdd[t.get("from")]=t.get("to")

#check the extras formatted as tsv
for xml_file in pathlib.Path(os.path.join(base_dir,EXTENSIONSFOLDER)).glob('*.tsv'):
        with open(xml_file, 'r', encoding='utf-8') as f:
                lines=list(f)
        for line in lines:
                line=line.replace("\n","")      #extra line feeds
                x = line.split("\t")
                transformsToAdd[x[0]]=x[1]


#add the cycles
for k,v in cycles.items():
        if len(v)==1:
                transformsToAdd[k+"\\m{C}"]="\\u{"+hex(ord(dGardiner[v[0]]))[2:]+"}"
        elif len(v)>1:
                transformsToAdd[k+"\\m{C}"]="\\u{"+hex(ord(dGardiner[v[0]]))[2:]+"}\m{cycle"+k+"}"
                for i in range(0,len(v)-1):
                        transformsToAdd["\\u{"+hex(ord(dGardiner[v[i]]))[2:]+"}\m{cycle"+k+"}\m{C}"]="\\u{"+hex(ord(dGardiner[v[i+1]]))[2:]+"}\m{cycle"+k+"}"
                transformsToAdd["\\u{"+hex(ord(dGardiner[v[len(v)-1]]))[2:]+"}\m{cycle"+k+"}\m{C}"]="\\u{"+hex(ord(dGardiner[v[0]]))[2:]+"}\m{cycle"+k+"}"      
                

##order those transformsToAdd by decreasing length
def longueur(s):
    # \u{.....} and \m{.....} each count for 1 character
    # We replace these special tokens with exactly 1 character
    return len(re.sub(r'\\(?:u|m)\{[^}]*\}', 'X', s))
l=sorted(transformsToAdd.items(), key=lambda item: longueur(item[0]), reverse=True)

#find the first "transforms" tag and insert a new transformGroup at the top
firstTransforms = mainRoot.find("k:transforms",ns)
tg = ET.Element("transformGroup")
#for t in transformsToAdd:
for t in l:
        tr = ET.SubElement(tg,"transform")
        tr.set("from",t[0])
        tr.set("to",t[1])
        
firstTransforms.insert(0,tg)

ET.register_namespace('', ns_url)
ET.indent(mainET, '  ')
mainET.write(os.path.join(base_dir,OUTPUTKEYBOARD), encoding="utf-8", xml_declaration=True)
print("Built " + os.path.join(base_dir,OUTPUTKEYBOARD))
