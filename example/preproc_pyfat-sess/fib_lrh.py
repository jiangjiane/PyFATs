#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import vtk
import numpy as np
from dipy.tracking.utils import length
import nibabel as nib
from scipy.spatial.distance import cdist
from dipy.viz import actor, window, ui
from dipy.data import read_viz_icons, fetch_viz_icons
from dipy.tracking.fbcmeasures import FBCMeasures
from dipy.tracking.streamline import set_number_of_points
import nibabel.streamlines.array_sequence as nibas
from dipy.denoise.enhancement_kernel import EnhancementKernel

from pyfat.viz.custom_interactor import MouseInteractorStylePP
from pyfat.algorithm.fiber_selection import select_by_vol_roi
from pyfat.io.save import save_tck
from pyfat.core.dataobject import Fasciculus

subjects_dir = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects'
subjects_id = '/home/brain/workingdir/pyfat/bin/pipeline_file/subjects_id'
tck_name = ['l.tck', 'r.tck']
# tck_name = ['test.tck']


vol_name = 'T1w_acpc_dc_restore_brain1.25.nii.gz'

results_dir = 'Diffusion/tractography/Det/new_results'


with open(subjects_id, 'r') as f:
    sessid = f.readlines()
    sessid = [_.strip() for _ in sessid]

for sub in sessid:
    print sub
    fib_lh = nibas.ArraySequence()
    fib_rh = nibas.ArraySequence()
    fib_l = Fasciculus(os.path.join(subjects_dir, sub, results_dir, tck_name[0]))
    fib_l_data = fib_l.get_data()
    fib_l_len = fib_l.get_lengths()
    fib_r = Fasciculus(os.path.join(subjects_dir, sub, results_dir, tck_name[1]))
    fib_r_data = fib_r.get_data()
    fib_r_len = fib_r.get_lengths()
    for i in range(len(fib_l_data)):
        fib = fib_l_data[i]
        fib = set_number_of_points(fib, int(2*fib_l_len[i]))
        l = fib[:, 0]
        l_ahead = list(l[:])
        a = l_ahead.pop(0)
        l_ahead.append(a)
        x_stemp = np.array([l, l_ahead])
        x_stemp_index = x_stemp.prod(axis=0)
        index0 = [v[0] for v in np.argwhere(x_stemp_index <= 0)]
        if len(index0) == 0:
            continue

        index = float('-Inf')
        y_v = float('-Inf')
        for ind in index0:
            if ind != len(fib)-1 and fib[ind][1] > y_v:
                y_v = fib[ind][1]
                index = ind
        offset = np.argmin([fib[index][0], fib[index - 1][0]])
        index -= offset

        if fib[:index, 0].sum() <= fib[index:, 0].sum():
            fib_lh.append(fib[:index])
        else:
            fib_lh.append(fib[index:])
    fib_l.set_data(fib_lh)
    fib_l.save2tck(os.path.join(subjects_dir, sub, results_dir, 'lh.tck'))

    for i in range(len(fib_r_data)):
        fib = fib_r_data[i]
        fib = set_number_of_points(fib, int(2*fib_r_len[i]))
        l = fib[:, 0]
        l_ahead = list(l[:])
        a = l_ahead.pop(0)
        l_ahead.append(a)
        x_stemp = np.array([l, l_ahead])
        x_stemp_index = x_stemp.prod(axis=0)
        index0 = [v[0] for v in np.argwhere(x_stemp_index <= 0)]
        if len(index0) == 0:
            continue

        index = float('-Inf')
        y_v = float('-Inf')
        for ind in index0:
            if ind != len(fib)-1 and fib[ind][1] > y_v:
                y_v = fib[ind][1]
                index = ind
        offset = np.argmin([fib[index][0], fib[index-1][0]])
        index -= offset

        if fib[:index, 0].sum() >= fib[index:, 0].sum():
            fib_rh.append(fib[:index])
        else:
            fib_rh.append(fib[index:])
    fib_r.set_data(fib_rh)
    fib_r.save2tck(os.path.join(subjects_dir, sub, results_dir, 'rh.tck'))



