# !/usr/bin/python
# -*- coding: utf-8 -*-

import os
import numpy as np
import nibabel as nib
import numpy.linalg as npl
from nibabel.affines import apply_affine

from pyfat.io.save import save_nifti
from pyfat.core.dataobject import Fasciculus


prepath = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects/'
tck_path = 'Diffusion/tractography/Det/results'
tck_name = ['lvis1.tck', 'lvis2.tck', 'lvis22.tck', 'lvis3.tck', 'lvis33.tck',
            'lvis4.tck', 'rvis1.tck', 'rvis2.tck', 'rvis3.tck', 'rvis4.tck']

vol_name = 'T1w_acpc_dc_restore_brain1.25.nii.gz'


subjects_id = '/home/brain/workingdir/pyfat/bin/pipeline_file/subjects_ids'

with open(subjects_id, 'r') as f:
    sessid = f.readlines()
    sessid = [_.strip() for _ in sessid]

for sb_id in sessid:
    print sb_id
    img = nib.load(os.path.join(prepath, sb_id, vol_name))
    for tck in tck_name:
        tck_file = os.path.join(prepath, str(sb_id), tck_path, tck)

        if os.path.exists(tck_file):
            name, _ = tck.split('.')
            tck_fa_file = os.path.join(prepath, str(sb_id), tck_path, name + '_fa.txt')
            fas = Fasciculus(tck_file)
            fibs = fas.get_data()
            with open(tck_fa_file, 'r') as fa_txts:
                lines = fa_txts.readlines()
            fa_lines = [list(map(float, lines[i].split())) for i in range(len(lines))]

            img_new = np.zeros(img.shape)
            for j in range(len(fibs)):
                arr = []
                arr.append(fibs[j][0])
                arr.append(fibs[j][-1])
                arr = np.array(arr)
                terminus = apply_affine(npl.inv(img.affine), arr)
                orignal_val0 = img_new[int(terminus[0][0]), int(terminus[0][1]), int(terminus[0][2])]
                img_new[int(terminus[0][0]), int(terminus[0][1]), int(terminus[0][2])] = \
                    np.mean([np.mean(fa_lines[j]), orignal_val0]) if orignal_val0 != 0.0 else np.mean(fa_lines[j])
                orignal_val1 = img_new[int(terminus[1][0]), int(terminus[1][1]), int(terminus[1][2])]
                img_new[int(terminus[1][0]), int(terminus[1][1]), int(terminus[1][2])] = \
                    np.mean([np.mean(fa_lines[j]), orignal_val1]) if orignal_val1 != 0.0 else np.mean(fa_lines[j])

            out_path = os.path.join(prepath, sb_id, tck_path, name + '_terminus_fa.nii.gz')
            save_nifti(img_new, img.affine, out_path)
