# -*- coding: utf-8 -*
import scipy.ndimage as ndimg
from imagepy.core.engine import Simple
from skimage.morphology import skeletonize_3d
from imagepy.ipyalg import find_maximum, watershed
import numpy as np

class Dilation(Simple):
    """Dilation: derived from imagepy.core.engine.Filter """
    title = 'Dilation 3D'
    note = ['all', 'stack3d']
    para = {'r':3}
    view = [(int, (1,15), 0, 'r', 'r', 'pix')]

    def run(self, ips, imgs, para = None):
        strc = np.ones((para['r'], para['r'],para['r']), dtype=np.uint8)
        imgs[:] = ndimg.binary_dilation(imgs, strc)
        imgs *= 255

class Erosion(Simple):
    """Dilation: derived from imagepy.core.engine.Filter """
    title = 'Erosion 3D'
    note = ['all', 'stack3d']
    para = {'r':3}
    view = [(int, (1,15), 0, 'r', 'r', 'pix')]

    def run(self, ips, imgs, para = None):
        strc = np.ones((para['r'], para['r'], para['r']), dtype=np.uint8)
        imgs[:] = ndimg.binary_erosion(imgs, strc)
        imgs *= 255

class Opening(Simple):
    """Dilation: derived from imagepy.core.engine.Filter """
    title = 'Opening 3D'
    note = ['all', 'stack3d']
    para = {'r':3}
    view = [(int, (1,15), 0, 'r', 'r', 'pix')]

    def run(self, ips, imgs, para = None):
        strc = np.ones((para['r'], para['r'], para['r']), dtype=np.uint8)
        imgs[:] = ndimg.binary_opening(imgs, strc)
        imgs *= 255

class Closing(Simple):
    """Dilation: derived from imagepy.core.engine.Filter """
    title = 'Closing 3D'
    note = ['all', 'stack3d']
    para = {'r':3}
    view = [(int, (1,15), 0, 'r', 'r', 'pix')]

    def run(self, ips, imgs, para = None):
        strc = np.ones((para['r'], para['r'], para['r']), dtype=np.uint8)
        imgs[:] = ndimg.binary_closing(imgs, strc)
        imgs *= 255

class FillHole(Simple):
    """Dilation: derived from imagepy.core.engine.Filter """
    title = 'Fill Holes 3D'
    note = ['all', 'stack3d']


    def run(self, ips, imgs, para = None):
        imgs[:] = ndimg.binary_fill_holes(imgs)
        imgs *= 255

class Skeleton3D(Simple):
    title = 'Skeleton 3D'
    note = ['all', 'stack3d']

    #process
    def run(self, ips, imgs, para = None):
        imgs[skeletonize_3d(imgs>0)==0] = 0

class Distance3D(Simple):
    title = 'Distance 3D'
    note = ['all', 'stack3d']

    #process
    def run(self, ips, imgs, para = None):
        dismap = ndimg.distance_transform_edt(imgs>0)
        imgs[:] = np.clip(dismap, ips.range[0], ips.range[1])

class Watershed(Simple):
    """Mark class plugin with events callback functions"""
    title = 'Binary Watershed 3D'
    note = ['8-bit', 'stack3d']


    para = {'tor':2, 'con':False}
    view = [(int, (0,255), 0, 'tolerance', 'tor', 'value'),
            (bool, 'full connectivity', 'con')]

    ## TODO: Fixme!
    def run(self, ips, imgs, para = None):
        dist = -ndimg.distance_transform_edt(imgs)
        pts = find_maximum(dist, para['tor'], False)
        buf = np.zeros(imgs.shape, dtype=np.uint16)
        buf[pts[:,0], pts[:,1], pts[:,2]] = 1
        markers, n = ndimg.label(buf, np.ones((3,3, 3)))
        line = watershed(dist, markers, line=True, conn=para['con']+1)
        imgs[line==0] = 0

plgs = [Dilation, Erosion, Opening, Closing, '-', FillHole, Skeleton3D, '-', Distance3D, Watershed]