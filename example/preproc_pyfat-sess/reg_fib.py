# !/usr/bin/python
# -*- coding: utf-8 -*-

import os
import nibabel as nib
import numpy as np

from pyfat.core.dataobject import Fasciculus
from dipy.segment.quickbundles import QuickBundles
import nibabel.streamlines.array_sequence as nibas
from pyfat.io.save import save_nifti
from pyfat.algorithm.fiber_maths import bundle_registration
# subjects_dir = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects'
subjects_dir = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects_testretest'

subjects_id = '/home/brain/workingdir/pyfat/bin/pipeline_file/subjects_qyk'
tck_name = ['lvis1.tck', 'lvis2.tck', 'lvis3.tck', 'lvis4.tck',
            'rvis1.tck', 'rvis2.tck', 'rvis3.tck', 'rvis4.tck']

# vol_name = 'T1w_acpc_dc_restore_brain1.25.nii.gz'

# results_dir = 'Diffusion/tractography/Det/new_results'

with open(subjects_id, 'r') as f:
    sessid = f.readlines()
    sessid = [_.strip() for _ in sessid]


for tck in tck_name:
    print tck
    if tck[0] == 'l':
        template = '101309'
    elif tck[0] == 'r':
        template = '101915'
    else:
        raise ValueError("Error")
    fib_template_path = os.path.join(subjects_dir, template, 'new_results', tck)
    fas_template = Fasciculus(fib_template_path)
    fib_template = fas_template.get_data()
    fib_template_centroids = QuickBundles(fib_template, float('inf')).centroids
    fibs = nibas.ArraySequence()
    for subject in sessid:
        print subject
        fib_path = os.path.join(subjects_dir, subject, 'new_results', tck)
        if not os.path.exists(fib_path):
            continue
        fas = Fasciculus(fib_path)
        fib = fas.get_data()
        fib_centroids = QuickBundles(fib, float('inf')).centroids
        reg_fib = bundle_registration(fib_template_centroids, fib_centroids, 200)
                                      # max(len(fib_template_centroids[0]), len(fib_centroids[0])))
        fibs.append(reg_fib[0])
    fas_template.set_data(fibs)
    fas_template.save2tck(os.path.join(subjects_dir, template, 'new_results', tck.split('.')[0] + '_template_centroids.tck'))
