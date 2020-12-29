# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/03_geometry.ipynb (unless otherwise specified).

__all__ = ['PolarToCartesianWarp', 'CameraRadarCoordinateTransform', 'compute_radar_intrinsic_matrix']

# Cell

import tensorflow as tf
from tensorflow.keras import models, layers
import tensorflow_addons as tfa

import numpy as np

from .radar import v1_constants

# Cell

class PolarToCartesianWarp(layers.Layer):
    """Differentiable Polar Image to Cartersian Mapping
    This is a Tensorflow Keras Layer and
    expects a batch of input with shape [n, r, az, c]

    Running eagerly is supported as well.
    For single example input, use expanddims or newaxis.
    """
    def __init__(self, full=True, scale=1.):
        super(PolarToCartesianWarp, self).__init__()
        self.full = full
        self.scale = scale

    def build(self, input_shape):
        range_bins, angle_bins = input_shape[1:3]
        xx = np.arange(-range_bins, range_bins)/range_bins
        yy = 1 - np.arange(0, range_bins)/range_bins

        mg = np.meshgrid(xx, yy)

        rr = range_bins - np.sqrt(mg[0]**2 + mg[1]**2) * range_bins
        tt = angle_bins - np.arctan2(mg[1], mg[0])/np.pi*angle_bins

        self.warp = tf.Variable(
            np.stack([tt, rr], axis=-1)[np.newaxis, ...],
            trainable=False,
            dtype=tf.float32
        )

        self.warp = tf.repeat(self.warp, repeats=input_shape[0], axis=0)

    def call(self, inputs):
        return tfa.image.resampler(inputs, self.warp)

# Cell

class CameraRadarCoordinateTransform:
    """Stub Not implemented yet"""
    def __init__(self, camera_f, camera_p, radar_f, radar_p):
        self.camera_f = camera_f
        self.camera_p = camera_p
        self.radar_f = radar_f
        self.radar_p = radar_p


    def camera2world(self, uv, depth=None):
        """Projects camera pixel coordinates u, v, depth to world coordinates
        uv can be n x 2 lists or n x 3
        if uv is n x 2, depth image needs to be provided.
        Depth will be retreived using nearest neighbor interpolation
        """
        pass

    def world2camera(self, xyz):
        pass

    def radar2world(self, xy, h=None):
        pass

    def world2radar(self, xyz):
        pass

    def camera2radar(self, uv, depth=None):
        """Convenience function combining `camera2world` and `world2radar`"""
        xyz = self.camera2world(uv, depth)
        radar_xy = self.world2camera(xyz)

        return radar_xy

    def radar2camera(self, radar_xy, radar_height=None):
        """Convenience function combining `radar2world` and `world2camera`"""
        xyz = self.radar2world(radar_xy, radar_height)
        uvz = self.world2camera(xyz)

        return uvz

# Cell
def compute_radar_intrinsic_matrix(radarframe):
    """Radar frame needs to provide max_range and range_nbins"""
    scale = 1/radarframe.max_range
    nbins = radarframe.range_nbins
    if radarframe.flipped:
        f = np.array([
            [nbins, 0,      nbins],
            [0,     -nbins, nbins],
            [0,     0,      1./scale]
        ])
    else:
        f = np.array([
            [nbins, 0,      nbins],
            [0,     -nbins, nbins],
            [0,     0,      1/scale]
        ])

    return scale * f