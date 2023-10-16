class Block():
	def __init__(self, size, name=None):
		self.size = size
		self.name = name
		self.used = 0
		self.next = None
		self.prev = None
		self.side = []


	def split(self):
		if self.size < 2:
			raise Exception("El bloque no se puede dividir más")
		
		# Se divide por la mitad
		left = Block(self.size//2)
		right = Block(self.size//2)

		# Se asignan sus bloques compañeros
		left.side = self.side + ['left']
		right.side = self.side + ['right']
		
		# Se actualizan los valores de los bloques en la lista
		if self.prev is not None:
			self.prev.next = left
		left.prev = self.prev
		left.next = right
		right.prev = left
		right.next = self.next
		if self.next is not None:
			self.next.prev = right

		return left


	def join(self):
		# Se verifica que el bloque pueda unirse
		if not self.getBuddy():
			return None

		# Se crea el bloque unido
		block = Block(self.size*2)


		# Si el bloque es el izquierdo
		if self.side[-1] == 'left':
			# Se unen los bloques
			block.prev = self.prev
			if block.prev is not None:
				block.prev.next = block
			
			block.next = self.next.next
			if block.next is not None:
				block.next.prev = block

		# Si el bloque es el derecho
		else:
			# Se unen los bloques
			block.prev = self.prev.prev
			if block.prev is not None:
				block.prev.next = block

			block.next = self.next
			if block.next is not None:
				block.next.prev = block
		
		# Se obtiene el nuevo rol del bloque
		block.side = self.side[:-1]

		return block
	

	def getBuddy(self):
		if len(self.side) == 0:
			return None
		elif self.side[-1] == 'left'and self.next is not None and self.next.name is None:
			return self.next
		elif self.side[-1] == 'right' and self.prev is not None and self.prev.name is None:
			return self.prev
		else:
			return None


	def __str__(self) -> str:
		if self.name is None:
			return f"({self.used}/{self.size})"
		else:
			return f"{self.name}({self.used}/{self.size})"

	def __repr__(self) -> str:
		if self.name is None:
			return f"({self.used}/{self.size})"
		else:
			return f"{self.name}({self.used}/{self.size})"