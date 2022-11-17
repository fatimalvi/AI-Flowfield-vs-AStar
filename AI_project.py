import pygame
counter=0
y = 0
dir = 1
running = 1
width = 1000
height = 1000
screen = pygame.display.set_mode((width, height))
linecolor = 255, 255, 255
bgcolor = 0, 0, 0
clock=pygame.time.Clock()
while running:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        running = 0

    screen.fill(bgcolor)
    for i in range(0,width, 30):
        clock.tick(10)
        if counter==0:
            pygame.display.update()
        pygame.draw.line(screen, linecolor, (0, i), (width-1, i))
        pygame.draw.line(screen, linecolor, (i, 0), (i, height-1))

    counter=1

    # if y == 0 or y == height-1: dir *= -1

    pygame.display.flip()