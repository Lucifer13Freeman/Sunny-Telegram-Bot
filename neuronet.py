import cv2

import constants
import paths


face_proto = paths.PATH_FACE_PROTO
face_model = paths.PATH_FACE_MODEL

gender_proto = paths.PATH_GENDER_PROTO
gender_model = paths.PATH_GENDER_MODEL

age_proto = paths.PATH_AGE_PROTO
age_model = paths.PATH_AGE_MODEL

gender_list = [constants.IS_MALE, constants.IS_FEMALE]
age_list = [constants.AGE_0_2, constants.AGE_4_6, constants.AGE_8_12, 
            constants.AGE_15_20, constants.AGE_32_25, constants.AGE_38_43, 
            constants.AGE_48_53, constants.AGE_60_100]

face_net = cv2.dnn.readNet(face_model, face_proto)
gender_net = cv2.dnn.readNet(gender_model, gender_proto)
age_net = cv2.dnn.readNet(age_model, age_proto)

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)


def highlight(net, frame, treshold = 0.7):

    frame_opencv_dnn = frame.copy()
    height = frame_opencv_dnn.shape[0]
    width = frame_opencv_dnn.shape[1]

    blob = cv2.dnn.blobFromImage(frame_opencv_dnn, 1.0, (300, 300), [104, 117, 123], True, False)

    net.setInput(blob)
    detections = net.forward()
    faceboxes = []

    for i in range(detections.shape[2]):

        confidence = detections[0, 0, i, 2]

        if confidence > treshold:
            
            x1 = int(detections[0, 0, i, 3] * width)
            y1 = int(detections[0, 0, i, 4] * height)
            x2 = int(detections[0, 0, i, 5] * width)
            y2 = int(detections[0, 0, i, 6] * height)
            faceboxes.append([x1, y1, x2, y2])

    return frame_opencv_dnn, faceboxes


def resolve(image):

    video = cv2.VideoCapture(image if image else 0)
    padding = 20

    while cv2.waitKey(1) < 0:

        has_frame, frame = video.read()

        if not has_frame:

            cv2.waitKey()
            break

        result_img, faceboxes = highlight(face_net, frame)

        if not faceboxes: print(constants.NO_FACE_DETECTED)

        genders = []
        ages = []

        for facebox in faceboxes:
            
            face = frame[
		        max(0, facebox[1] - padding) : min(facebox[3] + padding, frame.shape[0] - 1),
                max(0, facebox[0] - padding) : min(facebox[2] + padding, frame.shape[1] - 1)
            ]

            blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB = False)
            
            gender_net.setInput(blob)
            gender_predictions = gender_net.forward()
            gender = gender_list[gender_predictions[0].argmax()]
            genders.append(gender)

            age_net.setInput(blob)
            age_predictions = age_net.forward()
            age = age_list[age_predictions[0].argmax()]
            ages.append(age)
            
        return [genders, ages]
