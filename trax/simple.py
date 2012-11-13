
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

	def _impl_checkpoint(self, fd, value):
		pickle.dump(value, fd)

	def _impl_log(self, fd, value):
		fd.write(value)


	def _impl_cpt_recover_open(self):
		mode = 'r' if self._picklemode == 0 else 'rb'
		return open(self.cpt_path, mode)

	def _impl_log_recover_open(self):
		return open(self.log_path)

	def recover(self, log_handler):
		def cpt_handler(fd):
			return pickle.load(fd)
		return base.AbstractTransactional.recover(self, checkpoint_handler=cpt_handler, log_handler=log_handler)
