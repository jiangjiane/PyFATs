#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import vtk
import numpy as np
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
l_tck_name = ['l1.tck', 'l2.tck', 'l3.tck']
r_tck_name = ['r1.tck', 'r2.tck', 'r3.tck']


vol_name = 'T1w_acpc_dc_restore_brain1.25.nii.gz'

results_dir = 'Diffusion/tractography/Det/new_results'


with open(subjects_id, 'r') as f:
    sessid = f.readlines()
    sessid = [_.strip() for _ in sessid]

for sub in sessid:
    print sub
    fib_lh = nibas.ArraySequence()
    fib_rh = nibas.ArraySequence()
    file_dir = os.path.join(subjects_dir, sub, results_dir)
    tcks = sorted(os.listdir(file_dir))
    for tck in tcks:
        if tck in l_tck_name:
            fib_l = Fasciculus(os.path.join(subjects_dir, sub, results_dir, tck))
            fib_lh.extend(fib_l.get_data())
        elif tck in r_tck_name:
            fib_r = Fasciculus(os.path.join(subjects_dir, sub, results_dir, tck))
            fib_rh.extend(fib_r.get_data())
        else:
            pass
    fib_l.set_data(fib_lh)
    fib_r.set_data(fib_rh)
    fib_l.save2tck(os.path.join(subjects_dir, sub, results_dir, 'l.tck'))
    fib_r.save2tck(os.path.join(subjects_dir, sub, results_dir, 'r.tck'))

