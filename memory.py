from Block import Block, isPowerOf2
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
			

		# Se obtiene el bloque de tamaño mas cercano
		block = self.unasigned[i].pop(0)

		# Se ajusta el tamaño del bloque de ser necesario
		block = self.fit(block, size)

		# Se asigna el bloque
		block.name = name
		block.used = size
		self.assigned[name] = block

		return block
	
	def fit(self, block, size):
		# Se divide de ser posible hasta obtener el tamaño mas ajustado
		while block.size//2 >= size:
			block = block.split()
			self.unasigned[ceil(log2(block.size))].append(block.next)

		# Se actualiza el tamaño usado y se desfragmenta si es necesario
		block.used = size
		if block.size > size:
			block = block.split(defrag=True)
			buddy = block.next

			# Si el bloque compañero no es potencia de 2, se divide hasta que lo sea
			while not isPowerOf2(buddy.size):
				buddy = buddy.split()
				# Se van agregando los sub-bloques a la lista de bloques libres
				self.unasigned[ceil(log2(buddy.size))].append(buddy)
				buddy = buddy.next

			# Se agrega el compañero a la lista de bloques libres
			self.unasigned[ceil(log2(buddy.size))].append(buddy)

		# Se reafirma la cabeza de la lista
		if block.prev is None:
			self.head = block

		return block
	
	def free(self, name):
		# Se verifica que el nombre esté en uso
		if name not in self.assigned:
			raise Exception("No se encontró memoria asignada con ese nombre")
		
		# Se obtiene el bloque
		block = self.assigned[name]

		# Se libera el bloque
		block.free()
		self.assigned.pop(name)
		self.unasigned[ceil(log2(block.size))].append(block)

		# Se unen los bloques contiguos
		block = self.joinContiguous(block)

		# Si el bloque no es potencia de 2, se divide hasta que lo sea
		while not isPowerOf2(block.size):
			self.unasigned[ceil(log2(block.size))].remove(block)
			block = block.split()
			self.unasigned[ceil(log2(block.size))].append(block)
			self.unasigned[ceil(log2(block.next.size))].append(block.next)

			# Se asegura la cabeza de la lista
			if block.prev is None:
				self.head = block

			block = block.next

		return block

	def joinContiguous(self, block):
		# Se verifica que el bloque pueda unirse
		if not block.parent or not block.parent.isFree():
			return block
		
		# Se busca en el arbol un bloque que sea potencia de 2 y este libre
		goal = block.parent
		lastPowerOf2 = goal if isPowerOf2(goal.size) else None
		while goal.parent and goal.parent.isFree():
			goal = goal.parent
			if isPowerOf2(goal.size):
				lastPowerOf2 = goal

		# Si no se encontro un bloque potencia de 2, se retorna el bloque
		if not lastPowerOf2:
			return block
		
		# Se ajusta el objetivo si no es potencia de 2
		if not isPowerOf2(goal.size):
			goal = lastPowerOf2
				

		buddy = block.getBuddy()
		# Se une el bloque con su compañero hasta llegar al objetivo
		while block != goal and buddy:

			# El compañero esta particionado si no esta en la lista de bloques libres
			if buddy not in self.unasigned[ceil(log2(buddy.size))]:
					# Se junta la particion desde el primer bloque libre del compañero
					if block.side == 'left':
						return self.joinContiguous(block.next)
					else:
						return self.joinContiguous(block.prev)
					
			# Se eliminan los bloques de la lista de bloques libres
			self.unasigned[ceil(log2(block.size))].remove(block)
			self.unasigned[ceil(log2(buddy.size))].remove(buddy)

			# Se unen los bloques y se asinan a la lista de bloques libres
			block = block.join()
			self.unasigned[ceil(log2(block.size))].append(block)

			buddy = block.getBuddy()

		# Se reafirma la cabeza de la lista
		if block.prev is None:
			self.head = block

		return block

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

	def getPartition(self):
		partition = []
		block = self.head
		while block is not None:
			partition.append(block)
			block = block.next

		return partition