# This script builds an xml CLDR keyboard for hieroglyphs for non-QWERTY/US keyboards
# Its main goals are:
#       - to take transform items with \m{C} and order them by decreasing lengths so that they work as intended
#       - to implement the "/" convention at the end of unicode control code abreviations in order to avoid ambiguities
#               (e.g. ss/ can be used along with ss and ss/ which may clash with other abreviations)
# Its inputs are:
# - an xml for QWERTY/US keyboards
# - a partial CLDR keyboard (LOCALIZEDKEYBOARD) with the info, version, keys and layers tags correctly filled (i.e. mostly the physical layout of the keyboard)
# - an arbitrary number of "extensions" xml files that contain transformGroup tags to be included (e.g. for JSesh-like cycles
# - an arbitrary number of "extensions" tsv (tab-separated-values) files with two columns ("from" and "to") in order to implement extra abreviations, e.g. mdc phonetic abreviations)
# Its output is:
#  - a compliant keyboard that can be compiled in keyman
import xml.etree.ElementTree as ET
import os
import re
import pathlib

SOURCEQWERTYKEYBOARD = r".\sources\egyptian_hieroglyphic.xml"
LOCALIZEDKEYBOARD = r".\sources\localized.xml"
EXTENSIONSFOLDER = r".\sources\extensions\\"
OUTPUTKEYBOARD = r".\output\egyptian_hieroglyphic_modded.xml"
LOCALIZEDTAGS = ['info','version','keys','layers']

script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(script_dir)
mainET=ET.ElementTree(file=os.path.join(base_dir,SOURCEQWERTYKEYBOARD))
mainRoot=mainET.getroot()
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

transformsToAdd={}



for t in mainET.findall(".//k:transform", ns):
        fromCode = t.get("from")
        #check all transforms with the "/xxx" convention, and add the "xxx/" convention )
        m=re.match(r'/(.*)\\m{C}',fromCode)
        if m:
                toCode = t.get("to")
                if not(m.group(1)=="0"):                #On ne permet pas l'abréviation 0/ sinon on ne peut pas faire 90/ ou 270/ par exemple
                        #transformsToAdd.append({'from': m.group(1) +r"/\m{C}", 'to': toCode})
                        transformsToAdd[m.group(1)+r"/\m{C}"]=toCode
        #all other m{C} transforms have to be reordered
        m=re.match(r'(.*)\\m{C}',fromCode)
        if m:
                #transformsToAdd.append({'from': t.get("from"), 'to': t.get("to")})
                transformsToAdd[t.get("from")]=t.get("to")
                #add variants with upper case
                pattern = r"^[A-Z]\d{1,3}[a-z]$"
                if re.match(pattern,m.group(1)):
                        #transformsToAdd.append({'from': m.group(1).upper() +r"\m{C}", 'to': t.get('to')})
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
                #transformsToAdd.append({'from': x[0], 'to': x[1]})
                transformsToAdd[x[0]]=x[1]

##order those transformsToAdd by decreasing length
#def lenFrom(e):
#        return len(e["from"])
l=sorted(transformsToAdd.items(), key=lambda item: len(item[0]), reverse=True)
#transformsToAdd.sort(key=lenFrom, reverse=True)

#find the first "transforms" tag and insert a new transformGroup at the top
firstTransforms = mainRoot.find("k:transforms",ns)
tg = ET.Element("transformGroup")
#for t in transformsToAdd:
for t in l:
        tr = ET.SubElement(tg,"transform")
        #tr.set("from",t['from'])
        tr.set("from",t[0])
        #tr.set("to",t['to'])
        tr.set("to",t[1])
        
firstTransforms.insert(0,tg)

ET.register_namespace('', ns_url)
ET.indent(mainET, '  ')
mainET.write(os.path.join(base_dir,OUTPUTKEYBOARD), encoding="utf-8", xml_declaration=True)
print("Built " + os.path.join(base_dir,OUTPUTKEYBOARD))
