import subprocess

def antsRegistration(fixed_image,moving_image,output_name):
    #  fixed image to which we register the moving image,absolute path,type:string;
    #  moving image to be mapped to fixed space,absolute path,type:string;
    #  subject_num,type:string
    # first,we try to acquire the affine matrix and Warp.
    # all files need to be placed in same directory.
    subprocess.call('antsRegistrationSyNQuick.sh -d 3 -f {} -m {} -o {}'.format(fixed_image,moving_image,output_name),
                    shell = True)
    print('Affine and Warp files acquired')


def antsApplyTransforms_e0(fixed_image,moving_image,affine,warp,outputname):
    # second,we apply transforms to more moving images to subject native space.
    subprocess.call('antsApplyTransforms -d 3 -e 0 -i {} -r {} -t {} -t {} -o {}'.format(moving_image,
                    fixed_image,affine,warp,outputname),shell = True)


def antsApplyTransforms_e3(fixed_image,moving_image,affine,warp,outputname):
    # second,we apply transforms to more moving images to subject native space.
    # t1 = '0GenericAffine.mat'
    # t2 = '1Warp.nii.gz'
    subprocess.call('antsApplyTransforms -d 3 -e 3 -i {} -r {} -t {} -t {} -o {}'.format(moving_image,
                    fixed_image,affine,warp,outputname),shell = True)

#Apply transform for tract_prob from standard space to native space.
fixed_image = '/nfs/s2/userhome/quyukun/workingdir/fiberdata/subjects/100206/T1w/T1w_acpc_dc_restore_brain1.25.nii.gz'
moving_image = '/nfs/s2/userhome/quyukun/workingdir/fiberdata/prob_atlas/JHU-ICBM-tracts-prob-2mm.nii.gz'
t1 = '/nfs/s2/userhome/quyukun/workingdir/fiberdata/subjects/100206/regis_ROI/transfrom/1002060GenericAffine.mat'
t2 = '/nfs/s2/userhome/quyukun/workingdir/fiberdata/subjects/100206/regis_ROI/transfrom/1002061Warp.nii.gz'
outputname = '/nfs/s2/userhome/quyukun/workingdir/fiberdata/subjects/100206/prob_atlas/100206_JHU_tract_prob.nii.gz'

antsApplyTransforms_e3(fixed_image,moving_image,t1,t2,outputname)
