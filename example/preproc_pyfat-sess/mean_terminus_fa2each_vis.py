# !/usr/bin/python
# -*- coding: utf-8 -*-

import os
import numpy as np
import nibabel as nib

from pyfat.io.save import save_nifti


prepath = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects/'
terminus_fa_name = ['mean_lvis_terminus_fa_MNI152.nii.gz', 'mean_rvis_terminus_fa_MNI152.nii.gz']

for fas_name in terminus_fa_name:
    fa_name = os.path.join(prepath, 'results', fas_name)
    img = nib.load(fa_name)
    print img.shape[3]
    for i in range(img.shape[3]):
        img_new = img.get_data()[:, :, :, i]
        out_path = os.path.join(prepath, 'results', str(i+1) + '_' + fas_name)
        save_nifti(img_new, img.affine, out_path)
