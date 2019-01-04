import cython

@cython.boundscheck(False)
cpdef float percent_white_pixels(unsigned char [:, :] image):
    cdef int x, y, w, h, threshold
    cdef float total_pixels, white_pixels

    threshold = 250
    total_pixels = 0
    white_pixels = 0

    h = image.shape[0]
    w = image.shape[1]

    for y in range(0, h):
        for x in range(0, w):
            total_pixels += 1
            if image[y, x] > threshold:
                white_pixels += 1

    return white_pixels / total_pixels
