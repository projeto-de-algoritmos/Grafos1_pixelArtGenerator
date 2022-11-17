import pygame
import sys
import random

BLACK = (0, 0, 0)
RED = (204, 20, 20)
WHITE = (255, 255, 255)
COR_INICIAL = WHITE

class Vortex:
  def __init__(self, x, y, width, height, display) -> None:
    self.x = x
    self.y = y
    self.color = COR_INICIAL
    self.width = width
    self.height = height
    self.display = display
    self.neighbours = []

  def vortex(self, display, color=None):
    if color is None:
      color = self.color
    else:
      self.color = color
    pygame.draw.rect(display, color, (self.x, self.y, self.width, self.height))

WIDTH = 720
HEIGHT = 480
BLOCK_SIZE = 1
FPS = 1

pygame.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
display.fill(BLACK)
clock = pygame.time.Clock()
pygame.display.set_caption("PixelArt")

vertices = []


def escolhe_cor(cor):
  peso_cor = 50
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
    nova_cor[i] = (cor[i] + 2) % limite


  # print(nova_cor)

  return tuple(nova_cor)

for i in range(WIDTH):
  cols = []
  for j in range(HEIGHT):
    cols.append(Vortex(i, j, BLOCK_SIZE, BLOCK_SIZE, display))
  vertices.append(cols)

def draw_field(w, h):
  for i in range(0, w, BLOCK_SIZE):
    for j in range(0, h, BLOCK_SIZE):
      # if i != 0 and j != 0:
      vertices[i][j].vortex(display, color=(i % 255, j % 255, ((i + j) % 255)))


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

