"""
1. Setup
2. Call a "unit"
3. Make an assertion about the result
4. Teardown
"""
# std lib imports
import unittest

# local imports
from markov import (Markov, get_table)

# 3rd party imports
#import abcd
     
class TestMarkov(unittest.TestCase):
    
    def test_get_table(self):
        res = get_table('ab')
        self.assertEqual(res, {'a':{'b':1}})
 
 
if __name__ == '__main__':
    unittest.main()

