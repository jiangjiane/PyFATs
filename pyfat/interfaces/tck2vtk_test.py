# !/usr/bin/python
# -*- coding=utf-8 -*-

import nipype.interfaces.mrtrix3 as mrt


def tck2vtk(in_file, reference, out_file):
    vtk = mrt.TCK2VTK()
    vtk.inputs.in_file = in_file
    vtk.inputs.reference = reference
    vtk.inputs.out_file = out_file
    vtk.run()


if __name__ == '__main__':
    in_file = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
              'response_dhollander/100408/Diffusion/SD/1M_20_01_20dynamic250_SD_Stream_lhemi_occipital5_vis_interface.tck'
    reference = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
                'response_dhollander/100408/Diffusion/data/meanb0.mif'
    out_file = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
               'response_dhollander/100408/Diffusion/SD/1M_20_01_20dynamic250_SD_Stream_lhemi_occipital5_vis_interface.vtk'
    tck2vtk(in_file, reference, out_file)
