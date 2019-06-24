# !/usr/bin/python
# -*- coding: utf-8 -*-

import os
import numpy as np
import nibabel as nib

from pyfat.io.save import save_nifti


prepath = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects/'
terminus_fa_path = 'Diffusion/tractography/Det/results'
# terminus_fa_name = ['lvis1_terminus_fa.nii.gz', 'lvis2_terminus_fa.nii.gz',
#                     'lvis3_terminus_fa.nii.gz', 'lvis4_terminus_fa.nii.gz']
terminus_fa_name = ['rvis1_terminus_fa.nii.gz', 'rvis2_terminus_fa.nii.gz',
                    'rvis3_terminus_fa.nii.gz', 'rvis4_terminus_fa.nii.gz']

vol_name = 'T1w_acpc_dc_restore_brain1.25.nii.gz'


subjects_id = '/home/brain/workingdir/pyfat/bin/pipeline_file/subjects_ids'

with open(subjects_id, 'r') as f:
    sessid = f.readlines()
    sessid = [_.strip() for _ in sessid]

for sb_id in sessid:
    print sb_id
    img = nib.load(os.path.join(prepath, sb_id, vol_name))
    img_new = np.zeros((img.shape[0], img.shape[1], img.shape[2], 4))
    for i in range(len(terminus_fa_name)):
        fa_name = os.path.join(prepath, str(sb_id), terminus_fa_path, terminus_fa_name[i])
        if not os.path.exists(fa_name):
            continue
        img_new[:, :, :, i] = nib.load(fa_name).get_data()

    out_path = os.path.join(prepath, sb_id, terminus_fa_path, 'rvis_terminus_fa.nii.gz')
    save_nifti(img_new, img.affine, out_path)
