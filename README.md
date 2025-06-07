# 🐍 Snake-T: Juego señuelo con reverse shell en segundo plano

Este proyecto es una combinación de dos componentes:
1. Un **juego clásico de Snake** hecho con `pygame`.
2. Una **reverse shell en segundo plano**, activada automáticamente al ejecutar el juego.


## ⚠️ ADVERTENCIA

Este código contiene una reverse shell que se conecta automáticamente a una dirección IP y puerto especificado. **Su uso indebido puede ser ilegal**. Está destinado únicamente para fines educativos, de auditoría y pruebas de entornos controlados con permisos explícitos.


## 🎮 Características

- Juego Snake con IA automática que se mueve hacia la comida.
- Reverse shell embebida que se conecta a un servidor remoto.
- Ejecución discreta del payload usando hilos (`threading`).
- Interfaz del juego funcional y atractiva usando `pygame`.


## ⚙️ Requisitos

- Python 3.x
- `pygame`  
  Puedes instalarlo con:

bash

pip install pygame --break-system-packages
