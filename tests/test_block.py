import unittest
from Block import Block

class TestBlock(unittest.TestCase):
	
	def test_empty_block_creation(self):
		block = Block(8)
		self.assertEqual(block.size, 8)
		self.assertEqual(block.used, 0)
		self.assertEqual(block.name, None)
		self.assertEqual(block.prev, None)
		self.assertEqual(block.next, None)
		self.assertEqual(block.parent, None)
		self.assertEqual(block.side, None)
	
	def test_block_creation(self):
		block = Block(8, 'test')
		self.assertEqual(block.size, 8)
		self.assertEqual(block.used, 0)
		self.assertEqual(block.name, 'test')
		self.assertEqual(block.prev, None)
		self.assertEqual(block.next, None)
		self.assertEqual(block.parent, None)
		self.assertEqual(block.side, None)

	def test_block_split(self):
		block = Block(8)
		
		left = block.split()
		self.assertEqual(left.size, 4)
		self.assertEqual(left.used, 0)
		self.assertEqual(left.name, None)
		self.assertEqual(left.prev, None)
		self.assertNotEqual(left.next, None)
		self.assertEqual(left.side, 'left')
		self.assertEqual(left.parent, block)

		right = left.next
		self.assertEqual(right.size, 4)
		self.assertEqual(right.used, 0)
		self.assertEqual(right.name, None)
		self.assertEqual(right.prev, left)
		self.assertEqual(right.next, None)
		self.assertEqual(right.side, 'right')
		self.assertEqual(right.parent, block)

		# Se verifica que los bloques esten asignados como compañeros
		self.assertEqual(left.getBuddy(), right)
		self.assertEqual(right.getBuddy(), left)
		self.assertEqual(block.left, left)
		self.assertEqual(block.right, right)

	def test_block_split_twice(self):
		block = Block(16)
		
		left = block.split()
		a = left.split()
		b = a.next

		right = left.next
		c = right.split()
		d = c.next

		for x in [a,b,c,d]:
			self.assertEqual(x.size, 4)
			self.assertEqual(x.used, 0)
			self.assertEqual(x.name, None)
			self.assertEqual(x.parent.parent, block)

		# Se verifica que los bloques estén enlazados de ida
		self.assertEqual(a.next, b)
		self.assertEqual(b.next, c)
		self.assertEqual(c.next, d)
		self.assertEqual(d.next, None)

		# Se verifica que los bloques estén enlazados de vuelta
		self.assertEqual(a.prev, None)
		self.assertEqual(b.prev, a)
		self.assertEqual(c.prev, b)
		self.assertEqual(d.prev, c)

		# Se verifican los roles de los bloques
		self.assertEqual(a.side, 'left')
		self.assertEqual(b.side, 'right')
		self.assertEqual(c.side, 'left')
		self.assertEqual(d.side, 'right')

	def test_split_4_times(self):
		block = Block(32)
		
		left = block.split()
		le = left.split()
		ft = le.next

		a = le.split()
		b = a.next

		c = ft.split()
		d = c.next

		right = left.next
		ri = right.split()
		ght = ri.next

		e = ri.split()
		f = e.next

		g = ght.split()
		h = g.next


		for x in [a,b,c,d,e,f,g,h]:
			self.assertEqual(x.size, 4)
			self.assertEqual(x.used, 0)
			self.assertEqual(x.name, None)
			self.assertEqual(x.parent.parent.parent, block)

		# Se verifica que los bloques estén enlazados de ida
		self.assertEqual(a.next, b)
		self.assertEqual(b.next, c)
		self.assertEqual(c.next, d)
		self.assertEqual(d.next, e)
		self.assertEqual(e.next, f)
		self.assertEqual(f.next, g)
		self.assertEqual(g.next, h)
		self.assertEqual(h.next, None)

		# Se verifica que los bloques estén enlazados de vuelta
		self.assertEqual(a.prev, None)
		self.assertEqual(b.prev, a)
		self.assertEqual(c.prev, b)
		self.assertEqual(d.prev, c)
		self.assertEqual(e.prev, d)
		self.assertEqual(f.prev, e)
		self.assertEqual(g.prev, f)
		self.assertEqual(h.prev, g)

		# Se verifican los roles de los bloques
		self.assertEqual(a.side, 'left')
		self.assertEqual(b.side, 'right')

		self.assertEqual(c.side, 'left')
		self.assertEqual(d.side, 'right')

		self.assertEqual(e.side, 'left')
		self.assertEqual(f.side, 'right')

		self.assertEqual(g.side, 'left')
		self.assertEqual(h.side, 'right')

	def test_block_cant_join(self):
		block = Block(8)
		left = block.split()
		right = left.next

		right.name = 'used'
		right.used = 4

		self.assertEqual(left.join(), None)

	def test_block_join(self):
		block = Block(8)
		left = block.split()
		right = left.next

		parent = left.join()

		self.assertEqual(parent.size, 8)
		self.assertEqual(parent.used, 0)
		self.assertEqual(parent.name, None)
		self.assertEqual(parent.prev, None)
		self.assertEqual(parent.next, None)
		self.assertEqual(parent.side, None)
		self.assertEqual(parent.side, None)
		self.assertEqual(parent.parent, None)

	def test_block_join_left(self):
		block = Block(8)
		left = block.split()
		right = left.next

		a = left.split()
		b = a.next

		parent = a.join()

		self.assertEqual(parent.size, 4)
		self.assertEqual(parent.used, 0)
		self.assertEqual(parent.name, None)
		self.assertEqual(parent.prev, None)
		self.assertEqual(parent.next, right)
		self.assertEqual(parent.side, 'left')

	def test_block_join_right(self):
		block = Block(8)
		left = block.split()
		right = left.next

		a = right.split()
		b = a.next

		parent = a.join()

		self.assertEqual(parent.size, 4)
		self.assertEqual(parent.used, 0)
		self.assertEqual(parent.name, None)
		self.assertEqual(parent.prev, left)
		self.assertEqual(parent.next, None)
		self.assertEqual(parent.side, 'right')		

		
if __name__ == '__main__':
	unittest.main()
