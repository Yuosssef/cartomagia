import pygame
import random
import sys
import threading
import time

# Som
pygame.mixer.init()
pygame.init()

def som_rodada0():
    
    som1 = pygame.mixer.Sound("escolha sua carta.mp3")
    som2 = pygame.mixer.Sound("em que fileira esta.mp3")

    som1.play()
    time.sleep(som1.get_length())
    som2.play()
    time.sleep(som2.get_length())
   

def som_rodada1():
 
    som3 = pygame.mixer.Sound("pela segunda vez.mp3")
    som3.play()

def som_rodada2():
    som4 = pygame.mixer.Sound("pela ultima vez.mp3")
    som4.play()
    
def main():

    # Cores
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (220, 20, 60)
    GRAY = (200, 200, 200)
    SHADOW = (180, 180, 180)
    BUTTON_COLOR = (220, 20, 60)
    BUTTON_SHADOW = (104, 00, 0)
    TEXT_COLOR = WHITE
    
    # Tela
    WIDTH, HEIGHT = 1280, 768
    fundo = pygame.image.load("fundo.png")
    fundo = pygame.transform.scale(fundo, (WIDTH, HEIGHT))
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Adivinhação das 21 Cartas")

    # Fontes
    font = pygame.font.SysFont('Times New Roman', 32)
    font_btn = pygame.font.SysFont('Arial', 28, bold=True)

    # Baralho
    suits = ['♥', '♦', '♣', '♠']
    values = ['A'] + [str(n) for n in range(2, 11)] + ['J', 'Q', 'K']
    baralho = [v + s for s in suits for v in values]

    def cor_carta(carta):
        return RED if '♥' in carta or '♦' in carta else BLACK

    def embaralhar_cartas():
        return random.sample(baralho, 21)

    def distribuir_em_montes(cartas):
        montes = [[], [], []]
        for i, carta in enumerate(cartas):
            montes[i % 3].append(carta)
        return montes

    def recompor_cartas(montes, escolha):
        if escolha == 0:
            nova_ordem = montes[1] + montes[0] + montes[2]
        elif escolha == 1:
            nova_ordem = montes[0] + montes[1] + montes[2]
        else:
            nova_ordem = montes[0] + montes[2] + montes[1]
        return nova_ordem

    def desenhar_carta(carta, x, y):
        largura, altura = 80, 120
        sombra_offset = 5
        pygame.draw.rect(screen, SHADOW, (x + sombra_offset, y + sombra_offset, largura, altura))
        pygame.draw.rect(screen, WHITE, (x, y, largura, altura))
        pygame.draw.rect(screen, BLACK, (x, y, largura, altura), 2)
        texto = font.render(carta, True, cor_carta(carta))
        text_rect = texto.get_rect(center=(x + largura // 2, y + altura // 2))
        screen.blit(texto, text_rect)

    def desenhar_montes(montes):
        screen.fill(WHITE)
        screen.blit(fundo, (0, 0))
        for i, monte in enumerate(montes):
            y_base = 140 + i * 180
            for j, carta in enumerate(monte):
                desenhar_carta(carta, 200 + j * 105, y_base)

            sombra = botoes[i].move(3, 3)
            pygame.draw.rect(screen, BUTTON_SHADOW, sombra, border_radius=10)
            pygame.draw.rect(screen, BUTTON_COLOR, botoes[i], border_radius=10)
            txt_btn = font_btn.render("Está aqui", True, TEXT_COLOR)
            text_rect = txt_btn.get_rect(center=botoes[i].center)
            screen.blit(txt_btn, text_rect)
        pygame.display.flip()
        
    def mostrar_carta_escolhida(carta):
        pygame.event.clear()  # Limpa todos os eventos pendentes
        screen.fill(WHITE)
        screen.blit(fundo, (0, 0))
        mensagem = font.render("A carta escolhida foi:", True, BLACK)
        screen.blit(mensagem, (WIDTH // 2 - mensagem.get_width() // 2, HEIGHT // 2 - 100))
        largura, altura = 80, 120
        x = WIDTH // 2 - largura // 2
        y = HEIGHT // 2 - altura // 2
        sombra_offset = 5
        pygame.draw.rect(screen, SHADOW, (x + sombra_offset, y + sombra_offset, largura, altura))
        pygame.draw.rect(screen, WHITE, (x, y, largura, altura))
        pygame.draw.rect(screen, BLACK, (x, y, largura, altura), 2)
        texto = font.render(carta, True, cor_carta(carta))
        text_rect = texto.get_rect(center=(x + largura // 2, y + altura // 2))
        screen.blit(texto, text_rect)
        pygame.display.flip()
            
        # Som carta revelada
        carta = carta_escolhida
        ext = '.mp3'
        if carta[-1] == '♥': 
            som_naipe = "copas"+ ext
        elif carta[-1] == '♠':
            som_naipe = "espadas"+ ext
        elif carta[-1] == '♣':
            som_naipe = "paus"+ ext
        elif carta[-1] == '♦':
            som_naipe = "ouros"+ ext
        som_carta = carta[:-1].lower() + ext
       
        som1 = pygame.mixer.Sound("a carta escolhida foi.mp3")
        som2 = pygame.mixer.Sound(som_carta)
        som3 = pygame.mixer.Sound(som_naipe)
        som1.play()
        time.sleep(som1.get_length())
        som2.play()
        time.sleep(som2.get_length())
        som3.play()
        
        pygame.time.wait(5000)
        pygame.event.clear()  # Garante que nenhum clique fique acumulado ao voltar      
        
    cartas = embaralhar_cartas()
    rodada = 0
    botoes = [pygame.Rect(1000, 130 + i * 180 + 40, 150, 60) for i in range(3)]

    running = True
    mostrar_revelacao = False
    
    while running:
        montes = distribuir_em_montes(cartas)
        desenhar_montes(montes)

        esperando_click = True

        if rodada == 0:
   
            threading.Thread(target=som_rodada0).start()
        elif rodada == 1:
            threading.Thread(target=som_rodada1).start()
        elif rodada == 2:
            threading.Thread(target=som_rodada2).start()

        while esperando_click:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    esperando_click = False
                    break

                elif event.type == pygame.MOUSEBUTTONDOWN and not mostrar_revelacao:
                    for i, botao in enumerate(botoes):
                        if botao.collidepoint(event.pos):
                            cartas = recompor_cartas(montes, i)
                            rodada += 1
                            esperando_up = True
                            while esperando_up:
                                for e in pygame.event.get():
                                    if e.type == pygame.MOUSEBUTTONUP:
                                        esperando_up = False
                            pygame.event.clear()
                            esperando_click = False
                            break

        # Ultima rodada
        if rodada == 3:
            mostrar_revelacao = True
            carta_escolhida = cartas[10]
            mostrar_carta_escolhida(carta_escolhida)
            cartas = embaralhar_cartas()
            rodada = 0
            mostrar_revelacao = False
       
        # Deixar esse codigo: don't ask... :)
        elif rodada > 3:
            mostrar_revelacao = False
            cartas = embaralhar_cartas()
            rodada = 0
            
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
