# CommBots
Basic communication between one or more "bots" in one or more python processes using a flat log file.

Either run commbots.py or something similar to spin up multiple bots in the same process, or open multiple terminals or shells and instantiate multiple bots that way. Bots must share a heart_beats.log file in order to "see" each other. By default they will each watch their own .conf file.
```
$ python
>>> from MainCls import CommBot
>>> bot = CommBot('my_comm_bot')
>>> while True:
...     bot.main_loop()
...
```