# !/usr/bin/python
# -*- coding: utf-8 -*-

import os
import numpy as np
import nibabel as nib
from dipy.tracking.utils import length
import nibabel.streamlines.tck as nibas
from pyfat.core.dataobject import Fasciculus
from dipy.segment.quickbundles import QuickBundles
from dipy.segment.quickbundles import bundles_distances_mdf
from pyfat.algorithm.fiber_maths import create_registration_paths, bundle_registration, muti_bundle_registration
from pyfat.viz.fiber_simple_viz_advanced import fiber_simple_3d_show_advanced

prepath = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects_all/aligned_centroids/'

paths_file = os.listdir(prepath)

all_MD = {}
for i in range(len(paths_file)):
    MD = []
    fa = Fasciculus(os.path.join(prepath, paths_file[i]))
    fasciculus_id = fa.get_header()['fasciculus_id']
    for fas_id in set(fasciculus_id):
        if fas_id is not fasciculus_id[0]:
            md = bundles_distances_mdf(fa.get_data()[np.array(fasciculus_id) == fasciculus_id[0]],
                                       fa.get_data()[np.array(fasciculus_id) == fas_id])
            MD.append(md.mean())

    all_MD[fasciculus_id[0]] = MD

print all_MD.keys()
print all_MD.values()
print np.array(all_MD.values()).mean(axis=1)
print np.array(all_MD.values()).std(axis=1)

print np.array(all_MD.keys())[np.argmin(np.array(all_MD.values()).mean(axis=1))]
print np.array(all_MD.keys())[np.argmin(np.array(all_MD.values()).std(axis=1))]
