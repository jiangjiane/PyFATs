import vtk

class CustomInteractor(vtk.vtkInteractorStyleTrackballCamera):

    def __init__(self, renderer, renWin):
        self.AddObserver('LeftButtonPressEvent', self.OnLeftButtonDown)
        self.AddObserver('LeftButtonReleaseEvent', self.OnLeftButtonRelease)
        self.AddObserver('MouseMoveEvent', self.OnMouseMove)

        self.renderer = renderer
        self.chosenPiece = None
        self.renWin = renWin

    def OnLeftButtonRelease(self, obj, eventType):
        self.chosenPiece = None
        vtk.vtkInteractorStyleTrackballCamera.OnLeftButtonUp(self)

    def OnLeftButtonDown(self, obj, eventType):
        clickPos = self.GetInteractor().GetEventPosition()

        picker = vtk.vtkPropPicker()
        picker.Pick(clickPos[0], clickPos[1], 0, self.renderer)
        actor = picker.GetActor2D()

        self.chosenPiece = actor

        vtk.vtkInteractorStyleTrackballCamera.OnLeftButtonDown(self)

    def OnMouseMove(self, obj, eventType):
        if self.chosenPiece is not None:

            mousePos = self.GetInteractor().GetEventPosition()

            self.chosenPiece.SetPosition(mousePos[0], mousePos[1])

            self.renWin.Render()
        else :
            vtk.vtkInteractorStyleTrackballCamera.OnMouseMove(self)


def buildDiskActor(inner_radius = 10, outer_radius = 20, position = (100, 20), color = (1, 1, 1)):
    disk = vtk.vtkDiskSource()
    disk.SetInnerRadius(inner_radius)
    disk.SetOuterRadius(outer_radius)
    disk.SetRadialResolution(100)
    disk.SetCircumferentialResolution(100)
    disk.Update()

    mapper = vtk.vtkPolyDataMapper2D()
    mapper.SetInputConnection(disk.GetOutputPort())

    actor = vtk.vtkActor2D()
    actor.SetMapper(mapper)

    actor.SetPosition(position[0], position[1])

    actor.GetProperty().SetColor(color)

    return actor

ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetSize(600, 600)

elements = [
    buildDiskActor(position = (200, 400), color=(1, 0, 0)),
    buildDiskActor(position = (400, 400), color=(0, 1, 0)),
    buildDiskActor(position = (300, 200), color=(0, 0, 1)),
]

for actor in elements:
    ren.AddActor(actor)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
inStyle = CustomInteractor(ren, renWin)
iren.SetInteractorStyle(inStyle)

renWin.Render()
iren.Start()