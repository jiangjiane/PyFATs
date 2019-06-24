import vtk
from vtk.util.colors import *

math = vtk.vtkMath()

actors = []

# create a rat's nest of lines
points = vtk.vtkPoints()
lines = vtk.vtkCellArray()
lines.InsertNextCell(200)
for i in range(10):
    #points.InsertPoint(i, math.Random(-1, 1), math.Random(-1, 1), math.Random(-0.2, 0.2))
    ip = (i-5.0) / 5.0
    for j in range(10):
        jp = (j-5.0) / 5.0
        pt = i * j * 2
        points.InsertPoint(pt, -1.0, ip, -jp)
        lines.InsertCellPoint(pt)
        points.InsertPoint(pt+1, 1.0, -ip, jp)
        lines.InsertCellPoint(pt+1)
    #
#

linePolys = vtk.vtkPolyData()
linePolys.SetPoints(points)
linePolys.SetLines(lines)

# clip to the sphere
# a sphere to clip
cutSphere = vtk.vtkSphere()
cutSphere.SetRadius(0.5)

clipper = vtk.vtkClipPolyData()
clipper.SetInputConnection(linePolys)
clipper.SetClipFunction(cutSphere)
#clipper.GenerateClipScalarsOn()
clipper.GenerateClippedOutputOn()
#clipper.GenerateClippedData(True)
#clipper.SetValue(0.5)

cutter = vtk.vtkCutter()
cutter.SetInput(linePolys)
cutter.SetCutFunction(cutSphere)
cutter.GenerateCutScalarsOn()
#cutter.SetValue(1.0, 0.5)

lineMapper = vtk.vtkPolyDataMapper()
#lineMapper.SetInput(linePolys)
#lineMapper.SetInput(clipper.GetOutput())
lineMapper.SetInput(cutter.GetOutput())
lineActor = vtk.vtkActor()
lineActor.SetMapper(lineMapper)
lineActor.GetProperty().SetColor(red)
#lineActor.GetProperty().SetOpacity(0.6)
actors.append(lineActor)

# a sphere to show
sphere = vtk.vtkSphereSource()
sphere.SetRadius(0.5)
sphereMapper = vtk.vtkPolyDataMapper()
sphereMapper.SetInput(sphere.GetOutput())
sphereActor = vtk.vtkActor()
sphereActor.SetMapper(sphereMapper)
sphereActor.GetProperty().SetOpacity(0.05)
actors.append(sphereActor)

# rendering stuff
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
# Add the actors to the renderer, set the background and size
for actor in actors:
    ren.AddActor(actor)

ren.SetBackground(1, 1, 1)
renWin.SetSize(600, 400)

camera = vtk.vtkCamera()
camera.SetClippingRange(1.81325, 90.6627)
camera.SetFocalPoint(0, 0, 0)
camera.SetPosition(4.5, 1.0, 6.73257)
camera.SetViewUp(0, 1, 0)
camera.Zoom(1.0)
ren.SetActiveCamera(camera)

iren.Initialize()
renWin.Render()
iren.Start()