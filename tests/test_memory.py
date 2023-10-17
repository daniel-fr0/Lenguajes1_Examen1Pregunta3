import unittest
from memory import Memory

class TestMemory(unittest.TestCase):
	def setUp(self):
		self.memory = Memory(1024) # 1024 possible blocks of size 1

	def test_getPartition(self):
		self.memory.reserve(100, "block2")
		self.memory.reserve(120, "block1")
		self.memory.reserve(50, "block3")

		# Se verifica que la memoria este dividida en la secuencia correcta
		partition = self.memory.getPartition()
		block = self.memory.head
		while block:
			self.assertEqual(block, partition.pop(0))
			block = block.next

	def test_reserve(self):
		# Se reserva un bloque de 512
		block1 = self.memory.reserve(512, "block1")
		# Deberia haber 1 bloque de 512 asignado
		self.assertEqual(len(self.memory.assigned), 1)
		self.assertEqual(self.memory.assigned['block1'], block1)
		free = block1.next

		# Deberia haber 1 bloque de 512 libre
		self.assertEqual(len(self.memory.unasigned[9]), 1)
		self.assertEqual(self.memory.unasigned[9][0], free)
		self.assertEqual(free.size, 512)
		self.assertEqual(free.name, None)
		self.assertEqual(free.used, 0)

		# Se reserva un bloque de 100
		block2 = self.memory.reserve(100, "block2")
		# Deberia haber 2 bloques asignados, uno de 512 y otro de 100
		self.assertEqual(len(self.memory.assigned), 2)
		self.assertEqual(self.memory.assigned['block1'], block1)
		self.assertEqual(self.memory.assigned['block2'], block2)
		self.assertEqual(block2.size, 100)
		self.assertEqual(block2.used, 100)

		# Deberia haber 1 bloque de 256, 1 de 128, 1 de 16, 1 de 8 y 1 de 4 libres
		self.assertEqual(len(self.memory.unasigned[8]), 1)
		self.assertEqual(len(self.memory.unasigned[7]), 1)
		self.assertEqual(len(self.memory.unasigned[4]), 1)
		self.assertEqual(len(self.memory.unasigned[3]), 1)
		self.assertEqual(len(self.memory.unasigned[2]), 1)

		# Se verifica la cadena de bloques en memoria
		blocks = self.memory.getPartition()
		self.assertEqual(blocks[:2], [block1, block2])
		self.assertEqual([b.size for b in blocks], [512, 100, 16, 8, 4, 128, 256])

	def test_free(self):
		# Se reservan 4 bloques de distintos tamaños
		self.memory.reserve(100, "block2")
		self.memory.reserve(120, "block1")
		self.memory.reserve(50, "block3")

		# Se verifica que la memoria este dividida en la secuencia correcta
		sequence = [100, 16, 8, 4, 120, 8, 50, 8, 4, 2, 64, 128, 512]
		self.assertEqual([b.size for b in self.memory.getPartition()], sequence)

		# Despues de liberar block1 se revisa la secuencia de nuevo
		sequence = [100, 16, 8, 4, 128, 50, 8, 4, 2, 64, 128, 512]
		self.memory.free("block1")
		self.assertEqual([b.size for b in self.memory.getPartition()], sequence)

		# Despues de liberar block2 se revisa la secuencia de nuevo
		sequence = [256, 50, 8, 4, 2, 64, 128, 512]
		self.memory.free("block2")
		self.assertEqual([b.size for b in self.memory.getPartition()], sequence)

		# # Despues de liberar third, se deberian juntar todos los bloques
		self.memory.free("block3")
		self.assertEqual(len(self.memory.unasigned[10]), 1)
		self.assertEqual(self.memory.getPartition()[0], self.memory.head)
		self.assertEqual(self.memory.unasigned[10][0], self.memory.head)
		self.assertEqual(self.memory.head.size, 1024)
		self.assertEqual(self.memory.head.used, 0)
		self.assertEqual(self.memory.head.name, None)

		# # Se verifica que no quedan bloques asignados ni libres que no sean el de 1024
		self.assertEqual(len(self.memory.assigned), 0)
		for i in range(10):
			self.assertEqual(len(self.memory.unasigned[i]), 0)

	def test_reserve_error(self):
		# Excepcion si se reserva un bloque mayor al de la memoria
		self.assertRaises(Exception, self.memory.reserve, 1025, "HUGE")
		self.memory.reserve(512, "block1")

		# Excepcion si se reserva un bloque con un nombre ya en uso
		self.assertRaises(Exception, self.memory.reserve, 513, "block1")

		# Excepcion si no quedan bloques libres de tamaño suficiente
		self.memory.reserve(200, "block2")
		self.assertRaises(Exception, self.memory.reserve, 300, "block3")

	def test_free_error(self):
		# Excepcion si se libera un bloque que no existe
		self.assertRaises(Exception, self.memory.free, "block1")

		# O si ya fue liberado
		self.memory.reserve(512, "block1")
		self.memory.free("block1")
		self.assertRaises(Exception, self.memory.free, "block1")

	def test_small_run(self):
		memory = Memory(16)
		memory.reserve(11, "block1")
		memory.reserve(2, "block2")
		self.assertListEqual([b.size for b in memory.getPartition()], [11, 2, 2, 1])

		memory.free("block1")
		self.assertListEqual([b.size for b in memory.getPartition()], [8, 2, 1, 2, 2, 1])

		memory.reserve(3, "block3")
		self.assertListEqual([b.size for b in memory.getPartition()], [3, 1, 4, 2, 1, 2, 2, 1])

		memory.free("block2")
		self.assertListEqual([b.size for b in memory.getPartition()], [3, 1, 4, 2, 1, 4, 1])

		memory.free("block3")
		self.assertListEqual([b.size for b in memory.getPartition()], [16])

if __name__ == '__main__':
	unittest.main()
