#!/usr/bin/env python

"""
Modified from VTK/Examples/GUI/Python/StreamlinesWithLineWidget.py.
This program encompasses the functionality of
  StreamlinesWithLineWidget.tcl and LineWidget.tcl.
"""

import vtk


def main():
    colors = vtk.vtkNamedColors()
    fileName1 = 'combxyz.bin'
    fileName2 = 'combq.bin'

    # Start by loading some data.
    pl3d = vtk.vtkMultiBlockPLOT3DReader()
    pl3d.SetXYZFileName(fileName1)
    pl3d.SetQFileName(fileName2)
    pl3d.SetScalarFunctionNumber(100)  # Density
    pl3d.SetVectorFunctionNumber(202)  # Momentum
    pl3d.Update()

    pl3d_output = pl3d.GetOutput().GetBlock(0)
    print pl3d_output

    # Create the Renderer, RenderWindow and RenderWindowInteractor.
    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    # Needed by: vtkStreamTracer and vtkLineWidget.
    seeds = vtk.vtkPolyData()
    streamline = vtk.vtkActor()

    # The line widget is used seed the streamlines.
    # lineWidget = vtk.vtkLineWidget()
    lineWidget = vtk.vtkSphereWidget()
    lineWidget.SetInputData(pl3d_output)
    lineWidget.GetPolyData(seeds)

    lineWidget.SetRepresentationToSurface()
    lineWidget.PlaceWidget()
    # Associate the line widget with the interactor and setup callbacks.
    lineWidget.SetInteractor(iren)
    lineWidget.AddObserver("StartInteractionEvent", EnableActorCallback(streamline))
    lineWidget.AddObserver("InteractionEvent", GenerateStreamlinesCallback(seeds, renWin))

    # Here we set up two streamlines.
    # rk4 = vtk.vtkRungeKutta4()
    streamer = vtk.vtkStreamTracer()
    streamer.SetInputData(pl3d_output)
    streamer.SetSourceData(seeds)
    streamer.SetMaximumPropagation(100)
    streamer.SetInitialIntegrationStep(0.2)
    streamer.SetIntegrationDirectionToForward()
    streamer.SetComputeVorticity(1)
    # streamer.SetIntegrator(rk4)
    rf = vtk.vtkRibbonFilter()
    rf.SetInputConnection(streamer.GetOutputPort())
    rf.SetWidth(0.1)
    rf.SetWidthFactor(5)
    streamMapper = vtk.vtkPolyDataMapper()
    streamMapper.SetInputConnection(rf.GetOutputPort())
    streamMapper.SetScalarRange(pl3d_output.GetScalarRange())
    streamline.SetMapper(streamMapper)
    streamline.VisibilityOff()

    # Get an outline of the data set for context.
    outline = vtk.vtkStructuredGridOutlineFilter()
    outline.SetInputData(pl3d_output)
    outlineMapper = vtk.vtkPolyDataMapper()
    outlineMapper.SetInputConnection(outline.GetOutputPort())
    outlineActor = vtk.vtkActor()
    outlineActor.GetProperty().SetColor(colors.GetColor3d("Black"))
    outlineActor.SetMapper(outlineMapper)

    # Add the actors to the renderer, set the background and size.
    ren.AddActor(outlineActor)
    ren.AddActor(streamline)
    renWin.SetSize(512, 512)

    cam = ren.GetActiveCamera()
    lineWidget.EnabledOn()
    streamline.VisibilityOn()
    lineWidget.GetPolyData(seeds)
    renWin.Render()

    cam.SetClippingRange(14.216207, 68.382915)
    cam.SetFocalPoint(9.718210, 0.458166, 29.399900)
    cam.SetPosition(-15.827551, -16.997463, 54.003120)
    cam.SetViewUp(0.616076, 0.179428, 0.766979)
    ren.SetBackground(colors.GetColor3d("Silver"))

    iren.Initialize()
    renWin.Render()
    iren.Start()


class EnableActorCallback(object):
    def __init__(self, actor):
        self.actor = actor

    def __call__(self, caller, ev):
        self.actor.VisibilityOn()


class GenerateStreamlinesCallback(object):
    def __init__(self, polyData, renWin):
        self.polyData = polyData
        self.renWin = renWin

    def __call__(self, caller, ev):
        caller.GetPolyData(self.polyData)
        self.renWin.Render()


if __name__ == '__main__':
    main()
