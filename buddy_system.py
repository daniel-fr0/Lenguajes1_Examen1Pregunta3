from sys import argv
from memory import Memory
from Block import isPowerOf2

def main(argv):
	if len(argv) < 2:
		print("Uso: python3 buddy_system.py <numero de bloques de memoria>")
		return
	
	size = int(argv[1])
	if size <= 0:
		print("El numero de bloques debe ser mayor a 0")
		return
	
	if not isPowerOf2(size):
		print("El numero de bloques debe ser una potencia de 2")
		return
	
	memory = Memory(size)

	while True:
		print("\n\nQue desea hacer?")
		print("Comandos disponibles:")
		print("Para reservar memoria: RESERVAR <cantidad> <nombre>")
		print("Para liberar memoria: LIBERAR <nombre>")
		print("Para mostrar el estado de la memoria: MOSTRAR")
		print("Para salir: SALIR")
		print("Ingrese un comando a continuacion...")

		command = input()
		print("\n")

		command = command.split()
		if command[0].upper() == "RESERVAR":
			if len(command) < 3:
				print("Faltan argumentos")
				continue

			try:
				size = int(command[1])
				name = command[2]
				memory.reserve(size, name)
				print("Memoria reservada exitosamente")
			except Exception as e:
				print("Error: ", e)
		elif command[0].upper() == "LIBERAR":
			if len(command) < 2:
				print("Faltan argumentos")
				continue

			try:
				name = command[1]
				memory.free(name)
				print("Memoria liberada exitosamente")
			except Exception as e:
				print("Error: ", e)
		elif command[0].upper() == "MOSTRAR":
			memory.show()
		elif command[0].upper() == "SALIR":
			break
		else:
			print("Comando no reconocido")




if __name__ == '__main__':
    main(argv)