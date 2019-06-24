# !/usr/bin/python
# -*- coding: utf-8 -*-

import os
import numpy as np
import subprocess as sp
import nibabel as nib
print nib.__version__
from dipy.segment.quickbundles import QuickBundles
import nibabel.streamlines.array_sequence as nibas


from pyfat.core.dataobject import Fasciculus


subjects_dir = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects'
subjects_id = '/home/brain/workingdir/pyfat/bin/pipeline_file/subjects_id'

temp_path = 'Diffusion/tractography/Det/new_results'
target = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects/results_bc'

tck_name = ['left_vis_all.tck', 'right_vis_all.tck']

with open(subjects_id, 'r') as f:
    sessid = f.readlines()
    sessid = [_.strip() for _ in sessid]

for sub in sessid:
    tck1 = os.path.join(subjects_dir, sub, temp_path, tck_name[0])
    tck2 = os.path.join(subjects_dir, sub, temp_path, tck_name[1])
    result_dir = os.path.join(target, sub)
    os.makedirs(result_dir)
    cmd1 = "cp {tck1} {result_dir}"
    cmd2 = "cp {tck2} {result_dir}"
    sp.call(cmd1.format(tck1=tck1, result_dir=result_dir), shell=True)
    sp.call(cmd2.format(tck2=tck2, result_dir=result_dir), shell=True)

