#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from fake_sms_chat.fake_sms_chat import FakeSmsChat
fake = FakeSmsChat()
fake.add_me_sms('Кек, а меня уволили.', '10:01')
fake.add_other_sms('за что уже?', '10:02')
fake.add_me_sms('За то что у кошки\n роды принимал.', '10:03')
fake.add_other_sms('ШТОООА7', '10:04')
fake.add_other_sms('прям на работе?')
fake.add_me_sms('Нет. Я один день не \nвышел на работу.')
fake.add_other_sms('зато у тебя есть котики', '10:07')
fake.add_other_sms('котики - это хорошо')

im = fake.get_QImage()
im.save('fakesms.png')
