# BIManalyst group 37
print("hello we are group 37")
import bpy
from bonsai.bim.ifc import IfcStore
model = IfcStore.get_file()
beam = model.by_type("IfcBeam")
a=list(beam)
print("there is",len(a),"beams in the model")


