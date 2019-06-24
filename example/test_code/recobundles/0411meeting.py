# !/usr/bin/python
# -*- coding: utf-8 -*-

import nibabel as nib
from pyfat.core.dataobject import Fasciculus
from pyfat.algorithm.fiber_maths import create_registration_paths
from pyfat.viz.fiber_simple_viz_advanced import fiber_simple_3d_show_advanced

prepath = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/'
pos_outpath = 'Diffusion/SD/1M_20_01_20dynamic250_SD_Stream.tck'

paths_file = create_registration_paths(prepath, pos_outpath)

img_path = '/Structure/T1w_acpc_dc_restore_brain1.25.nii.gz'

for pf in paths_file:
    # load fib
    fa = Fasciculus(pf)
    streamlines = fa.get_data()

    sb_id = int(pf.split('/')[9])
    print sb_id
    # fiber_simple_3d_show_advanced(img, streamlines, colormap_full, imgcolor=True)

    img_path_qs = prepath + '%s' % sb_id + img_path
    img = nib.load(img_path_qs)
    fiber_simple_3d_show_advanced(img, streamlines)
