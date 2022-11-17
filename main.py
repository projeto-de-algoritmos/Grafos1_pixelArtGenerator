import pygame
import sys
import random

"""CONSTANTES"""
BLACK = (0, 0, 0)
RED = (204, 20, 20)
WHITE = (255, 255, 255)
COR_INICIAL = WHITE
WIDTH = 720
HEIGHT = 480
BLOCK_SIZE = 1
FPS = 30
vertices = []
cor_anterior = (random.randrange(256),random.randrange(256),random.randrange(256))

pygame.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
display.fill(BLACK)
clock = pygame.time.Clock()
pygame.display.set_caption("PixelArt")

class Vortex:
  def __init__(self, x, y, width, height, display) -> None:
    self.x = x
    self.y = y
    self.color = COR_INICIAL
    self.width = width
    self.height = height
    self.display = display
    self.neighbours = []
    self.is_vortex = True

  def vortex(self, display, color=None):
    if color is None or not self.is_vortex:
      color = self.color
    else:
      self.color = color
    pygame.draw.rect(display, color, (self.x, self.y, self.width, self.height))

  def is_wall(self):
    w = self.display.get_width()
    h = self.display.get_height()

    if self.x == 0 or self.x == w - 1 or self.y == 0 or self.y == h - 1:
      self.is_vortex = False
      self.color = BLACK
      self.neighbours = []

  def discover_neightbours(self, field):
    w = self.display.get_width()
    h = self.display.get_height()

    if (self.x > 0 and self.x < w -1) and (self.y > 0 and self.y < h - 1):
      if field[self.x + 1][self.y].is_vortex:
        self.neighbours.append(field[self.x + 1][self.y]) # vizinho da direita
      if field[self.x - 1][self.y].is_vortex:
        self.neighbours.append(field[self.x - 1][self.y]) # vizinho da esquerda
      if field[self.x][self.y + 1].is_vortex:
        self.neighbours.append(field[self.x][self.y + 1]) # vizinho de baixo
      if field[self.x][self.y - 1].is_vortex:
        self.neighbours.append(field[self.x][self.y - 1]) # vizinho de cima

def escolhe_cor(cor):
  peso_cor = 3
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

for i in range(WIDTH):
  cols = []
  for j in range(HEIGHT):
    cols.append(Vortex(i, j, BLOCK_SIZE, BLOCK_SIZE, display))
    cols[j].is_wall()
  vertices.append(cols)

for i in range(WIDTH):
  for j in range(HEIGHT):
    vertices[i][j].discover_neightbours(vertices)

def draw_field(w, h):
  global cor_anterior
  for i in range(0, w, BLOCK_SIZE):
    for j in range(0, h, BLOCK_SIZE):
      cor = escolhe_cor(cor_anterior)
      cor_anterior = cor
      vertices[i][j].vortex(display, color=cor)
      # pygame.display.update() # manter comentado se quiser atualizar a tela toda de uma vez (se tirar o comentario, sera atualizado pixel por pixel)

def bfs(graph, g):
  pass

while True:
  draw_field(WIDTH, HEIGHT)
  clock.tick(FPS)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      screenshot = pygame.Surface((WIDTH, HEIGHT))
      screenshot.blit(display, (0, 0))
      pygame.image.save(screenshot, "print.png")
      pygame.quit()
      sys.exit()

  pygame.display.update()

