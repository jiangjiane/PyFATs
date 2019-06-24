#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nibabel as nib
from dipy.tracking.fbcmeasures import FBCMeasures
from dipy.denoise.enhancement_kernel import EnhancementKernel

from pyfat.io.save import save_tck

fib_file = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/100408/result/result20vs45/cc_20fib_lr1.5_new_SD_Stream_hierarchical_single_cc.tck'

fib = nib.streamlines.tck.TckFile.load(fib_file)
streamlines = fib.streamlines
print len(streamlines)
header = fib.header
data_per_streamline = fib.tractogram.data_per_streamline
data_per_point = fib.tractogram.data_per_point
affine_to_rasmm = fib.tractogram.affine_to_rasmm

# Compute lookup table
D33 = 1.0
D44 = 0.02
t = 1
k = EnhancementKernel(D33, D44, t)

# Apply FBC measures
fbc = FBCMeasures(streamlines, k)

# Calculate LFBC for original fibers
fbc_sl_orig, clrs_orig, rfbc_orig = fbc.get_points_rfbc_thresholded(0, emphasis=0.01)
print len(fbc_sl_orig)
out_path1 = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/100408/result/FBC/cc_fbc_sl_orig.tck'
# Apply a threshold on the RFBC to remove spurious fibers
fbc_sl_thres, clrs_thres, rfbc_thres = fbc.get_points_rfbc_thresholded(0.125, emphasis=0.01)
print len(fbc_sl_thres)
out_path2 = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/100408/result/FBC/cc_fbc_sl_thres.tck'

save_tck(fbc_sl_orig, header, data_per_streamline, data_per_point, affine_to_rasmm, out_path1)
save_tck(fbc_sl_thres, header, data_per_streamline, data_per_point, affine_to_rasmm, out_path2)

