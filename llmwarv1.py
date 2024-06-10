import pygame
import random
pygame.init()
hv = (1280,720)
screen = pygame.display.set_mode(hv)
clock = pygame.time.Clock()
running = True

#create troop classes
class troop():
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
        self.jitter = 1
        pass

#troop event
troop_created = False
troop_list = []
troop_count = 20
#end troop event


while running:
        #event poll
        #quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        #screen refresh
        screen.fill("black")
        #create a troop for testing
        if troop_created == False:
            troop_created = True
            for i in range(troop_count):
                troop_list.append(troop(random.randint(0,hv[0]),random.randint(0,hv[1])))
        #render block
        for i in troop_list:
            pygame.draw.circle(screen,'red',(i.x,i.y),5)
        #end render
        pygame.display.flip()


        #calculate next frame
        for i in troop_list:
            i.x += random.randint(i.jitter*-1,i.jitter)
            i.y += random.randint(i.jitter*-1,i.jitter)
        clock.tick(60) #framerate

pygame.quit()

