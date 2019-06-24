#!/usr/bin/env python
# -*- coding: utf-8 -*-

import vtk
import numpy as np
import nibabel as nib
from dipy.viz import actor, window, ui

fib_file = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/100206/Diffusion/SD/1M_20_01_20dynamic250_SD_Stream_occipital5.tck'

fib = nib.streamlines.tck.TckFile.load(fib_file)
streamlines = fib.streamlines

# create a rendering renderer
ren = window.Renderer()
stream_actor = actor.line(streamlines[:100])
# add streamlines
ren.add(stream_actor)

# print streamlines[:2]
##########################################################
show_m = window.ShowManager(ren, size=(1200, 900))
# Call back function
def sphereCallback(obj, event):
    print('Center: {}, {}, {}'.format(*obj.GetCenter()))
renwin = show_m.window
renwin.AddRenderer(ren)

# An interactor
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(renwin)
# A Sphere widget
sphereWidget = vtk.vtkSphereWidget()
sphereWidget.SetCenter(3.98, -30.94, 9.16)
sphereWidget.SetRadius(5)
sphereWidget.SetInteractor(interactor)
sphereWidget.SetRepresentationToSurface()
sphereWidget.On()


# Connect the event to a function
# sphereWidget.AddObserver("InteractionEvent", sphereCallback)

# enable user interface interactor
show_m.initialize()
ren.zoom(1.5)
ren.reset_clipping_range()
show_m.render()
show_m.start()
