

CHECKPOINT_FILE_MODE = 'a'
LOG_FILE_MODE = 'a'

class AbstractTransactional(object):

	def __init__(self, checkpoint=None, log=None):
		assert type(checkpoint) is str, type(checkpoint)
		assert type(log)        is str, type(checkpoint)

		self._checkpoint_path = checkpoint
		self._log_path        = log
		self._checkpoint_fd   = None
		self._log_fd          = None

	def _assert_file_modes(self, checkpoint_mode, log_mode):
		assert self._checkpoint_fd is None
		assert self._log_fd        is None

	def _assert_closed(self):
		assert self._checkpoint_fd is None
		assert self._log_fd        is None

	def open(self, checkpoint_mode=CHECKPOINT_FILE_MODE, log_mode=LOG_FILE_MODE):
		self._assert_closed()
		self._assert_file_modes(checkpoint_mode, log_mode)
		self._checkpoint_fd  = open(self._checkpoint_path, checkpoint_mode)
		self._log_fd         = open(self._log_path       , log_mode)

	def close(self):
		self._checkpoint_fd.close() if self._checkpoint_fd is not None else ()
		self._log_fd.close()        if self._checkpoint_fd is not None else ()
		self._checkpoint_fd = None
		self._log_fd        = None


	def __enter__(self):
		self.open()
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		self.close()


	def checkpoint(self, value):
		raise NotImplementedError

	def log(self, value):
		raise NotImplementedError

	def recover(self, checkpoint_handler=None, log_handler=None):
		"""
		checkpoint_handler :: FilePath -> IO a
		log_handler        :: a -> FilePath -> IO a
		"""
		obj = checkpoint_handler(self._checkpoint_path)
		obj = log_handler(obj, self._log_path)
		return obj
