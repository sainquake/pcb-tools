from test_pcb import get_parameters_in_projpcb 
from test_pcb import get_project_name
from common import getBBoxFromSTEP
from common import getBBoxFromGerber
from common import layerStackParce
from common import minTrace
from common import minFromAllNCDrill
from common import generatBOMToPCBWay

#COPY ALL NEEDE FILES
import shutil
import os

path = "./PCBWay-output"
isExist = os.path.exists(path)
if not isExist:
    os.makedirs(path)

shutil.copyfile('./Project Outputs/Pick Place/Pick Place for PCB.txt', './PCBWay-output/Pick Place.txt')
path = "./PCBWay-output/Gerber"
isExist = os.path.exists(path)
if not isExist:
   os.makedirs(path)
for path in os.listdir('./Project Outputs/Gerber/'):
    print(path)
    shutil.copyfile(f'./Project Outputs/Gerber/{path}', f'./PCBWay-output/Gerber/{path}')
shutil.copyfile('./Project Outputs/CAMtastic1.Cam', './PCBWay-output/CAMtastic1.Cam')
shutil.copyfile('./doc/drw.png', './PCBWay-output/drw.png')

for path in os.listdir('./Project Outputs/NC Drill/'):
    if '.TXT'.lower() in path.lower():
        shutil.copyfile('./Project Outputs/NC Drill/'+path, './PCBWay-output/'+path)

bom = generatBOMToPCBWay('./PCBWay-output/BOM.xlsx')






#GET MODEL DIMENSIONS
stepBBox = getBBoxFromSTEP()
# GET GERBER DIMENSION
gerberBBox = getBBoxFromGerber()
layerStack = layerStackParce()

f = open("PCBWay-output/README.md", "w",encoding='UTF-8')   # 'r' for reading and 'w' for writing

params = get_parameters_in_projpcb()


minwidth = minTrace()
mindrill = minFromAllNCDrill()

f.write(f"# {get_project_name()} v{params['Version']} Order details\n\n")
f.write(f'''

### PCB Specification Selection

- Board type : Panel by PCBWay
- Break-away rail: Yes
- Instructions:
~~~
Final size is larger ( {stepBBox[0]} x {stepBBox[1]} mm ) than board it self ( {gerberBBox[0]} x {gerberBBox[1]} mm), 
take a look at the picure in attachements. 
Panel should be designed to be able to install PWM1, PWM2 while assembly.
~~~
- Route Process: Panel as PCBWay prefer
- X-out Allowance in Panel:  Accept

- Size (single): {gerberBBox[0]} x {gerberBBox[1]} mm
- Quantity (single): 200
- Layers: {len(layerStack["list"])} -   {layerStack["list"]} check [PCBway layer stack](https://www.pcbway.com/multi-layer-laminated-structure.html)

- Material: FR-4
- FR4-TG: TG 150-160
- Thickness: {layerStack["stndart height"]}
- Min Track/Spacing: {round(minwidth*39.3701)}/{round(minwidth*39.3701)}mil ({minwidth} mm)
- Min Hole Size: {mindrill} mm
- Solder Mask: Black
- Silkscreen: White
- Edge connector: No
- Surface Finish: HASL with lead
- Yes - Tick means you accept we might change "HASL" to "ENIG" at our discretion without extra charge.
- Via Process: Tenting vias
- Finished Copper: 1 oz Cu
- Other Special request:
~~~
Final size is larger ( {stepBBox[0]} x {stepBBox[1]} mm ) than board it self ( {gerberBBox[0]} x {gerberBBox[1]} mm )
~~~

### Assembly Service

- Turnkey
- Board type : Panelized PCBs
-  Assembly Side(s): Both sides
- Quantity: 200
- Contains Sensitive components/parts - No; 
- Do you accept alternatives/substitutes made in China? - Yes

- Number of Unique Parts: 0
- Number of SMD Parts: 0
- Number of BGA/QFP Parts: 0
- Number of Through-Hole Parts: 0

### Additional Options

- Firmware loading: Yes
- Detailed information of assembly:
~~~
Firmware is in attachements.
Take a look at the picure in attachements should be installed from the side.
~~~

''')






f.close()