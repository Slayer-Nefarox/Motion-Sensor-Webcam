from time import sleep
import numpy as np
import pygame as pg
import cv2

# Programa de segmentação aplicado à interface do pygame.
# Feito por Gabriel Spressola Ziviani.
#-------------------------------------------------------

# Inicializa a captura de vídeo da webcam 
capture = cv2.VideoCapture(3)  # Atualizar esse índice dependendo da máquina
print("webcam inicializada")

# Lê um quadro da webcam para obter a resolução
ret, frame = capture.read()
if not ret:
    print("Erro ao capturar a webcam.")
    capture.release()
    pg.quit()
    exit()

# Obtém a resolução da imagem
height, width = frame.shape[:2]

# Número de quadros para amostragem do fundo
n = 20
background = np.zeros((height, width), dtype=float)

# Loop para capturar 'n' quadros para o fundo
for _ in range(n):
    ret, frame = capture.read()
    if ret:
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        background += frame_gray

# Calcula a média dos quadros capturados para usar como fundo
background /= n

# Define o limiar e o fator de atualização do fundo
threshold = 70
alpha = 1.2

# Inicializa o pygame
pg.init()
display = pg.display.set_mode((width, height))  # Define o tamanho da janela
clock = pg.time.Clock()  # Inicializa o relógio para controle de FPS
running = True
frame_count = 0
skip_frames = 2  # Captura a cada 2 quadros

# Buffer para armazenar até n posições do centróide
buffer_centroides = []
#define o tamanho do buffer
buffer_size = 5

trigger_threshold = 1000

def atualizar_buffer(nova_posicao):
    # Adiciona nova posição ao buffer
    buffer_centroides.append(nova_posicao)
    
    # Mantém o buffer com no máximo 3 elementos
    if len(buffer_centroides) > buffer_size:
        buffer_centroides.pop(0)

def media_buffer():
    # Se o buffer estiver vazio, retorna None
    if len(buffer_centroides) == 0:
        return None
    
    # Calcula a média das posições no buffer
    media_x = np.mean([pos[0] for pos in buffer_centroides])
    media_y = np.mean([pos[1] for pos in buffer_centroides])
    
    return (int(media_x), int(media_y))

def desenha_centroide(x, y):
    # Desenha um quadrado vermelho de 5x5 pixels no centróide
    rect_size = 5
    color = (255, 0, 0)  # Cor vermelha
    # Desenha o quadrado centralizado na posição (x, y)
    pg.draw.rect(display, color, pg.Rect(x - rect_size // 2, y - rect_size // 2, rect_size, rect_size))

def calcular_centroid(mt):
    # Encontra as coordenadas onde o valor é 255
    coords = np.column_stack(np.where(mt == 255))
    
    # Se houver pixels com valor 255, calcula o centróide
    if coords.size > 0:
        cont = coords.shape[0]  # Número de pixels brancos
        cont_x, cont_y = np.mean(coords, axis=0)  # Média das coordenadas
        if(cont > trigger_threshold):
            print("pew")
        print(f'Número de pixels brancos: {cont}, centroide: x[{cont_x}], y[{cont_y}]')

        # Atualiza o buffer com a nova posição do centróide
        atualizar_buffer((cont_x, cont_y))

        # Calcula a média das posições no buffer
        media_posicao = media_buffer()

        # Se houver uma média, desenha o quadrado na média
        if media_posicao is not None:
            desenha_centroide(media_posicao[0], media_posicao[1])
    else:
        print('matriz nula')


# Loop principal do programa
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False  # Fecha o programa ao clicar no 'X'

    # Captura a cada 'skip_frames' quadros
    if frame_count % skip_frames == 0:
        ret, frame = capture.read()
        if not ret:
            continue  # Pular se falhar ao capturar

        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY).astype(float)

        # Calcula a diferença entre o quadro atual e o fundo
        dif = np.abs(frame_gray - background)

        # Aplica o limiar: cria uma máscara onde a diferença é maior que o limiar
        mt = (dif > threshold) * 255
        mt = np.transpose(mt)  # Transpõe a matriz para exibição correta

        # Atualiza o fundo com o novo quadro
        background = alpha * frame_gray + (1 - alpha) * background

        # Cria uma superfície do Pygame a partir da máscara
        surf = pg.surfarray.make_surface(mt)
        display.blit(surf, (0, 0))  # Desenha a superfície na tela
        calcular_centroid(mt)

    pg.display.flip()  # Atualiza a janela
    clock.tick(60)  # Limita o FPS
    frame_count += 1

# Libera recursos
capture.release()
pg.quit()
