# !/usr/bin/python
# -*- coding: utf-8 -*-

import os
import nibabel as nib
import numpy as np

from pyfat.core.dataobject import Fasciculus
from pyfat.io.save import save_nifti
from pyfat.algorithm.fasc_mapping import fib_density_map

subjects_dir = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects'
subjects_id = '/home/brain/workingdir/pyfat/bin/pipeline_file/subjects_qyk'
tck_name = ['lvis1.tck', 'lvis2.tck', 'lvis3.tck', 'lvis4.tck',
            'rvis1.tck', 'rvis2.tck', 'rvis3.tck', 'rvis4.tck']

results_dir = 'Diffusion/tractography/Det/new_results'

with open(subjects_id, 'r') as f:
    sessid = f.readlines()
    sessid = [_.strip() for _ in sessid]

# sessid = ['101309']
# sessid = ['101915']


counts = []
for tck in tck_name:
    print tck
    count = []
    for subject in sessid:
        fib_path = os.path.join(subjects_dir, subject, results_dir, tck)
        if not os.path.exists(fib_path):
            continue
        fas = Fasciculus(fib_path)
        count.append(fas.get_counts())
    counts.append(np.mean(count))

print counts

