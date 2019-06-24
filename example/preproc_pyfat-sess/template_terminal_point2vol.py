# !/usr/bin/python
# -*- coding: utf-8 -*-

import os
import nibabel as nib
import numpy as np
import numpy.linalg as npl
from nibabel.affines import apply_affine

from pyfat.core.dataobject import Fasciculus
from pyfat.io.save import save_nifti
from pyfat.algorithm.fasc_mapping import fib_density_map

subjects_dir = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects'
subjects_id = '/home/brain/workingdir/pyfat/bin/pipeline_file/temp_sub_id'
tck_name = [['lvis1_template_centroids.tck', 'lvis2_template_centroids.tck',
             'lvis3_template_centroids.tck', 'lvis4_template_centroids.tck'],
            ['rvis1_template_centroids.tck', 'rvis2_template_centroids.tck',
             'rvis3_template_centroids.tck', 'rvis4_template_centroids.tck']]

vol_name = 'T1w_acpc_dc_restore_brain1.25.nii.gz'

results_dir = 'Diffusion/tractography/Det/new_results'

with open(subjects_id, 'r') as f:
    sessid = f.readlines()
    sessid = [_.strip() for _ in sessid]


for i in range(len(sessid)):
    print sessid[i]
    img = nib.load(os.path.join(subjects_dir, sessid[i], vol_name))

    tcks = tck_name[i]

    for tck in tcks:
        fib_path = os.path.join(subjects_dir, sessid[i], results_dir, tck)
        if not os.path.exists(fib_path):
                continue
        fas = Fasciculus(fib_path)
        fib = fas.get_data()
        arr = []
        for fs in fib:
            if fs[0][1] < fs[-1][1]:
                arr.append(fs[0])
            else:
                arr.append(fs[-1])
        arr = np.array(arr)
        # arr = np.array([s[0] for s in fib] + [s[-1] for s in fib])
        stream_terminus = apply_affine(npl.inv(img.affine), arr)
        img_zero = np.zeros(img.shape)
        for st in stream_terminus:
            img_zero[int(st[0]), int(st[1]), int(st[2])] += 1
        out_path = os.path.join(subjects_dir, sessid[i], results_dir,
                                '{hemi}_terminus.nii.gz'.format(hemi=tck.split('.')[0]))
        save_nifti(img_zero, img.affine, out_path)

