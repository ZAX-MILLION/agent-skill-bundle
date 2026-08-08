#!/usr/bin/env python3
"""Cluster hand-drawn red marks in a user screenshot and print each blob's bbox.

Usage: python3 red_marks.py <image_path> [red_threshold]

The user marks EVERY element they care about with red circles; missing one costs
an extra round-trip ("you forgot the two I marked in red"). Run this BEFORE
coding, then crop + vision-analyze each blob individually.

Needs pillow + numpy (e.g. /root/pw-venv/bin/python).
"""
import sys
from collections import deque

import numpy as np
from PIL import Image


def main(path: str, r_min: int = 140, g_max: int = 90, b_max: int = 90) -> None:
    a = np.array(Image.open(path).convert("RGB"))
    h, w = a.shape[:2]
    print(f"image {w}x{h}")
    red = (a[:, :, 0] > r_min) & (a[:, :, 1] < g_max) & (a[:, :, 2] < b_max)
    pts = set(zip(*np.where(red)))  # (y, x) pairs
    seen, blobs = set(), []
    for p in pts:
        if p in seen:
            continue
        q = deque([p])
        seen.add(p)
        blob = []
        while q:
            y, x = q.popleft()
            blob.append((y, x))
            for dy in (-2, -1, 0, 1, 2):
                for dx in (-2, -1, 0, 1, 2):
                    n = (y + dy, x + dx)
                    if n in pts and n not in seen:
                        seen.add(n)
                        q.append(n)
        blobs.append(blob)
    blobs.sort(key=len, reverse=True)
    for i, bl in enumerate(blobs[:8]):
        ys = [p[0] for p in bl]
        xs = [p[1] for p in bl]
        print(f"red blob {i}: x {min(xs)}..{max(xs)}, y {min(ys)}..{max(ys)}, n={len(bl)}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1], *[int(x) for x in sys.argv[2:4]])
