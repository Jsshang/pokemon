#!/usr/bin/env python

# --------------------------------------------------------
# Tensorflow Faster R-CNN
# Licensed under The MIT License [see LICENSE for details]
# Written by Xinlei Chen, based on code from Ross Girshick
# --------------------------------------------------------

"""
Demo script showing detections in sample images.

See README.md for installation instructions before running.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import os

import cv2
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from lib.config import config as cfg
from lib.utils.nms_wrapper import nms
from lib.utils.test import im_detect
from lib.nets.resnet_v1 import resnetv1
#from lib.nets.vgg16 import vgg16
from lib.utils.timer import Timer

CLASSES = ('__background__', 'pikachu', 'charizard', 'bulbasaur', 'blastoise', 'eevee', 'lapras', 'lucario'  # always index 0
                         )

plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']

#NETS = {'vgg16': ('vgg16_faster_rcnn_iter_20000.ckpt',), 'res101': ('res101_faster_rcnn_iter_110000.ckpt',)}
NETS = {'vgg16': ('vgg16_faster_rcnn_iter_20000.ckpt',), 'res101': ('res101_faster_rcnn_iter_30000.ckpt',)}
DATASETS = {'pascal_voc': ('voc_2007_trainval',), 'pascal_voc_0712': ('voc_2007_trainval+voc_2012_trainval',)}


def vis_detections(im, class_name, dets, thresh=0.5):
    """Draw detected bounding boxes."""
    inds = np.where(dets[:, -1] >= thresh)[0]
    if len(inds) == 0:
        return
    if class_name == 'pikachu':
        class_Cname = "皮卡丘"
    elif class_name == 'charizard':
        class_Cname = "喷火龙"
    elif class_name == 'bulbasaur':
        class_Cname = "妙蛙种子"
    elif class_name == 'blastoise':
        class_Cname = "水箭龟"
    elif class_name == 'eevee':
        class_Cname = "伊布"
    elif class_name == 'lapras':
        class_Cname = "乘龙"
    elif class_name == 'lucario':
        class_Cname = "路卡利欧"


    im = im[:, :, (2, 1, 0)]
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.imshow(im, aspect='equal')
    for i in inds:
        bbox = dets[i, :4]
        score = dets[i, -1]

        ax.add_patch(
            plt.Rectangle((bbox[0], bbox[1]),
                          bbox[2] - bbox[0],
                          bbox[3] - bbox[1], fill=False,
                          edgecolor='red', linewidth=3.5)
        )
        ax.text(bbox[0], bbox[1] - 2,
                '{:s} {:.3f}'.format(class_Cname, score),
                bbox=dict(facecolor='blue', alpha=0.5),
                fontsize=22, color='white')

    ax.set_title(('{} detections with '
                  'p({} | box) >= {:.1f}').format(class_Cname, class_Cname,
                                                  thresh),
                 fontsize=14)
    plt.axis('off')
    plt.tight_layout()
    plt.draw()


def demo(sess, net, image_name):
    """Detect object classes in an image using pre-computed object proposals."""

    # Load the demo image
    im_file = os.path.join(cfg.FLAGS2["data_dir"], 'demo', image_name)
    im = cv2.imread(im_file)

    # Detect all object classes and regress object bounds
    timer = Timer()
    timer.tic()
    scores, boxes = im_detect(sess, net, im)
    timer.toc()
    print('Detection took {:.3f}s for {:d} object proposals'.format(timer.total_time, boxes.shape[0]))
    # Visualize detections for each class
    CONF_THRESH = 0.5
    NMS_THRESH = 0.5
    for cls_ind, cls in enumerate(CLASSES[1:]):
        cls_ind += 1  # because we skipped background
        cls_boxes = boxes[:, 4 * cls_ind:4 * (cls_ind + 1)]
        cls_scores = scores[:, cls_ind]
        dets = np.hstack((cls_boxes,
                          cls_scores[:, np.newaxis])).astype(np.float32)
        keep = nms(dets, NMS_THRESH)
        dets = dets[keep, :]
        vis_detections(im, cls, dets, thresh=CONF_THRESH)


def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='Tensorflow Faster R-CNN demo')
    parser.add_argument('--net', dest='demo_net', help='Network to use [vgg16 res101]',
                        choices=NETS.keys(), default='res101')
    parser.add_argument('--dataset', dest='dataset', help='Trained dataset [pascal_voc pascal_voc]',
                        choices=DATASETS.keys(), default='pascal_voc')
    args = parser.parse_args()

    return args


if __name__ == '__main__':
    args = parse_args()

    # model path
    demonet = args.demo_net
    dataset = args.dataset
    #tfmodel = os.path.join('output', demonet, DATASETS[dataset][0], 'default', NETS[demonet][0])
    tfmodel = r'D:\pycharm\resnet101-Multiple-3d\default\voc_2007_trainval\default\resnet101_faster_rcnn_iter_30000.ckpt'

    if not os.path.isfile(tfmodel + '.meta'):
        print(tfmodel)
        raise IOError(('{:s} not found.\nDid you download the proper networks from '
                       'our server and place them properly?').format(tfmodel + '.meta'))

    # set config
    tfconfig = tf.ConfigProto(allow_soft_placement=True)
    tfconfig.gpu_options.allow_growth = True

    # init session
    sess = tf.Session(config=tfconfig)
    # load network
    # if demonet == 'vgg16':
    #     net = vgg16(batch_size=1)
    if demonet == 'res101':
         net = resnetv1(batch_size=1, num_layers=101)
    else:
        raise NotImplementedError
    net.create_architecture(sess, "TEST", 8,
                            tag='default', anchor_scales=[8, 16, 32])
    
    saver = tf.train.Saver()
    saver.restore(sess, tfmodel)

    print('Loaded network {:s}'.format(tfmodel))

    for i in range(36, 64):
        im_add = str(i) + ".jpg"

        #
        # #im_names = ['1.jpg', '2.jpg','3.jpg','4.jpg','5.jpg','6.jpg', '7.jpg','8.jpg','9.jpg'
        # #          ]
        # for im_name in im_names:
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        # print('Demo for data/demo/{}'.format(im_name))
        # demo(sess, net, im_name)
        print('Demo for data/demo/{}'.format(im_add))
        demo(sess, net, im_add)

    plt.show()
