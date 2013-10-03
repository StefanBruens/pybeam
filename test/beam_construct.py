#
# Copyright (c) 2013 Matwey V. Kornilov <matwey.kornilov@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

from pybeam import beam_construct
from construct import *
import unittest

class BEAMConstructTest(unittest.TestCase):
	def setUp(self):
		pass
	def test_erl_version_magic(self):
		c = beam_construct.erl_version_magic
		self.assertEqual(c.parse('\x83'), '\x83')
		self.assertRaises(ConstError, c.parse, '\x84')
	def test_beam(self):
		c = beam_construct.beam
		self.assertEqual(c.parse('FOR1\x00\x00\x00\x00BEAM'), Container(for1="FOR1", beam="BEAM", chunk=[], size=0))
	def test_chunk_atom(self):
		c = beam_construct.chunk_atom
		self.assertEqual(c.parse('\x00\x00\x00\x00'), Container(len=0, atom=[]))
		self.assertEqual(c.parse('\x00\x00\x00\x01\x08burtovoy'), Container(len=1, atom=["burtovoy"]))
		self.assertEqual(c.parse(c.build(Container(len=0, atom=[]))), Container(len=0, atom=[]))
		self.assertEqual(c.parse(c.build(Container(len=1, atom=["burtovoy"]))), Container(len=1, atom=["burtovoy"]))
		self.assertRaises(ArrayError, c.build, Container(len=2, atom=[]))
		self.assertRaises(ArrayError, c.parse, '\x00\x00\xff\x00')

if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(BEAMConstructTest)
	unittest.TextTestRunner(verbosity=2).run(suite)

