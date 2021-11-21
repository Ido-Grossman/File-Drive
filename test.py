import utils
import os

hi = "hello, i am ido"
toremove = "hello, i a"
hi = utils.remove_prefix(toremove, hi)
print(hi)
files = os.walk('ToSync', True)
print(files)
