import numpy as np
import cv2

def rotate_x(pts, angle):
    r = np.radians(angle)
    m = np.array([[1,0,0],[0,np.cos(r),-np.sin(r)],[0,np.sin(r),np.cos(r)]])
    return pts @ m.T

def rotate_y(pts, angle):
    r = np.radians(angle)
    m = np.array([[np.cos(r),0,np.sin(r)],[0,1,0],[-np.sin(r),0,np.cos(r)]])
    return pts @ m.T

def rotate_z(pts, angle):
    r = np.radians(angle)
    m = np.array([[np.cos(r),-np.sin(r),0],[np.sin(r),np.cos(r),0],[0,0,1]])
    return pts @ m.T

def project(pts, cx, cy, scale=200, fov=500):
    out = []
    for x, y, z in pts:
        zp = z + fov
        px = int(cx + x * scale / zp * fov)
        py = int(cy + y * scale / zp * fov)
        out.append((px, py))
    return out

CUBE_VERTS = np.array([
    [-1,-1,-1],[1,-1,-1],[1,1,-1],[-1,1,-1],
    [-1,-1, 1],[1,-1, 1],[1,1, 1],[-1,1, 1]
], dtype=float)
CUBE_EDGES = [(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)]

PYRAMID_VERTS = np.array([
    [-1,-1,-1],[1,-1,-1],[1,-1,1],[-1,-1,1],[0,1,0]
], dtype=float)
PYRAMID_EDGES = [(0,1),(1,2),(2,3),(3,0),(0,4),(1,4),(2,4),(3,4)]

def sphere_verts_edges(steps=10):
    verts = []
    for i in range(steps+1):
        lat = np.pi * i / steps - np.pi/2
        for j in range(steps):
            lon = 2 * np.pi * j / steps
            verts.append([np.cos(lat)*np.cos(lon), np.sin(lat), np.cos(lat)*np.sin(lon)])
    edges = []
    for i in range(steps+1):
        for j in range(steps):
            a = i*steps+j
            b = i*steps+(j+1)%steps
            if a < len(verts) and b < len(verts):
                edges.append((a, b))
            if i < steps:
                c = (i+1)*steps+j
                if c < len(verts):
                    edges.append((a, c))
    return np.array(verts, dtype=float), edges

SPHERE_VERTS, SPHERE_EDGES = sphere_verts_edges()

SHAPES = {
    "CUBE":    (CUBE_VERTS,    CUBE_EDGES),
    "PYRAMID": (PYRAMID_VERTS, PYRAMID_EDGES),
    "SPHERE":  (SPHERE_VERTS,  SPHERE_EDGES),
}

SHAPE_COLORS = {
    "CUBE":    [(0, 255, 255), (0, 180, 255)],
    "PYRAMID": [(0, 255, 120), (0, 200, 80)],
    "SPHERE":  [(180, 80, 255), (120, 40, 220)],
}

def draw_shape_glow(frame, shape_name, rx, ry, rz, scale, cx, cy):
    verts, edges = SHAPES[shape_name]
    pts = verts.copy()
    pts = rotate_x(pts, rx)
    pts = rotate_y(pts, ry)
    pts = rotate_z(pts, rz)
    proj = project(pts, cx, cy, scale=scale)
    c1, c2 = SHAPE_COLORS[shape_name]

    overlay = frame.copy()
    for a, b in edges:
        cv2.line(overlay, proj[a], proj[b], c2, 6, cv2.LINE_AA)
    cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)

    for a, b in edges:
        cv2.line(frame, proj[a], proj[b], c1, 2, cv2.LINE_AA)

    for p in proj:
        cv2.circle(frame, p, 3, c1, -1, cv2.LINE_AA)
