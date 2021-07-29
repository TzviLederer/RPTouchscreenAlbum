from argparse import ArgumentParser
from pathlib import Path

import cv2
import screeninfo


def main():
    # get arguments
    parser = ArgumentParser()
    parser.add_argument('-p', '--images_path', type=str, help='path to images directory')
    parser.add_argument('-t', '--time', type=float, default=5, help='time in second for each image')
    args = parser.parse_args()

    directory = args.images_path
    assert directory is not None, 'User must enter images path with -p argument'

    # read screen height and width
    screen = screeninfo.get_monitors()[0]
    width, height = screen.width, screen.height

    # create display window
    window_name = 'projector'
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.moveWindow(window_name, screen.x - 1, screen.y - 1)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    if not list(Path(directory).glob('*[.j][jp][epn]g')):
        print('Directory is empty. Make sure that the path is right and the images has the right formats (read README)')
        return False

    while True:
        for filename in Path(directory).glob('*[.j][jp][epn]g'):
            # read image
            im = cv2.imread(str(filename))
            if im is None:
                continue

            # resize image to screen size
            im, new_shape = resize(im, height, width)

            # crop image to fit the screen
            im = crop(im, height, width, new_shape)

            cv2.imshow(window_name, im)
            k = cv2.waitKey(args.time * 1000)
            if k == ord('q') or k == 27:
                return False


def resize(im, height, width):
    im_h, im_w, _ = im.shape
    ratio = min(im_h / height, im_w / width)
    new_shape = (int(im_w / ratio), int(im_h / ratio))
    im = cv2.resize(im, new_shape)
    return im, new_shape


def crop(im, height, width, new_shape):
    if new_shape[0] == width:
        new_y = int((new_shape[1] - height) / 2)
        im = im[new_y:new_y + height, :, :]
    elif new_shape[1] == height:
        new_x = int((new_shape[0] - width) / 2)
        im = im[:, new_x:new_x + width]
    return im


if __name__ == '__main__':
    main()
