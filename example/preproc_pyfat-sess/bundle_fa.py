# !/usr/bin/python
# -*- coding: utf-8 -*-

import os
import subprocess as sp
from dipy.tracking.streamline import set_number_of_points
from pyfat.core.dataobject import Fasciculus


prepath = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects/'
tck_prepath = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects_testretest/'
tck_path = 'Diffusion/tractography/Det/new_results'
# tck_name = ['lvis1.tck', 'lvis2.tck', 'lvis3.tck', 'lvis4.tck',
#             'rvis1.tck', 'rvis2.tck', 'rvis3.tck', 'rvis4.tck']

tck_name = ['lvis1.tck', 'lvis2.tck', 'lvis3.tck', 'lvis4.tck',
            'rvis1.tck', 'rvis2.tck', 'rvis3.tck', 'rvis4.tck']

subjects_id = '/home/brain/workingdir/pyfat/bin/pipeline_file/subjects_qyk'

with open(subjects_id, 'r') as f:
    sessid = f.readlines()
    sessid = [_.strip() for _ in sessid]

for sb_id in sessid:
    print sb_id
    fa_file = os.path.join(prepath, str(sb_id), 'Diffusion/metrics/fa.nii.gz')
    for tck in tck_name:
        tck_file = os.path.join(tck_prepath, str(sb_id), 'new_results', tck)

        if os.path.exists(tck_file):
            # fas = Fasciculus(tck_file)
            # curvature = fas.get_mean_curvature()
            # orientation = fas.get_mean_orientation()
            # data = fas.get_data()
            # fib = set_number_of_points(data, 200)
            # fas.set_data(fib)
            # fas.save2tck(tck_file)

            name, _ = tck.split('.')
            tck_fa_file = os.path.join(tck_prepath, str(sb_id), 'new_results', name + '_fa.txt')
            cmd = "tcksample {tck_file} {fa_file} {tck_fa_file} -force"
            sp.call(cmd.format(tck_file=tck_file, fa_file=fa_file, tck_fa_file=tck_fa_file), shell=True)


# tck_img = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
#           'response_dhollander/subjects/200008/Diffusion/tractography/Det/results/lvis33.tck'
# fa_txt = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
#          'response_dhollander/subjects/200008/Diffusion/tractography/Det/results/test_lvis33_fa.txt'
#
# img = Fasciculus(tck_img)
# streams = img.get_data()
# print len(streams)
#
# fa_lines = []
# with open(fa_txt, 'r') as fa_txts:
#     lines = fa_txts.readlines()
# for i in range(len(lines)):
#     fa_lines.append(list(map(float, lines[i].split())))
# print len(fa_lines)
