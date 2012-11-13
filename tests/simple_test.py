
import trax

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

		transactional = trax.SimpleTransactional()
		with transactional as trx:
			state = []
			for i in xrange(1000):
				v = random.randint(0,100000)
				state.append(v)
				trx.log(str(v) + '\n')
				if i % 50 == 0:
					trx.checkpoint(state)

		def log_handler(obj, fd):
			for line in map(str.strip, fd):
				obj.append(int(line))
			return obj

		with transactional as trx:
			recovered = trx.recover(log_handler)

		self.assertTrue( state == recovered )


if __name__ == '__main__':
	TestExample().test_example()
