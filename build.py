import cadquery as cq
from cadquery import exporters
from cadquery import Vector, Edge, Wire, Solid, Shell, Face

def polyhedron(points, faces):
    
    def _edges(vectors, face_indices):
        leng_vertices = len(face_indices)   
        return (
            Edge.makeLine(
                vectors[face_indices[i]], 
                vectors[face_indices[(i + 1) % leng_vertices]]
            ) 
            for i in range(leng_vertices)
        )

    vectors = [Vector(*p) for p in points]
    
    return Solid.makeSolid(
        Shell.makeShell(
            Face.makeFromWires(
                Wire.assembleEdges(
                    _edges(vectors, face_indices)
                )
            )
            for face_indices in faces
        )
    )

f = open('coordination.txt', 'r')
size = f.readline().split()
height = int(size[0])
width = int(size[1])
build_height = 300
thickness = 1.0
# make the base
base = cq.Workplane("XY").box(width, height, thickness)
shapes = f.readlines()
for x in shapes:
    x = x.split()
    if x[4] == "Circle":
        txt = cq.Workplane().circle(int(x[3])/2).extrude(build_height)
        base.add(txt.translate((int(x[1])+int(x[3])/2-height/2,int(x[0])+int(x[2])/2-width/2,0)))
    elif x[4] == "Rectangle" or x[4] == "Square":
        txt = cq.Workplane().box(int(x[3]),int(x[2]),build_height)
        base.add(txt.translate((int(x[1])+int(x[3])/2-height/2,int(x[0])+int(x[2])/2-width/2,build_height/2)))
    elif x[4] == "triangle":
        points = ((int(x[1])+int(x[3])-height/2, int(x[0])-width/2, 0), 
                  (int(x[1])+int(x[3])-height/2, int(x[0])-width/2+int(x[2]), 0), 
                  (int(x[1])+int(x[3])-height/2-int(x[3]), int(x[0])-width/2+int(x[2])/2, 0), 
                  (int(x[1])+int(x[3])-height/2-int(x[3])/2, int(x[0])-width/2+int(x[2])/2, build_height))
        faces = ((0, 1, 2), (0, 3, 1), (1, 3, 2), (0, 2, 3))
        txt = polyhedron(points, faces)
        base.add(txt)
# Render the solid

exporters.export(base, 'box.stl')