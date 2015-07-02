# CommBots
Basic communication between one or more "bots" in one or more python processes using a flat log. 

## There are two ways to use them...
* Run commbots.py or something similar to spin up multiple bots in the same process.

* Alternatively, open multiple terminals or shells and instantiate multiple bots that way. Bots must share a heart_beats.log file in order to "see" each other. By default they will each watch their own .conf file for changes.
```
$ python
Python 2.7.6 (default, Sep  9 2014, 15:04:36)
[GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.39)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from MainCls import CommBot
>>> bot = CommBot('my_comm_bot')
>>> while True:
...     bot.main_loop()
...
```