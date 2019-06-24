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
subjects_id = '/home/brain/workingdir/pyfat/bin/pipeline_file/subjects_id'
# tck_name = ['Diffusion/tractography/Det/results/l_vis4.tck',
#             'Diffusion/tractography/Det/results/r_vis4.tck']
tck_name = [['lvis1.tck', 'lvis2.tck', 'lvis3.tck', 'lvis4.tck'], ['rvis1.tck', 'rvis2.tck', 'rvis3.tck', 'rvis4.tck']]

vol_name = 'T1w_acpc_dc_restore_brain1.25.nii.gz'

results_dir = 'Diffusion/tractography/Det/new_results'

with open(subjects_id, 'r') as f:
    sessid = f.readlines()
    sessid = [_.strip() for _ in sessid]


for subject in sessid:
    print subject
    img = nib.load(os.path.join(subjects_dir, subject, vol_name))

    for tcks in tck_name:
        img_zero = np.zeros((img.shape[0], img.shape[1], img.shape[2], 4))
        hemi = tcks[0][0]

        for tck in tcks:
            index = int(tck[4])
            fib_path = os.path.join(subjects_dir, subject, results_dir, tck)
            if not os.path.exists(fib_path):
                continue
            fas = Fasciculus(fib_path)
            fib = fas.get_data()
            arr = []
            for fs in fib:
                arr.append(fs[0])
                arr.append(fs[-1])
            arr = np.array(arr)
            # arr = np.array([s[0] for s in fib] + [s[-1] for s in fib])
            stream_terminus = apply_affine(npl.inv(img.affine), arr)
            counts = np.zeros(img.shape)
            for st in stream_terminus:
                counts[int(st[0]), int(st[1]), int(st[2])] += 1
            img_zero[:, :, :, index - 1] = counts
            # vol = fib_density_map(img, fib)
            # img_zero[:, :, :, index-1] = vol
        out_path = os.path.join(subjects_dir, subject, results_dir,
                                '{hemi}_terminus.nii.gz'.format(hemi=hemi[0]))
        save_nifti(img_zero, img.affine, out_path)

