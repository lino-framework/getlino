=============
Miscellaneous
=============

>>> from getlino.utils import perm2text
>>> print(perm2text(0o3777))
rwxrwsrwt
>>> print(perm2text(0o2775))
rwxrwsr-x
>>> print(perm2text(1533))
rwxrwsr-x
>>> print(perm2text(509))
rwxrwxr-x
>>> print(perm2text(436))
rw-rw-r--

>>> print(perm2text(1))
--------x

>>> print(perm2text(0o123456))
Traceback (most recent call last):
...
Exception: value must be less than 0o7777
