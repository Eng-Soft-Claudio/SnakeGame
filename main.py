"""Este módulo implementa o clássico jogo da Cobrinha (Snake) com Pygame.

O jogo apresenta uma tela inicial para entrada do nome do jogador, um ranking
persistente dos 5 melhores placares armazenados em um banco de dados SQLite
e um ciclo de jogo que reinicia após a tela de "Game Over".
"""

import pygame
import random
import sqlite3

pygame.init()

PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
AZUL_CLARO = (173, 216, 230)
AMARELO = (255, 255, 0)

largura_tela, altura_tela = 800, 600
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption('Jogo da Cobrinha com Placar')

clock = pygame.time.Clock()
tamanho_bloco = 20
velocidade_cobra = 15

fonte_titulo = pygame.font.SysFont("consolas", 40)
fonte_instrucao = pygame.font.SysFont("bahnschrift", 25)
fonte_placar = pygame.font.SysFont("bahnschrift", 22)

DB_FILE = "placar.db"

def inicializar_banco():
    """Garante a existência do banco de dados e da tabela 'placares'.
    
    Conecta-se ao arquivo SQLite e executa um comando SQL para criar a
    tabela 'placares' caso ela ainda não exista, definindo as colunas
    para id, nome e pontos.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS placares (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        pontos INTEGER NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def salvar_placar(nome, pontos):
    """Insere um novo registro de pontuação na tabela de placares.

    Args:
        nome (str): O nome do jogador.
        pontos (int): A pontuação final obtida na partida.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO placares (nome, pontos) VALUES (?, ?)", (nome, pontos))
    conn.commit()
    conn.close()

def obter_melhores_placares(limite=10):
    """Consulta o banco de dados e retorna os melhores placares.

    Args:
        limite (int, optional): O número máximo de placares a serem retornados.
                                 Padrão é 10.

    Returns:
        list[tuple[str, int]]: Uma lista de tuplas, onde cada tupla contém
                               o nome e a pontuação (nome, pontos), ordenada
                               da maior para a menor pontuação.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT nome, pontos FROM placares ORDER BY pontos DESC LIMIT ?", (limite,))
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def desenhar_melhores_placares(surface, placares):
    """Renderiza a lista dos melhores placares em uma superfície Pygame.

    Args:
        surface (pygame.Surface): A superfície onde o placar será desenhado.
        placares (list[tuple[str, int]]): A lista de placares a ser exibida.
    """
    titulo = fonte_titulo.render("Melhores 10:", True, AMARELO)
    surface.blit(titulo, (550, 40))
    
    pos_y = 100
    for i, (nome, pontos) in enumerate(placares):
        texto = f"{i+1}. {nome} - {pontos} pts"
        render_texto = fonte_placar.render(texto, True, BRANCO)
        surface.blit(render_texto, (550, pos_y))
        pos_y += 35

def desenhar_pontuacao(pontos, nome_jogador):
    """Renderiza a pontuação atual do jogador na tela do jogo.

    Args:
        pontos (int): A pontuação atual.
        nome_jogador (str): O nome do jogador atual.
    """
    texto = fonte_placar.render(f"{nome_jogador} | Pontos: {pontos}", True, BRANCO)
    tela.blit(texto, [10, 10])

def desenhar_cobra(lista_cobra):
    """Desenha todos os segmentos da cobra na tela.

    Args:
        lista_cobra (list[list[int, int]]): Uma lista de coordenadas [x, y]
                                             representando os blocos da cobra.
    """
    for bloco in lista_cobra:
        pygame.draw.rect(tela, VERDE, [bloco[0], bloco[1], tamanho_bloco, tamanho_bloco])

def tela_inicial():
    """Gerencia a tela de início do jogo.

    Esta tela tem duas fases: primeiro, coleta o nome do jogador através de
    entrada de texto. Segundo, após o nome ser inserido, aguarda o jogador
    pressionar qualquer tecla para iniciar a partida. Durante todo o tempo,
    exibe os melhores placares.

    Returns:
        str: O nome do jogador inserido para ser usado na partida.
    """
    nome_jogador = ""
    coletando_nome = True
    melhores_placares = obter_melhores_placares(10)
    
    while coletando_nome:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and nome_jogador:
                    coletando_nome = False
                elif event.key == pygame.K_BACKSPACE:
                    nome_jogador = nome_jogador[:-1]
                elif len(nome_jogador) < 15:
                    nome_jogador += event.unicode

        tela.fill(PRETO)
        desenhar_melhores_placares(tela, melhores_placares)
        pygame.draw.line(tela, AZUL_CLARO, (500, 20), (500, altura_tela - 20), 2)
        
        instrucao = fonte_instrucao.render("Digite seu nome e pressione ENTER:", True, BRANCO)
        tela.blit(instrucao, (20, 200))
        
        caixa_nome = fonte_titulo.render(nome_jogador, True, AZUL_CLARO)
        tela.blit(caixa_nome, (20, 250))

        pygame.display.flip()
        clock.tick(30)
    
    esperando_inicio = True
    while esperando_inicio:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                return nome_jogador

        tela.fill(PRETO)
        desenhar_melhores_placares(tela, melhores_placares)
        pygame.draw.line(tela, AZUL_CLARO, (500, 20), (500, altura_tela - 20), 2)

        msg_inicio = fonte_instrucao.render("Pressione qualquer tecla para iniciar!", True, BRANCO)
        tela.blit(msg_inicio, (20, 200))

        pygame.draw.rect(tela, VERDE, [150, 300, 150, 50])
        texto_botao = fonte_titulo.render("INICIAR", True, PRETO)
        rect_botao = texto_botao.get_rect(center=(225, 325))
        tela.blit(texto_botao, rect_botao)
        
        pygame.display.flip()
        clock.tick(30)

def rodar_jogo(nome_jogador):
    """Executa o loop principal do jogo da cobrinha.

    Gerencia a lógica de movimento da cobra, detecção de colisões (com paredes
    e com o próprio corpo), ingestão de comida e atualização da pontuação. O loop
    continua até que o jogador perca por colisão ou feche a janela.

    Args:
        nome_jogador (str): O nome do jogador atual para exibição no placar.

    Returns:
        int: A pontuação final do jogador. Retorna -1 se o jogador fechar
             a janela pelo botão de sair, sinalizando uma interrupção.
    """
    game_over = False
    x1, y1 = largura_tela / 2, altura_tela / 2
    x1_change, y1_change = 0, 0
    lista_cobra, comprimento_cobra = [], 1
    pontos = 0
    
    comida_x = round(random.randrange(0, largura_tela - tamanho_bloco) / tamanho_bloco) * tamanho_bloco
    comida_y = round(random.randrange(0, altura_tela - tamanho_bloco) / tamanho_bloco) * tamanho_bloco

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change, y1_change = -tamanho_bloco, 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change, y1_change = tamanho_bloco, 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    x1_change, y1_change = 0, -tamanho_bloco
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    x1_change, y1_change = 0, tamanho_bloco

        if x1 >= largura_tela or x1 < 0 or y1 >= altura_tela or y1 < 0:
            game_over = True
        
        x1 += x1_change
        y1 += y1_change

        tela.fill(PRETO)
        pygame.draw.rect(tela, VERMELHO, [comida_x, comida_y, tamanho_bloco, tamanho_bloco])
        
        cabeca_cobra = [x1, y1]
        lista_cobra.append(cabeca_cobra)
        if len(lista_cobra) > comprimento_cobra:
            del lista_cobra[0]

        for bloco in lista_cobra[:-1]:
            if bloco == cabeca_cobra:
                game_over = True

        desenhar_cobra(lista_cobra)
        desenhar_pontuacao(pontos, nome_jogador)
        pygame.display.update()

        if x1 == comida_x and y1 == comida_y:
            comida_x = round(random.randrange(0, largura_tela - tamanho_bloco) / tamanho_bloco) * tamanho_bloco
            comida_y = round(random.randrange(0, altura_tela - tamanho_bloco) / tamanho_bloco) * tamanho_bloco
            comprimento_cobra += 1
            pontos += 10

        clock.tick(velocidade_cobra)
        
    return pontos

def tela_game_over(pontuacao_final, nome_jogador):
    """Exibe a tela de "Game Over" com o placar final por 5 segundos.

    Args:
        pontuacao_final (int): A pontuação que o jogador alcançou.
        nome_jogador (str): O nome do jogador para exibição na mensagem.
    """
    tempo_inicio = pygame.time.get_ticks()
    
    while pygame.time.get_ticks() - tempo_inicio < 5000:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        tela.fill(PRETO)
        msg_gameover = fonte_titulo.render("GAME OVER", True, VERMELHO)
        rect_gameover = msg_gameover.get_rect(center=(largura_tela / 2, altura_tela / 2 - 50))
        
        msg_placar = fonte_instrucao.render(f"{nome_jogador}, seu placar foi: {pontuacao_final}", True, BRANCO)
        rect_placar = msg_placar.get_rect(center=(largura_tela / 2, altura_tela / 2 + 20))
        
        tela.blit(msg_gameover, rect_gameover)
        tela.blit(msg_placar, rect_placar)
        pygame.display.flip()

def main():
    """Função principal que controla o fluxo de estados do jogo.
    
    Inicializa o banco de dados e executa um loop infinito que transita entre
    a tela inicial, o jogo e a tela de game over, permitindo múltiplas
    partidas sem reiniciar o programa. O loop é interrompido se o jogador
    fecha a janela.
    """
    inicializar_banco()
    
    while True:
        nome_do_jogador = tela_inicial()
        pontuacao_final = rodar_jogo(nome_do_jogador)
        
        if pontuacao_final == -1:
            break
            
        if pontuacao_final > 0:
            salvar_placar(nome_do_jogador, pontuacao_final)
            
        tela_game_over(pontuacao_final, nome_do_jogador)

    pygame.quit()
    quit()

if __name__ == '__main__':
    main()