#!/usr/bin/env python

# import os
# os.chdir("VTKData/Data")

import vtk

file_name = '/home/brain/workingdir/pyfat/example/test_code/data/1M_20_01_20dynamic250_SD_Stream_occipital5.vtk'

pl3d = vtk.vtkPolyDataReader()
pl3d.SetFileName(file_name)
# pl3d.Update()

# pl3d = vtk.vtkMultiBlockPLOT3DReader()

# xyx_file = "combxyz.bin"
# q_file = "combq.bin"
# pl3d.SetXYZFileName(xyx_file)
# pl3d.SetQFileName(q_file)
# pl3d.SetScalarFunctionNumber(100)
# pl3d.SetVectorFunctionNumber(202)
pl3d.Update()

seeds = vtk.vtkPlaneSource()
seeds.SetXResolution(4)
seeds.SetYResolution(4)
seeds.SetOrigin(2, -2, 26)
seeds.SetPoint1(2, 2, 26)
seeds.SetPoint2(2, -2, 32)

streamline = vtk.vtkStreamTracer()
streamline.SetInputData(pl3d.GetOutput())
streamline.SetSourceConnection(seeds.GetOutputPort())
streamline.SetMaximumPropagation(200)
streamline.SetInitialIntegrationStep(.2)
streamline.SetIntegrationDirectionToForward()
streamline.SetComputeVorticity(1)

streamline_mapper = vtk.vtkPolyDataMapper()
streamline_mapper.SetInputConnection(streamline.GetOutputPort())
streamline_actor = vtk.vtkActor()
streamline_actor.SetMapper(streamline_mapper)
streamline_actor.VisibilityOn()

outline = vtk.vtkStructuredGridOutlineFilter()
outline.SetInputData(pl3d.GetOutput())
outline_mapper = vtk.vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())
outline_actor = vtk.vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(1, 1, 1)

renderer = vtk.vtkRenderer()
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
render_window.SetInteractor(interactor)

renderer.AddActor(streamline_actor)
# renderer.AddActor(outline_actor)

renderer.SetBackground(0.1, 0.2, 0.4)
interactor.Initialize()
render_window.Render()
interactor.Start()
