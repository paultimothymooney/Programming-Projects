
import os
os.chdir('/Users/ptm/desktop/Current_working_directory/DIPY/')


"""
=========================
Getting started with DIPY
=========================

In diffusion MRI (dMRI) usually we use three types of files, a Nifti file with the
diffusion weighted data, and two text files one with b-values and
one with the b-vectors.

In dipy_ we provide tools to load and process these files and we also provide
access to publically available datasets for those who haven't acquired yet
their own datasets.

With the following commands we can download a dMRI dataset
"""

from dipy.data import fetch_sherbrooke_3shell
fetch_sherbrooke_3shell()

"""
By default these datasets will go in the ``.dipy`` folder inside your home directory.
Here is how you can access them.
"""

from os.path import expanduser, join
home = expanduser('~')

"""
``dname`` holds the directory name where the 3 files are in.
"""

dname = join(home, '.dipy', 'sherbrooke_3shell')

"""
Here, we show the complete filenames of the 3 files
"""

fdwi = join(dname, 'HARDI193.nii.gz')

print(fdwi)

fbval = join(dname, 'HARDI193.bval')

print(fbval)

fbvec = join(dname, 'HARDI193.bvec')

print(fbvec)

"""
``/home/username/.dipy/sherbrooke_3shell/HARDI193.nii.gz``

``/home/username/.dipy/sherbrooke_3shell/HARDI193.bval``

``/home/username/.dipy/sherbrooke_3shell/HARDI193.bvec``

Now, that we have their filenames we can start checking what these look like.

Let's start first by loading the dMRI datasets. For this purpose, we
use a python library called nibabel_ which enables us to read and write
neuroimaging-specific file formats.
"""

import nibabel as nib
img = nib.load(fdwi)
data = img.get_data()

"""
``data`` is a 4D array where the first 3 dimensions are the i, j, k voxel
coordinates and the last dimension is the number of non-weighted (S0s) and
diffusion-weighted volumes.

We can very easily check the size of ``data`` in the following way:
"""

print(data.shape)

"""
``(128, 128, 60, 194)``

We can also check the dimensions of each voxel in the following way:
"""

print(img.header.get_zooms()[:3])

"""
``(2.0, 2.0, 2.0)``

We can quickly visualize the results using matplotlib_. For example,
let's show here the middle axial slices of volume 0 and volume 10.
"""

import matplotlib.pyplot as plt

axial_middle = data.shape[2] // 2
plt.figure('Showing the datasets')
plt.subplot(1, 2, 1).set_axis_off()
plt.imshow(data[:, :, axial_middle, 0].T, cmap='gray', origin='lower')
plt.subplot(1, 2, 2).set_axis_off()
plt.imshow(data[:, :, axial_middle, 10].T, cmap='gray', origin='lower')
plt.show()
#plt.savefig('data.png', bbox_inches='tight')
plt.clf()




"""
.. figure:: data.png
   :align: center

   Showing the middle axial slice without (left) and with (right) diffusion weighting.

The next step is to load the b-values and b-vectors from the disk using
the function ``read_bvals_bvecs``.
"""

from dipy.io import read_bvals_bvecs
bvals, bvecs = read_bvals_bvecs(fbval, fbvec)

"""
In DIPY, we use an object called ``GradientTable`` which holds all the
acquisition specific parameters, e.g. b-values, b-vectors, timings and others.
To create this object you can use the function ``gradient_table``.
"""

from dipy.core.gradients import gradient_table
gtab = gradient_table(bvals, bvecs)

"""
Finally, you can use ``gtab`` (the GradientTable object) to show some information about the
acquisition parameters
"""

print(gtab.info)

"""
B-values shape (193,)
         min 0.000000
         max 3500.000000
B-vectors shape (193, 3)
         min -0.964050
         max 0.999992

You, can also see the b-values using:
"""

print(gtab.bvals)

"""

::

    [    0.  1000.  1000.  1000.  1000.  1000.  1000.  1000.  1000.  1000.
      1000.  1000.  1000.  1000.  1000.  1000.  1000.  1000.  1000.  1000.
      1000.  1000.  1000.  1000.  1000.  1000.  1000.  1000.  1000.  1000.
      1000.  1000.  1000.  1000.  1000.  1000.  1000.  1000.  1000.  1000.
      1000.  1000.  1000.  1000.  1000.  1000.  1000.  1000.  1000.  1000.
      1000.  1000.  1000.  1000.  1000.  1000.  1000.  1000.  1000.  1000.
      1000.  1000.  1000.  1000.  1000.  2000.  2000.  2000.  2000.  2000.
      2000.  2000.  2000.  2000.  2000.  2000.  2000.  2000.  2000.  2000.
      2000.  2000.  2000.  2000.  2000.  2000.  2000.  2000.  2000.  2000.
      2000.  2000.  2000.  2000.  2000.  2000.  2000.  2000.  2000.  2000.
      2000.  2000.  2000.  2000.  2000.  2000.  2000.  2000.  2000.  2000.
      2000.  2000.  2000.  2000.  2000.  2000.  2000.  2000.  2000.  2000.
      2000.  2000.  2000.  2000.  2000.  2000.  2000.  2000.  2000.  3500.
      3500.  3500.  3500.  3500.  3500.  3500.  3500.  3500.  3500.  3500.
      3500.  3500.  3500.  3500.  3500.  3500.  3500.  3500.  3500.  3500.
      3500.  3500.  3500.  3500.  3500.  3500.  3500.  3500.  3500.  3500.
      3500.  3500.  3500.  3500.  3500.  3500.  3500.  3500.  3500.  3500.
      3500.  3500.  3500.  3500.  3500.  3500.  3500.  3500.  3500.  3500.
      3500.  3500.  3500.  3500.  3500.  3500.  3500.  3500.  3500.  3500.
      3500.  3500.  3500.]

Or, for example the 10 first b-vectors using:
"""

print(gtab.bvecs[:10, :])

"""

::

    array([[ 0.        ,  0.        ,  0.        ],
           [ 0.999979  , -0.00504001, -0.00402795],
           [ 0.        ,  0.999992  , -0.00398794],
           [-0.0257055 ,  0.653861  , -0.756178  ],
           [ 0.589518  , -0.769236  , -0.246462  ],
           [-0.235785  , -0.529095  , -0.815147  ],
           [-0.893578  , -0.263559  , -0.363394  ],
           [ 0.79784   ,  0.133726  , -0.587851  ],
           [ 0.232937  ,  0.931884  , -0.278087  ],
           [ 0.93672   ,  0.144139  , -0.31903   ]])

``gtab``  can be used to tell what part of the data is the S0 volumes
(volumes which correspond to b-values of 0).
"""

S0s = data[:, :, :, gtab.b0s_mask]

"""
Here, we had only 1 S0 as we can verify by looking at the dimensions of S0s
"""

print(S0s.shape)

"""
``(128, 128, 60, 1)``

Just, for fun let's save this in a new Nifti file.
"""

nib.save(nib.Nifti1Image(S0s, img.affine), 'HARDI193_S0.nii.gz')

##
##
##
import nibabel as nib
#newImage = join(dname, 'HARDI193_S0.nii.gz')
newImage = '/Users/ptm/desktop/Current_working_directory/DIPY/HARDI193_S0.nii.gz'
img = nib.load(newImage)
data = img.get_data()
import matplotlib.pyplot as plt
axial_middle = data.shape[2] // 2
plt.figure('Showing the datasets')
plt.subplot(1, 2, 1).set_axis_off()
plt.imshow(data[:, :, axial_middle, 0].T, cmap='gray', origin='lower')
#plt.subplot(1, 2, 2).set_axis_off()
#plt.imshow(data[:, :, axial_middle, 10].T, cmap='gray', origin='lower')
plt.show()
#plt.savefig('HARDI193_S0.png', bbox_inches='tight')
plt.clf()
##
##
##




"""
Now, that we learned how to load dMRI datasets we can start the analysis.
See example :ref:`example_reconst_dti` to learn how to create FA maps.

.. include:: ../links_names.inc

"""

#https://dipy.herokuapp.com/documentation/0.12.0.dev/examples_built/reconst_dti/#example-reconst-dti

"""

.. _reconst_dti:

============================================================
Reconstruction of the diffusion signal with the Tensor model
============================================================

The diffusion tensor model is a model that describes the diffusion within a
voxel. First proposed by Basser and colleagues [Basser1994]_, it has been very
influential in demonstrating the utility of diffusion MRI in characterizing the
micro-structure of white matter tissue and of the biophysical properties of
tissue, inferred from local diffusion properties and it is still very commonly
used.

The diffusion tensor models the diffusion signal as:

.. math::

    \frac{S(\mathbf{g}, b)}{S_0} = e^{-b\mathbf{g}^T \mathbf{D} \mathbf{g}}

Where $\mathbf{g}$ is a unit vector in 3 space indicating the direction of
measurement and b are the parameters of measurement, such as the strength and
duration of diffusion-weighting gradient. $S(\mathbf{g}, b)$ is the
diffusion-weighted signal measured and $S_0$ is the signal conducted in a
measurement with no diffusion weighting. $\mathbf{D}$ is a positive-definite quadratic
form, which contains six free parameters to be fit. These six parameters are:

.. math::

   \mathbf{D} = \begin{pmatrix} D_{xx} & D_{xy} & D_{xz} \\
                       D_{yx} & D_{yy} & D_{yz} \\
                       D_{zx} & D_{zy} & D_{zz} \\ \end{pmatrix}

This matrix is a variance/covariance matrix of the diffusivity along the three
spatial dimensions. Note that we can assume that diffusivity has antipodal
symmetry, so elements across the diagonal are equal. For example:
$D_{xy} = D_{yx}$. This is why there are only 6 free parameters to estimate
here.

In the following example we show how to reconstruct your diffusion datasets
using a single tensor model.

First import the necessary modules:

``numpy`` is for numerical computation

"""

import numpy as np

"""
``nibabel`` is for loading imaging datasets
"""

import nibabel as nib

"""
``dipy.reconst`` is for the reconstruction algorithms which we use to create
voxel models from the raw data.
"""

import dipy.reconst.dti as dti

"""
``dipy.data`` is used for small datasets that we use in tests and examples.
"""

from dipy.data import fetch_stanford_hardi

"""
Fetch will download the raw dMRI dataset of a single subject. The size of the
dataset is 87 MBytes. You only need to fetch once.
"""

fetch_stanford_hardi()

"""
Next, we read the saved dataset
"""

from dipy.data import read_stanford_hardi

img, gtab = read_stanford_hardi()

"""
``img`` contains a nibabel Nifti1Image object (with the data) and gtab contains a
``GradientTable`` object (information about the gradients e.g. b-values and
b-vectors).
"""

data = img.get_data()
print('data.shape (%d, %d, %d, %d)' % data.shape)

"""
data.shape ``(81, 106, 76, 160)``

First of all, we mask and crop the data. This is a quick way to avoid
calculating Tensors on the background of the image. This is done using dipy_'s
``mask`` module.
"""

from dipy.segment.mask import median_otsu

maskdata, mask = median_otsu(data, 3, 1, True,
                             vol_idx=range(10, 50), dilate=2)
print('maskdata.shape (%d, %d, %d, %d)' % maskdata.shape)

"""
maskdata.shape ``(72, 87, 59, 160)``

Now that we have prepared the datasets we can go forward with the voxel
reconstruction. First, we instantiate the Tensor model in the following way.
"""

tenmodel = dti.TensorModel(gtab)

"""
Fitting the data is very simple. We just need to call the fit method of the
TensorModel in the following way:
"""

tenfit = tenmodel.fit(maskdata)

"""
The fit method creates a ``TensorFit`` object which contains the fitting parameters
and other attributes of the model. For example we can generate fractional
anisotropy (FA) from the eigen-values of the tensor. FA is used to characterize
the degree to which the distribution of diffusion in a voxel is
directional. That is, whether there is relatively unrestricted diffusion in one
particular direction.

Mathematically, FA is defined as the normalized variance of the eigen-values of
the tensor:

.. math::

        FA = \sqrt{\frac{1}{2}\frac{(\lambda_1-\lambda_2)^2+(\lambda_1-
                    \lambda_3)^2+(\lambda_2-\lambda_3)^2}{\lambda_1^2+
                    \lambda_2^2+\lambda_3^2}}

Note that FA should be interpreted carefully. It may be an indication of the
density of packing of fibers in a voxel, and the amount of myelin wrapping these
axons, but it is not always a measure of "tissue integrity". For example, FA
may decrease in locations in which there is fanning of white matter fibers, or
where more than one population of white matter fibers crosses.
"""

print('Computing anisotropy measures (FA, MD, RGB)')
from dipy.reconst.dti import fractional_anisotropy, color_fa, lower_triangular

FA = fractional_anisotropy(tenfit.evals)

"""
In the background of the image the fitting will not be accurate there is no
signal and possibly we will find FA values with nans (not a number). We can
easily remove these in the following way.
"""

FA[np.isnan(FA)] = 0

"""
Saving the FA images is very easy using nibabel_. We need the FA volume and the
affine matrix which transform the image's coordinates to the world coordinates.
Here, we choose to save the FA in ``float32``.
"""

fa_img = nib.Nifti1Image(FA.astype(np.float32), img.affine)
nib.save(fa_img, 'tensor_fa.nii.gz')


##
##
##
import nibabel as nib
#newImage = join(dname, 'HARDI193_S0.nii.gz')
newImage = '/Users/ptm/desktop/Current_working_directory/DIPY/tensor_fa.nii.gz'
img = nib.load(newImage)
data = img.get_data()
import matplotlib.pyplot as plt
axial_middle = data.shape[2] // 2
plt.figure('Showing the datasets')
plt.subplot(1, 2, 1).set_axis_off()
plt.imshow(data[:, :, axial_middle].T, cmap='gray', origin='lower')
#plt.imshow(data[:, :, axial_middle, 0].T, cmap='gray', origin='lower')
#plt.subplot(1, 2, 2).set_axis_off()
#plt.imshow(data[:, :, axial_middle, 10].T, cmap='gray', origin='lower')
plt.show()
#plt.savefig('tensor_fa.png', bbox_inches='tight')
plt.clf()
##
##
##



"""
You can now see the result with any nifti viewer or check it slice by slice
using matplotlib_'s ``imshow``. In the same way you can save the eigen values, the
eigen vectors or any other properties of the tensor.
"""

evecs_img = nib.Nifti1Image(tenfit.evecs.astype(np.float32), img.affine)
nib.save(evecs_img, 'tensor_evecs.nii.gz')

##
##
##
import nibabel as nib
#newImage = join(dname, 'HARDI193_S0.nii.gz')
newImage = '/Users/ptm/desktop/Current_working_directory/DIPY/tensor_evecs.nii.gz'
img = nib.load(newImage)
data = img.get_data()
import matplotlib.pyplot as plt
axial_middle = data.shape[2] // 2
plt.figure('Showing the datasets')
plt.subplot(1, 2, 1).set_axis_off()
plt.imshow(data[:, :, axial_middle, 0, 0].T, cmap='gray', origin='lower')
#plt.imshow(data[:, :, axial_middle, 0].T, cmap='gray', origin='lower')
#plt.subplot(1, 2, 2).set_axis_off()
#plt.imshow(data[:, :, axial_middle, 10].T, cmap='gray', origin='lower')
plt.show()
#plt.savefig('tensor_fa.png', bbox_inches='tight')
plt.clf()
##
##
##



"""
Other tensor statistics can be calculated from the ``tenfit`` object. For example,
a commonly calculated statistic is the mean diffusivity (MD). This is simply the
mean of the  eigenvalues of the tensor. Since FA is a normalized
measure of variance and MD is the mean, they are often used as complimentary
measures. In DIPY, there are two equivalent ways to calculate the mean
diffusivity. One is by calling the ``mean_diffusivity`` module function on the
eigen-values of the ``TensorFit`` class instance:
"""

MD1 = dti.mean_diffusivity(tenfit.evals)
nib.save(nib.Nifti1Image(MD1.astype(np.float32), img.affine), 'tensors_md.nii.gz')

##
##
##
import nibabel as nib
#newImage = join(dname, 'HARDI193_S0.nii.gz')
newImage = '/Users/ptm/desktop/Current_working_directory/DIPY/tensors_md.nii.gz'
img = nib.load(newImage)
data = img.get_data()
import matplotlib.pyplot as plt
axial_middle = data.shape[2] // 2
plt.figure('Showing the datasets')
plt.subplot(1, 2, 1).set_axis_off()
plt.imshow(data[:, :, axial_middle].T, cmap='gray', origin='lower')
#plt.imshow(data[:, :, axial_middle, 0].T, cmap='gray', origin='lower')
#plt.subplot(1, 2, 2).set_axis_off()
#plt.imshow(data[:, :, axial_middle, 10].T, cmap='gray', origin='lower')
plt.show()
#plt.savefig('tensor_fa.png', bbox_inches='tight')
plt.clf()
##
##
##

"""
The other is to call the ``TensorFit`` class method:
"""

MD2 = tenfit.md

"""
Obviously, the quantities are identical.

We can also compute the colored FA or RGB-map [Pajevic1999]_. First, we make sure
that the FA is scaled between 0 and 1, we compute the RGB map and save it.
"""

FA = np.clip(FA, 0, 1)
RGB = color_fa(FA, tenfit.evecs)
nib.save(nib.Nifti1Image(np.array(255 * RGB, 'uint8'), img.affine), 'tensor_rgb.nii.gz')

##
##
##
import nibabel as nib
#newImage = join(dname, 'HARDI193_S0.nii.gz')
newImage = '/Users/ptm/desktop/Current_working_directory/DIPY/tensor_rgb.nii.gz'
img = nib.load(newImage)
data = img.get_data()
import matplotlib.pyplot as plt
axial_middle = data.shape[2] // 2
plt.figure('Showing the datasets')
plt.subplot(1, 2, 1).set_axis_off()
plt.imshow(data[:, :, axial_middle, 0].T, cmap='gray', origin='lower')
#plt.imshow(data[:, :, axial_middle, 0].T, cmap='gray', origin='lower')
#plt.subplot(1, 2, 2).set_axis_off()
#plt.imshow(data[:, :, axial_middle, 10].T, cmap='gray', origin='lower')
plt.show()
#plt.savefig('tensor_fa.png', bbox_inches='tight')
plt.clf()
##
##
##

"""
Let's try to visualize the tensor ellipsoids of a small rectangular
area in an axial slice of the splenium of the corpus callosum (CC).
"""

print('Computing tensor ellipsoids in a part of the splenium of the CC')

from dipy.data import get_sphere
sphere = get_sphere('symmetric724')

from dipy.viz import fvtk
ren = fvtk.ren()

evals = tenfit.evals[13:43, 44:74, 28:29]
evecs = tenfit.evecs[13:43, 44:74, 28:29]

"""
We can color the ellipsoids using the ``color_fa`` values that we calculated
above. In this example we additionally normalize the values to increase the
contrast.
"""

cfa = RGB[13:43, 44:74, 28:29]
cfa /= cfa.max()

fvtk.add(ren, fvtk.tensor(evals, evecs, cfa, sphere))

print('Saving illustration as tensor_ellipsoids.png')
fvtk.record(ren, n_frames=1, out_path='/Users/ptm/desktop/Current_working_directory/DIPY/tensor_ellipsoids.png', size=(600, 600))

##
##
##
import cv2 as cv2
# Plot Image
#%matplotlib inline
image_name = "/Users/ptm/desktop/Current_working_directory/DIPY/tensor_ellipsoids.png" #Image to be used as query
def plotImage(image_location):
    image = cv2.imread(image_name)
    image = cv2.resize(image, (512,512))
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)); plt.axis('off')
    return
plotImage(image_name)
plt.show()
plt.clf()
##
##
##


"""
.. figure:: tensor_ellipsoids.png
   :align: center

   Tensor Ellipsoids.
"""

fvtk.clear(ren)

"""
Finally, we can visualize the tensor Orientation Distribution Functions
for the same area as we did with the ellipsoids.
"""

##
##
##
import nibabel as nib
img, gtab = read_stanford_hardi()
data = img.get_data()
##
##
##


tensor_odfs = tenmodel.fit(data[20:50, 55:85, 38:39]).odf(sphere)

fvtk.add(ren, fvtk.sphere_funcs(tensor_odfs, sphere, colormap=None))
#fvtk.show(r)
print('Saving illustration as tensor_odfs.png')
fvtk.record(ren, n_frames=1, out_path='/Users/ptm/desktop/Current_working_directory/DIPY/tensor_odfs.png', size=(600, 600))



##
##
##
import cv2 as cv2
# Plot Image
#%matplotlib inline
image_name = "/Users/ptm/desktop/Current_working_directory/DIPY/tensor_odfs.png" #Image to be used as query
def plotImage(image_location):
    image = cv2.imread(image_name)
    image = cv2.resize(image, (512,512))
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)); plt.axis('off')
    return
plotImage(image_name)
plt.show()
plt.clf()
##
##
##


"""
.. figure:: tensor_odfs.png
   :align: center

   Tensor ODFs.

Note that while the tensor model is an accurate and reliable model of the
diffusion signal in the white matter, it has the drawback that it only has one
principal diffusion direction. Therefore, in locations in the brain that
contain multiple fiber populations crossing each other, the tensor model may
indicate that the principal diffusion direction is intermediate to these
directions. Therefore, using the principal diffusion direction for tracking in
these locations may be misleading and may lead to errors in defining the
tracks. Fortunately, other reconstruction methods can be used to represent the
diffusion and fiber orientations in those locations. These are presented in
other examples.

References
----------

.. [Basser1994] Basser PJ, Mattielo J, LeBihan (1994). MR diffusion tensor
   spectroscopy and imaging.

.. [Pajevic1999] Pajevic S, Pierpaoli (1999). Color schemes to represent the
   orientation of anisotropic tissues from diffusion tensor data: application
   to white matter fiber tract mapping in the human brain.

.. include:: ../links_names.inc

"""


# https://dipy.herokuapp.com/documentation/0.12.0.dev/examples_built/affine_registration_3d/#example-affine-registration-3d

"""
==========================================
Affine Registration in 3D
==========================================
This example explains how to compute an affine transformation to register two
3D volumes by maximization of their Mutual Information [Mattes03]_. The
optimization strategy is similar to that implemented in ANTS [Avants11]_.
"""

import numpy as np
from dipy.viz import regtools
from dipy.data import fetch_stanford_hardi, read_stanford_hardi
from dipy.data.fetcher import fetch_syn_data, read_syn_data
from dipy.align.imaffine import (transform_centers_of_mass,
                                 AffineMap,
                                 MutualInformationMetric,
                                 AffineRegistration)
from dipy.align.transforms import (TranslationTransform3D,
                                   RigidTransform3D,
                                   AffineTransform3D)

"""
Let's fetch two b0 volumes, the static image will be the b0 from the Stanford
HARDI dataset
"""

fetch_stanford_hardi()
nib_stanford, gtab_stanford = read_stanford_hardi()
static = np.squeeze(nib_stanford.get_data())[..., 0]
static_grid2world = nib_stanford.affine

"""
Now the moving image
"""

fetch_syn_data()
nib_syn_t1, nib_syn_b0 = read_syn_data()
moving = np.array(nib_syn_b0.get_data())
moving_grid2world = nib_syn_b0.affine

"""
We can see that the images are far from aligned by drawing one on top of
the other. The images don't even have the same number of voxels, so in order
to draw one on top of the other we need to resample the moving image on a grid
of the same dimensions as the static image, we can do this by "transforming"
the moving image using an identity transform
"""

identity = np.eye(4)
affine_map = AffineMap(identity,
                       static.shape, static_grid2world,
                       moving.shape, moving_grid2world)
resampled = affine_map.transform(moving)
regtools.overlay_slices(static, resampled, None, 0,
                        "Static", "Moving", "resampled_0.png")
regtools.overlay_slices(static, resampled, None, 1,
                        "Static", "Moving", "resampled_1.png")
regtools.overlay_slices(static, resampled, None, 2,
                        "Static", "Moving", "resampled_2.png")


##
##
##
import cv2 as cv2
# Plot Image
#%matplotlib inline
image_name = "/Users/ptm/desktop/Current_working_directory/DIPY/resampled_0.png" #Image to be used as query
image_nameTwo = "/Users/ptm/desktop/Current_working_directory/DIPY/resampled_1.png"
image_nameThree = "/Users/ptm/desktop/Current_working_directory/DIPY/resampled_2.png"

def plotImage(image_location):
    image = cv2.imread(image_name)
    #image = cv2.resize(image, (512,512))
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)); plt.axis('off')
    return
plotImage(image_name)
plotImage(image_nameTwo)
plotImage(image_nameThree)
plt.show()
plt.clf()
##
##
##



"""
.. figure:: resampled_0.png
   :align: center
.. figure:: resampled_1.png
   :align: center
.. figure:: resampled_2.png
   :align: center

   Input images before alignment.
"""

"""
We can obtain a very rough (and fast) registration by just aligning the centers
of mass of the two images
"""

c_of_mass = transform_centers_of_mass(static, static_grid2world,
                                      moving, moving_grid2world)

"""
We can now transform the moving image and draw it on top of the static image,
registration is not likely to be good, but at least they will occupy roughly
the same space
"""

transformed = c_of_mass.transform(moving)
regtools.overlay_slices(static, transformed, None, 0,
                        "Static", "Transformed", "transformed_com_0.png")
regtools.overlay_slices(static, transformed, None, 1,
                        "Static", "Transformed", "transformed_com_1.png")
regtools.overlay_slices(static, transformed, None, 2,
                        "Static", "Transformed", "transformed_com_2.png")


##
##
##
import cv2 as cv2
# Plot Image
#%matplotlib inline
image_name = "/Users/ptm/desktop/Current_working_directory/DIPY/transformed_com_0.png" #Image to be used as query
image_nameTwo = "/Users/ptm/desktop/Current_working_directory/DIPY/transformed_com_1.png"
image_nameThree = "/Users/ptm/desktop/Current_working_directory/DIPY/transformed_com_2.png"

def plotImage(image_location):
    image = cv2.imread(image_name)
    #image = cv2.resize(image, (512,512))
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)); plt.axis('off')
    return
plotImage(image_name)
plotImage(image_nameTwo)
plotImage(image_nameThree)
plt.show()
plt.clf()
##
##
##


"""
.. figure:: transformed_com_0.png
   :align: center
.. figure:: transformed_com_1.png
   :align: center
.. figure:: transformed_com_2.png
   :align: center

   Registration result by aligning the centers of mass of the images.
"""

"""
This was just a translation of the moving image towards the static image, now
we will refine it by looking for an affine transform. We first create the
similarity metric (Mutual Information) to be used. We need to specify the
number of bins to be used to discretize the joint and marginal probability
distribution functions (PDF), a typical value is 32. We also need to specify
the percentage (an integer in (0, 100]) of voxels to be used for computing the
PDFs, the most accurate registration will be obtained by using all voxels, but
it is also the most time-consuming choice. We specify full sampling by passing
None instead of an integer
"""

nbins = 32
sampling_prop = None
metric = MutualInformationMetric(nbins, sampling_prop)

"""
To avoid getting stuck at local optima, and to accelerate convergence, we use a
multi-resolution strategy (similar to ANTS [Avants11]_) by building a Gaussian
Pyramid. To have as much flexibility as possible, the user can specify how this
Gaussian Pyramid is built. First of all, we need to specify how many
resolutions we want to use. This is indirectly specified by just providing a
list of the number of iterations we want to perform at each resolution. Here we
will just specify 3 resolutions and a large number of iterations, 10000 at the
coarsest resolution, 1000 at the medium resolution and 100 at the finest. These
are the default settings
"""

level_iters = [10000, 1000, 100]

"""
To compute the Gaussian pyramid, the original image is first smoothed at each
level of the pyramid using a Gaussian kernel with the requested sigma. A good
initial choice is [3.0, 1.0, 0.0], this is the default
"""

sigmas = [3.0, 1.0, 0.0]

"""
Now we specify the sub-sampling factors. A good configuration is [4, 2, 1],
which means that, if the original image shape was (nx, ny, nz) voxels, then the
shape of the coarsest image will be about (nx//4, ny//4, nz//4), the shape in
the middle resolution will be about (nx//2, ny//2, nz//2) and the image at the
finest scale has the same size as the original image. This set of factors is
the default
"""

factors = [4, 2, 1]

"""
Now we go ahead and instantiate the registration class with the configuration
we just prepared
"""

affreg = AffineRegistration(metric=metric,
                            level_iters=level_iters,
                            sigmas=sigmas,
                            factors=factors)

"""
Using AffineRegistration we can register our images in as many stages as we
want, providing previous results as initialization for the next (the same logic
as in ANTS). The reason why it is useful is that registration is a non-convex
optimization problem (it may have more than one local optima), which means that
it is very important to initialize as close to the solution as possible. For
example, lets start with our (previously computed) rough transformation
aligning the centers of mass of our images, and then refine it in three stages.
First look for an optimal translation. The dictionary regtransforms contains
all available transforms, we obtain one of them by providing its name and the
dimension (either 2 or 3) of the image we are working with (since we are
aligning volumes, the dimension is 3)
"""

transform = TranslationTransform3D()
params0 = None
starting_affine = c_of_mass.affine
translation = affreg.optimize(static, moving, transform, params0,
                              static_grid2world, moving_grid2world,
                              starting_affine=starting_affine)

"""
If we look at the result, we can see that this translation is much better than
simply aligning the centers of mass
"""

transformed = translation.transform(moving)
regtools.overlay_slices(static, transformed, None, 0,
                        "Static", "Transformed", "transformed_trans_0.png")
regtools.overlay_slices(static, transformed, None, 1,
                        "Static", "Transformed", "transformed_trans_1.png")
regtools.overlay_slices(static, transformed, None, 2,
                        "Static", "Transformed", "transformed_trans_2.png")

##
##
##
import cv2 as cv2
# Plot Image
#%matplotlib inline
image_name = "/Users/ptm/desktop/Current_working_directory/DIPY/transformed_trans_0.png" #Image to be used as query
image_nameTwo = "/Users/ptm/desktop/Current_working_directory/DIPY/transformed_trans_1.png"
image_nameThree = "/Users/ptm/desktop/Current_working_directory/DIPY/transformed_trans_2.png"

def plotImage(image_location):
    image = cv2.imread(image_name)
    #image = cv2.resize(image, (512,512))
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)); plt.axis('off')
    return
plotImage(image_name)
plotImage(image_nameTwo)
plotImage(image_nameThree)
plt.show()
plt.clf()
##
##
##


"""
.. figure:: transformed_trans_0.png
   :align: center
.. figure:: transformed_trans_1.png
   :align: center
.. figure:: transformed_trans_2.png
   :align: center

   Registration result by translating the moving image, using Mutual Information.
"""

"""
Now lets refine with a rigid transform (this may even modify our previously
found optimal translation)
"""

transform = RigidTransform3D()
params0 = None
starting_affine = translation.affine
rigid = affreg.optimize(static, moving, transform, params0,
                        static_grid2world, moving_grid2world,
                        starting_affine=starting_affine)

"""
This produces a slight rotation, and the images are now better aligned
"""

transformed = rigid.transform(moving)
regtools.overlay_slices(static, transformed, None, 0,
                        "Static", "Transformed", "transformed_rigid_0.png")
regtools.overlay_slices(static, transformed, None, 1,
                        "Static", "Transformed", "transformed_rigid_1.png")
regtools.overlay_slices(static, transformed, None, 2,
                        "Static", "Transformed", "transformed_rigid_2.png")


##
##
##
import cv2 as cv2
# Plot Image
#%matplotlib inline
image_name = "/Users/ptm/desktop/Current_working_directory/DIPY/transformed_rigid_0.png" #Image to be used as query
image_nameTwo = "/Users/ptm/desktop/Current_working_directory/DIPY/transformed_rigid_1.png"
image_nameThree = "/Users/ptm/desktop/Current_working_directory/DIPY/transformed_rigid_2.png"

def plotImage(image_location):
    image = cv2.imread(image_name)
    #image = cv2.resize(image, (512,512))
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)); plt.axis('off')
    return
plotImage(image_name)
plotImage(image_nameTwo)
plotImage(image_nameThree)
plt.show()
plt.clf()
##
##
##

"""
.. figure:: transformed_rigid_0.png
   :align: center
.. figure:: transformed_rigid_1.png
   :align: center
.. figure:: transformed_rigid_2.png
   :align: center

   Registration result with a rigid transform, using Mutual Information.
"""

"""
Finally, lets refine with a full affine transform (translation, rotation, scale
and shear), it is safer to fit more degrees of freedom now, since we must be
very close to the optimal transform
"""

transform = AffineTransform3D()
params0 = None
starting_affine = rigid.affine
affine = affreg.optimize(static, moving, transform, params0,
                         static_grid2world, moving_grid2world,
                         starting_affine=starting_affine)

"""
This results in a slight shear and scale
"""

transformed = affine.transform(moving)
regtools.overlay_slices(static, transformed, None, 0,
                        "Static", "Transformed", "transformed_affine_0.png")
regtools.overlay_slices(static, transformed, None, 1,
                        "Static", "Transformed", "transformed_affine_1.png")
regtools.overlay_slices(static, transformed, None, 2,
                        "Static", "Transformed", "transformed_affine_2.png")


##
##
##
import cv2 as cv2
# Plot Image
#%matplotlib inline
image_name = "/Users/ptm/desktop/Current_working_directory/DIPY/transformed_affine_0.png" #Image to be used as query
image_nameTwo = "/Users/ptm/desktop/Current_working_directory/DIPY/transformed_affine_1.png"
image_nameThree = "/Users/ptm/desktop/Current_working_directory/DIPY/transformed_affine_2.png"

def plotImage(image_location):
    image = cv2.imread(image_name)
    #image = cv2.resize(image, (512,512))
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)); plt.axis('off')
    return
plotImage(image_name)
plotImage(image_nameTwo)
plotImage(image_nameThree)
plt.show()
plt.clf()
##
##
##

"""
.. figure:: transformed_affine_0.png
   :align: center
.. figure:: transformed_affine_1.png
   :align: center
.. figure:: transformed_affine_2.png
   :align: center

   Registration result with an affine transform, using Mutual Information.

.. [Mattes03] Mattes, D., Haynor, D. R., Vesselle, H., Lewellen, T. K.,
              Eubank, W. (2003). PET-CT image registration in the chest using
              free-form deformations. IEEE Transactions on Medical Imaging,
              22(1), 120-8.
.. [Avants11] Avants, B. B., Tustison, N., & Song, G. (2011). Advanced
              Normalization Tools ( ANTS ), 1-35.

.. include:: ../links_names.inc

"""


# https://github.com/nipy/dipy/blob/master/doc/examples/brain_extraction_dwi.py

"""
===================================
Brain segmentation with median_otsu
===================================

We show how to extract brain information and mask from a b0 image using dipy_'s
``segment.mask`` module.

First import the necessary modules:
"""

import numpy as np
import nibabel as nib

"""
Download and read the data for this tutorial.

The ``scil_b0`` dataset contains different data from different companies and
models. For this example, the data comes from a 1.5 Tesla Siemens MRI.
"""

from dipy.data.fetcher import fetch_scil_b0, read_siemens_scil_b0
fetch_scil_b0()
img = read_siemens_scil_b0()
data = np.squeeze(img.get_data())

"""
``img`` contains a nibabel Nifti1Image object. Data is the actual brain data as
a numpy ndarray.

Segment the brain using DIPY's ``mask`` module.

``median_otsu`` returns the segmented brain data and a binary mask of the brain.
It is possible to fine tune the parameters of ``median_otsu`` (``median_radius``
and ``num_pass``) if extraction yields incorrect results but the default
parameters work well on most volumes. For this example, we used 2 as
``median_radius`` and 1 as ``num_pass``
"""

from dipy.segment.mask import median_otsu
b0_mask, mask = median_otsu(data, 2, 1)

"""
Saving the segmentation results is very easy using nibabel. We need the
``b0_mask``, and the binary mask volumes. The affine matrix which transform the
image's coordinates to the world coordinates is also needed. Here, we choose to
save both images in ``float32``.
"""

mask_img = nib.Nifti1Image(mask.astype(np.float32), img.affine)
b0_img = nib.Nifti1Image(b0_mask.astype(np.float32), img.affine)

fname = 'se_1.5t'
nib.save(mask_img, fname + '_binary_mask.nii.gz')
nib.save(b0_img, fname + '_mask.nii.gz')



##
##
##
import nibabel as nib
newImage = '/Users/ptm/desktop/Current_working_directory/DIPY/se_1.5t_binary_mask.nii.gz'
newImageTwo = '/Users/ptm/desktop/Current_working_directory/DIPY/se_1.5t_mask.nii.gz'
img = nib.load(newImage)
data = img.get_data()
imgTwo = nib.load(newImageTwo)
dataTwo = imgTwo.get_data()
import matplotlib.pyplot as plt
axial_middle = data.shape[2] // 2
axial_middleTwo = dataTwo.shape[2] // 2
plt.figure('Showing the datasets')
plt.subplot(1, 2, 1).set_axis_off()
plt.imshow(data[:, :, axial_middle].T, cmap='gray', origin='lower')
#plt.imshow(data[:, :, axial_middle, 0].T, cmap='gray', origin='lower')
plt.subplot(1, 2, 2).set_axis_off()
plt.imshow(dataTwo[:, :, axial_middleTwo].T, cmap='gray', origin='lower')
plt.show()
#plt.savefig('tensor_fa.png', bbox_inches='tight')
plt.clf()
##
##
##


"""
Quick view of the results middle slice using ``matplotlib``.
"""

import matplotlib.pyplot as plt
from dipy.core.histeq import histeq

sli = data.shape[2] // 2
plt.figure('Brain segmentation')
plt.subplot(1, 2, 1).set_axis_off()
plt.imshow(histeq(data[:, :, sli].astype('float')).T,
           cmap='gray', origin='lower')

plt.subplot(1, 2, 2).set_axis_off()
plt.imshow(histeq(b0_mask[:, :, sli].astype('float')).T,
           cmap='gray', origin='lower')

plt.savefig('median_otsu.png')



##
##
##
import cv2 as cv2
# Plot Image
#%matplotlib inline
image_name = "/Users/ptm/desktop/Current_working_directory/DIPY/median_otsu.png" #Image to be used as query
def plotImage(image_location):
    image = cv2.imread(image_name)
    #image = cv2.resize(image, (512,512))
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)); plt.axis('off')
    return
plotImage(image_name)
plt.show()
plt.clf()
##
##
##


"""
.. figure:: median_otsu.png
   :align: center

   An application of median_otsu for brain segmentation.

``median_otsu`` can also automatically crop the outputs to remove the largest
possible number of background voxels. This makes outputted data significantly
smaller. Auto-cropping in ``median_otsu`` is activated by setting the
``autocrop`` parameter to ``True``.
"""

b0_mask_crop, mask_crop = median_otsu(data, 4, 4, autocrop=True)

"""
Saving cropped data using nibabel as demonstrated previously.
"""

mask_img_crop = nib.Nifti1Image(mask_crop.astype(np.float32), img.affine)
b0_img_crop = nib.Nifti1Image(
    b0_mask_crop.astype(np.float32), img.affine)
nib.save(mask_img_crop, fname + '_binary_mask_crop.nii.gz')
nib.save(b0_img_crop, fname + '_mask_crop.nii.gz')


##
##
##
import nibabel as nib
newImage = '/Users/ptm/desktop/Current_working_directory/DIPY/se_1.5t_binary_mask_crop.nii.gz'
newImageTwo = '/Users/ptm/desktop/Current_working_directory/DIPY/se_1.5t_mask_crop.nii.gz'
img = nib.load(newImage)
data = img.get_data()
imgTwo = nib.load(newImageTwo)
dataTwo = imgTwo.get_data()
import matplotlib.pyplot as plt
axial_middle = data.shape[2] // 2
axial_middleTwo = dataTwo.shape[2] // 2
plt.figure('Showing the datasets')
plt.subplot(1, 2, 1).set_axis_off()
plt.imshow(data[:, :, axial_middle].T, cmap='gray', origin='lower')
#plt.imshow(data[:, :, axial_middle, 0].T, cmap='gray', origin='lower')
plt.subplot(1, 2, 2).set_axis_off()
plt.imshow(dataTwo[:, :, axial_middleTwo].T, cmap='gray', origin='lower')
plt.show()
#plt.savefig('tensor_fa.png', bbox_inches='tight')
plt.clf()
##
##
##



"""

.. include:: ../links_names.inc

"""





# https://github.com/nipy/dipy/blob/master/doc/examples/viz_advanced.py

"""
==================================
Advanced interactive visualization
==================================

In dipy_ we created a thin interface to access many of the capabilities
available in the Visualization Toolkit framework (VTK) but tailored to the
needs of structural and diffusion imaging. Initially the 3D visualization
module was named ``fvtk``, meaning functions using vtk. This is still available
for backwards compatibility but now there is a more comprehensive way to access
the main functions using the following modules.
"""

import numpy as np
from dipy.viz import actor, window, ui

"""
In ``window`` we have all the objects that connect what needs to be rendered
to the display or the disk e.g., for saving screenshots. So, there you will
find key objects and functions like the ``Renderer`` class which holds and
provides access to all the actors and the ``show`` function which displays what
is in the renderer on a window. Also, this module provides access to functions
for opening/saving dialogs and printing screenshots (see ``snapshot``).

In the ``actor`` module we can find all the different primitives e.g.,
streamtubes, lines, image slices, etc.

In the ``ui`` module we have some other objects which allow to add buttons
and sliders and these interact both with windows and actors. Because of this
they need input from the operating system so they can process events.

Let's get started. In this tutorial, we will visualize some bundles
together with FA or T1. We will be able to change the slices using
a ``LineSlider2D`` widget.

First we need to fetch and load some datasets.
"""

from dipy.data.fetcher import fetch_bundles_2_subjects, read_bundles_2_subjects

fetch_bundles_2_subjects()

"""
The following function outputs a dictionary with the required bundles e.g. ``af
left`` (left arcuate fasciculus) and maps, e.g. FA for a specific subject.
"""

res = read_bundles_2_subjects('subj_1', ['t1', 'fa'],
                              ['af.left', 'cst.right', 'cc_1'])

"""
We will use 3 bundles, FA and the affine transformation that brings the voxel
coordinates to world coordinates (RAS 1mm).
"""

streamlines = res['af.left'] + res['cst.right'] + res['cc_1']
data = res['fa']
shape = data.shape
affine = res['affine']

"""
With our current design it is easy to decide in which space you want the
streamlines and slices to appear. The default we have here is to appear in
world coordinates (RAS 1mm).
"""

world_coords = True

"""
If we want to see the objects in native space we need to make sure that all
objects which are currently in world coordinates are transformed back to
native space using the inverse of the affine.
"""

if not world_coords:
    from dipy.tracking.streamline import transform_streamlines
    streamlines = transform_streamlines(streamlines, np.linalg.inv(affine))

"""
Now we create, a ``Renderer`` object and add the streamlines using the ``line``
function and an image plane using the ``slice`` function.
"""

ren = window.Renderer()
stream_actor = actor.line(streamlines)

if not world_coords:
    image_actor_z = actor.slicer(data, affine=np.eye(4))
else:
    image_actor_z = actor.slicer(data, affine)

"""
We can also change also the opacity of the slicer.
"""

slicer_opacity = 0.6
image_actor_z.opacity(slicer_opacity)

"""
We can add additonal slicers by copying the original and adjusting the
``display_extent``.
"""

image_actor_x = image_actor_z.copy()
image_actor_x.opacity(slicer_opacity)
x_midpoint = int(np.round(shape[0] / 2))
image_actor_x.display_extent(x_midpoint,
                             x_midpoint, 0,
                             shape[1] - 1,
                             0,
                             shape[2] - 1)

image_actor_y = image_actor_z.copy()
image_actor_y.opacity(slicer_opacity)
y_midpoint = int(np.round(shape[1] / 2))
image_actor_y.display_extent(0,
                             shape[0] - 1,
                             y_midpoint,
                             y_midpoint,
                             0,
                             shape[2] - 1)

"""
Connect the actors with the Renderer.
"""

ren.add(stream_actor)
ren.add(image_actor_z)
ren.add(image_actor_x)
ren.add(image_actor_y)

"""
Now we would like to change the position of each ``image_actor`` using a
slider. The sliders are widgets which require access to different areas of the
visualization pipeline and therefore we don't recommend using them with
``show``. The more appropriate way is to use them with the ``ShowManager``
object which allows accessing the pipeline in different areas. Here is how:
"""

show_m = window.ShowManager(ren, size=(1200, 900))
show_m.initialize()

"""
After we have initialized the ``ShowManager`` we can go ahead and create
sliders to move the slices and change their opacity.
"""

line_slider_z = ui.LineSlider2D(min_value=0,
                                max_value=shape[2] - 1,
                                initial_value=shape[2] / 2,
                                text_template="{value:.0f}",
                                length=140)

line_slider_x = ui.LineSlider2D(min_value=0,
                                max_value=shape[0] - 1,
                                initial_value=shape[0] / 2,
                                text_template="{value:.0f}",
                                length=140)

line_slider_y = ui.LineSlider2D(min_value=0,
                                max_value=shape[1] - 1,
                                initial_value=shape[1] / 2,
                                text_template="{value:.0f}",
                                length=140)

opacity_slider = ui.LineSlider2D(min_value=0.0,
                                 max_value=1.0,
                                 initial_value=slicer_opacity,
                                 length=140)

"""
Now we will write callbacks for the sliders and register them.
"""


def change_slice_z(i_ren, obj, slider):
    z = int(np.round(slider.value))
    image_actor_z.display_extent(0, shape[0] - 1, 0, shape[1] - 1, z, z)


def change_slice_x(i_ren, obj, slider):
    x = int(np.round(slider.value))
    image_actor_x.display_extent(x, x, 0, shape[1] - 1, 0, shape[2] - 1)


def change_slice_y(i_ren, obj, slider):
    y = int(np.round(slider.value))
    image_actor_y.display_extent(0, shape[0] - 1, y, y, 0, shape[2] - 1)


def change_opacity(i_ren, obj, slider):
    slicer_opacity = slider.value
    image_actor_z.opacity(slicer_opacity)
    image_actor_x.opacity(slicer_opacity)
    image_actor_y.opacity(slicer_opacity)

line_slider_z.add_callback(line_slider_z.slider_disk,
                           "MouseMoveEvent",
                           change_slice_z)
line_slider_x.add_callback(line_slider_x.slider_disk,
                           "MouseMoveEvent",
                           change_slice_x)
line_slider_y.add_callback(line_slider_y.slider_disk,
                           "MouseMoveEvent",
                           change_slice_y)
opacity_slider.add_callback(opacity_slider.slider_disk,
                            "MouseMoveEvent",
                            change_opacity)

"""
We'll also create text labels to identify the sliders.
"""


def build_label(text):
    label = ui.TextBlock2D()
    label.message = text
    label.font_size = 18
    label.font_family = 'Arial'
    label.justification = 'left'
    label.bold = False
    label.italic = False
    label.shadow = False
    label.actor.GetTextProperty().SetBackgroundColor(0, 0, 0)
    label.actor.GetTextProperty().SetBackgroundOpacity(0.0)
    label.color = (1, 1, 1)

    return label


line_slider_label_z = build_label(text="Z Slice")
line_slider_label_x = build_label(text="X Slice")
line_slider_label_y = build_label(text="Y Slice")
opacity_slider_label = build_label(text="Opacity")

"""
Now we will create a ``panel`` to contain the sliders and labels.
"""


panel = ui.Panel2D(center=(1030, 120),
                   size=(300, 200),
                   color=(1, 1, 1),
                   opacity=0.1,
                   align="right")

panel.add_element(line_slider_label_x, 'relative', (0.1, 0.75))
panel.add_element(line_slider_x, 'relative', (0.65, 0.8))
panel.add_element(line_slider_label_y, 'relative', (0.1, 0.55))
panel.add_element(line_slider_y, 'relative', (0.65, 0.6))
panel.add_element(line_slider_label_z, 'relative', (0.1, 0.35))
panel.add_element(line_slider_z, 'relative', (0.65, 0.4))
panel.add_element(opacity_slider_label, 'relative', (0.1, 0.15))
panel.add_element(opacity_slider, 'relative', (0.65, 0.2))

show_m.ren.add(panel)

"""
Then, we can render all the widgets and everything else in the screen and
start the interaction using ``show_m.start()``.


However, if you change the window size, the panel will not update its position
properly. The solution to this issue is to update the position of the panel
using its ``re_align`` method every time the window size changes.
"""


global size
size = ren.GetSize()


def win_callback(obj, event):
    global size
    if size != obj.GetSize():
        size_old = size
        size = obj.GetSize()
        size_change = [size[0] - size_old[0], 0]
        panel.re_align(size_change)

show_m.initialize()

"""
Finally, please set the following variable to ``True`` to interact with the
datasets in 3D.
"""

#interactive = False
interactive = True


ren.zoom(1.5)
ren.reset_clipping_range()

if interactive:

    show_m.add_window_callback(win_callback)
    show_m.render()
    show_m.start()

else:

    window.record(ren, out_path='bundles_and_3_slices.png', size=(1200, 900),
                  reset_camera=False)

"""
.. figure:: bundles_and_3_slices.png
   :align: center

   A few bundles with interactive slicing.
"""

del show_m

"""

.. include:: ../links_names.inc

"""



#https://dipy.herokuapp.com/documentation/0.12.0.dev/examples_built/tracking_quick_start/#example-tracking-quick-start


"""
====================
Tracking Quick Start
====================

This example shows how to perform fast fiber tracking using dipy_
[Garyfallidis12]_.

We will use Constrained Spherical Deconvolution (CSD) [Tournier07]_ for local
reconstruction and then generate deterministic streamlines using the fiber
directions (peaks) from CSD and fractional anisotropic (FA) from DTI as a
stopping criteria for the tracking.

Let's load the necessary modules.
"""

import numpy as np
from dipy.tracking.local import LocalTracking, ThresholdTissueClassifier
from dipy.tracking.utils import random_seeds_from_mask
from dipy.reconst.dti import TensorModel
from dipy.reconst.csdeconv import (ConstrainedSphericalDeconvModel,
                                   auto_response)
from dipy.direction import peaks_from_model
from dipy.data import fetch_stanford_hardi, read_stanford_hardi, get_sphere
from dipy.segment.mask import median_otsu
from dipy.viz import actor, window
from dipy.io.image import save_nifti
from nibabel.streamlines import save as save_trk
from nibabel.streamlines import Tractogram
from dipy.tracking.streamline import Streamlines

"""
Enables/disables interactive visualization
"""

#interactive = False
interactive = True

"""
Load one of the available datasets with 150 gradients on the sphere and 10 b0s
"""

fetch_stanford_hardi()
img, gtab = read_stanford_hardi()

data = img.get_data()

"""
Create a brain mask. This dataset is a bit difficult to segment with the
default ``median_otsu`` parameters (see :ref:`example_brain_extraction_dwi`)
therefore we use here more advanced options.
"""

maskdata, mask = median_otsu(data, 3, 1, False,
                             vol_idx=range(10, 50), dilate=2)

"""
For the Constrained Spherical Deconvolution we need to estimate the response
function (see :ref:`example_reconst_csd`) and create a model.
"""

response, ratio = auto_response(gtab, data, roi_radius=10, fa_thr=0.7)

csd_model = ConstrainedSphericalDeconvModel(gtab, response)

"""
Next, we use ``peaks_from_model`` to fit the data and calculated the fiber
directions in all voxels.
"""

sphere = get_sphere('symmetric724')

csd_peaks = peaks_from_model(model=csd_model,
                             data=data,
                             sphere=sphere,
                             mask=mask,
                             relative_peak_threshold=.5,
                             min_separation_angle=25,
                             parallel=True)

"""
For the tracking part, we will use the fiber directions from the ``csd_model``
but stop tracking in areas where fractional anisotropy is low (< 0.1).
To derive the FA, used here as a stopping criterion, we would need to fit a
tensor model first. Here, we fit the tensor using weighted least squares (WLS).
"""

tensor_model = TensorModel(gtab, fit_method='WLS')
tensor_fit = tensor_model.fit(data, mask)

fa = tensor_fit.fa

"""
In this simple example we can use FA to stop tracking. Here we stop tracking
when FA < 0.1.
"""

tissue_classifier = ThresholdTissueClassifier(fa, 0.1)

"""
Now, we need to set starting points for propagating each track. We call those
seeds. Using ``random_seeds_from_mask`` we can select a specific number of
seeds (``seeds_count``) in each voxel where the mask ``fa > 0.3`` is true.
"""

seeds = random_seeds_from_mask(fa > 0.3, seeds_count=1)

"""
For quality assurance we can also visualize a slice from the direction field
which we will use as the basis to perform the tracking.
"""

ren = window.Renderer()
ren.add(actor.peak_slicer(csd_peaks.peak_dirs,
                          csd_peaks.peak_values,
                          colors=None))

if interactive:
    window.show(ren, size=(900, 900))
else:
    window.record(ren, out_path='/Users/ptm/desktop/Current_working_directory/DIPY/csd_direction_field.png', size=(900, 900))

##
##
##
import cv2 as cv2
# Plot Image
#%matplotlib inline
image_name = "/Users/ptm/desktop/Current_working_directory/DIPY/csd_direction_field.png" #Image to be used as query
def plotImage(image_location):
    image = cv2.imread(image_name)
    image = cv2.resize(image, (512,512))
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)); plt.axis('off')
    return
plotImage(image_name)
plt.show()
plt.clf()
##
##
##




"""
.. figure:: csd_direction_field.png
 :align: center

 **Direction Field (peaks)**

``EuDX`` [Garyfallidis12]_ is a fast algorithm that we use here to generate
streamlines. This algorithm is what is used here and the default option
when providing the output of peaks directly in LocalTracking.
"""

streamline_generator = LocalTracking(csd_peaks, tissue_classifier,
                                     seeds, affine=np.eye(4),
                                     step_size=0.5)

streamlines = Streamlines(streamline_generator)

"""
The total number of streamlines is shown below.
"""

print(len(streamlines))

"""
To increase the number of streamlines you can change the parameter
``seeds_count`` in ``random_seeds_from_mask``.

We can visualize the streamlines using ``actor.line`` or ``actor.streamtube``.
"""

ren.clear()
ren.add(actor.line(streamlines))

if interactive:
    window.show(ren, size=(900, 900))
else:
    print('Saving illustration as det_streamlines.png')
    window.record(ren, out_path='/Users/ptm/desktop/Current_working_directory/DIPY/det_streamlines.png', size=(900, 900))

##
##
##
import cv2 as cv2
# Plot Image
#%matplotlib inline
image_name = "/Users/ptm/desktop/Current_working_directory/DIPY/det_streamlines.png" #Image to be used as query
def plotImage(image_location):
    image = cv2.imread(image_name)
    image = cv2.resize(image, (512,512))
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)); plt.axis('off')
    return
plotImage(image_name)
plt.show()
plt.clf()
##
##
##


"""
.. figure:: det_streamlines.png
 :align: center

 **Deterministic streamlines using EuDX (new framework)**

To learn more about this process you could start playing with the number of
seed points or, even better, specify seeds to be in specific regions of interest
in the brain.

Save the resulting streamlines in a Trackvis (.trk) format and FA as
Nifti1 (.nii.gz).
"""

save_trk(Tractogram(streamlines, affine_to_rasmm=img.affine),
         '/Users/ptm/desktop/Current_working_directory/DIPY/det_streamlines.trk')

save_nifti('/Users/ptm/desktop/Current_working_directory/DIPY/fa_map.nii.gz', fa, img.affine)



##
##
##
import nibabel as nib
#newImage = join(dname, 'HARDI193_S0.nii.gz')
newImage = '/Users/ptm/desktop/Current_working_directory/DIPY/fa_map.nii.gz'
img = nib.load(newImage)
data = img.get_data()
import matplotlib.pyplot as plt
axial_middle = data.shape[2] // 2
plt.figure('Showing the datasets')
plt.subplot(1, 2, 1).set_axis_off()
plt.imshow(data[:, :, axial_middle].T, cmap='gray', origin='lower')
#plt.imshow(data[:, :, axial_middle, 0].T, cmap='gray', origin='lower')
#plt.subplot(1, 2, 2).set_axis_off()
#plt.imshow(data[:, :, axial_middle, 10].T, cmap='gray', origin='lower')
plt.show()
#plt.savefig('tensor_fa.png', bbox_inches='tight')
plt.clf()
##
##
##


"""
In Windows if you get a runtime error about frozen executable please start
your script by adding your code above in a ``main`` function and use:

``
if __name__ == '__main__':
    import multiprocessing
    multiprocessing.freeze_support()
    main()
``

References
----------

.. [Garyfallidis12] Garyfallidis E., "Towards an accurate brain tractography",
   PhD thesis, University of Cambridge, 2012.

.. [Tournier07] J-D. Tournier, F. Calamante and A. Connelly, "Robust
   determination of the fibre orientation distribution in diffusion MRI:
   Non-negativity constrained super-resolved spherical deconvolution",
   Neuroimage, vol. 35, no. 4, pp. 1459-1472, 2007.


.. include:: ../links_names.inc

"""

