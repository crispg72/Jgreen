import pygame

def hitscreenedge():
    if x < 0:
        return True
    if y < 0:
        return True
    if (x + width) > 500:
        return True
    if (y + height) > 500:
        return True

    return  False

LEFT = 1
RIGHT = 2
UP = 3
DOWN = 4

class Tail():

    def __init__(self):
        self.length = 0
        self.sections = []

    def update(self, x, y, speed, direction):
        if self.sections:

            currentx = x
            currenty = y
            total_length = 0
            self.sections[0]["length"] += speed

            piece_counter = 0
            tail_pieces = []
            sections_to_remove = []
            for section in self.sections:
                total_length += section["length"]
                if total_length > self.length:
                    section["length"] -= (total_length - self.length)
    
                if section["length"] <= 0:
                    sections_to_remove.append(section)
                else:
                    length = section["length"]
                    stepx = 0
                    stepy = 0
                    if section["direction"] == LEFT:
                        stepx = tailpiece_diameter
                        xsection = currentx
                        ysection = currenty
                        currentx += length
                    elif section["direction"] == RIGHT:
                        stepx = -tailpiece_diameter
                        xsection = currentx
                        ysection = currenty
                        currentx -= length
                    elif section["direction"] == UP:
                        stepy = tailpiece_diameter
                        xsection = currentx
                        ysection = currenty
                        currenty += length
                    elif section["direction"] == DOWN:
                        stepy = -tailpiece_diameter
                        xsection = currentx 
                        ysection = currenty
                        currenty -= length

                    while piece_counter < length:
                        pygame.draw.circle(
                            win,
                            (255, 0, 0),
                            (int(xsection + (stepx / 2)), int(ysection + (stepy / 2))), 
                            int(tailpiece_diameter / 2),
                            1
                        )
                        xsection += stepx
                        ysection += stepy
                        piece_counter += tailpiece_diameter

                    piece_counter -= length

            for section in sections_to_remove:
                self.sections.remove(section)

    def changed_direction(self, x, y, direction):
        if self.length:
            self.sections.insert(0, {
                "length":0,
                "pos":(x, y),
                "direction":direction
            })

pygame.init()

win = pygame.display.set_mode((500, 500))

pygame.display.set_caption("First Game")

x = 250
y = 250
width = 8
height = 8
speed = 0
tailpiece_diameter = 8

image = pygame.image.load('./content/snakehead.jpg')
head = pygame.transform.scale(image, (width, height))

run = True
direction = None
tail = Tail()

while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        if not direction == RIGHT:
            direction = LEFT
            tail.changed_direction(x, y, direction)

    if keys[pygame.K_RIGHT]:
        if not direction == LEFT:
            direction = RIGHT
            tail.changed_direction(x, y, direction)

    if keys[pygame.K_UP]:
        if not direction == DOWN:
            direction = UP
            tail.changed_direction(x, y, direction)

    if keys[pygame.K_DOWN]:
        if direction != UP and direction != DOWN:
            direction = DOWN
            tail.changed_direction(x, y, direction)

    if keys[pygame.K_SPACE]:
        tail.length += speed

        if not tail.sections:
            tail.changed_direction(x, y, direction)

    if not speed and direction:
        speed = 5

    x += speed if direction == RIGHT else -speed if direction == LEFT else 0
    y += speed if direction == DOWN else -speed if direction == UP else 0

    background=(0, 0, 0)
    if hitscreenedge():
        background=(234, 234, 122)
    win.fill(background)

    tail.update(x, y, speed, direction)

    #win.blit(head, (x, y))
    pygame.draw.circle(win, (255,0,0), (x, y), width, 1)
    pygame.display.update()

pygame.quit()
