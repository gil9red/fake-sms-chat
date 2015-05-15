#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# Написать генератор переписки
# Пример:
# big_cbe19cc65a4b10e3d7f3658bfa9f845a.jpg
# bXxitzIH4JPg.jpg
#
# // Очень простой стиль облачка сообщения:
# big_93524ee2aa1ed71f35f086eafc04c0d0.jpg
# big_213bdee063ce096c2f8154f4e7e174fe.jpg
# http://stackoverflow.com/questions/13364231/qpainterdrawtext-get-bounding-boxes-for-each-character
# http://doc.qt.io/qt-4.8/qpainter.html#drawText-10
# http://doc.qt.io/qt-4.8/qt.html#TextFlag-enum

# generator of the fake sms chat
# генератор фейкового смс чата
# TODO: сделать сначала консольный вариант, которому кормишь текст
# и получаешь сгенерированную картинку
# Потом сделать gui'шный вариант с предпросмотром



from PySide.QtGui import *
from PySide.QtCore import *
import sys

class Sms:
    def __init__(self, me, text, time):
        self.me = me
        self.text = text
        self.time = time

        # self.font = QFont('Tahoma', 10)
        # self.font_time = QFont('Tahoma', 8)

    def get_sms_size(self, font):
        """Функция возвращает размеры облачка смс"""

        w, h = 0, 0

        for line in self.text.split('\n'):
            # TODO: доработать -- расстояние внутри между рамками
            # облачка и текстом получается меньше, если многострочный
            # текст смс
            # text_rect = QFontMetrics(self.font).boundingRect(line)
            text_rect = QFontMetrics(font).boundingRect(line)
            w = max(w, text_rect.width())
            h = max(h, text_rect.height())

        # TODO: наверное, лучше будет увеличить процентно
        return w + 20, h + 20

        # text_rect = QFontMetrics(self.font).boundingRect(text)
        #
        # # Немного увеличим облачко, чтобы текст в нем вмещался свободно
        # # TODO: наверное, лучше будет увеличить процентно
        # return text_rect.width() + 20, text_rect.height() + 20

    def get_time_sms_size(self, font):
        """Функция возвращает размеры текст с временем смс"""

        # time_rect = QFontMetrics(self.font_time).boundingRect(self.time)
        time_rect = QFontMetrics(font).boundingRect(self.time)
        return time_rect.width(), time_rect.height()


class FakeSmsChat:
    def __init__(self):
        self.sms_chats = []
        self.font = QFont('Tahoma', 10)
        self.me_color = QColor(0, 255, 120)
        self.other_color = Qt.gray
        self.text_color = Qt.black
        self.indent = 10
        self.left_indent = 5
        self.right_indent = 5
        self.top_indent = 5
        self.indent_time = 5
        self.font_time = QFont('Tahoma', 8)

    def add_sms(self, me, text, time):
        sms = Sms(me, text, time)

        self.sms_chats.append(sms)

        # self.sms_chats.append(
        #     (me, text, time)
        # )

    def add_me_sms(self, text, time=None):
        self.add_sms(True, text, time)

    def add_other_sms(self, text, time=None):
        self.add_sms(False, text, time)

    # def get_sms_size(self, text):
    #     """Функция возвращает размеры облачка смс"""
    #
    #     w, h = 0, 0
    #
    #     for line in text.split('\n'):
    #         text_rect = QFontMetrics(self.font).boundingRect(line)
    #         w = max(w, text_rect.width())
    #         h = max(h, text_rect.height())
    #
    #     # TODO: наверное, лучше будет увеличить процентно
    #     return w + 20, h + 20
    #
    #     # text_rect = QFontMetrics(self.font).boundingRect(text)
    #     #
    #     # # Немного увеличим облачко, чтобы текст в нем вмещался свободно
    #     # # TODO: наверное, лучше будет увеличить процентно
    #     # return text_rect.width() + 20, text_rect.height() + 20
    #
    # def get_time_sms_size(self, time):
    #     """Функция возвращает размеры текст с временем смс"""
    #
    #     time_rect = QFontMetrics(self.font_time).boundingRect(time)
    #     return time_rect.width(), time_rect.height()

    def size(self):
        """Функция для размера переписки в пикселях."""
        w, h = 0, 0

        for sms in self.sms_chats:
            # w_sms, h_sms = self.get_sms_size(sms[1])
            w_sms, h_sms = sms.get_sms_size(self.font)

            # TODO: учитывать размер времени sms[2]
            # t_w = self.get_time_sms_size(sms[2])[0]
            t_w = sms.get_time_sms_size(self.font_time)[0]
            w_sms += t_w + self.indent_time

            w = max(w, w_sms)
            h += h_sms

        # Нужно учитывать отступы между облаками сообщений
        h += len(self.sms_chats) * self.indent

        # Немного добавим размера
        w += 10
        h += 10

        return w, h

    def get_QImage(self):
        """Отрисовка смс диалога на QImage"""

        w_im, h_im = self.size()

        im = QImage(w_im, h_im, QImage.Format_ARGB32)
        im.fill(Qt.white)

        p = QPainter(im)
        p.setRenderHint(QPainter.Antialiasing)

        last_y = self.top_indent

        for sms in self.sms_chats:
            # me = sms[0]
            # message = sms[1]
            # time = sms[2]
            me = sms.me
            message = sms.text
            time = sms.time

            # Цвет облачков собеседников должны отличаться
            sms_color = self.me_color if me else self.other_color
            text_color = self.text_color

            # w, h = self.get_sms_size(message)
            w, h = sms.get_sms_size(self.font)

            # "Мои" смс будут находиться с левой стороны, а собеседника с правой стороны
            x = self.left_indent if me else w_im - w - self.right_indent

            p.setPen(sms_color)
            p.setBrush(sms_color)
            p.setFont(self.font)
            p.drawRoundedRect(x, last_y, w, h, 20, 20)

            p.setPen(text_color)
            p.drawText(x, last_y, w, h, Qt.AlignCenter, message)
            # p.drawText(x, last_y, w, h, Qt.AlignCenter | Qt.TextWordWrap, message)

            # TODO: refactoring
            if time:
                # time_w, time_h = self.get_time_sms_size(time)
                time_w, time_h = sms.get_time_sms_size(self.font_time)

                # Высчитываем горизонтальное положение текста с временем отправки смс
                if me:
                    # К горизонтальному положению смс добавляем его ширину и отступ текста времени отправки
                    time_x = x + w + self.indent_time
                else:
                    # Из горизонтального положения смс вычитаем его ширину и отступ текста времени отправки
                    time_x = x - time_w - self.indent_time

                p.setFont(self.font_time)
                p.drawText(time_x, last_y, time_w, h, Qt.AlignCenter, time)

            last_y += h + self.indent

        # # Обнуляем ссылку на QPainter
        # p = None

        return im


app = QApplication(sys.argv)


fake = FakeSmsChat()
fake.add_me_sms('Кек, а меня уволили.', '10:01')
fake.add_other_sms('за что уже?', '10:02')
fake.add_me_sms('За то что у кошки роды принимал.', '10:03')
fake.add_other_sms('ШТОООА7', '10:04')
fake.add_other_sms('прям на работе?')
fake.add_me_sms('Нет. Я один день не \nвышел на работу.')
fake.add_other_sms('зато у тебя есть котики', '10:07')
fake.add_other_sms('котики - это хорошо')

im = fake.get_QImage()
im.save('fakesms.png')

# l = QLabel()
# l.setPixmap(QPixmap.fromImage(im))
# l.show()
#
# sys.exit(app.exec_())
