#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import nibabel as nib

from pyfat.core.dataobject import Fasciculus
import nibabel.streamlines.array_sequence as nibas
from pyfat.algorithm.fiber_selection import select_by_vol_roi


subjects_dir = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects'

subject_id = [100408, 101410]

temp_path = 'Diffusion/tractography/Det'

file_name = 'SD_Stream_angle20_cutoff0.03_length50_250_seedFP_100k.tck'

roi_name = ['ROI/L_Occipital.nii.gz', 'ROI/R_Occipital.nii.gz']

out_file_name = ['SD_Stream_angle20_cutoff0.03_length50_250_seedFP_roiOccipital_L_100k.tck',
                 'SD_Stream_angle20_cutoff0.03_length50_250_seedFP_roiOccipital_R_100k.tck']


for i in xrange(len(subject_id)):
    print subject_id[i]
    file_path = os.path.join(subjects_dir, str(subject_id[i]), temp_path, file_name)
    for j in xrange(len(roi_name)):
        fas = Fasciculus(file_path)
        roi_path = os.path.join(subjects_dir, str(subject_id[i]), roi_name[j])
        out_path = os.path.join(subjects_dir, str(subject_id[i]), temp_path, out_file_name[j])
        roi_img = nib.load(roi_path)
        streamlines = select_by_vol_roi(fas.get_data(), roi_img.get_data(), roi_img.affine)
        fas.set_data(nibas.ArraySequence(streamlines))
        fas.save2tck(out_path)
