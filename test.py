import utils

handler = utils.Handler()
w = utils.Watcher('ToSync', handler)
w.run(30)
print(handler.changes)
