import cv2
import numpy as np
import time
from hand_tracker import HandTracker
from shape_renderer import draw_shape_glow
from ui import draw_buttons, check_button_hover, draw_hud, draw_crosshair, draw_hand_skeleton

def apply_dark_overlay(frame):
    return cv2.convertScaleAbs(frame, alpha=0.55, beta=0)

def draw_grid(frame, spacing=60):
    h, w = frame.shape[:2]
    color = (25, 35, 45)
    for x in range(0, w, spacing):
        cv2.line(frame, (x, 0), (x, h), color, 1)
    for y in range(0, h, spacing):
        cv2.line(frame, (0, y), (w, y), color, 1)

def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    tracker = HandTracker()

    shape = "CUBE"
    rot_x = rot_y = rot_z = 0.0
    scale = 100
    prev_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        h, w = frame.shape[:2]

        frame = apply_dark_overlay(frame)
        draw_grid(frame)

        landmarks = tracker.get_landmarks(frame)
        index_pos = (w // 2, h // 2)

        if landmarks:
            draw_hand_skeleton(frame, landmarks, frame.shape)
            (ix, iy), (tx, ty), distance, angle = tracker.get_index_thumb(landmarks, frame.shape)
            cx, cy = tracker.get_hand_center(landmarks, frame.shape)
            index_pos = (ix, iy)

            scale = int(np.interp(distance, [20, 300], [40, 300]))
            rot_z = angle
            rot_x = np.interp(cy, [0, h], [-60, 60])
            rot_y = np.interp(cx, [0, w], [-60, 60])

            cv2.line(frame, (ix, iy), (tx, ty), (60, 80, 100), 1, cv2.LINE_AA)

        draw_shape_glow(frame, shape, rot_x, rot_y, rot_z, scale, w//2, h//2)

        rects = draw_buttons(frame, shape, index_pos)
        hovered = check_button_hover(index_pos, rects)
        if hovered:
            shape = hovered

        draw_crosshair(frame, index_pos)

        now = time.time()
        fps = 1.0 / max(now - prev_time, 0.001)
        prev_time = now

        draw_hud(frame, shape, scale, rot_x, rot_y, rot_z, fps)

        cv2.imshow("3D Hand Tracker", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
