import pygame
import sys
import random

# Inicializa o Pygame
pygame.init()

# Configurações da janela
LARGURA = 800
ALTURA = 600
janela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Faroeste')

# Carregar imagens
fundo_imagem = pygame.image.load("C:/Users/henri/Desktop/Codigo/Imagens/fundo.jpg")
jogador_imagem = pygame.image.load("C:/Users/henri/Desktop/Codigo/Imagens/c.jpg")
inimigo_imagem = pygame.image.load("C:/Users/henri/Desktop/Codigo/Imagens/vilao.jpg")
bala_imagem = pygame.image.load("C:/Users/henri/Desktop/Codigo/Imagens/bala.png")
# Ajustar o tamanho das imagens
jogador_imagem = pygame.transform.scale(jogador_imagem, (60, 100))
inimigo_imagem = pygame.transform.scale(inimigo_imagem, (60, 100))
bala_imagem = pygame.transform.scale(bala_imagem, (15, 5))

# Definir cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

# Carregar sons
pygame.mixer.music.load("C:/Users/henri/Desktop/Codigo/sons/a.ogg")  # Som de fundo (use .mp3 ou .ogg)
pygame.mixer.music.set_volume(0.3)  # Ajusta o volume do fundo
som_disparo = pygame.mixer.Sound("C:/Users/henri/Desktop/Codigo/sons/b.ogg")  # Som do disparo

# Configurações do jogador
LARGURA_JOGADOR = 60
ALTURA_JOGADOR = 100
x_jogador = 100
y_jogador = ALTURA - ALTURA_JOGADOR - 10
velocidade_jogador = 5  # Aumentando a velocidade do jogador
velocidade_bala = 10  # Aumentando a velocidade da bala

# Variáveis para pulo
pulo = False  # Status do pulo (se está pulando ou não)
velocidade_pulo = -15  # Velocidade inicial do pulo (quanto mais negativo, mais alto o pulo)
gravidade = 1  # Gravidade, o que vai fazer o personagem cair
velocidade_queda = 0  # Velocidade atual de queda

# Configuração da "câmera" (simula o movimento de tela)
camera_x = 0
estagio = 1  # Inicia com o Stage 1

# Configurações dos inimigos
inimigos = []
inimigos_ativos = []
tiros_inimigos = []

# Função para desenhar o jogador
def desenhar_jogador(x, y):
    janela.blit(jogador_imagem, (x - camera_x, y))

# Função para desenhar as balas
def desenhar_balas(balas):
    for bala in balas:
        janela.blit(bala_imagem, (bala[0] - camera_x, bala[1]))

# Função para desenhar os tiros dos inimigos
def desenhar_tiros_inimigos(tiros):
    for tiro in tiros:
        janela.blit(bala_imagem, (tiro[0] - camera_x, tiro[1]))

# Função para desenhar os inimigos
def desenhar_inimigos(inimigos):
    for inimigo in inimigos:
        janela.blit(inimigo_imagem, (inimigo[0] - camera_x, inimigo[1]))

# Função para criar inimigos
def criar_inimigos():
    for _ in range(1):  # Limite para inimigos, 1 por vez
        y_inimigo = ALTURA - 120
        x_inimigo = random.randint(LARGURA + 100, LARGURA + 400)
        inimigos.append([x_inimigo, y_inimigo])

# Função para criar tiro inimigo
def criar_tiro_inimigo(x, y):
    tiros_inimigos.append([x, y + 50, -2])  # Tiro vai para a esquerda (diminui a velocidade do tiro)

# Função para verificar colisão entre bala e inimigo
def verificar_colisao(balas, inimigo_x, inimigo_y, inimigo_largura, inimigo_altura):
    for bala in balas:
        if (bala[0] + 15 > inimigo_x and bala[0] < inimigo_x + inimigo_largura) and \
           (bala[1] + 5 > inimigo_y and bala[1] < inimigo_y + inimigo_altura):
            return True
    return False

# Função para verificar colisão entre tiro inimigo e jogador
def verificar_colisao_tiro_inimigo(tiros, jogador_x, jogador_y, jogador_largura, jogador_altura):
    for tiro in tiros:
        if (tiro[0] + 15 > jogador_x and tiro[0] < jogador_x + jogador_largura) and \
           (tiro[1] + 5 > jogador_y and tiro[1] < jogador_y + jogador_altura):
            return True
    return False

# Função para mover os inimigos
def mover_inimigos(inimigos, balas):
    for inimigo in inimigos:
        inimigo[0] -= 1  # Diminui a velocidade de movimento dos inimigos
        if random.randint(1, 60) == 1:  # Chance aleatória de disparar
            criar_tiro_inimigo(inimigo[0], inimigo[1])

# Função para mover as balas
def mover_balas(balas):
    for bala in balas:
        bala[0] += bala[2]  # Movimenta a bala para a direita ou para a esquerda com base na direção da bala
    balas[:] = [bala for bala in balas if bala[0] < LARGURA and bala[0] > 0]  # Remove balas que saem da tela

# Função para mover os tiros dos inimigos
def mover_tiros_inimigos(tiros):
    for tiro in tiros:
        tiro[0] += tiro[2]  # Movimenta o tiro para a esquerda
    tiros[:] = [tiro for tiro in tiros if tiro[0] > 0]  # Remove os tiros que saem da tela

# Função para desenhar o fundo
def desenhar_fundo():
    # Desenha o fundo duas vezes, para que pareça que a tela se move
    janela.blit(fundo_imagem, (-camera_x % fundo_imagem.get_width(), 0))  # Fundo inicial
    janela.blit(fundo_imagem, (-camera_x % fundo_imagem.get_width() - fundo_imagem.get_width(), 0))  # Segundo fundo

# Função para exibir o estágio (Stage 1, Stage 2, etc.)
def exibir_stage():
    fonte = pygame.font.SysFont(None, 40)  # Defina o tamanho da fonte
    texto = fonte.render(f"Stage {estagio}", True, BRANCO)
    janela.blit(texto, (LARGURA // 2 - texto.get_width() // 2, 10))  # Centraliza o texto na parte superior

# Função para exibir a tela de "Fim"
def exibir_fim():
    fonte = pygame.font.SysFont(None, 60)
    texto = fonte.render("Fim de Jogo!", True, BRANCO)
    janela.blit(texto, (LARGURA // 2 - texto.get_width() // 2, ALTURA // 2 - texto.get_height() // 2))

# Função para aplicar a física do pulo e gravidade
def aplicar_fisica():
    global y_jogador, pulo, velocidade_pulo

    # Se o jogador está no ar, aplicamos a gravidade
    if pulo:
        y_jogador += velocidade_pulo  # O pulo move o jogador para cima
        velocidade_pulo += gravidade  # A gravidade afeta a velocidade do pulo

    # Se o jogador atinge o chão, ele para de cair
    if y_jogador >= ALTURA - ALTURA_JOGADOR - 10:
        y_jogador = ALTURA - ALTURA_JOGADOR - 10  # Posiciona o jogador no chão
        pulo = False  # O jogador não está mais pulando
        velocidade_pulo = -15  # Reseta a velocidade do pulo

# Loop principal do jogo
clock = pygame.time.Clock()
rodando = True
balas = []
pygame.mixer.music.play(-1, 0.0, 0)  # fade_ms = 0 como inteiro
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Movimentação do jogador
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        x_jogador -= velocidade_jogador
    if teclas[pygame.K_RIGHT]:
        x_jogador += velocidade_jogador
    if teclas[pygame.K_DOWN]:
        y_jogador += velocidade_jogador  # Agachar (simulando uma ação simples)

    # Pulo com a seta para cima
    if teclas[pygame.K_UP] and not pulo:
        pulo = True  # Ativa o pulo

    # Atirar com a tecla de espaço
    if teclas[pygame.K_SPACE]:
        balas.append([x_jogador + LARGURA_JOGADOR, y_jogador + ALTURA_JOGADOR // 2, 10])  # Adiciona uma bala à lista (movendo para a direita)
        som_disparo.play()  # Toca o som do disparo

    # A "câmera" segue o jogador
    camera_x = max(0, x_jogador - LARGURA // 2)

    # Aplicar a física do pulo e da gravidade
    aplicar_fisica()

    # Criar inimigos conforme o jogador anda
    if random.randint(1, 100) < 3:
        criar_inimigos()

    # Mover as balas
    mover_balas(balas)

    # Mover os inimigos
    mover_inimigos(inimigos, balas)

    # Mover os tiros dos inimigos
    mover_tiros_inimigos(tiros_inimigos)

    # Verificar colisão entre as balas e os inimigos
    inimigos_ativos[:] = [inimigo for inimigo in inimigos if not verificar_colisao(balas, inimigo[0], inimigo[1], 60, 100)]
    inimigos = inimigos_ativos

    # Verificar colisão entre os tiros dos inimigos e o jogador
    if verificar_colisao_tiro_inimigo(tiros_inimigos, x_jogador, y_jogador, LARGURA_JOGADOR, ALTURA_JOGADOR):
        print("Você foi atingido pelos tiros inimigos!")  # Implemente a lógica de perda de vida ou fim de jogo
        rodando = False

    # Atualizar a tela
    janela.fill(PRETO)  # Limpa a tela
    desenhar_fundo()  # Desenha o fundo que segue a câmera
    exibir_stage()  # Exibe o estágio
    desenhar_jogador(x_jogador, y_jogador)  # Desenha o jogador
    desenhar_balas(balas)  # Desenha as balas
    desenhar_inimigos(inimigos)  # Desenha os inimigos
    desenhar_tiros_inimigos(tiros_inimigos)  # Desenha os tiros inimigos

    pygame.display.flip()  # Atualiza a tela

    clock.tick(30)  # Limite de 30 quadros por segundo

# Encerra o Pygame
pygame.quit()
sys.exit()
