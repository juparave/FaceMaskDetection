## detector de Cubrebocas
## para correrlo en ambiente python > 3.7
## $ python opencv_dnn_infer.py --img-mode 0 --video-path 0

from datetime import datetime

import threading

import sys
from threading import Event

import cv2
import argparse
import numpy as np

import utils.tvservice as tvservice
from utils import is_raspberrypi
from utils.anchor_generator import generate_anchors
from utils.anchor_decode import decode_bbox
from utils.nms import single_class_non_max_suppression

if is_raspberrypi():
    from utils.buzzer import do_buzzer
    from utils.led import do_led

    print("Running on PI!")

feature_map_sizes = [[33, 33], [17, 17], [9, 9], [5, 5], [3, 3]]
anchor_sizes = [[0.04, 0.056], [0.08, 0.11], [0.16, 0.22], [0.32, 0.45], [0.64, 0.72]]
anchor_ratios = [[1, 0.62, 0.42]] * 5

anchors = generate_anchors(feature_map_sizes, anchor_sizes, anchor_ratios)
anchors_exp = np.expand_dims(anchors, axis=0)

id2class = {0: 'Mascarilla', 1: 'SinMasc'}
colors = ((0, 255, 0), (255, 0, 0))


def show_status():
    # ref: https://programtalk.com/vs2/?source=python/2635/pyLCI/apps/raspberrypi/tvservice/main.py
    try:
        status = tvservice.status()
    except (IndexError, KeyError) as ex:
        print("Unknown video mode")
        return False
    mode = status['mode']
    if mode == 'UNKNOWN':
        print("Unknown mode")
        return False
    if mode == 'NONE':
        print("No video out", "active")
        return False
    if mode in ('HDMI', 'TV'):
        print("Video out active")
        return True


def get_outputs_names(net):
    # Get the names of all the layers in the network
    layers_names = net.getLayerNames()
    # Get the names of the output layers, i.e. the layers with unconnected outputs
    return [layers_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]


def inference(net, image, conf_thresh=0.5, iou_thresh=0.4, target_shape=(160, 160), draw_result=True, led_event=None,
              buzzer_event=None):
    height, width, _ = image.shape
    blob = cv2.dnn.blobFromImage(image, scalefactor=1 / 255.0, size=target_shape)
    net.setInput(blob)
    y_bboxes_output, y_cls_output = net.forward(get_outputs_names(net))
    # remove the batch dimension, for batch is always 1 for inference.
    y_bboxes = decode_bbox(anchors_exp, y_bboxes_output)[0]
    y_cls = y_cls_output[0]
    # To speed up, do single class NMS, not multiple classes NMS.
    bbox_max_scores = np.max(y_cls, axis=1)
    bbox_max_score_classes = np.argmax(y_cls, axis=1)

    # keep_idx is the alive bounding box after nms.
    keep_idxs = single_class_non_max_suppression(y_bboxes, bbox_max_scores, conf_thresh=conf_thresh,
                                                 iou_thresh=iou_thresh)
    # keep_idxs  = cv2.dnn.NMSBoxes(y_bboxes.tolist(), bbox_max_scores.tolist(), conf_thresh, iou_thresh)[:,0]
    masked = 0
    tl = round(0.002 * (height + width) * 0.5) + 1  # line thickness
    for idx in keep_idxs:
        conf = float(bbox_max_scores[idx])
        class_id = bbox_max_score_classes[idx]
        if class_id == 0:
            masked += 1
        else:
            if is_raspberrypi():
                do_buzzer(buzzer_event)
                do_led(led_event)
                pass
        bbox = y_bboxes[idx]
        # clip the coordinate, avoid the value exceed the image boundary.
        xmin = max(0, int(bbox[0] * width))
        ymin = max(0, int(bbox[1] * height))
        xmax = min(int(bbox[2] * width), width)
        ymax = min(int(bbox[3] * height), height)
        if draw_result:
            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), colors[class_id], thickness=tl)
            cv2.putText(image, "%s: %.2f" % (id2class[class_id], conf), (xmin + 2, ymin - 2),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, colors[class_id])
    return image, len(keep_idxs), masked


def run_on_video(Net, video_path, conf_thresh=0.5, led_event=None, buzzer_event=None):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("Falla al abrir video.")
        return
    status = True
    show_status_status = None  # is a monitor connected?
    # add date to frame
    font = cv2.FONT_HERSHEY_SIMPLEX
    while status:
        status, img_raw = cap.read()
        if not status:
            print("Fin de proceso !!!")
            break
        date_text = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
        img_raw = cv2.rectangle(img_raw, pt1=(0, 0), pt2=(850, 59), color=(0, 0, 0), thickness=-1)
        img_raw = cv2.putText(img_raw, date_text, (10, 40), font, 1, (0, 255, 255), 2, cv2.LINE_AA)
        img_raw = cv2.cvtColor(img_raw, cv2.COLOR_BGR2RGB)
        img_raw, faces, masked = inference(Net, img_raw, target_shape=(260, 260), conf_thresh=conf_thresh,
                                           led_event=led_event, buzzer_event=buzzer_event)
        # write how many faces where found
        img_raw = cv2.putText(img_raw, "Caras {}".format(faces), (400, 40), font, 1, (0, 255, 255), 2, cv2.LINE_AA)
        img_raw = cv2.putText(img_raw, "Mascarillas {}".format(masked), (550, 40), font, 1, (255, 0, 255), 2,
                              cv2.LINE_AA)
        if show_status_status is None:
            show_status_status = show_status()

        if show_status_status:
            try:
                cv2.imshow('image', img_raw[:, :, ::-1])
            except cv2.error as ex:
                print("Error al mostrar video: {}".format(ex))
            cv2.waitKey(1)
        print("faces: {}, masked: {}".format(faces, masked), end='\r')
    cv2.destroyAllWindows()


def do_local_tests(Net):
    from os import listdir
    from os.path import isfile, join
    test_path = 'tests'
    onlyjpgfiles = [f for f in listdir(test_path) if isfile(join(test_path, f)) and 'jpg' in f]

    for jpg in onlyjpgfiles:
        img = cv2.imread(join(test_path, jpg))
        if img is not None:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            result, faces, masked = inference(Net, img, target_shape=(260, 260))
            print("For {} \n \t Faces: {} \t Masks: {}".format(jpg, faces, masked))

    print("\nEnd")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detector de Cubrebocas")
    parser.add_argument('--proto', type=str, default='models/face_mask_detection.prototxt', help='prototxt path')
    parser.add_argument('--model', type=str, default='models/face_mask_detection.caffemodel', help='model path')
    parser.add_argument('--img-mode', type=int, default=0, help=u'1 para correr en fotografía, 0 para video.')
    parser.add_argument('--img-path', type=str, default='img/demo2.jpg', help=u'fotografía a analizar.')
    parser.add_argument('--video-path', type=str, default='0', help=u'video, `0` usar cámara.')
    parser.add_argument('--test', type=str, default='', help=u'pruebas locales.')
    args = parser.parse_args()

    try:
        # hide cursor
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

        # create threads events
        led_event = threading.Event()
        buzzer_event = threading.Event()

        Net = cv2.dnn.readNet(args.model, args.proto)
        if args.test:
            do_local_tests(Net)
            exit(0)

        if args.img_mode:
            img = cv2.imread(args.img_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            result, faces, masked = inference(Net, img, target_shape=(260, 260))
            cv2.namedWindow('detect', cv2.WINDOW_NORMAL)
            cv2.imshow('detect', result[:, :, ::-1])
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            video_path = args.video_path
            if args.video_path == '0':
                video_path = 0
            if args.video_path == '1':
                video_path = 1

            # blink led twice to signal start on video
            do_led(led_event, True)

            run_on_video(Net, video_path, conf_thresh=0.5, led_event=led_event, buzzer_event=buzzer_event)
    finally:
        # show cursor
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()
