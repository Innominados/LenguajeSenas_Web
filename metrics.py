import math
import numpy as np
from scipy.spatial import ConvexHull
from mediapipe.python.solutions.hands import HandLandmark

def thumb_position_metric(hand_landmarks):
    if hand_landmarks:
        thumb_tip = hand_landmarks.landmark[HandLandmark.THUMB_TIP]
        base_index = hand_landmarks.landmark[HandLandmark.INDEX_FINGER_MCP]
        return np.linalg.norm(np.array([thumb_tip.x, thumb_tip.y]) - np.array([base_index.x, base_index.y]))
    return 0.0

def fingers_extended(hand_landmarks):
    if hand_landmarks:
        fingers_tips = [
            HandLandmark.INDEX_FINGER_TIP, 
            HandLandmark.MIDDLE_FINGER_TIP, 
            HandLandmark.RING_FINGER_TIP, 
            HandLandmark.PINKY_TIP
        ]
        fingers_pips = [
            HandLandmark.INDEX_FINGER_PIP, 
            HandLandmark.MIDDLE_FINGER_PIP, 
            HandLandmark.RING_FINGER_PIP, 
            HandLandmark.PINKY_PIP
        ]
        count = 0
        for tip, pip in zip(fingers_tips, fingers_pips):
            if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
                count += 1
        return count
    return 0

def distance_between_fingers(hand_landmarks):
    if hand_landmarks:
        distances = []
        fingers_tips = [
            HandLandmark.THUMB_TIP,
            HandLandmark.INDEX_FINGER_TIP,
            HandLandmark.MIDDLE_FINGER_TIP,
            HandLandmark.RING_FINGER_TIP,
            HandLandmark.PINKY_TIP
        ]
        for i in range(len(fingers_tips)):
            for j in range(i + 1, len(fingers_tips)):
                tip1 = hand_landmarks.landmark[fingers_tips[i]]
                tip2 = hand_landmarks.landmark[fingers_tips[j]]
                distance = np.linalg.norm(np.array([tip1.x, tip1.y]) - np.array([tip2.x, tip2.y]))
                distances.append(distance)
        return distances
    return [0.0] * 10

def angle_between(v1, v2):
    """ Calculate the angle in radians between vectors 'v1' and 'v2' """
    v1_u = v1 / np.linalg.norm(v1)
    v2_u = v2 / np.linalg.norm(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def angles_between_fingers(hand_landmarks):
    if hand_landmarks:
        fingers_indices = [
            HandLandmark.THUMB_TIP,
            HandLandmark.INDEX_FINGER_TIP,
            HandLandmark.MIDDLE_FINGER_TIP,
            HandLandmark.RING_FINGER_TIP,
            HandLandmark.PINKY_TIP
        ]
        wrist = hand_landmarks.landmark[HandLandmark.WRIST]
        angles = []
        for i in range(len(fingers_indices) - 1):
            finger1 = hand_landmarks.landmark[fingers_indices[i]]
            finger2 = hand_landmarks.landmark[fingers_indices[i + 1]]
            v1 = np.array([finger1.x - wrist.x, finger1.y - wrist.y])
            v2 = np.array([finger2.x - wrist.x, finger2.y - wrist.y])
            angle = angle_between(v1, v2)
            angles.append(angle)
        return angles
    return [0.0] * 4

def finger_curvature(hand_landmarks):
    if hand_landmarks:
        curvatures = []
        fingers_joints = [
            [HandLandmark.INDEX_FINGER_TIP, HandLandmark.INDEX_FINGER_DIP, HandLandmark.INDEX_FINGER_PIP],
            [HandLandmark.MIDDLE_FINGER_TIP, HandLandmark.MIDDLE_FINGER_DIP, HandLandmark.MIDDLE_FINGER_PIP],
            [HandLandmark.RING_FINGER_TIP, HandLandmark.RING_FINGER_DIP, HandLandmark.RING_FINGER_PIP],
            [HandLandmark.PINKY_TIP, HandLandmark.PINKY_DIP, HandLandmark.PINKY_PIP]
        ]
        for joints in fingers_joints:
            tip = hand_landmarks.landmark[joints[0]]
            dip = hand_landmarks.landmark[joints[1]]
            pip = hand_landmarks.landmark[joints[2]]
            curvature = (np.linalg.norm(np.array([tip.x - dip.x, tip.y - dip.y])) +
                         np.linalg.norm(np.array([dip.x - pip.x, dip.y - pip.y])))
            curvatures.append(curvature)
        return curvatures
    return [0.0] * 4

def distance_wrist_to_fingers(hand_landmarks):
    if hand_landmarks:
        distances = []
        wrist = hand_landmarks.landmark[HandLandmark.WRIST]
        fingers_tips = [
            HandLandmark.THUMB_TIP,
            HandLandmark.INDEX_FINGER_TIP,
            HandLandmark.MIDDLE_FINGER_TIP,
            HandLandmark.RING_FINGER_TIP,
            HandLandmark.PINKY_TIP
        ]
        for tip in fingers_tips:
            finger_tip = hand_landmarks.landmark[tip]
            distance = np.linalg.norm(np.array([finger_tip.x - wrist.x, finger_tip.y - wrist.y]))
            distances.append(distance)
        return distances
    return [0.0] * 5

def hand_symmetry(left_hand_landmarks, right_hand_landmarks):
    if left_hand_landmarks and right_hand_landmarks:
        left_distances = distance_between_fingers(left_hand_landmarks)
        right_distances = distance_between_fingers(right_hand_landmarks)
        symmetry = np.mean([abs(ld - rd) for ld, rd in zip(left_distances, right_distances)])
        return symmetry
    return 0.0

previous_landmarks = None

def finger_movement_speed(hand_landmarks, previous_landmarks, delta_time):
    if hand_landmarks and previous_landmarks:
        speeds = []
        for tip in [
            HandLandmark.THUMB_TIP,
            HandLandmark.INDEX_FINGER_TIP,
            HandLandmark.MIDDLE_FINGER_TIP,
            HandLandmark.RING_FINGER_TIP,
            HandLandmark.PINKY_TIP
        ]:
            current_tip = hand_landmarks.landmark[tip]
            previous_tip = previous_landmarks.landmark[tip]
            distance = np.linalg.norm(np.array([current_tip.x - previous_tip.x, current_tip.y - previous_tip.y]))
            speed = distance / delta_time
            speeds.append(speed)
        return speeds
    return [0.0] * 5

def hand_area(hand_landmarks):
    if hand_landmarks:
        points = np.array([
            [hand_landmarks.landmark[tip].x, hand_landmarks.landmark[tip].y]
            for tip in [
                HandLandmark.THUMB_TIP,
                HandLandmark.INDEX_FINGER_TIP,
                HandLandmark.MIDDLE_FINGER_TIP,
                HandLandmark.RING_FINGER_TIP,
                HandLandmark.PINKY_TIP,
                HandLandmark.WRIST
            ]
        ])
        hull = ConvexHull(points)
        return hull.volume  # or hull.area if you want the 2D area
    return 0.0

def finger_length_ratio(hand_landmarks):
    if hand_landmarks:
        lengths = []
        fingers_joints = [
            [HandLandmark.THUMB_TIP, HandLandmark.THUMB_IP, HandLandmark.THUMB_MCP],
            [HandLandmark.INDEX_FINGER_TIP, HandLandmark.INDEX_FINGER_DIP, HandLandmark.INDEX_FINGER_PIP, HandLandmark.INDEX_FINGER_MCP],
            [HandLandmark.MIDDLE_FINGER_TIP, HandLandmark.MIDDLE_FINGER_DIP, HandLandmark.MIDDLE_FINGER_PIP, HandLandmark.MIDDLE_FINGER_MCP],
            [HandLandmark.RING_FINGER_TIP, HandLandmark.RING_FINGER_DIP, HandLandmark.RING_FINGER_PIP, HandLandmark.RING_FINGER_MCP],
            [HandLandmark.PINKY_TIP, HandLandmark.PINKY_DIP, HandLandmark.PINKY_PIP, HandLandmark.PINKY_MCP]
        ]
        for joints in fingers_joints:
            length = sum(np.linalg.norm(
                np.array([hand_landmarks.landmark[joints[i]].x, hand_landmarks.landmark[joints[i]].y]) -
                np.array([hand_landmarks.landmark[joints[i+1]].x, hand_landmarks.landmark[joints[i+1]].y])
            ) for i in range(len(joints) - 1))
            lengths.append(length)
        return lengths
    return [0.0] * 5

def hand_orientation(hand_landmarks):
    if hand_landmarks:
        wrist = hand_landmarks.landmark[HandLandmark.WRIST]
        middle_finger_mcp = hand_landmarks.landmark[HandLandmark.MIDDLE_FINGER_MCP]
        vector = np.array([middle_finger_mcp.x - wrist.x, middle_finger_mcp.y - wrist.y])
        orientation = np.arctan2(vector[1], vector[0])
        return orientation
    return 0.0

def distance_between_fingertips(hand_landmarks):
    if hand_landmarks:
        distances = []
        fingers_tips = [
            HandLandmark.THUMB_TIP,
            HandLandmark.INDEX_FINGER_TIP,
            HandLandmark.MIDDLE_FINGER_TIP,
            HandLandmark.RING_FINGER_TIP,
            HandLandmark.PINKY_TIP
        ]
        for i in range(len(fingers_tips)):
            for j in range(i + 1, len(fingers_tips)):
                tip1 = hand_landmarks.landmark[fingers_tips[i]]
                tip2 = hand_landmarks.landmark[fingers_tips[j]]
                distance = np.linalg.norm(np.array([tip1.x, tip1.y]) - np.array([tip2.x, tip2.y]))
                distances.append(distance)
        return distances
    return [0.0] * 10  # 5 choose 2 = 10 distances

def calculate_keypoints_variation(keypoints_sequence):
    variations = []
    for i in range(1, len(keypoints_sequence)):
        prev_keypoints = keypoints_sequence[i-1]
        current_keypoints = keypoints_sequence[i]
        variation = np.linalg.norm(np.array(current_keypoints) - np.array(prev_keypoints))
        variations.append(variation)
    return variations

def is_static_or_moving(variations, threshold=0.1):
    mean_variation = np.mean(variations)
    return 1 if mean_variation < threshold else 0


def extract_metrics(results, previous_results, delta_time):
    metrics = {
        'thumb_distance_left': 0.0,
        'thumb_distance_right': 0.0,
        'fingers_extended_left': 0,
        'fingers_extended_right': 0,
        'finger_distances_left': [0.0] * 10,
        'finger_distances_right': [0.0] * 10,
        'angles_between_fingers_left': [0.0] * 4,
        'angles_between_fingers_right': [0.0] * 4,
        'finger_curvature_left': [0.0] * 4,
        'finger_curvature_right': [0.0] * 4,
        'distance_wrist_to_fingers_left': [0.0] * 5,
        'distance_wrist_to_fingers_right': [0.0] * 5,
        'hand_symmetry': 0.0,
        'finger_movement_speed_left': [0.0] * 5,
        'finger_movement_speed_right': [0.0] * 5,
        'hand_area_left': 0.0,
        'hand_area_right': 0.0,
        'finger_length_ratio_left': [0.0] * 5,
        'finger_length_ratio_right': [0.0] * 5,
        'hand_orientation_left': 0.0,
        'hand_orientation_right': 0.0,
        'fingertip_distances_left': [0.0] * 10,
        'fingertip_distances_right': [0.0] * 10
    }
    if results.left_hand_landmarks:
        metrics['thumb_distance_left'] = thumb_position_metric(results.left_hand_landmarks)
        metrics['fingers_extended_left'] = fingers_extended(results.left_hand_landmarks)
        metrics['finger_distances_left'] = distance_between_fingers(results.left_hand_landmarks)
        metrics['angles_between_fingers_left'] = angles_between_fingers(results.left_hand_landmarks)
        metrics['finger_curvature_left'] = finger_curvature(results.left_hand_landmarks)
        metrics['distance_wrist_to_fingers_left'] = distance_wrist_to_fingers(results.left_hand_landmarks)
        metrics['hand_area_left'] = hand_area(results.left_hand_landmarks)
        metrics['finger_length_ratio_left'] = finger_length_ratio(results.left_hand_landmarks)
        metrics['hand_orientation_left'] = hand_orientation(results.left_hand_landmarks)
        metrics['fingertip_distances_left'] = distance_between_fingertips(results.left_hand_landmarks)
        if previous_results:
            metrics['finger_movement_speed_left'] = finger_movement_speed(results.left_hand_landmarks, previous_results.left_hand_landmarks, delta_time)
    if results.right_hand_landmarks:
        metrics['thumb_distance_right'] = thumb_position_metric(results.right_hand_landmarks)
        metrics['fingers_extended_right'] = fingers_extended(results.right_hand_landmarks)
        metrics['finger_distances_right'] = distance_between_fingers(results.right_hand_landmarks)
        metrics['angles_between_fingers_right'] = angles_between_fingers(results.right_hand_landmarks)
        metrics['finger_curvature_right'] = finger_curvature(results.right_hand_landmarks)
        metrics['distance_wrist_to_fingers_right'] = distance_wrist_to_fingers(results.right_hand_landmarks)
        metrics['hand_area_right'] = hand_area(results.right_hand_landmarks)
        metrics['finger_length_ratio_right'] = finger_length_ratio(results.right_hand_landmarks)
        metrics['hand_orientation_right'] = hand_orientation(results.right_hand_landmarks)
        metrics['fingertip_distances_right'] = distance_between_fingertips(results.right_hand_landmarks)
        if previous_results:
            metrics['finger_movement_speed_right'] = finger_movement_speed(results.right_hand_landmarks, previous_results.right_hand_landmarks, delta_time)
    if results.left_hand_landmarks and results.right_hand_landmarks:
        metrics['hand_symmetry'] = hand_symmetry(results.left_hand_landmarks, results.right_hand_landmarks)
    return metrics
