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
