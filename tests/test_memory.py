import unittest
from memory import Memory

class TestMemory(unittest.TestCase):
	def setUp(self):
		self.memory = Memory(1024) # 1024 possible blocks of size 1

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
		# Deberia haber 2 bloques asignados, uno de 512 y otro de 128
		self.assertEqual(len(self.memory.assigned), 2)
		self.assertEqual(self.memory.assigned['block2'], block2)
		self.assertEqual(block2.size, 128)
		self.assertEqual(block2.used, 100)

		# Deberia haber 1 bloque de 256 y 1 de 128 libres
		self.assertEqual(len(self.memory.unasigned[8]), 1)
		self.assertEqual(len(self.memory.unasigned[7]), 1)
		free256 = self.memory.unasigned[8][0]
		free128 = self.memory.unasigned[7][0]

		# Se verifica la cadena de ida
		self.assertEqual(block1.next, block2)
		self.assertEqual(block2.next, free128)
		self.assertEqual(free128.next, free256)
		self.assertEqual(free256.next, None)

		# Se verifica la cadena de vuelta
		self.assertEqual(block1.prev, None)
		self.assertEqual(block2.prev, block1)
		self.assertEqual(free128.prev, block2)
		self.assertEqual(free256.prev, free128)

	def test_free(self):
		# Se reservan 4 bloques de distintos tamaños
		second = self.memory.reserve(100, "second")
		first = self.memory.reserve(120, "first")
		third = self.memory.reserve(50, "third")

		# Se verifica que la memoria este dividida en 6 bloques
		sequence = [128, 128, 64, 64, 128, 512]
		head = self.memory.head
		for size in sequence:
			self.assertEqual(head.size, size)
			head = head.next

		# Donde hay solo 3 libres: de 64, 128 y 512
		self.assertEqual(len(self.memory.unasigned[6]), 1)
		self.assertEqual(len(self.memory.unasigned[7]), 1)
		self.assertEqual(len(self.memory.unasigned[9]), 1)

		# Despues de liberar first deben haber 2 libres de 128
		self.memory.free("first")
		self.assertEqual(len(self.memory.unasigned[7]), 2)

		# Despues de liberar second, se juntan los 2 bloques de 128 y se crea uno de 256
		self.memory.free("second")
		self.assertEqual(len(self.memory.unasigned[7]), 1) # sigue habiendo 1 de 128 libre
		self.assertEqual(len(self.memory.unasigned[8]), 1) # se crea uno de 256

		# Despues de liberar third, se deberian juntar todos los bloques
		self.memory.free("third")
		self.assertEqual(len(self.memory.unasigned[10]), 1)
		self.assertEqual(self.memory.unasigned[10][0], self.memory.head)
		self.assertEqual(self.memory.head.size, 1024)
		self.assertEqual(self.memory.head.used, 0)
		self.assertEqual(self.memory.head.name, None)

		# Se verifica que no quedan bloques asignados ni libres que no sean el de 1024
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



if __name__ == '__main__':
	unittest.main()
