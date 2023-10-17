class Block():
	def __init__(self, size, name=None):
		self.size = size
		self.name = name
		self.used = 0
		self.next = None
		self.prev = None
		self.side = None
		self.parent = None
		self.right = None
		self.left = None


	def split(self, defrag=False):
		if self.size < 2:
			raise Exception("El bloque no se puede dividir más")

		partSize = self.size//2 if isPowerOf2(self.size) else 2**(self.size.bit_length()-1)
		
		if defrag:
			partSize = self.used
		
		# Se divide de acuerdo al tamaño del bloque mayor
		left = Block(partSize)
		left.parent = self
		left.side = 'left'

		right = Block(self.size - partSize)
		right.parent = self
		right.side = 'right'
		
		# Se actualizan los valores de los bloques en la lista
		if self.prev:
			self.prev.next = left
		left.prev = self.prev
		left.next = right
		right.prev = left
		right.next = self.next
		if self.next:
			self.next.prev = right

		# Se libera el bloque actual, ya que se dividió y no se usa
		self.free()

		# Se guardan los bloques hijos
		self.left = left
		self.right = right

		return left

	def join(self):
		# Se verifica que el bloque pueda unirse
		buddy = self.getBuddy()
		if buddy is None:
			return None

		# Se obtiene el padre
		block = self.parent

		# Si el bloque es el izquierdo
		if self.side == 'left':
			# Se enlazan los bloques
			block.prev = self.prev
			if block.prev:
				block.prev.next = block
			
			block.next = buddy.next
			if block.next:
				block.next.prev = block

		# Si el bloque es el derecho
		else:
			# Se enlazan los bloques
			block.prev = buddy.prev
			if block.prev:
				block.prev.next = block

			block.next = self.next
			if block.next:
				block.next.prev = block

		return block

	def getBuddy(self):
		if not self.parent:
			return None
		
		# Si el bloque es izquierdo y su compañero esta libre
		if (self.side == 'left' and self.parent.right.isFree()):
			return self.parent.right
		
		# Si el bloque es derecho y su compañero esta libre
		elif (self.side == 'right' and self.parent.left.isFree()):
			return self.parent.left
		
		return None
		
	def free(self):
		self.name = None
		self.used = 0
		self.left = None
		self.right = None

	def isFree(self):
		if not self.right and not self.left:
			return not self.name
		
		return self.left.isFree() and self.right.isFree()

	def __str__(self) -> str:
		if not self.name:
			return f"({self.used}/{self.size})"
		else:
			return f"{self.name}({self.used}/{self.size})"

	def __repr__(self) -> str:
		if not self.name:
			return f"({self.used}/{self.size})"
		else:
			return f"{self.name}({self.used}/{self.size})"
		

def isPowerOf2(n):
	return n & (n-1) == 0