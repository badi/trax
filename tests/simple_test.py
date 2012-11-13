
from trax import simple

import os, random, unittest




class  TestSimple(unittest.TestCase):

	def clean(self):
		for p in ['transactional.cpt', 'transactional.log']:
			if os.path.exists(p):
				os.unlink(p)

	def setUp(self):
		self.clean()

	def tearDown(self):
		self.clean()


	def test_example(self):

		trax = simple.SimpleTransactional()
		with trax as trx:
			state = []
			for i in xrange(1000):
				state.append(i)
				trx.log(str(i) + '\n')
				if i % 50 == 0:
					# print 'Checkpointing', state
					trx.checkpoint(state)

		def log_handler(obj, fd):
			for line in map(str.strip, fd):
				obj.append(int(line))
			return obj

		recovered = trax.recover(log_handler)
		# print 'State:', state
		# print 'Recov:', recovered
		self.assertTrue( state == recovered )


if __name__ == '__main__':
	TestExample().test_example()
