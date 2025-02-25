# Copyright 2020-2022 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""
Testing RandomCropWithBBox op in DE
"""
import numpy as np
import mindspore.dataset as ds
import mindspore.dataset.vision as vision
import mindspore.dataset.vision.utils as mode

from mindspore import log as logger
from util import config_get_set_seed, config_get_set_num_parallel_workers, save_and_check_md5, \
    helper_perform_ops_bbox, helper_test_visual_bbox, helper_invalid_bounding_box_test

GENERATE_GOLDEN = False

# Updated VOC dataset with correct annotations - DATA_DIR
DATA_DIR_VOC = "../data/dataset/testVOC2012_2"
# COCO dataset - DATA_DIR, ANNOTATION_DIR
DATA_DIR_COCO = ["../data/dataset/testCOCO/train/",
                 "../data/dataset/testCOCO/annotations/train.json"]


def test_random_crop_with_bbox_op_c(plot_vis=False):
    """
    Feature: RandomCropWithBBox op
    Description: Prints images and bboxes side by side with and without RandomCropWithBBox Op applied
    Expectation: Images and bboxes are printed side by side as expected
    """
    logger.info("test_random_crop_with_bbox_op_c")

    # Load dataset
    data_voc1 = ds.VOCDataset(
        DATA_DIR_VOC, task="Detection", usage="train", shuffle=False, decode=True)
    data_voc2 = ds.VOCDataset(
        DATA_DIR_VOC, task="Detection", usage="train", shuffle=False, decode=True)

    # define test OP with values to match existing Op UT
    test_op = vision.RandomCropWithBBox([512, 512], [200, 200, 200, 200])

    # map to apply ops
    data_voc2 = helper_perform_ops_bbox(data_voc2, test_op)

    helper_test_visual_bbox(plot_vis, data_voc1, data_voc2)


def test_random_crop_with_bbox_op_coco_c(plot_vis=False):
    """
    Feature: RandomCropWithBBox op
    Description: Prints images and bboxes side by side with and without RandomCropWithBBox Op applied with CocoDataset
    Expectation: Images and bboxes are printed side by side as expected
    """
    logger.info("test_random_crop_with_bbox_op_coco_c")
    # load dataset
    data_coco1 = ds.CocoDataset(DATA_DIR_COCO[0], annotation_file=DATA_DIR_COCO[1], task="Detection",
                                decode=True, shuffle=False)

    data_coco2 = ds.CocoDataset(DATA_DIR_COCO[0], annotation_file=DATA_DIR_COCO[1], task="Detection",
                                decode=True, shuffle=False)

    test_op = vision.RandomCropWithBBox([512, 512], [200, 200, 200, 200])

    data_coco2 = helper_perform_ops_bbox(data_coco2, test_op)

    helper_test_visual_bbox(plot_vis, data_coco1, data_coco2)


def test_random_crop_with_bbox_op2_c(plot_vis=False):
    """
    Feature: RandomCropWithBBox op
    Description: Prints images and bboxes side by side with and without RandomCropWithBBox Op applied with md5 check
    Expectation: Passes the md5 check test
    """
    logger.info("test_random_crop_with_bbox_op2_c")
    original_seed = config_get_set_seed(593447)
    original_num_parallel_workers = config_get_set_num_parallel_workers(1)

    # Load dataset
    data_voc1 = ds.VOCDataset(
        DATA_DIR_VOC, task="Detection", usage="train", shuffle=False, decode=True)
    data_voc2 = ds.VOCDataset(
        DATA_DIR_VOC, task="Detection", usage="train", shuffle=False, decode=True)

    # define test OP with values to match existing Op unit - test
    test_op = vision.RandomCropWithBBox(
        512, [200, 200, 200, 200], fill_value=(255, 255, 255))

    # map to apply ops
    data_voc2 = helper_perform_ops_bbox(data_voc2, test_op)
    data_voc2 = data_voc2.project(["image", "bbox"])

    filename = "random_crop_with_bbox_01_c_result.npz"
    save_and_check_md5(data_voc2, filename, generate_golden=GENERATE_GOLDEN)

    helper_test_visual_bbox(plot_vis, data_voc1, data_voc2)

    # Restore config setting
    ds.config.set_seed(original_seed)
    ds.config.set_num_parallel_workers(original_num_parallel_workers)


def test_random_crop_with_bbox_op3_c(plot_vis=False):
    """
    Feature: RandomCropWithBBox op
    Description: Prints images and bboxes side by side with and without RandomCropWithBBox Op applied with padding_mode
    Expectation: Images and bboxes are printed side by side as expected
    """
    logger.info("test_random_crop_with_bbox_op3_c")

    # Load dataset
    data_voc1 = ds.VOCDataset(
        DATA_DIR_VOC, task="Detection", usage="train", shuffle=False, decode=True)
    data_voc2 = ds.VOCDataset(
        DATA_DIR_VOC, task="Detection", usage="train", shuffle=False, decode=True)

    # define test OP with values to match existing Op unit - test
    test_op = vision.RandomCropWithBBox(
        512, [200, 200, 200, 200], padding_mode=mode.Border.EDGE)

    # map to apply ops
    data_voc2 = helper_perform_ops_bbox(data_voc2, test_op)

    helper_test_visual_bbox(plot_vis, data_voc1, data_voc2)


def test_random_crop_with_bbox_op_edge_c(plot_vis=False):
    """
    Feature: RandomCropWithBBox op
    Description: Prints images and bboxes side by side with and without RandomCropWithBBox Op applied on edge case
    Expectation: Passes the dynamically generated edge case
    """
    logger.info("test_random_crop_with_bbox_op_edge_c")

    # Load dataset
    data_voc1 = ds.VOCDataset(
        DATA_DIR_VOC, task="Detection", usage="train", shuffle=False, decode=True)
    data_voc2 = ds.VOCDataset(
        DATA_DIR_VOC, task="Detection", usage="train", shuffle=False, decode=True)

    # define test OP with values to match existing Op unit - test
    test_op = vision.RandomCropWithBBox(
        512, [200, 200, 200, 200], padding_mode=mode.Border.EDGE)

    # maps to convert data into valid edge case data
    data_voc1 = helper_perform_ops_bbox(data_voc1, None, True)

    # Test Op added to list of Operations here
    data_voc2 = helper_perform_ops_bbox(data_voc2, test_op, True)

    helper_test_visual_bbox(plot_vis, data_voc1, data_voc2)


def test_random_crop_with_bbox_op_invalid_c():
    """
    Feature: RandomCropWithBBox op
    Description: Test RandomCropWithBBox Op on invalid constructor parameters
    Expectation: Error is raised as expected
    """
    logger.info("test_random_crop_with_bbox_op_invalid_c")

    # Load dataset
    data_voc2 = ds.VOCDataset(
        DATA_DIR_VOC, task="Detection", usage="train", shuffle=False, decode=True)

    try:
        # define test OP with values to match existing Op unit - test
        test_op = vision.RandomCropWithBBox([512, 512, 375])

        # map to apply ops
        data_voc2 = helper_perform_ops_bbox(data_voc2, test_op)

        for _ in data_voc2.create_dict_iterator(num_epochs=1):
            break
    except TypeError as err:
        logger.info("Got an exception in DE: {}".format(str(err)))
        assert "Size should be a single integer" in str(err)


def test_random_crop_with_bbox_op_bad_c():
    """
    Feature: RandomCropWithBBox op
    Description: Test RandomCropWithBBox Op with invalid bounding boxes
    Expectation: Multiple errors are caught as expected
    """
    logger.info("test_random_crop_with_bbox_op_bad_c")
    test_op = vision.RandomCropWithBBox([512, 512], [200, 200, 200, 200])

    helper_invalid_bounding_box_test(DATA_DIR_VOC, test_op)


def test_random_crop_with_bbox_op_bad_padding():
    """
    Feature: RandomCropWithBBox op
    Description: Test RandomCropWithBBox Op on invalid constructor parameters for padding
    Expectation: Error is raised as expected
    """
    logger.info("test_random_crop_with_bbox_op_invalid_c")

    data_voc2 = ds.VOCDataset(
        DATA_DIR_VOC, task="Detection", usage="train", shuffle=False, decode=True)

    try:
        test_op = vision.RandomCropWithBBox([512, 512], padding=-1)

        data_voc2 = helper_perform_ops_bbox(data_voc2, test_op)

        for _ in data_voc2.create_dict_iterator(num_epochs=1):
            break
    except ValueError as err:
        logger.info("Got an exception in DE: {}".format(str(err)))
        assert "Input padding is not within the required interval of [0, 2147483647]." in str(
            err)

    try:
        test_op = vision.RandomCropWithBBox(
            [512, 512], padding=[16777216, 16777216, 16777216, 16777216])

        data_voc2 = helper_perform_ops_bbox(data_voc2, test_op)

        for _ in data_voc2.create_dict_iterator(num_epochs=1):
            break
    except RuntimeError as err:
        logger.info("Got an exception in DE: {}".format(str(err)))
        assert "padding size is three times bigger than the image size" in str(
            err)


def test_random_crop_with_bbox_padded_dataset():
    """
    Feature: RandomCropWithBBox op
    Description: RandomCropWithBBox need to copy its input image and image bbox, otherwise numpy memory will be reused
    Expectation: Images and bboxes are transformed as expected
    """
    original_seed = ds.config.get_seed()
    ds.config.set_seed(1234)
    # load dataset
    dataset = ds.CocoDataset(DATA_DIR_COCO[0], annotation_file=DATA_DIR_COCO[1], task="Detection",
                             decode=True, shuffle=True, extra_metadata=True, num_samples=2)

    for data in dataset.create_dict_iterator(output_numpy=True, num_epochs=1):
        image_data = data['image']
        bbox_data = data['bbox']
        break

    padded_samples = [{'image': image_data, 'bbox': bbox_data, 'category_id': np.zeros((2, 1), np.uint32),
                       'iscrowd': np.zeros((2, 1), np.uint32), '_meta-filename': np.array('0', dtype=str)}]

    padded_ds = ds.PaddedDataset(padded_samples)
    dataset = dataset + padded_ds
    dataset = dataset.repeat(5)

    randomcrop_op = vision.RandomCropWithBBox(size=(300, 300), padding=[200, 200, 200, 200],
                                              pad_if_needed=True, fill_value=(1, 1, 0), padding_mode=vision.Border.EDGE)
    dataset = dataset.map(input_columns=["image", "bbox"], operations=randomcrop_op, num_parallel_workers=1)
    dataset = dataset.map(input_columns=["image", "bbox"], operations=randomcrop_op, num_parallel_workers=1)

    for data in dataset.create_dict_iterator(output_numpy=True, num_epochs=1):
        pass

    ds.config.set_seed(original_seed)


if __name__ == "__main__":
    test_random_crop_with_bbox_op_c(plot_vis=True)
    test_random_crop_with_bbox_op_coco_c(plot_vis=True)
    test_random_crop_with_bbox_op2_c(plot_vis=True)
    test_random_crop_with_bbox_op3_c(plot_vis=True)
    test_random_crop_with_bbox_op_edge_c(plot_vis=True)
    test_random_crop_with_bbox_op_invalid_c()
    test_random_crop_with_bbox_op_bad_c()
    test_random_crop_with_bbox_op_bad_padding()
    test_random_crop_with_bbox_padded_dataset()
