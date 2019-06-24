# !/usr/bin/python
# -*- coding: utf-8 -*-

from pyfat.io.load import load_tck
from pyfat.io.save import save_tck

import re
import os


def is_number(num):
    pattern = re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$')
    result = pattern.match(num)

    return True if result else False


subjects_dir = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects_testretest/'
subjects_id = '/home/brain/workingdir/pyfat/bin/pipeline_file/subjects_qyk'
tck_template = ['left_vis_all.tck', 'right_vis_all.tck']

tck_name = [['lvis1.tck', 'lvis2.tck', 'lvis3.tck', 'lvis4.tck'],
            ['rvis1.tck', 'rvis2.tck', 'rvis3.tck', 'rvis4.tck']]


with open(subjects_id, 'r') as f:
    sessid = f.readlines()
    sessid = [_.strip() for _ in sessid]


for subject in sessid:
    out_path = os.path.join(subjects_dir, subject, 'new_results')
    os.makedirs(out_path)
    for i in range(len(tck_template)):
        tck_template_path = os.path.join(subjects_dir, subject, tck_template[i])
        img = load_tck(tck_template_path)
        header = img.header
        del header['fasciculus_id']
        for tck in tck_name[i]:
            tck_path = os.path.join(subjects_dir, subject, tck)
            if not os.path.exists(tck_path):
                continue
            img_t = load_tck(tck_path)
            save_tck(img_t.streamlines, header, img_t.tractogram.data_per_streamline,
                     img_t.tractogram.data_per_point, img_t.tractogram.affine_to_rasmm, os.path.join(out_path, tck))
