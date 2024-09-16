# BIManalyst group 37
#importing the file
import bpy
from bonsai.bim.ifc import IfcStore
model = IfcStore.get_file()
# here going through wall, but can change it to beam or column 
wall = model.by_type('IfcWall')[0]
for definition in wall.IsDefinedBy:
    for prop in definition.RelatingPropertyDefinition.HasProperties:
        print(prop.Name)
        if prop.Name == "Volume":
            #print("si")
            print("the volume is", prop.NominalValue.wrappedValue)
        if prop.Name == "Area":
            print("the area is", prop.NominalValue.wrappedValue)
        if prop.Name == "Length":
            print("the length is", prop.NominalValue.wrappedValue)
        
print(wall)




