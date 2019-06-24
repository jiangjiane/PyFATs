# !/usr/bin/python
# -*- coding: utf-8 -*-


import os
import subprocess


subjects_id = '/home/brain/workingdir/pyfat/bin/pipeline_file/subjects_id'

with open(subjects_id, 'r') as f:
    sessid = f.readlines()
    sessid = [_.strip() for _ in sessid]

for s in sessid:
    subprocess.call('cp /home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subject/{subject}/Diffusion/tractography/Det/SD_Stream_angle20_cutoff0.03_length50_250_seedFP_roiOccipital_L_100k_rh.tck /media/brain/jiangjian/QUYUKUN/{subject}'.format(subject=s), shell=True)
    subprocess.call('cp /home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects/{subject}/Diffusion/tractography/Det/SD_Stream_angle20_cutoff0.03_length50_250_seedFP_roiOccipital_R_100k_lh.tck /media/brain/jiangjian/QUYUKUN/{subject}'.format(subject=s), shell=True)




