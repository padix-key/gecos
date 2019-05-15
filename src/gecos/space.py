# This source code is part of the Gecos package and is distributed
# under the 3-Clause BSD License. Please see 'LICENSE.rst' for further
# information.

__author__ = "Patrick Kunzmann"
__all__ = ["ColorSpace"]

from os.path import join, dirname, realpath
import itertools
import numpy as np
from .colors import lab_to_rgb


SPACE_FILE_NAME = join(dirname(realpath(__file__)), "space.npy")


class ColorSpace():

    def __init__(self, file_name=None):
        if file_name is None:
            file_name = SPACE_FILE_NAME
        
        l = np.arange(100)
        a = b = np.arange(-128,128)
        self._lab = np.zeros((100,256,256,3), dtype=int)
        self._lab[:,:,:,0] = l[:, np.newaxis, np.newaxis]
        self._lab[:,:,:,1] = a[np.newaxis, :, np.newaxis]
        self._lab[:,:,:,2] = b[np.newaxis, np.newaxis, :]

        with open(file_name, "rb") as file:
            self._space = np.load(file)

    def remove(self, mask):
        self._space &= ~mask
    
    def get_rgb_space(self):
        rgb = lab_to_rgb(self._lab)
        rgb[~self._space] = np.nan
        return rgb

    @property
    def space(self):
        return self._space.copy()

    @property
    def shape(self):
        return (256, 256)
    
    @property
    def lab(self):
        return self._lab.copy()

    @staticmethod
    def _generate(file_name=None):
        lab = np.zeros((100, 256, 256, 3), dtype=int)
        lab[:,:,:,0] = np.arange(100      )[:, np.newaxis, np.newaxis]
        lab[:,:,:,1] = np.arange(-128, 128)[np.newaxis, :, np.newaxis]
        lab[:,:,:,2] = np.arange(-128, 128)[np.newaxis, np.newaxis, :]
        
        rgb = lab_to_rgb(lab)
        space = np.ones((100, 256, 256), dtype=bool)
        space[np.isnan(rgb).any(axis=-1)] = False
        
        if file_name is None:
            file_name = SPACE_FILE_NAME
        with open(file_name, "wb") as file:
            np.save(file, space)