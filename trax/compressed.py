
import base

import bz2

class AbstractBZ2CompressedTransactional(base.AbstractTransactional):

	def __init__(self, buffersize=0, compresslevel=1, **kws):
		assert type(buffersize)    is int
		assert type(compresslevel) is int
		assert 0 <= buffersize
		assert 1 <= compresslevel <= 9

		self._buffersize    = buffersize
		self._compresslevel = compresslevel

		base.AbstractTransactional.__init__(self, **kws)

	def open(self):
		self._assert_closed()
		self._checkpoint_fd = bz2.BZ2File(self._checkpoint_path, self._cpt_mode, self._buffersize, self._compresslevel)
		self._log_fd        = bz2.BZ2File(self._log_path       , self._log_mode, self._buffersize, self._compresslevel)

