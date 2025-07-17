import subprocess
import logging

MIRROR = "https://pypi.tuna.tsinghua.edu.cn/simple"


def drawLandmarks(image, results):
    import mediapipe.python.solutions as sol
    # Draw face connections
    sol.drawing_utils.draw_landmarks(
        image,
        results.face_landmarks,
        sol.holistic.FACEMESH_TESSELATION,
        landmark_drawing_spec=None,
        connection_drawing_spec=sol.drawing_styles.
        get_default_face_mesh_tesselation_style())
    sol.drawing_utils.draw_landmarks(
        image,
        results.face_landmarks,
        sol.holistic.FACEMESH_CONTOURS,
        landmark_drawing_spec=None,
        connection_drawing_spec=sol.drawing_styles.
        get_default_face_mesh_contours_style())
    # Draw pose connections
    sol.drawing_utils.draw_landmarks(
        image, results.pose_landmarks, sol.holistic.POSE_CONNECTIONS,
        sol.drawing_styles.get_default_pose_landmarks_style())
    # Draw left hand connections
    sol.drawing_utils.draw_landmarks(
        image, results.left_hand_landmarks, sol.holistic.HAND_CONNECTIONS,
        sol.drawing_styles.get_default_hand_landmarks_style(),
        sol.drawing_styles.get_default_hand_connections_style())
    # Draw right hand connections
    sol.drawing_utils.draw_landmarks(
        image, results.right_hand_landmarks, sol.holistic.HAND_CONNECTIONS,
        sol.drawing_styles.get_default_hand_landmarks_style(),
        sol.drawing_styles.get_default_hand_connections_style())


def extractLandmarks(x):
    res = {}
    if not x.pose_landmarks is None:
        a = x.pose_landmarks.landmark
        b = []
        for i in range(len(a)):
            b.append([a[i].x, a[i].y, a[i].z])
        res['body'] = b
    else:
        res['body'] = None
    if not x.left_hand_landmarks is None:
        a = x.left_hand_landmarks.landmark
        b = []
        for i in range(len(a)):
            b.append([a[i].x, a[i].y, a[i].z])
        res['rightHand'] = b
    else:
        res['rightHand'] = None
    if not x.right_hand_landmarks is None:
        a = x.right_hand_landmarks.landmark
        b = []
        for i in range(len(a)):
            b.append([a[i].x, a[i].y, a[i].z])
        res['leftHand'] = b
    else:
        res['leftHand'] = None
    if not x.face_landmarks is None:
        a = x.face_landmarks.landmark
        b = []
        for i in range(len(a)):
            b.append([a[i].x, a[i].y, a[i].z])
        res['face'] = b
    else:
        res['face'] = None
    return res


def generateNullLandmarks():
    res = {}
    res['body'] = None
    res['leftHand'] = None
    res['rightHand'] = None
    res['face'] = None
    return res


def testPackages(download=True):
    flag1 = False
    flag2 = False
    flag3 = False
    flag4 = False
    try:
        import mediapipe
    except ModuleNotFoundError:
        logging.error("Missing package mediapipe")
        flag1 = True

    try:
        import cv2
    except ModuleNotFoundError:
        logging.error("Missing package opencv-python")
        flag2 = True

    try:
        import pyautogui
    except ModuleNotFoundError:
        logging.error("Missing package PyAutoGUI")
        flag3 = True

    try:
        import numpy
    except ModuleNotFoundError:
        logging.error("Missing package numpy")
        flag4 = True

    if download and (flag1 or flag2 or flag3 or flag4):
        try:
            logging.info(
                "Downloading" +
                (" mediapipe==0.10.14" if flag1 else "") +
                (" opencv-python==4.10.0.84" if flag2 else "") +
                (" PyAutoGUI==0.9.54" if flag3 else "") +
                (" numpy==1.26.4" if flag4 else "")
            )
            res = subprocess.run(
                ['pip', 'install', '-i', MIRROR] +
                (['mediapipe==0.10.14'] if flag1 else []) +
                (['opencv-python==4.10.0.84'] if flag2 else []) +
                (['PyAutoGUI==0.9.54'] if flag3 else []) +
                (['numpy==1.26.4'] if flag4 else [])
            )
        except OSError as e:
            logging.error(f"Download Packages Error: {e}")
        if res.returncode != 0:
            logging.error(f"Download Packages Error: {res}")
        else:
            logging.info("Download Complete")

    return not (flag1 or flag2 or flag3 or flag4)