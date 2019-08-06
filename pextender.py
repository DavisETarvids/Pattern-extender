import sys
import os
# image load/save
import imageio
# image manipulation
import numpy as np
import math


def filler2(canvas, pattern, i, j, h, w):
    canvas[i:i + h, j:j + w] = pattern[0:h, 0:w]


def filler3(canvas, pattern, i, j, h, w):
    canvas[i:i + h, j:j + w, :] = pattern[0:h, 0:w, :]


def pattern_extender(src, dest, new_shape):
    pattern = imageio.imread(src)

    assert pattern.shape[0] <= new_shape[0] and pattern.shape[1] <= new_shape[1],\
        ("Extended image's shape should be at least as large as the pattern shape, "
         "but got ({}, {}) whereas pattern shape is ({}, {})".format(*new_shape,
                                                                 *pattern.shape))

    is_bw = len(pattern.shape) == 2  # is black and white
    fill = filler2 if is_bw else filler3
    canvas = np.zeros(new_shape if is_bw else (*new_shape, 3))

    # prepare progress bar
    progressbar_width, progress = 50, 0
    sys.stdout.write("[%s]" % (" " * progressbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (progressbar_width + 1))

    i = 0
    while i < new_shape[0]:
        j = 0
        while j < new_shape[1]:
            h = (pattern.shape[0]
                 if i + pattern.shape[0] <= new_shape[0]
                 else new_shape[0] - i)
            w = (pattern.shape[1]
                 if j + pattern.shape[1] <= new_shape[1]
                 else new_shape[1] - j)
            fill(canvas, pattern, i, j, h, w)
            j += pattern.shape[1]
        i += pattern.shape[0]
        # update progress bar
        current_progress = math.floor((i / new_shape[0]) * progressbar_width)
        for p in range(current_progress - progress):
            sys.stdout.write("-")
            sys.stdout.flush()
        progress = current_progress

    sys.stdout.write("]\nsaving...\n")
    imageio.imsave(dest, canvas.astype('uint8'))


argv = sys.argv

assert len(argv) == 5, """input must be 4 arguments, namely: pattern image name, output image name, pixel height and width of output image, but got {} argument{}""".format(
    len(argv) - 1, 's' if len(argv) > 2 else '')

src_path, dest_path = argv[1], argv[2]
new_shape = (int(argv[3]), int(argv[4]))

pattern_extender(src_path, dest_path, new_shape)

print("Completed creating new image: {}".format(src_path))
