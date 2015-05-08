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

    def add_sms(self, text, me):
        # TODO: в качестве развития, можно добавлять время отправки

        self.sms_chats.append(
            (text, me)
        )

    def add_me_sms(self, text):
        self.add_sms(text, me=True)

    def add_other_sms(self, text):
        self.add_sms(text, me=False)

    def get_sms_size(self, text):
        """Функция возвращает размеры облачка смс"""

        text_rect = QFontMetrics(self.font).boundingRect(text)

        # Немного увеличим облачко, чтобы текст в нем вмещался свободно
        # TODO: наверное, лучше будет увеличить процентно
        return text_rect.width() + 20, text_rect.height() + 20

    def size(self):
        """Функция для размера переписки в пикселях."""
        w, h = 0, 0

        for sms in self.sms_chats:
            w_sms, h_sms = self.get_sms_size(sms[0])

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
            message = sms[0]
            me = sms[1]

            # Цвет облачков собеседников должны отличаться
            sms_color = self.me_color if me else self.other_color
            text_color = self.text_color

            w, h = self.get_sms_size(message)

            # "Мои" смс будут находиться с левой стороны, а собеседника с правой стороны
            x = self.left_indent if me else w_im - w - self.right_indent

            p.setPen(sms_color)
            p.setBrush(sms_color)
            p.setFont(self.font)
            p.drawRoundedRect(x, last_y, w, h, 20, 20)

            p.setPen(text_color)
            p.drawText(x, last_y, w, h, Qt.AlignCenter, message)
            # p.drawText(x, last_y, w, h, Qt.AlignCenter | Qt.TextWordWrap, message)

            last_y += h + self.indent

        # Обнуляем ссылку на QPainter
        # p = None

        return im


app = QApplication(sys.argv)


fake = FakeSmsChat()
fake.add_me_sms('Кек, а меня уволили.')
fake.add_other_sms('за что уже?')
fake.add_me_sms('За то что у кошки роды принимал.')
fake.add_other_sms('ШТОООА7')
fake.add_other_sms('прям на работе?')
fake.add_me_sms('Нет. Я один день не вышел на работу.')
fake.add_other_sms('зато у тебя есть котики')
fake.add_other_sms('котики - это хорошо')

im = fake.get_QImage()
im.save('fakesms.png')

# l = QLabel()
# l.setPixmap(QPixmap.fromImage(im))
# l.show()
#
# sys.exit(app.exec_())
