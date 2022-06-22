#Add screen stretching later
import pygame
width, height = 400, 200
frameRate = 60

#Initizalize and configure basic pygame stuff
pygame.font.init()
endGame = False
#this doens't work. I think i should make a seperate fake screen and blit it to the real screen
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE|pygame.DOUBLEBUF|pygame.SCALED)

pygame.display.set_caption("Dinosaur Jumping Game")
image = pygame.image.load(r"player.png")


class gameLogic:
    """Controls the player object, including the gravity"""
    def __init__(self) -> None:
        self.objectDimension = [10, 25] #object dimension -> width, height 
        self.objectVelocity = [0, 0]
        self.objectLocation = [width / 4 - self.objectDimension[0], height / 2 - self.objectDimension[1]]
        self.frameRate = frameRate
        self.gravity = -10
        self.groundLevel = [0, 200] #the empty value is reverved for later :)
        self.onGround = False

    def playerGravity(self) -> None:
        """
        The objectLocation here is reversed. You have to reverse it again
        The ground too.
        """
        self.objectLocation[1] += self.objectVelocity[1] / self.frameRate
        self.objectLocation[0] += self.objectVelocity[0] / self.frameRate

        if self.objectLocation[1] > self.groundLevel[1] + self.objectDimension[1]:
            """
            #you can use for loop but I thought it would be less laggier idk
            self.objectLocation[1] += self.objectVelocity[1] / self.frameRate
            self.objectLocation[0] += self.objectVelocity[0] / self.frameRate
            """

            self.objectVelocity[1] += self.gravity
            self.onGround = False
        else: 
            self.objectVelocity[1] = 0
            self.objectLocation[1] = self.groundLevel[1] + self.objectDimension[1]
            self.onGround = True

    def drawBackground(self) -> None:
        #draw the floor
        pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(0, 100, width, height))


object = gameLogic()
print(object.objectLocation)
object.objectVelocity = [0, 100]


while not endGame:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT: endGame = True #makes you able to close the script (don't remove this)
    
    if pygame.key.get_pressed()[pygame.K_UP] and object.onGround:
        object.objectVelocity = [0,200]

    screen.fill((255,255,255)) #fill the screen with the RGB color
    #hitbox visualizer:
    #pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(object.objectLocation[0], height - object.objectLocation[1] + 100, object.objectDimension[0], object.objectDimension[1]))

    #stuff i need to do later on: make the image stretch according to the different dimension i set
    screen.blit(image, [object.objectLocation[0], height - object.objectLocation[1] + 100])

    object.drawBackground()
    object.playerGravity()
    print(object.objectVelocity, object.objectLocation, height - object.groundLevel[1])

    pygame.time.Clock().tick(frameRate) #should cap the fps
    pygame.display.update()
    #pygame.display.update() only updates parts of a screen
