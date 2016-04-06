#!/usr/bin/env python3
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

# TODO: поиграть с градиентами

from PySide.QtGui import *
from PySide.QtCore import *
import sys

class Sms:
    def __init__(self, me, text, time):
        self.me = me
        self.text = text
        self.time = time

    def get_sms_size(self, font):
        """Функция возвращает размеры облачка смс"""

        w, h = 0, 0

        # Разбиваем строку, определяем максимальную ширину и
        # подсчитываем высоту смс
        for line in self.text.split('\n'):
            text_rect = QFontMetrics(font).boundingRect(line)
            w = max(w, text_rect.width())
            h += text_rect.height()

        return w + 15, h + 15

    def get_time_sms_size(self, font):
        """Функция возвращает размеры текст с временем смс"""

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
        self.left_indent = 15
        self.right_indent = 15
        self.top_indent = 10
        self.indent_time = 5
        self.font_time = QFont('Tahoma', 8)

        self.h_triangle = 10
        self.w_triangle = 10

    def add_sms(self, me, text, time):
        sms = Sms(me, text, time)

        self.sms_chats.append(sms)

    def add_me_sms(self, text, time=None):
        self.add_sms(True, text, time)

    def add_other_sms(self, text, time=None):
        self.add_sms(False, text, time)

    def size(self):
        """Функция для размера переписки в пикселях."""
        w, h = 0, 0

        for sms in self.sms_chats:
            w_sms, h_sms = sms.get_sms_size(self.font)

            # Получаем ширину текста с временем отправки
            t_w = sms.get_time_sms_size(self.font_time)[0]
            w_sms += t_w + self.indent_time + self.w_triangle * 2

            w = max(w, w_sms)
            h += h_sms

        # Нужно учитывать отступы между облаками сообщений
        h += len(self.sms_chats) * self.indent

        # Немного добавим размера
        return w + 40, h + 40

    def drawSmsCloud(self, x, y, w, h, painter, color, sms):
        painter.save()
        painter.setPen(color)
        painter.setBrush(color)

        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)
        path.addRoundRect(x, y, w, h, 5, 5)

        # Нарисуем треугольник сбоку от прямоугольника
        if sms.me:
            path.moveTo(x - self.w_triangle, y + h / 2)
            path.lineTo(x, y + h / 2 - self.h_triangle / 2)
            path.lineTo(x, y + h / 2 + self.h_triangle / 2)
        else:
            path.moveTo(x + w + self.w_triangle, y + h / 2)
            path.lineTo(x + w, y + h / 2 - self.h_triangle / 2)
            path.lineTo(x + w, y + h / 2 + self.h_triangle / 2)

        path.closeSubpath()

        painter.drawPath(path)
        painter.restore()

    def drawSmsText(self, x, y, w, h, painter, color, sms):
        painter.save()
        painter.setFont(self.font)
        painter.setPen(color)
        painter.drawText(x, y, w, h, Qt.AlignCenter, sms.text)
        painter.restore()

    def drawSmsTime(self, x, y, w, h, painter, sms):
        time_w, time_h = sms.get_time_sms_size(self.font_time)

        # Высчитываем горизонтальное положение текста с временем отправки смс
        if sms.me:
            # К горизонтальному положению смс добавляем его ширину и отступ текста времени отправки
            time_x = x + w + self.indent_time
        else:
            # Из горизонтального положения смс вычитаем его ширину и отступ текста времени отправки
            time_x = x - time_w - self.indent_time

        painter.save()
        painter.setFont(self.font_time)
        painter.drawText(time_x, y, time_w, h, Qt.AlignCenter, sms.time)
        painter.restore()

    def get_QImage(self):
        """Отрисовка смс диалога на QImage"""

        w_im, h_im = self.size()

        im = QImage(w_im, h_im, QImage.Format_ARGB32)
        im.fill(Qt.white)

        p = QPainter(im)
        p.setRenderHint(QPainter.Antialiasing)

        last_y = self.top_indent

        for sms in self.sms_chats:
            me = sms.me

            # Цвет облачков собеседников должны отличаться
            sms_color = self.me_color if me else self.other_color
            text_color = self.text_color

            w, h = sms.get_sms_size(self.font)

            # "Мои" смс будут находиться с левой стороны, а собеседника с правой стороны
            x = self.left_indent if me else w_im - w - self.right_indent

            # Рисуем тень облачка смс
            self.drawSmsCloud(x + 1, last_y + 1, w, h, p, Qt.black, sms)
            self.drawSmsCloud(x, last_y, w, h, p, sms_color, sms)
            self.drawSmsText(x, last_y, w, h, p, text_color, sms)
            self.drawSmsTime(x, last_y, w, h, p, sms)

            last_y += h + self.indent

        # Обнуляем ссылку на QPainter
        p = None

        return im
