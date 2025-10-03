import sys
import FreeCAD as App
import Part
import Mesh

inp = sys.argv[1]
outp = sys.argv[2]

shape = Part.Shape()
shape.read(inp)
doc = App.newDocument('Doc')
pf = doc.addObject("Part::Feature","MyShape")
pf.Shape = shape
Mesh.export([pf], outp)