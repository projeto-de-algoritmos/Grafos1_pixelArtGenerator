import pygame
import sys
import random

"""CONFIGURAÇÔES"""
WIDTH = 1000
BLOCK_SIZE = 9     # tamanho do block
ROWS = WIDTH // BLOCK_SIZE
BLACK = (0, 0, 0)
RED = (204, 20, 20)
WHITE = (255, 255, 255)
COR_INICIAL = WHITE
FPS = 30000     # VELOCIDADE DOS PIXELS
RANDOM_BFS = True
vertices = []
visitados = []
fila = []
cor_anterior = (random.randrange(256),random.randrange(256),random.randrange(256))

pygame.init()
display = pygame.display.set_mode((WIDTH, WIDTH))
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
    if (self.x > 0 and self.x < ROWS - 1) and (self.y > 0 and self.y < ROWS - 1):
      if field[self.x + 1][self.y].is_vortex:
        self.neighbours.append(field[self.x + 1][self.y]) # vizinho da direita
      if field[self.x - 1][self.y].is_vortex:
        self.neighbours.append(field[self.x - 1][self.y]) # vizinho da esquerda
      if field[self.x][self.y + 1].is_vortex:
        self.neighbours.append(field[self.x][self.y + 1]) # vizinho de baixo
      if field[self.x][self.y - 1].is_vortex:
        self.neighbours.append(field[self.x][self.y - 1]) # vizinho de cima

def escolhe_cor(cor):
  peso_cor = 1
  nova_cor = list(cor)
  limite = 256

  if cor[0] > cor[1] and cor[0] > cor[2]: # elemento 0 é o maior da lista
    nova_cor[0] = (cor[0] + peso_cor) % limite
  if cor[1] > cor[0] and cor[1] > cor[2]: # elemento 1 é o maior da lista 
    nova_cor[1] = (cor[1] + peso_cor) % limite
  if cor[2] > cor[1] and cor[2] > cor[0]: # elemento 2 é o maior da lista 
    nova_cor[2] = (cor[2] + peso_cor) % limite
  else:
    i = random.randrange(0, 3)
    nova_cor[i] = (cor[i] + peso_cor) % limite

  return tuple(nova_cor)

for i in range(ROWS):
  cols = []
  for j in range(ROWS):
    cols.append(Vortex(i, j, WIDTH // ROWS, display))
  vertices.append(cols)

for i in range(ROWS):
  for j in range(ROWS):
    vertices[i][j].discover_neighbours(vertices)


def bfs(queue, node):
  global cor_anterior
  node.visited = True
  node.vortex(display, color=COR_INICIAL)
  queue.append(node)
  
  while queue:
    s = random.choice(queue) if RANDOM_BFS else queue.pop(0)
    queue.pop(queue.index(s)) if RANDOM_BFS else None

    for n in s.neighbours:
      if not n.visited:
        n.visited = True
        queue.append(n)
        cor = escolhe_cor(cor_anterior)
        cor_anterior = cor
        n.vortex(display, color=cor)
        

while True:
  bfs(fila, vertices[int(ROWS // 2)][int(ROWS // 2)])
  clock.tick(FPS)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      screenshot = pygame.Surface((WIDTH, WIDTH))
      screenshot.blit(display, (0, 0))
      pygame.image.save(screenshot, "print.png")
      pygame.quit()
      sys.exit()

