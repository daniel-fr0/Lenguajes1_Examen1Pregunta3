from Block import Block
from math import ceil, log2

# Memory using buddy system
class Memory():
	def __init__(self, size):
		self.size = size
		self.head = Block(size)
		self.assigned = {}
		self.unasigned = []
		i = 1
		while i <= size:
			self.unasigned.append([])
			i *= 2
		self.unasigned[-1].append(self.head)

	def reserve(self, size, name):
		# Se verifica que el tamaño del bloque no sea mayor al de la memoria total
		if size > self.size:
			raise Exception("El tamaño del bloque es mayor al de la memoria")
		
		# Se verifica que el nombre no esté en uso
		if name in self.assigned:
			raise Exception("El nombre ya está en uso")
		

		# Se busca el bloque más pequeño que pueda contener la memoria
		i = ceil(log2(size))
		while len(self.unasigned[i]) == 0:
			i += 1
			if i >= len(self.unasigned):
				raise Exception("No quedan bloques libres de tamaño suficiente")
			

		# Se obtiene el bloque de tamaño adecuado
		block = self.unasigned[i].pop(0)

		# Se divide de ser posible hasta obtener el tamaño mas ajustado
		while block.size//2 >= size:
			block = block.split()
			self.unasigned[i-1].append(block.next)
			i -= 1

		# Se reafirma la cabeza de la lista
		if block.prev is None:
			self.head = block

		# Se asigna el bloque
		block.name = name
		block.used = size
		self.assigned[name] = block

		return block
	
	def free(self, name):
		# Se verifica que el nombre esté en uso
		if name not in self.assigned:
			raise Exception("No se encontró memoria asignada con ese nombre")
		
		# Se obtiene el bloque
		block = self.assigned[name]

		# Se libera el bloque
		block.name = None
		block.used = 0
		self.assigned.pop(name)
		self.unasigned[ceil(log2(block.size))].append(block)

		# Se une el bloque con sus compañeros mientras sea posible
		buddy = block.getBuddy()
		while buddy is not None:
			self.unasigned[ceil(log2(buddy.size))].remove(block)
			self.unasigned[ceil(log2(buddy.size))].remove(buddy)
			block = block.join()
			self.unasigned[ceil(log2(block.size))].append(block)
			buddy = block.getBuddy()

		# Se reafirma la cabeza de la lista
		if block.prev is None:
			self.head = block

	def show(self):
		# El estado de la memoria actual
		print("MEMORIA")
		print("Tamaño total: ", self.size)
		print(f"Estado actual: ", end="")
		block = self.head
		print(block, end="")
		while block.next is not None:
			print(f" -> {block.next}", end="")
			block = block.next
		print()


		# Los bloques asignados
		print("\n\nBLOQUES ASIGNADOS")
		for name in self.assigned:
			print(f"{name}: {self.assigned[name]}")

		# La lista de bloques libres
		print("\n\nLISTAS DE BLOQUES LIBRES")
		for i in range(len(self.unasigned)):
			print(f"{2**i}: {self.unasigned[i]}")