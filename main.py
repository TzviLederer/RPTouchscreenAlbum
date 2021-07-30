from argparse import ArgumentParser
from pathlib import Path
import time

import cv2
import screeninfo

from display import Display, bar_boundaries, rectangle_boundaries
from messages_manager import Messages


def main():
    # get arguments
    parser = ArgumentParser()
    parser.add_argument('-p', '--images_path', type=str, help='path to images directory')
    parser.add_argument('-t', '--time', type=float, default=5, help='time in second for each image')
    parser.add_argument('-r', '--reminders_path', type=str, default='reminders.txt',
                        help='path to reminders txt file')
    args = parser.parse_args()

    directory = args.images_path
    assert directory is not None, 'User must enter images path with -p argument'

    messages_manager = Messages(path=args.reminders_path)
    display = Display(messages_manager)

    # read screen height and width
    screen = screeninfo.get_monitors()[0]
    width, height = screen.width, screen.height

    # create display window
    window_name = 'projector'
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.moveWindow(window_name, screen.x - 1, screen.y - 1)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.setMouseCallback(window_name, click_callback, {'display_manager': display, 'shape': (height, width)})

    if not list(Path(directory).glob('*[.j][jp][epn]g')):
        print('Directory is empty. Make sure that the path is right and the images has the right formats (read README)')
        return False

    i = 0
    while True:
        messages_manager.update()
        for filename in Path(directory).glob('*[.j][jp][epn]g'):
            # read image
            im = cv2.imread(str(filename))
            if im is None:
                continue

            # resize image to screen size
            im, new_shape = resize(im, height, width)

            # crop image to fit the screen
            im = crop(im, height, width, new_shape)

            t = time.time()
            while time.time() - t < args.time:
                i += 1

                im_display = display.draw_on_frame(frame=im, i=i)

                cv2.imshow(window_name, im_display)
                k = cv2.waitKey(1)
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


def click_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        display_manager = param['display_manager']
        if display_manager.rectangle:
            (x0, y0), (x1, y1) = rectangle_boundaries
            if x1 < 0:
                x1 = param['shape'][1] + x1
            if y1 < 0:
                y1 = param['shape'][0] + y1
            if x0 < x < x1 and y0 < y < y1:
                display_manager.rectangle = False
        else:
            y0, y1 = bar_boundaries
            if y0 < y < y1:
                display_manager.rectangle = True


if __name__ == '__main__':
    main()
