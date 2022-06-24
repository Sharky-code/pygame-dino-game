"""
features to add later:
- add long jump and short jump (DONE)
- add ducking (HALF DONE)
- add background scrolling
- add animations (ADDED LEG ANIMATIONS)
- easily change FLOOR level
"""

import pygame, random, copy

from pygame.time import get_ticks
width, height = 400, 200
frameRate = 60
pauseGame = False

#Initizalize and configure basic pygame stuff
pygame.font.init()
font = pygame.font.SysFont('Arial', 30)
endGame = False
#this doens't work. I think i should make a seperate fake screen and blit it to the real screen
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE|pygame.DOUBLEBUF|pygame.SCALED)

pygame.display.set_caption("Dinosaur Jumping Game")
image = pygame.image.load(r"player.png")
runningImage = pygame.image.load(r"runplayer.png")

class Button:
    def __init__(self, color, pos, text, orientation, font, fontSize, fontColor):
        #button logic stuff
        self.pressed = False
        self.color = color
        self.originalColor = copy.deepcopy(color)

        #rect stuff
        self.left = pos[0]
        self.top = pos[1]
        self.width = pos[2]
        self.height = pos[3]

        #text stuff
        self.text = text
        self.font = font
        self.orientation = orientation
        self.fontSize = fontSize
        self.fontColor = fontColor

    def createButton(self):
        global screen
        self.Rect = pygame.Rect(self.left, self.top, self.width, self.height)
        font = pygame.font.SysFont(self.font, self.fontSize)

        pygame.draw.rect(screen, self.color, self.Rect)
        if self.orientation:
            screen.blit(font.render(self.text, False, self.fontColor),(self.left,self.top))
        else:
            for x in range(len(self.text)):
                screen.blit(font.render(self.text[x], False, self.fontColor),(self.left,self.top + (x*self.fontSize)))
    
    def detectClick(self):
        leftMouseClick = pygame.mouse.get_pressed()[0]
        inButton = self.Rect.collidepoint(pygame.mouse.get_pos())
        self.color = copy.deepcopy(self.originalColor)
        #print('{0}, {1}, {2}'.format(leftMouseClick, inButton, self.pressed))

        if inButton:
            for x in range(len(self.color)):
                if self.color[x] == 0:
                    self.color[x] = 100
            if leftMouseClick:
                self.pressed = True

                for y in range(len(self.color)):
                    if self.color[y] == 255:
                        self.color[y] = 100
            else:
                if self.pressed:
                    #print("Command Execute")
                    self.pressed = False
                    return True
        else:
            if leftMouseClick:
                self.pressed = False


class gameLogic:
    """Controls the player object, including the gravity"""

    def __init__(self) -> None:
        self.relativeTick = copy.deepcopy(pygame.time.get_ticks())

        self.previousTimeSpace = 0
        self.spacePressed = False

        self.objectDimension = [10, 25] #object dimension -> width, height 
        self.objectVelocity = [0, 0]
        self.objectLocation = [width / 4 - self.objectDimension[0], height / 2 - self.objectDimension[1]]

        self.frameRate = frameRate
        self.gravity = -15
        self.groundLevel = [0, 200] #the empty value is reverved for later :)
        self.onGround = False

        self.enemyList = {'dino' : [], 'bird' : []}
        self.previousTimeEnemy = 0
        #The first item was minium time
        self.randomRangeEnemy = [0.4, 2]
        self.randomTimeFrameEnemy = random.uniform(self.randomRangeEnemy[0], self.randomRangeEnemy[1])
        self.speed = 2.5

    def restart(self):
        self.speed = 2.5
        self.enemyList = {'dino' : [], 'bird' : []}
        self.objectLocation = [width / 4 - self.objectDimension[0], height / 2 - self.objectDimension[1]]
        self.relativeTick = copy.deepcopy(pygame.time.get_ticks())

    def detectClick(self) -> None:
        """
        I just modified my old code lol
        """

        if (pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_SPACE]) and not pygame.key.get_pressed()[pygame.K_DOWN]:
            if not self.spacePressed:
                self.previousTimeSpace = copy.deepcopy(pygame.time.get_ticks())

            self.spacePressed = True
            
            if abs(self.previousTimeSpace - pygame.time.get_ticks()) > 70 and self.onGround:
                self.objectVelocity = [0, 220]
        else:
            if self.spacePressed:
                self.spacePressed = False

                if self.onGround:
                    self.objectVelocity = [0, 170]

            if pygame.key.get_pressed()[pygame.K_DOWN] and not self.onGround:
                self.objectVelocity[1] -= 20

    def playerGravity(self) -> None:
        """
        The objectLocation here is reversed. You have to reverse it again
        The ground too.

        you can use for loop but I thought it would be less laggier idk
        self.objectLocation[1] += self.objectVelocity[1] / self.frameRate
        self.objectLocation[0] += self.objectVelocity[0] / self.frameRa False
        """

        self.objectLocation[1] += self.objectVelocity[1] / self.frameRate
        self.objectLocation[0] += self.objectVelocity[0] / self.frameRate

        if self.objectLocation[1] > self.groundLevel[1] + self.objectDimension[1]:
            self.objectVelocity[1] += self.gravity
            self.onGround = False
        else: 
            self.objectVelocity[1] = 0
            self.objectLocation[1] = self.groundLevel[1] + self.objectDimension[1]
            self.onGround = True

    def drawBackground(self) -> None:
        #draw the floor
        global font
        pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(0, 100, width, height))
        text = font.render(f"{(pygame.time.get_ticks() - self.relativeTick) // 100}", False, (0, 0, 0))
        screen.blit(text, text.get_rect(center = (width // 2, height // 4 * 3)))
        print(screen.get_rect().center)

    def drawEnemy(self) -> None:
        """
        I need the enemy to be distant apart.

        I will use time to determine how it will spawn, because the faster
        the object goes the harder you jump.

        The speed increase are also constant for all objects, as the effect
        isn't that the enemy is going faster but you are running faster.
        (hopefully it'll work i dont want do distance :()

        I'm also gonna make the birds later. It shouldn't be the hardest to
        make but I'm going to make stuff one by one.
        """

        if (pygame.time.get_ticks() - self.previousTimeEnemy) > self.randomTimeFrameEnemy * 1000:
            self.enemyList[list(self.enemyList.keys())[random.randrange(0, 1)]].append([random.randint(1,3), width])
            self.previousTimeEnemy = copy.deepcopy(pygame.time.get_ticks())
            self.randomTimeFrameEnemy = random.uniform(self.randomRangeEnemy[0], self.randomRangeEnemy[1])

        self.speed += 0.0001 #put this to the if loop above if you want

        for y in list(self.enemyList.keys()):
            for x in range(len(self.enemyList[y])):
                try: 
                    pygame.draw.rect(screen, (10, 10, 10), pygame.Rect(self.enemyList[y][x][1], 100 - (10 if self.enemyList[y][x][0] == 1 else 12 if self.enemyList[y][x][0] == 2 else 15), 10, 10 if self.enemyList[y][x][0] == 1 else 12 if self.enemyList[y][x][0] == 2 else 15)) 

                    self.enemyList[y][x][1] -= self.speed

                    if self.enemyList[y][x][1] < -50:
                        self.enemyList[y].pop(x)
                except: pass

    def winLose(self):
        global pauseGame

        self.objectHitbox = pygame.Rect(self.objectLocation[0] + 1, height - self.objectLocation[1] + 100 + 1, self.objectDimension[0] - 2, self.objectDimension[1] - 2)

        for y in list(self.enemyList.keys()):
            for x in range(len(self.enemyList[y])):
                if self.objectHitbox.colliderect(pygame.Rect(self.enemyList[y][x][1], 100 - (10 if self.enemyList[y][x][0] == 1 else 12 if self.enemyList[y][x][0] == 2 else 15), 10, 10 if self.enemyList[y][x][0] == 1 else 12 if self.enemyList[y][x][0] == 2 else 15)):
                    pauseGame = True


object = gameLogic()
object.objectVelocity = [0, 100]

button = Button([100, 0, 0], (50, 50, 100, 100), "Restart", True, "Comic Sans MS", 20, (55,55,55))


while not endGame:

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT: endGame = True #makes you able to close the script (don't remove this)

    if not pauseGame:
        screen.fill((255,255,255)) #fill the screen with the RGB color
        screen.blit(image if ( (pygame.time.get_ticks() - object.relativeTick) // 100 ) % 2 == 1 or not object.onGround else runningImage, [object.objectLocation[0], height - object.objectLocation[1] + 100]) #pygame.draw.rect(screen, (100,100,100), pygame.Rect(object.objectLocation[0], height - object.objectLocation[1] + 100, object.objectDimension[0], object.objectDimension[1]))

        object.detectClick()
        object.drawBackground()
        object.playerGravity()
        object.drawEnemy()
        object.winLose()
    else:
        button.createButton()
        if button.detectClick():
            object.restart()
            pauseGame = False


    #for debugging:
    print("-" * 100)
    print(object.enemyList)

    #pygame.draw.rect(screen, (100, 10, 10), object.objectHitbox)

    pygame.time.Clock().tick(frameRate) #should cap the fps
    pygame.display.update() #pygame.display.flip()
