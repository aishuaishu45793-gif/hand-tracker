import cv2
import numpy as np

BUTTONS = ["CUBE", "PYRAMID", "SPHERE"]
BTN_W, BTN_H = 130, 38
BTN_Y = 12
BTN_GAP = 12

SHAPE_COLORS = {
    "CUBE":    (0, 255, 255),
    "PYRAMID": (0, 255, 120),
    "SPHERE":  (180, 80, 255),
}

def get_button_rects(frame_w):
    rects = {}
    total = len(BUTTONS) * BTN_W + (len(BUTTONS)-1) * BTN_GAP
    start_x = (frame_w - total) // 2
    for i, name in enumerate(BUTTONS):
        x = start_x + i * (BTN_W + BTN_GAP)
        rects[name] = (x, BTN_Y, BTN_W, BTN_H)
    return rects

def draw_buttons(frame, active_shape, index_pos):
    h_f, w_f = frame.shape[:2]
    rects = get_button_rects(w_f)
    for name, (x, y, bw, bh) in rects.items():
        color = SHAPE_COLORS[name]
        is_active = (name == active_shape)

        overlay = frame.copy()
        cv2.rectangle(overlay, (x, y), (x+bw, y+bh), (20, 20, 30), -1)
        cv2.addWeighted(overlay, 0.75, frame, 0.25, 0, frame)

        border_color = color if is_active else (60, 60, 80)
        cv2.rectangle(frame, (x, y), (x+bw, y+bh), border_color, 2 if is_active else 1)

        if is_active:
            tint = frame.copy()
            cv2.rectangle(tint, (x+1, y+1), (x+bw-1, y+bh-1),
                          tuple(int(c*0.25) for c in color), -1)
            cv2.addWeighted(tint, 0.5, frame, 0.5, 0, frame)

        text_color = color if is_active else (160, 160, 180)
        font = cv2.FONT_HERSHEY_SIMPLEX
        (tw, th), _ = cv2.getTextSize(name, font, 0.52, 1)
        tx = x + (bw - tw) // 2
        ty = y + (bh + th) // 2 - 2
        cv2.putText(frame, name, (tx, ty), font, 0.52, text_color, 1, cv2.LINE_AA)

    return rects

def check_button_hover(index_pos, rects):
    ix, iy = index_pos
    for name, (x, y, bw, bh) in rects.items():
        if x <= ix <= x+bw and y <= iy <= y+bh:
            return name
    return None

def draw_hud(frame, shape, scale, rot_x, rot_y, rot_z, fps):
    h, w = frame.shape[:2]
    color = SHAPE_COLORS[shape]
    bar_h = 44
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, h-bar_h), (w, h), (10, 10, 20), -1)
    cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
    cv2.line(frame, (0, h-bar_h), (w, h-bar_h), color, 1)
    font = cv2.FONT_HERSHEY_SIMPLEX
    stats = [
        f"SHAPE: {shape}",
        f"SCALE: {scale}",
        f"RX:{int(rot_x):+04d} RY:{int(rot_y):+04d} RZ:{int(rot_z):+04d}",
        f"FPS: {fps:.0f}",
    ]
    positions = [14, w//4+10, w//2-60, w-90]
    for i, (txt, px) in enumerate(zip(stats, positions)):
        cv2.putText(frame, txt, (px, h-14), font, 0.42,
                    color if i == 0 else (160,160,180), 1, cv2.LINE_AA)

def draw_crosshair(frame, pos, color=(0,255,180)):
    x, y = pos
    size = 10
    cv2.line(frame, (x-size, y), (x+size, y), color, 1, cv2.LINE_AA)
    cv2.line(frame, (x, y-size), (x, y+size), color, 1, cv2.LINE_AA)
    cv2.circle(frame, (x, y), 4, color, 1, cv2.LINE_AA)

def draw_hand_skeleton(frame, landmarks, frame_shape):
    h, w = frame_shape[:2]
    CONNECTIONS = [
        (0,1),(1,2),(2,3),(3,4),
        (0,5),(5,6),(6,7),(7,8),
        (0,9),(9,10),(10,11),(11,12),
        (0,13),(13,14),(14,15),(15,16),
        (0,17),(17,18),(18,19),(19,20),
        (5,9),(9,13),(13,17)
    ]
    FINGER_COLORS = [
        (0,200,255),(0,200,255),(0,200,255),(0,200,255),
        (0,255,180),(0,255,180),(0,255,180),(0,255,180),
        (80,180,255),(80,180,255),(80,180,255),(80,180,255),
        (180,80,255),(180,80,255),(180,80,255),(180,80,255),
        (255,180,80),(255,180,80),(255,180,80),(255,180,80),
        (255,255,255),
    ]
    pts = [(int(lm.x * w), int(lm.y * h)) for lm in landmarks]
    for a, b in CONNECTIONS:
        cv2.line(frame, pts[a], pts[b], (40,60,80), 3, cv2.LINE_AA)
        cv2.line(frame, pts[a], pts[b], (0,180,140), 1, cv2.LINE_AA)
    for i, pt in enumerate(pts):
        col = FINGER_COLORS[i] if i < len(FINGER_COLORS) else (255,255,255)
        cv2.circle(frame, pt, 5, (10,10,20), -1)
        cv2.circle(frame, pt, 4, col, -1, cv2.LINE_AA)
