import pygame
import numpy as np

# https://stackoverflow.com/questions/6339057/draw-a-transparent-rectangles-and-polygons-in-pygame
def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)

SIZE = 512

zoom = False

pygame.init()
window = pygame.display.set_mode((SIZE, SIZE))
pygame.display.set_caption("Mandelbrot")
fractal = pygame.Surface(window.get_size())
clock = pygame.time.Clock()

xvalues = np.linspace(-2.25,0.75,SIZE)
yvalues = np.linspace(-1.5,1.5,SIZE)

def mandel(c,maxiter):
    z=complex(0,0)
    for iteration in range(maxiter):
        z=(z*z) + c
        
        if abs(z) > 4:
            return iteration
        pass

    return 0

def draw_fractal(xvalues, yvalues, x1,y1,x2,y2):

    maxiter = 32

    newX1 = xvalues[x1]
    newX2 = xvalues[x2]
    newY1 = yvalues[y1]
    newY2 = yvalues[y2]

    new_xvalues = np.linspace(newX1, newX2, SIZE)
    new_yvalues = np.linspace(newY1, newY2, SIZE)

    xvalues = new_xvalues
    yvalues = new_yvalues

    sx = 0
    sy = 0

    for y in range(len(yvalues)):
        sx = 0
        for x in range(len(xvalues)):
           
            cx = xvalues[x]
            cy = yvalues[y]
        
            c = complex(cx,cy)
            fractal.set_at((sx,sy),(0,int(mandel(c,maxiter)/float(maxiter)*255),int(mandel(c,maxiter)/float(maxiter)*255)))
            sx = sx + 1
        sy = sy + 1


    return (xvalues,yvalues)

draw_fractal(xvalues, yvalues, 0,0,SIZE-1,SIZE-1)


x1 = 0
y1 = 0
x2 = 0
y2 = 0

drawRect = False

while True:
    clock.tick(60)
    window.blit(fractal,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT: raise SystemExit

        if event.type == pygame.MOUSEBUTTONDOWN:
            x1 = pygame.mouse.get_pos()[0]
            y1 = pygame.mouse.get_pos()[1]
            drawRect = True
        if event.type == pygame.MOUSEMOTION:
            x2 = pygame.mouse.get_pos()[0]
            y2 = pygame.mouse.get_pos()[1]
    
        if event.type == pygame.MOUSEBUTTONUP:   
            drawRect = False
            zoom = True

    if drawRect == True: draw_rect_alpha(window, (100,100,100,64) , (x1,y1,abs(x1-x2),abs(y1-y2)))
    
    if zoom == True:
        vals = draw_fractal(xvalues, yvalues, x1,y1,x2,y2)
        xvalues = vals[0]
        yvalues = vals[1]
        zoom = False

    pygame.display.flip()        
