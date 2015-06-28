#!/usr/bin/env python
from MainCls import CommBot

cb1 = CommBot('talkieBot-001')
cb2 = CommBot('talkieBot-002')
while True:
    cb1.main_loop()
    cb2.main_loop()