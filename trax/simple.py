
import base

try:
	import cPickle as pickle
except ImportError:
	print 'WARNING: Cannot import cPickle, using slower pickle'
	import pickle

class SimpleTransactional(base.AbstractTransactional):

	def __init__(self, picklemode=0, **kws):
		assert type(picklemode) is int
		assert picklemode >= 0
		self._picklemode = picklemode
		base.AbstractTransactional.__init__(self, *kws)

	def checkpoint(self, value):
		if self._checkpoint_fd is None:
			self._checkpoint_fd = open(self._checkpoint_path, self._cpt_mode)
		pickle.dump(value, self._checkpoint_fd)
		self.close()

	def log(self, value):
		if self._log_fd is None:
			self._log_fd = open(self._log_path, self._log_mode)
		self._log_fd.write(value)

	def recover(self, log_handler):
		self.close()
		mode = 'r' if self._picklemode == 0 else 'rb'
		with open(self._checkpoint_path, mode) as fd:
			obj = pickle.load(fd)
		return log_handler(obj, self._log_path)
