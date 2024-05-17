from test_pcb import get_parameters_in_projpcb 
from test_pcb import get_project_name
from common import getBOM
from common import alphaAndCut
from common import parseNetlist
from common import getBBoxFromSTEP
from common import getBBoxFromGerber
from common import layerStackParce

f = open("doc/README.md", "w",encoding='UTF-8')   # 'r' for reading and 'w' for writing

params = get_parameters_in_projpcb()

f.write(f"# {get_project_name()} v{params['Version']} hardware\n\n")

f.write('Here it is some text to be edited about this board\n\n')

alphaAndCut('./doc/view.png','./doc/t-view.png')
alphaAndCut('./doc/view-bottom.png','./doc/t-view-bottom.png')
alphaAndCut('./doc/view-top.png','./doc/t-view-top.png')

f.write('| | | |\n')
f.write('|-|-|-|\n')
f.write('| <img src="t-view.png" alt="drawing" width="300"> | <img src="t-view-top.png" alt="drawing" width="300"/> | <img src="t-view-bottom.png" alt="drawing" width="300"/> |\n')
f.write('|  | <img src="r-view-top.jpg" alt="drawing" width="300"/> | <img src="r-view-bottom.jpg" alt="drawing" width="300"/> |\n')
f.write('\n')

f.write('### 1. Features\n\n')

f.write('- first feature for example\n')
f.write('- second feature for example\n')
#for key in params:
#    f.write(f'{key} = {params[key]}\n')


f.write('### 2 Wire\n\n')

f.write(f"The node has connectors which are described in the table below.\n\n")

# from deep_translator import GoogleTranslator
# translated = GoogleTranslator(source='en', target='ru').translate(f"The node has connectors which are described in the table below.\n\n")  
# print(translated)
# f.write(translated+'\n\n')

f.write("**Connectors**\n\n")


f.write("The node has connectors which are described in the table below.\n\n")

f.write(f"| N | Connector | Description |\n")
f.write(f"| - | - | - |\n")

bom = getBOM()
i=1
con_des = []
for index, row in bom.iterrows():
    #print(row['System'], row['Designator'])
    if 'Connector' in row['System']:
        f.write(f"| {i} | {row['Designator']} |  |\n")
        con_des = con_des+ row['Designator'].replace(' ','').split(',')
        i+=1


f.write('**Pin configuration and functions**\n')
f.write('\n')

netlist = parseNetlist()

pinnames = []
for it in con_des:
    pn = {}
    pn['name'] = it
    #f.write(f"**{it}** \n\n")
    #f.write(f"| Pin N | Net name |\n")
    #f.write(f"| -     | -        |\n")
    
    l=[]
    for item in netlist:
        if it.lower() in item['designator'].lower():
            l.append([item['pinNum'],item['net']])
    l = sorted(l,key=lambda x: (x[0]))
    pn['list'] = l
    #for item in l:
    #    f.write(f"| {item[0]:2} | {item[1]:10} |\n")
    #f.write('\n')
    pinnames.append( pn )

#pinnames = sorted(pinnames,key=lambda x: (len(x['list'])))

strarr = []
strarr.append('|')
strarr.append('|')
for item in pinnames:
    strarr[0] += ' Pin N | '+item['name']+' |'
    strarr[1] += ' ----- | ---------------- |'
    i=3
    for it in item['list']:
        if len(strarr)<i:
            strarr.append('|')
        strarr[i-1] += f' {it[0]} | {it[1]} |'
        i+=1
    while i<len(strarr):
        strarr[i-1] += " | |"
        i+=1
for item in strarr:
    f.write(item+'\n')

f.write('\n\n')
f.write('Here you can see all connections of MCU.\n\n')

f.write('<img src="doc/pinout.png" alt="pinout"/>\n\n')


f.write("| MCU PIN         | PIN Numer | NET Name | Description |\n")
f.write("| ---------- |  -- | --------------  | - |\n")

for item in netlist:
    if 'STM'.lower() in item['component'].lower():
        if ('GND' not in item['net']) and ('3.3' not in item['net']) and ('3V3' not in item['net']) :
            #print(item['pinName'],item['net'])
            f.write(f"| {item['pinName']:14} |  {item['pinNum']:2} | {item['net']:10}  |  |\n")


f.write("### 2.3. Specifications\n\n")

f.write("#### **Mechanical**\n\n")

f.write("Scheme is shown on the picture below. CAN model can be provided via email request or issue on github or downloaded on [GrabCAD](https://grabcad.com/library/housing-for-raccoonlab-gnss-mag-baro-v250-1).\n\n")

f.write("![drw.png](drw.png?raw=true 'drw.png')\n\n")

# GENERATE PNG OF drw

try:
    # pip install pdf2image

    from pdf2image import convert_from_path
    pages = convert_from_path('./doc/doc.pdf', 500)
    pages[-1].save('./doc/drw.png', 'PNG')

    #Cut('./doc/drw.png','./doc/drw.png')
except:
    print('something wrong with pdf2image')


#GET MODEL DIMENSIONS
stepBBox = getBBoxFromSTEP()
# GET GERBER DIMENSION
gerberBBox = getBBoxFromGerber()
layerStack = layerStackParce()

f.write("|       | Width, mm | Length, mm | Height, mm |\n")
f.write("| ----- | --------- | ---------- | ---------- |\n")
f.write(f"|Outline| {stepBBox[0]:9} | {stepBBox[1]:10} | {stepBBox[2]:10} |\n")
f.write(f"|PCB    | {gerberBBox[0]:9} | {gerberBBox[1]:10} | {layerStack['stndart height']:10} |\n\n")

f.write("Total weight of device less than 50 g.\n\n")

f.write("#### **Housing**\n\n")

f.write('some text about housing\n\n')

f.write('<img src="housing.jpg" alt="housing" width="200">\n\n')


from datetime import date

today = date.today()
d1 = today.strftime("%d.%m.%Y")


f.write(f'''
#### **Absolute Maximum Ratings**

| Parameter     | MIN   | MAX | UNIT |
|-----------    |-------|-----|------|
| Vin (HV)      | 5.5   | 55* | V    |
| V (LV)        | 4.5   | 5.5 | V    |
| I max         |       | 1.0 | A    |
| Operating temperature
 
 *Noted Voltage should be delivered only with current limitation under 2.5 Amp.

#### **Recommended operating conditions**

| Parameter     | Value | UNIT |
|-----------    |-------|------|
| Vin (HV)      | 30    | V    |
| V (LV)        | 5     | V    |
| I max         |       | A    |

#### **ESD ratings**

| Description                | Value | UNIT |
|----------------------------|-------|------|
| Human-body model (HBM)     | 2000  | V    |
| Charged-device model (CDM) | 500   | V    |

### 2.4. Integration 

**Recommended mechanical mounting**

**Connection example diagram**

### 2.5. Power Supply Recommendations

Device is designed to operate from an input voltage supply range between 4.5 V and 5.5 V over CAN2 or CAN3 connector, or 5.5 - 30 V from CAN1. This input supply must be able to withstand the maximum input current and maintain a stable voltage. The resistance of the input supply rail should be low enough that an input current transient does not cause a high enough drop that can cause a false UVLO fault triggering and system reset. The amount of bulk capacitance is not critical, but a 47-μF or 100-μF electrolytic capacitor is a typical choice.

### 2.6. Revision history

| View | Version | Description |
| ---- | ------- | ----------- |
| <img src="t-view.png" alt="drawing" width="120"/> | v{params['Version']} <br /> {d1} | Latest version of the board <br /> Some other additional info |    
        
''')


f.close()