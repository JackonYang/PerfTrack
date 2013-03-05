import unittest
import watch_filter

class test_filter(unittest.TestCase):

	def setUp(self):
		pass
	def tearDown(self):
		pass

	def test_filter(self):
		data=[2.1,4.3,2.3,4.5,6.7,9.1,1.2,3.2,4.6,1.9,8.2,1.9,2.8,3.5,4.3,4.9,4.1,2.1,4.3,2.3,4.5,6.7,9.1,1.2,3.2,4.6,8.2,1.9,2.8,3.5,4.3,4.9,4.1]
		print(watch_filter.keep_peak(data))
	def test_read_data(self):
		for tag,value in watch_filter.read_data('test_03041503_cpu.txt').items():
			print(tag,value)
		for tag,value in watch_filter.read_data('test_03041503_mem.txt').items():
			print(tag,value)

if __name__=='__main__':
	suite=unittest.TestSuite()

	#suite.addTest(test_filter('test_filter'))
	suite.addTest(test_filter('test_read_data'))

	runner=unittest.TextTestRunner()
	runner.run(suite)
