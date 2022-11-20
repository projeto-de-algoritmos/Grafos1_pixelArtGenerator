import pygame
import sys
import random

"""CONFIGURAÇÔES"""
WIDTH = 2560                     # tamanho da tela
HEIGHT = 1080
BLOCK_SIZE = 5                  # tamanho do block
ROWS = WIDTH // BLOCK_SIZE      # quantidade de linhas
COLUMNS = HEIGHT // BLOCK_SIZE
FPS = 30                        # VELOCIDADE DOS PIXELS (nao altera nada)
RANDOM_BFS = False              # muda o efeito de preenchimento da BFS
RANDOM_DFS = True
vertices = []


'''CORES'''
cor_anterior = (random.randrange(256),random.randrange(256),random.randrange(256))
# cor_random = (random.randrange(256),random.randrange(256),random.randrange(256))
BLACK = (0, 0, 0)
RED = (204, 20, 20)
WHITE = (255, 255, 255)
COR_INICIAL = WHITE    
TAXA_COR = 50           # muda a frequencia com que cada cor é alterada, quanto maior, mais cores aparecerao (melhor efeito entre 16 e 100)

pygame.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
display.fill(BLACK)
clock = pygame.time.Clock()
pygame.display.set_caption("PixelArt")

class Vortex:
  def __init__(self, row, col, width, display) -> None:
    self.row = row * width
    self.col = col * width
    self.x = row
    self.y = col
    self.color = COR_INICIAL
    self.width = width
    self.display = display
    self.neighbours = []
    self.is_vortex = True
    self.visited = False
    self.is_wall()

  def vortex(self, display, color=None):
    if color is None or not self.is_vortex:
      color = self.color
    else:
      self.color = color
    pygame.draw.rect(display, color, (self.row, self.col, self.width, self.width))
    pygame.display.update()

  def is_wall(self):
    w = self.display.get_width()
    h = self.display.get_height()
    y_cond = self.y == 0 or self.y >= h - 1
    x_cond = self.x == 0 or self.x >= w - 1

    if x_cond or y_cond:
      self.is_vortex = False
      self.color = BLACK
      self.neighbours = []

  def discover_neighbours(self, field):
    if (self.x > 0 and self.x < ROWS - 1) and (self.y > 0 and self.y < COLUMNS - 1):
      if field[self.x + 1][self.y].is_vortex:
        self.neighbours.append(field[self.x + 1][self.y])     # vizinho da direita
      if field[self.x - 1][self.y].is_vortex:
        self.neighbours.append(field[self.x - 1][self.y])     # vizinho da esquerda
      if field[self.x][self.y + 1].is_vortex:
        self.neighbours.append(field[self.x][self.y + 1])     # vizinho de baixo
      if field[self.x][self.y - 1].is_vortex:
        self.neighbours.append(field[self.x][self.y - 1])     # vizinho de cima
      if field[self.x - 1][self.y - 1].is_vortex:
        self.neighbours.append(field[self.x - 1][self.y - 1]) # superior esquerdo
      if field[self.x - 1][self.y + 1].is_vortex:
        self.neighbours.append(field[self.x - 1][self.y + 1]) # superior direito
      if field[self.x + 1][self.y + 1].is_vortex:
        self.neighbours.append(field[self.x + 1][self.y + 1]) # inferior direito
      if field[self.x + 1][self.y - 1].is_vortex:
        self.neighbours.append(field[self.x + 1][self.y - 1]) # inferior esquerdo
    

def escolhe_cor(cor):
  nova_cor = list(cor)
  limite = 256

  if cor[0] > cor[1] and cor[0] > cor[2] and random.choice([True, False]): # elemento 0 é o maior da lista
    nova_cor[0] = (cor[0] + TAXA_COR) % limite
    nova_cor[1] = (cor[1] + random.randrange(0, 10) if TAXA_COR > 15 else 0) % limite
    nova_cor[2] = (cor[2] + random.randrange(0, 10) if TAXA_COR > 15 else 0) % limite
  if cor[1] > cor[0] and cor[1] > cor[2] and random.choice([True, False]): # elemento 1 é o maior da lista 
    nova_cor[1] = (cor[0] + random.randrange(0, 10) if TAXA_COR > 15 else 0) % limite
    nova_cor[1] = (cor[1] + TAXA_COR) % limite
    nova_cor[2] = (cor[2] + random.randrange(0, 10) if TAXA_COR > 15 else 0) % limite
  if cor[2] > cor[1] and cor[2] > cor[0] and random.choice([True, False]): # elemento 2 é o maior da lista 
    nova_cor[2] = (cor[0] + random.randrange(0, 10) if TAXA_COR > 15 else 0) % limite
    nova_cor[1] = (cor[1] + random.randrange(0, 10) if TAXA_COR > 15 else 0) % limite
    nova_cor[2] = (cor[2] + TAXA_COR) % limite
  else:
    i = random.randrange(0, 3)
    nova_cor[i] = (cor[i] + TAXA_COR) % limite

  return tuple(nova_cor)

def make_grid():

  for i in range(ROWS):
    cols = []
    for j in range(ROWS):
      cols.append(Vortex(i, j, WIDTH // ROWS, display))
    vertices.append(cols)

  for i in range(ROWS):
    for j in range(ROWS):
      vertices[i][j].discover_neighbours(vertices)

COR_DEFINIDA = (88, 0, 255)

def bfs(node):
  queue = []
  global cor_anterior
  node.visited = True
  node.vortex(display, color=RED)
  queue.append(node)
  
  while queue:
    s = random.choice(queue) if RANDOM_BFS else queue.pop(0)
    queue.pop(queue.index(s)) if RANDOM_BFS else None

    for n in s.neighbours:
      if not n.visited:
        n.visited = True
        queue.append(n)
        cor = escolhe_cor(s.color)
        cor_anterior = cor
        n.vortex(display, color=cor)

def dfs(node):
  stack = [node]

  while stack:
    s = stack.pop()

    if s.visited:
      continue
    s.visited = True
    for n in s.neighbours:
      stack.append(random.choice(s.neighbours) if RANDOM_DFS else n)
      cor = escolhe_cor(s.color)
      cor_anterior = cor
      n.vortex(display, color=cor)

make_grid()

while True:
  clock.tick(FPS)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      screenshot = pygame.Surface((WIDTH, HEIGHT))
      screenshot.blit(display, (0, 0))
      pygame.image.save(screenshot, "print.png")
      pygame.quit()
      sys.exit()
    elif event.type == pygame.MOUSEBUTTONDOWN:
      pos = pygame.mouse.get_pos()

      row = (pos[0]) // BLOCK_SIZE
      col = (pos[1]) // BLOCK_SIZE      

      dfs(vertices[int(row)][int(col)])
      # bfs(vertices[int(row)][int(col)])


