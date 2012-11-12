

from trax import base

import os, unittest

class ImplTransactional(base.AbstractTransactional):

	def checkpoint(self, value):
		self._checkpoint_fd.write(str(value))

	def log(self, value):
		self._log_fd.write(str(value) + '\n')


def checkpoint_handler(path):
	with open(path) as fd:
		return fd.read()

def log_handler(obj, path):
	with open(path) as fd:
		return [obj] + fd.readlines()


class TestBaseTransactional(unittest.TestCase):

	def setUp(self):
		self.cpt_path = 'transactional.cpt'
		self.log_path = 'transactional.log'
		self.trax = ImplTransactional(checkpoint=self.cpt_path, log=self.log_path)

	def tearDown(self):
		self.trax.close()
		os.unlink(self.cpt_path)
		os.unlink(self.log_path)

	def test_checkpoint(self):
		cpt = 'hello'
		log = 'world'

		with self.trax as t:
			t.checkpoint(cpt)
			t.log(log)

		recovered = self.trax.recover(checkpoint_handler=checkpoint_handler, log_handler=log_handler)
		self.assertTrue(recovered == [cpt, log + '\n'])
