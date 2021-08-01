from itertools import compress

import cv2
import numpy as np

from messages_manager import Messages

font = cv2.FONT_HERSHEY_PLAIN
bar_text_color = (1., 1., 1.)
bar_text_size = 2
bar_text_thickness = 2
bar_boundaries = (20, 60)
bar_text_y = 50
bar_color_ratio = 0.9
bar_separator = '     '
bar_text_speed = 5

rectangle_text_color = (1., 1., 1.)
rectangle_text_size = 3
rectangle_text_thickness = 3
rectangle_boundaries = ((50, 30), (-50, -30))
rectangle_text_gap = 70
rectangle_text_origin = (110, 80)
rectangle_color_ratio = 0.9
rectangle_box_origin = (70, 55)
rectangle_box_size = 20
rectangle_box_color = (1., 1., 1.)


class Display:
    def __init__(self, reminders):
        self.reminders = reminders
        self.rectangle = False

    def draw_on_frame(self, frame, i=0):
        if len(self.reminders.get_messages()[0]) == 0:
            return frame.copy()

        frame_display = frame.copy() / 255
        if self.rectangle:
            return np.uint8(self.draw_rectangle(frame_display) * 255)
        else:
            return np.uint8(self.draw_bar(frame_display, i) * 255)

    def draw_rectangle(self, frame):
        (x_0, y_0), (x_1, y_1) = rectangle_boundaries
        frame[y_0:y_1, x_0:x_1, :] *= rectangle_color_ratio

        messages, red = self.reminders.get_messages()
        x_t_0, y_t_0 = rectangle_text_origin
        self._draw_rect_messages(frame, messages, x_t_0, y_t_0, rectangle_text_thickness + 4, (0, 0, 0))
        self._draw_rect_messages(frame, messages, x_t_0, y_t_0, rectangle_text_thickness, rectangle_text_color, red)

        for i, r in enumerate(red):
            start_point = (rectangle_box_origin[0], rectangle_box_origin[1] + i * rectangle_text_gap)
            end_point = (rectangle_box_origin[0] + rectangle_box_size,
                         rectangle_box_origin[1] + i * rectangle_text_gap + rectangle_box_size)
            cv2.rectangle(frame, start_point, end_point, color=(0, 0, 0), thickness=rectangle_text_thickness + 4)
            if r:
                cv2.rectangle(frame, start_point, end_point, color=(0, 1, 0), thickness=rectangle_text_thickness)
            else:
                cv2.rectangle(frame, start_point, end_point, color=rectangle_box_color, thickness=rectangle_text_thickness)
        return frame

    @staticmethod
    def _draw_rect_messages(frame, messages, x_t_0, y_t_0, thickness, color_org, red=None):
        for i, m in enumerate(messages):
            color = Display.infer_color(color_org, i, red)
            cv2.putText(frame, text=m, org=(x_t_0, y_t_0 + i * rectangle_text_gap), fontFace=font,
                        fontScale=rectangle_text_size, thickness=thickness,
                        color=color)

    @staticmethod
    def infer_color(color_org, i, red):
        if red is not None:
            if red[i]:
                color = (0, 1, 0)
            else:
                color = color_org
        else:
            color = color_org
        return color

    def draw_bar(self, frame, i):
        messages = [m for m, r in zip(self.reminders.get_messages()[0], self.reminders.get_messages()[1]) if not r]
        if messages == []:
            return frame

        text = bar_separator.join(messages)

        (bar_length, _), _ = cv2.getTextSize(text, fontFace=font, fontScale=bar_text_size, thickness=bar_text_thickness)
        org = ((-i * bar_text_speed) % (frame.shape[1] + bar_length) - bar_length, bar_text_y)

        frame[bar_boundaries[0]:bar_boundaries[1], :, :] *= bar_color_ratio
        cv2.putText(frame, text=text, org=org, fontFace=font, fontScale=bar_text_size,
                    thickness=bar_text_thickness, color=bar_text_color)

        return frame


def main():
    frame = cv2.imread(r'im.jpg')
    frame = cv2.resize(frame, (800, 480))

    reminders = Messages(path='reminders.txt')
    display = Display(reminders=reminders)
    for i in range(1000):
        frame_display = display.draw_on_frame(frame, i)
        cv2.imshow('', frame_display)
        if cv2.waitKey(40) == 27:
            break


if __name__ == '__main__':
    main()
