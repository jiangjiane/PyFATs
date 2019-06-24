#!/usr/bin/env python
# -*- coding: utf-8 -*-

import vtk
import numpy as np
import nibabel as nib
from scipy.spatial.distance import cdist

from dipy.viz import actor, window, ui
from dipy.tracking.streamline import set_number_of_points

from pyfat.viz.custom_interactor import MouseInteractorStylePP
from pyfat.algorithm.fiber_selection import select_by_vol_roi
from pyfat.viz.fiber_interactor_viz import *


# fib_file = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
#            'response_dhollander/100206/Diffusion/SD/1M_20_01_20dynamic250_SD_Stream_occipital5.tck'
# fib_file = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
#            'response_dhollander/100206/Diffusion/SD/100206_FP.tck'
vol_file = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/100408/Structure/T1w_acpc_dc_restore_brain1.25.nii.gz'
roi_file = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/100408/ROI/100408_L_Occipital.nii.gz'
roi_file1 = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
            'response_dhollander/100408/ROI/100408_R_Occipital.nii.gz'
roi_vis = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
          'response_dhollander/100408/Structure/Native_cytoMPM_thr25_vis.nii.gz'
fib_file = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/100408/result/result20vs45/cc_20fib_lr1.5_new_SD_Stream_hierarchical_single_cc.tck'

fib = nib.streamlines.tck.TckFile.load(fib_file)
streamlines = fib.streamlines

print len(streamlines)
# # create a rendering renderer
# ren = window.Renderer()
# stream_actor = actor.line(streamlines)

roi_img = nib.load(roi_file)
roi1_img = nib.load(roi_file1)
####################################################
roi_vis = nib.load(roi_vis)

roi, roi_affine = set_viz_roi(roi_img, mask=True)
roi1, roi1_affine = set_viz_roi(roi1_img, mask=True)
roi_actor = create_roi_actor(roi, roi_affine)
roi1_actor = create_roi_actor(roi1, roi1_affine)

roi_viz, roi_viz_affine = set_viz_roi(roi_vis)
roi_viz_actor = create_roi_actor(roi_viz, roi_viz_affine)

streamlines = select_by_vol_roi(streamlines, roi[0], roi_img.affine)
print len(streamlines)
# create a rendering renderer
ren = window.Renderer()
stream_actor = actor.line(streamlines)
vol = nib.load(vol_file)

image_actor_x, image_actor_y, image_actor_z = create_image_actor(vol)
# assign actor to the renderer
ren.add(stream_actor)

#########################################
for act in roi_actor:
    ren.add(act)
for act1 in roi1_actor:
    ren.add(act1)
for act_viz in roi_viz_actor:
    ren.add(act_viz)
#########################################
ren.add(image_actor_z)
ren.add(image_actor_x)
ren.add(image_actor_y)
show_m = window.ShowManager(ren, size=(1200, 900), interactor_style=MouseInteractorStylePP(ren, roi_viz_actor))
show_m.initialize()

line_slider_x, line_slider_y, line_slider_z, opacity_slider = line_slider(vol.shape)
shape = vol.shape

line_slider_z.add_callback(line_slider_z.slider_disk,
                           "MouseMoveEvent",
                           change_slice_z)
line_slider_x.add_callback(line_slider_x.slider_disk,
                           "MouseMoveEvent",
                           change_slice_x)
line_slider_y.add_callback(line_slider_y.slider_disk,
                           "MouseMoveEvent",
                           change_slice_y)
opacity_slider.add_callback(opacity_slider.slider_disk,
                            "MouseMoveEvent",
                            change_opacity)

"""
We'll also create text labels to identify the sliders.
"""

line_slider_label_z = build_label(text="Z Slice")
line_slider_label_x = build_label(text="X Slice")
line_slider_label_y = build_label(text="Y Slice")
opacity_slider_label = build_label(text="Opacity")

panel = create_panel(line_slider_x, line_slider_label_x, line_slider_y, line_slider_label_y,
                     line_slider_z, line_slider_label_z, opacity_slider, opacity_slider_label)
show_m.ren.add(panel)
size = ren.GetSize()
global size

# enable user interface interactor
iren = show_m.iren
renWin = show_m.window
renWin.AddRenderer(ren)

sphereWidget = create_sphereWidget()
sphereWidget.SetInteractor(iren)
# Connect the event to a function
sphereWidget.AddObserver("InteractionEvent", computeFibCallback)
######################################

show_m.initialize()
ren.zoom(1.5)
ren.reset_clipping_range()
show_m.add_window_callback(win_callback)
show_m.render()
show_m.start()
