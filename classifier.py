import cv2
import os

from percent_white_pixels import percent_white_pixels


def classify_meme(image):
    results = {}

    meme_to_classify = cv2.cvtColor(cv2.imread(image), cv2.COLOR_BGR2GRAY)

    for file in os.listdir('templates'):
        # this is a weird transparent image that i don't want to deal with rn
        if file[:-4] == 'El Shaddai':
            continue

        meme_template = cv2.imread('templates/{0}'.format(file))

        # some of the templates are gif encoded
        if meme_template is None:
            gif = cv2.VideoCapture('templates/{0}'.format(file))

            _, meme_template = gif.read()

        # grayscale template
        meme_template = cv2.cvtColor(meme_template, cv2.COLOR_BGR2GRAY)

        # scale template
        scaling_factor = meme_to_classify.shape[0] / meme_template.shape[0]

        if meme_to_classify.shape[1] / meme_template.shape[1] < scaling_factor:
            scaling_factor = meme_to_classify.shape[1] / meme_template.shape[1]

        meme_template = cv2.resize(
            meme_template,
            None,
            fx=scaling_factor,
            fy=scaling_factor,
            interpolation=cv2.INTER_AREA
        )

        # match template
        res = cv2.matchTemplate(
            meme_to_classify,
            meme_template,
            cv2.TM_CCOEFF_NORMED
        )

        # get match region
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        w, h = meme_template.shape[::-1]

        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        match = meme_to_classify[top_left[1]: bottom_right[1], top_left[0]: bottom_right[0]]

        # only count matched colored pixels, not white pixels
        pct_white = percent_white_pixels(match)

        results[file[:-4]] = max_val * 1 - pct_white

    return results
