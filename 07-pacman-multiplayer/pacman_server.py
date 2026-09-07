import pygame, random, socket, pickle, threading
"""writen by Zahra Gharib & Seyed Sajjad Qavami"""

pygame.init()
TILE_SIZE = 32

class Wall(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(topleft=position)

class Pellet(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.Surface((6, 6))
        pygame.draw.circle(self.image, (255, 255, 255), (3, 3), 3)
        self.rect = self.image.get_rect(center=position)

class BigPellet(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.Surface((24, 24))
        pygame.draw.circle(self.image, (255, 255, 255), (12, 12), 12)
        self.rect = self.image.get_rect(center=position)

class Pacman(pygame.sprite.Sprite):
    def __init__(self,position, server, id):
        super().__init__()
        self.image = pygame.Surface((32,32))
        pygame.draw.circle(self.image, (255,255,0), (16,16), TILE_SIZE / 2)
        self.rect = self.image.get_rect(topleft = position)
        self.dx = -2
        self.dy = 0
        self.next_dx = 0
        self.next_dy = 0
        self.server = server
        self.player_id = id
        self.mode = "pacman"
    
    def update(self, keys, pellets):
        if self.mode == "pacman":
            self.pellets = pellets
            if keys[pygame.K_LEFT]:
                self.next_dx = -2
                self.next_dy = 0
            elif keys[pygame.K_RIGHT]:
                self.next_dx = 2
                self.next_dy = 0
            elif keys[pygame.K_UP]:
                self.next_dx = 0
                self.next_dy = -2
            elif keys[pygame.K_DOWN]:
                self.next_dx = 0
                self.next_dy = 2

            self.rect.x += self.next_dx
            self.rect.y += self.next_dy
            if not pygame.sprite.spritecollide(self, self.server.walls, False) and not 894 <= self.rect.x <= 898:
                self.dx = self.next_dx
                self.dy = self.next_dy
            self.rect.x -= self.next_dx
            self.rect.y -= self.next_dy

            self.rect.x += self.dx
            if pygame.sprite.spritecollide(self, self.server.walls, False):
                self.rect.x -= self.dx
                self.dx = 0
            self.rect.y += self.dy
            if pygame.sprite.spritecollide(self, self.server.walls, False):
                self.rect.y -= self.dy
                self.dy = 0

            if self.player_id == 0 and 928 <= self.rect.x <= 1792 :
                if pygame.sprite.collide_rect(self.server.players[1], self):
                    self.server.winner = "player1"
                    self.server.running_game = False
            elif self.player_id == 1 and 0 <= self.rect.x <= 864 :
                if pygame.sprite.collide_rect(self.server.players[0], self):
                    self.server.winner = "player2"
                    self.server.running_game = False
                    
            
            if self.rect.x == -32 and self.rect.y == 480 :
                self.rect.x = 864
            if self.rect.x == 1824 and self.rect.y == 480 :
                self.rect.x = 928
            if pygame.sprite.spritecollide(self,self.pellets[0],True):
                if self.player_id == 0 :
                    self.server.player0_score += 5
                    if self.server.player0_score == 1290:
                        self.server.winner = "player1"
                        self.server.running_game = False
                if self.player_id == 1 :
                    self.server.player1_score += 5
                    if self.server.player1_score == 1290:
                        self.server.winner = "player2"
                        self.server.running_game = False
            if pygame.sprite.spritecollide(self,self.pellets[1],True):
                if self.player_id == 0:
                    self.server.player0_score += 20
                    if self.server.player0_score == 1290:
                        self.server.winner = "player1"
                        self.server.running_game = False
                    self.last_mode = self.server.blinky.mode
                    self.server.blinky.mode = "frightened"
                    self.server.inky.multi_mode = "inky frightened"
                    self.server.pinky.multi_mode = "pinky frightened"
                    self.server.clyde.multi_mode = "clyde frightened"
                    if 0 <= self.server.players[1].rect.x <= 864:
                        self.server.players[1].mode = "ghost"
                        self.server.player1_color = (150,0,200)
                    self.server.blinky_color = (0,0,255)
                    self.server.inky_color = (0,0,255)
                    self.server.pinky_color = (0,0,255)
                    self.server.clyde_color = (0,0,255)
                if self.player_id == 1 :
                    self.server.player1_score += 20
                    if self.server.player1_score == 1290:
                        self.server.winner = "player2"
                        self.server.running_game = False
                    self.last_mode = self.server.blinky2.mode
                    self.server.blinky2.mode = "frightened"
                    self.server.inky2.multi_mode = "inky frightened"
                    self.server.pinky2.multi_mode = "pinky frightened"
                    self.server.clyde2.multi_mode = "clyde frightened"
                    if 928 <= self.server.players[0].rect.x <= 1792:
                        self.server.players[0].mode = "ghost"
                        self.server.player0_color = (150,0,200)
                    self.server.blinky2_color = (0,0,255)
                    self.server.inky2_color = (0,0,255)
                    self.server.pinky2_color = (0,0,255)
                    self.server.clyde2_color = (0,0,255)
                self.server.players[0].start_time = pygame.time.get_ticks()
                self.server.players[1].start_time = pygame.time.get_ticks()
        elif self.mode == "ghost" :
            self.time3 = pygame.time.get_ticks()
            if self.player_id == 0 :
                if self.time3 - self.server.players[0].start_time > 7000:
                    self.server.players[0].mode = "pacman"
                    self.server.player0_color = (255,255,0)
                if pygame.sprite.collide_rect(self.server.players[1], self):
                    self.server.winner = "player2"
                    self.server.running_game = False
            elif self.player_id == 1 :
                if self.time3 - self.server.players[1].start_time > 7000:
                    self.server.players[1].mode = "pacman"
                    self.server.player1_color = (255,255,0)
                if pygame.sprite.collide_rect(self.server.players[0], self):
                    self.server.winner = "player1"
                    self.server.running_game = False

class Ghost(pygame.sprite.Sprite):
    def __init__(self, position, server,scatters, limit):
        self.position = position
        super().__init__()
        self.image = pygame.Surface((32,32))
        pygame.draw.circle(self.image, (255,0,0), (16,16), 16)
        self.rect = self.image.get_rect(center = position)
        self.directions = ["up", "down", "left", "right"]
        self.lock_direction = "down"
        self.new_direction = "left"
        self.mode = "scatter"
        self.time = pygame.time.get_ticks()
        self.target_x = 768
        self.target_y = 128
        self.speed = 2
        self.server = server
        self.scatter = scatters
        self.limit = limit

    def can_move(self, direction):
        if direction == "up":
            self.rect.y -= self.speed
            if not pygame.sprite.spritecollide(self, self.server.walls, False):
                self.x_distance = abs(self.rect.x - self.target_x)
                self.y_distance = abs(self.rect.y - self.target_y)
                self.rect.y += self.speed
                return True
            self.rect.y += self.speed
            return False
        elif direction == "down":
            self.rect.y += self.speed
            if (not pygame.sprite.spritecollide(self, self.server.walls, False)) and (not (self.limit[0] <= self.rect.x <= self.limit[1] and 385 <= self.rect.y <= 386)):
                self.x_distance = abs(self.rect.x - self.target_x)
                self.y_distance = abs(self.rect.y - self.target_y)
                self.rect.y -= self.speed
                return True
            self.rect.y -= self.speed
            return False
        elif direction == "left":
            self.rect.x -= self.speed
            if not pygame.sprite.spritecollide(self, self.server.walls, False):
                self.x_distance = abs(self.rect.x - self.target_x)
                self.y_distance = abs(self.rect.y - self.target_y)
                self.rect.x += self.speed
                return True
            self.rect.x += self.speed
            return False
        elif direction == "right":
            self.rect.x += self.speed
            if not pygame.sprite.spritecollide(self, self.server.walls, False):
                self.x_distance = abs(self.rect.x - self.target_x)
                self.y_distance = abs(self.rect.y - self.target_y)
                self.rect.x -= self.speed
                return True
            self.rect.x -= self.speed
            return False
        
    def update(self, player):
        if self.mode == "chase":
            if (self.new_direction == "up" or self.new_direction == "down") and self.rect.y %2 == 0:
                if self.speed != 2 :
                    self.speed = 2
            if (self.new_direction == "right" or self.new_direction == "left") and self.rect.x %2 == 0:
                if self.speed != 2 :
                    self.speed = 2
            self.time2 = pygame.time.get_ticks()
            if self.time2 - self.time > 30000:
                self.time = self.time2
                self.mode = "scatter"
                self.target_x = self.scatter[0][0]
                self.target_y = self.scatter[0][1]
            self.distances = dict()
            for direction in self.directions:
                self.target_x = player.rect.x
                self.target_y = player.rect.y
                if self.can_move(direction) and direction != self.lock_direction:
                    self.distances[direction] = self.x_distance + self.y_distance
            self.min_distance = min(self.distances.values())
            self.new_direction = [key for key in self.distances.keys() if self.distances[key] == self.min_distance][0]
            
        elif self.mode == "scatter":
            if (self.new_direction == "up" or self.new_direction == "down") and self.rect.y %2 == 0:
                if self.speed != 2 :
                    self.speed = 2
            if (self.new_direction == "right" or self.new_direction == "left") and self.rect.x %2 == 0:
                if self.speed != 2 :
                    self.speed = 2
            self.time1 = pygame.time.get_ticks()
            if self.time1 - self.time > 10000:
                self.time = self.time1
                self.mode = "chase"
                self.target_x = player.rect.x
                self.target_y = player.rect.y
            self.distances_scatter = dict()
            for direction in self.directions:
                self.target_x = self.scatter[0][0]
                self.target_y = self.scatter[0][1]
                if self.can_move(direction) and direction != self.lock_direction:
                    self.distances_scatter[direction] = self.x_distance + self.y_distance
            self.min_distance_scatter = min(self.distances_scatter.values())
            self.new_direction = [key for key in self.distances_scatter.keys() if self.distances_scatter[key] == self.min_distance_scatter][0]

        elif self.mode == "frightened":
            self.time3 = pygame.time.get_ticks()
            if self.time3 - player.start_time > 7000:
                self.server.blinky_color = (255,0,0)
                self.server.blinky2_color = (255,0,0)
                self.time = self.time3
                self.mode = player.last_mode
            self.speed = 1
            if pygame.sprite.collide_rect(player, self):
                self.time4 = pygame.time.get_ticks()
                self.mode = player.last_mode
                if self.mode == "scatter":
                    self.target_x = self.scatter[0][0]
                    self.target_y = self.scatter[0][1]
                elif self.mode == "chase":
                    self.target_x = player.rect.x
                    self.target_y = player.rect.y
                self.time = self.time4
                self.rect.center = self.position
                self.server.blinky_color = (255, 0, 0)
                self.server.blinky2_color = (255, 0, 0)
            self.valids = []
            for d in self.directions:
                if d != self.lock_direction and self.can_move(d):
                    self.valids.append(d)
            if self.valids:
                self.direction = random.choice(self.valids)
                self.new_direction = self.direction

        if self.new_direction == "right":
            self.lock_direction = "left"
        elif self.new_direction == "left":
            self.lock_direction = "right"
        elif self.new_direction == "up":
            self.lock_direction = "down"
        elif self.new_direction == "down":
            self.lock_direction = "up"
        
        if self.new_direction == "up":
            self.rect.y -= self.speed
        elif self.new_direction == "down":
            self.rect.y += self.speed
        elif self.new_direction == "right":
            self.rect.x += self.speed
        elif self.new_direction == "left":
            self.rect.x -= self.speed
        if self.rect.x == -32 and self.rect.y == 480 :
            self.rect.x = 864
        if self.rect.x == 1824 and self.rect.y == 480 :
            self.rect.x = 928
        if self.rect.x == 894 and self.rect.y == 480 :
            self.rect.x = 0
        if self.rect.x == 896 and self.rect.y == 480 :
            self.rect.x = 1792
        

class Inky(Ghost):
    def __init__(self, position, server, blinky,scatters, limit):
        super().__init__(position, server,scatters, limit)
        self.position = position
        self.image = pygame.Surface((32,32))
        pygame.draw.circle(self.image, (0,255,255), (16,16), 16)
        self.mode = "in"
        self.new_direction = "up"
        self.multi_mode = ""
        self.blinky = blinky

    def get_target(self, player):
        self.player_x = player.rect.centerx
        self.player_y = player.rect.centery
        self.offset_x = self.player_x + player.dx * TILE_SIZE
        self.offset_y = self.player_y + player.dy * TILE_SIZE
        self.vector_x = self.offset_x - self.blinky.rect.centerx
        self.vector_y = self.offset_y - self.blinky.rect.centery
        return self.blinky.rect.centerx + self.vector_x * 2, self.blinky.rect.centery + self.vector_y * 2

    def update(self, player):
        if self.mode == "in" :
            self.tick = pygame.time.get_ticks()
            if self.tick - self.time > 6000 :
                self.mode = "out"
                self.time = self.tick
            if pygame.sprite.spritecollide(self,self.server.walls,False):
                if self.new_direction == "up" :
                    self.new_direction = "down"
                else:
                    self.new_direction = "up"

        elif self.mode == "out":
            self.time3 = pygame.time.get_ticks()
            if self.time3 - self.time > 1600:
                self.mode = "inky scatter"
                self.target_x = self.scatter[1][0]
                self.target_y = self.scatter[1][1]
            self.distances_scatter = dict()
            for direction in self.directions:
                self.target_x = self.scatter[0][0]
                self.target_y = self.scatter[0][1]
                if self.can_move(direction) and direction != self.lock_direction:
                    self.distances_scatter[direction] = self.x_distance + self.y_distance
            self.min_distance_scatter = min(self.distances_scatter.values())
            self.new_direction = [key for key in self.distances_scatter.keys() if self.distances_scatter[key] == self.min_distance_scatter][0]

        elif self.mode == "inky scatter" :
            if (self.new_direction == "up" or self.new_direction == "down") and self.rect.y %2 == 0:
                if self.speed != 2 :
                    self.speed = 2
            if (self.new_direction == "right" or self.new_direction == "left") and self.rect.x %2 == 0:
                if self.speed != 2 :
                    self.speed = 2
            self.time1 = pygame.time.get_ticks()
            if self.time1 - self.time > 10000:
                self.time = self.time1
                self.mode = "inky chase"
                self.target_x, self.target_y = self.get_target(player)
            self.distances_scatter = dict()
            for direction in self.directions:
                self.target_x = self.scatter[1][0]
                self.target_y = self.scatter[1][1]
                if self.can_move(direction) and direction != self.lock_direction:
                    self.distances_scatter[direction] = self.x_distance + self.y_distance
            self.min_distance_scatter = min(self.distances_scatter.values())
            self.new_direction = [key for key in self.distances_scatter.keys() if self.distances_scatter[key] == self.min_distance_scatter][0]

        elif self.mode == "inky chase":
            if (self.new_direction == "up" or self.new_direction == "down") and self.rect.y %2 == 0:
                if self.speed != 2 :
                    self.speed = 2
            if (self.new_direction == "right" or self.new_direction == "left") and self.rect.x %2 == 0:
                if self.speed != 2 :
                    self.speed = 2
            self.time2 = pygame.time.get_ticks()
            if self.time2 - self.time > 30000:
                self.time = self.time2
                self.mode = "inky scatter"
                self.target_x = self.scatter[1][0]
                self.target_y = self.scatter[1][1]
            self.distances = dict()
            for direction in self.directions:
                self.target_x, self.target_y = self.get_target(player)
                if self.can_move(direction) and direction != self.lock_direction:
                    self.distances[direction] = self.x_distance + self.y_distance
            self.min_distance = min(self.distances.values())
            self.new_direction = [key for key in self.distances.keys() if self.distances[key] == self.min_distance][0]

        if self.multi_mode == "inky frightened":
            self.time3 = pygame.time.get_ticks()
            if self.mode != "":
                if self.mode != "in":
                    self.last_mode = self.mode
                else :
                    self.last_mode = "inky scatter"
            if self.mode != "in" and self.mode != "out":
                self.mode = ""
            if self.time3 - player.start_time > 7000:
                self.server.inky_color =(0,255,255)
                self.server.inky2_color =(0,255,255)
                self.time = self.time3
                self.mode = self.last_mode
                self.multi_mode = ""
            if self.mode != "in" and self.mode != "out":
                self.speed = 1
                
                self.valids = []
                for d in self.directions:
                    if d != self.lock_direction and self.can_move(d):
                        self.valids.append(d)
                if self.valids:
                    self.direction = random.choice(self.valids)
                    self.new_direction = self.direction
                if pygame.sprite.collide_rect(player, self):
                    self.time4 = pygame.time.get_ticks()
                    self.mode = "in"
                    self.multi_mode = ""
                    self.new_direction = "up"
                    self.time = self.time4
                    self.rect.center = self.position
                    self.server.inky_color =(0, 255, 255)
                    self.server.inky2_color =(0, 255, 255)
                    self.speed = 2

        return super().update(player)
        
class Pinky(Ghost):
    def __init__(self, position,server,scatters, limit):
        super().__init__(position,server,scatters,limit)
        self.position = position
        self.image = pygame.Surface((32,32))
        pygame.draw.circle(self.image,(255,105,180), (16,16), 16)
        self.mode = "in"
        self.new_direction = "up"
        self.multi_mode = ""

    def get_target(self, player):
        self.player_x = player.rect.centerx
        self.player_y = player.rect.centery
        self.offset_x = self.player_x + 2 * player.dx * TILE_SIZE
        self.offset_y = self.player_y + 2 * player.dy * TILE_SIZE
        return self.offset_x , self.offset_y

    def update(self, player):
        if self.mode == "in" :
            self.tick = pygame.time.get_ticks()
            if self.tick - self.time > 2000 :
                self.mode = "out"
                self.time = self.tick
            if pygame.sprite.spritecollide(self,self.server.walls,False):
                if self.new_direction == "up" :
                    self.new_direction = "down"
                else:
                    self.new_direction = "up"

        elif self.mode == "out":
            self.time3 = pygame.time.get_ticks()
            if self.time3 - self.time > 1000:
                self.mode = "pinky scatter"
                self.target_x = self.scatter[2][0]
                self.target_y = self.scatter[2][1]
            self.distances_scatter = dict()
            for direction in self.directions:
                self.target_x = self.scatter[0][0]
                self.target_y = self.scatter[0][1]
                if self.can_move(direction) and direction != self.lock_direction:
                    self.distances_scatter[direction] = self.x_distance + self.y_distance
            self.min_distance_scatter = min(self.distances_scatter.values())
            self.new_direction = [key for key in self.distances_scatter.keys() if self.distances_scatter[key] == self.min_distance_scatter][0]

        elif self.mode == "pinky scatter" :
            if (self.new_direction == "up" or self.new_direction == "down") and self.rect.y %2 == 0:
                if self.speed != 2 :
                    self.speed = 2
            if (self.new_direction == "right" or self.new_direction == "left") and self.rect.x %2 == 0:
                if self.speed != 2 :
                    self.speed = 2
            self.time1 = pygame.time.get_ticks()
            if self.time1 - self.time > 10000:
                self.time = self.time1
                self.mode = "pinky chase"
                self.target_x, self.target_y = self.get_target(player)
            self.distances_scatter = dict()
            for direction in self.directions:
                self.target_x = self.scatter[2][0]
                self.target_y = self.scatter[2][1]
                if self.can_move(direction) and direction != self.lock_direction:
                    self.distances_scatter[direction] = self.x_distance + self.y_distance
            self.min_distance_scatter = min(self.distances_scatter.values())
            self.new_direction = [key for key in self.distances_scatter.keys() if self.distances_scatter[key] == self.min_distance_scatter][0]

        elif self.mode == "pinky chase":
            if (self.new_direction == "up" or self.new_direction == "down") and self.rect.y %2 == 0:
                if self.speed != 2 :
                    self.speed = 2
            if (self.new_direction == "right" or self.new_direction == "left") and self.rect.x %2 == 0:
                if self.speed != 2 :
                    self.speed = 2
            self.time2 = pygame.time.get_ticks()
            if self.time2 - self.time > 30000:
                self.time = self.time2
                self.mode = "pinky scatter"
                self.target_x = self.scatter[2][0]
                self.target_y = self.scatter[2][1]
            self.distances = dict()
            for direction in self.directions:
                self.target_x, self.target_y = self.get_target(player)
                if self.can_move(direction) and direction != self.lock_direction:
                    self.distances[direction] = self.x_distance + self.y_distance
            self.min_distance = min(self.distances.values())
            self.new_direction = [key for key in self.distances.keys() if self.distances[key] == self.min_distance][0]

        if self.multi_mode == "pinky frightened":
            self.time3 = pygame.time.get_ticks()
            if self.mode != "":
                self.last_mode = self.mode
            if self.mode != "in" and self.mode != "out":
                self.mode = ""
            if self.time3 - player.start_time > 7000:
                self.server.pinky_color = (255,105,180)
                self.server.pinky2_color = (255,105,180)
                self.time = self.time3
                self.mode = self.last_mode
                self.multi_mode = ""
            if self.mode != "in" and self.mode != "out":
                self.speed = 1
                
                self.valids = []
                for d in self.directions:
                    if d != self.lock_direction and self.can_move(d):
                        self.valids.append(d)
                if self.valids:
                    self.direction = random.choice(self.valids)
                    self.new_direction = self.direction
                if pygame.sprite.collide_rect(player, self):
                    self.time4 = pygame.time.get_ticks()
                    self.mode = "in"
                    self.multi_mode = ""
                    self.new_direction = "up"
                    self.time = self.time4
                    self.rect.center = self.position
                    self.server.pinky_color = (255,105,180)
                    self.server.pinky2_color = (255,105,180)
                    self.speed = 2
            
        return super().update(player)
    
class Clyde(Ghost):
    def __init__(self, position, server, scatters, limit):
        super().__init__(position,server, scatters, limit)
        self.position = position
        self.image = pygame.Surface((32,32))
        pygame.draw.circle(self.image, (255,100,0), (16,16), 16)
        self.mode = "in"
        self.new_direction = "up"
        self.multi_mode = ""

    def get_target(self, player):
        self.dx = abs(player.rect.centerx - self.rect.centerx)
        self.dy = abs(player.rect.centery - self.rect.centery)
        self.distance = self.dx + self.dy
        if self.distance > 8 * TILE_SIZE:
            return player.rect.centerx, player.rect.centery
        else :
            return 6 * TILE_SIZE, 28 * TILE_SIZE

    def update(self, player):
        if self.mode == "in" :
            self.tick = pygame.time.get_ticks()
            if self.tick - self.time > 10000 :
                self.mode = "out"
                self.time = self.tick
            if pygame.sprite.spritecollide(self,self.server.walls,False):
                if self.new_direction == "up" :
                    self.new_direction = "down"
                else:
                    self.new_direction = "up"

        elif self.mode == "out":
            self.time3 = pygame.time.get_ticks()
            if self.time3 - self.time > 1800:
                self.mode = "clyde scatter"
                self.target_x = self.scatter[3][0]
                self.target_y = self.scatter[3][1]
            self.distances_scatter = dict()
            for direction in self.directions:
                self.target_x = self.scatter[2][0]
                self.target_y = self.scatter[2][1]
                if self.can_move(direction) and direction != self.lock_direction:
                    self.distances_scatter[direction] = self.x_distance + self.y_distance
            self.min_distance_scatter = min(self.distances_scatter.values())
            self.new_direction = [key for key in self.distances_scatter.keys() if self.distances_scatter[key] == self.min_distance_scatter][0]

        elif self.mode == "clyde scatter":
            if (self.new_direction == "up" or self.new_direction == "down") and self.rect.y %2 == 0:
                if self.speed != 2 :
                    self.speed = 2
            if (self.new_direction == "right" or self.new_direction == "left") and self.rect.x %2 == 0:
                if self.speed != 2 :
                    self.speed = 2
            self.time1 = pygame.time.get_ticks()
            if self.time1 - self.time > 10000:
                self.time = self.time1
                self.mode = "clyde chase"
                self.target_x, self.target_y = self.get_target(player)
            self.distances_scatter = dict()
            for direction in self.directions:
                self.target_x = self.scatter[3][0]
                self.target_y = self.scatter[3][1]
                if self.can_move(direction) and direction != self.lock_direction:
                    self.distances_scatter[direction] = self.x_distance + self.y_distance
            self.min_distance_scatter = min(self.distances_scatter.values())
            self.new_direction = [key for key in self.distances_scatter.keys() if self.distances_scatter[key] == self.min_distance_scatter][0]

        elif self.mode == "clyde chase":
            if (self.new_direction == "up" or self.new_direction == "down") and self.rect.y %2 == 0:
                if self.speed != 2 :
                    self.speed = 2
            if (self.new_direction == "right" or self.new_direction == "left") and self.rect.x %2 == 0:
                if self.speed != 2 :
                    self.speed = 2
            self.time2 = pygame.time.get_ticks()
            if self.time2 - self.time > 30000:
                self.time = self.time2
                self.mode = "clyde scatter"
                self.target_x = self.scatter[3][0]
                self.target_y = self.scatter[3][1]
            self.distances = dict()
            for direction in self.directions:
                self.target_x, self.target_y = self.get_target(player)
                if self.can_move(direction) and direction != self.lock_direction:
                    self.distances[direction] = self.x_distance + self.y_distance
            self.min_distance = min(self.distances.values())
            self.new_direction = [key for key in self.distances.keys() if self.distances[key] == self.min_distance][0]

        if self.multi_mode == "clyde frightened":
            self.time3 = pygame.time.get_ticks()
            if self.mode != "":
                if self.mode != "in":
                    self.last_mode = self.mode
                else :
                    self.last_mode = "out"
            if self.mode != "in" and self.mode != "out":
                self.mode = ""
            if self.time3 - player.start_time > 7000:
                self.server.clyde_color = (255,100,0)
                self.server.clyde2_color = (255,100,0)
                self.time = self.time3
                self.mode = self.last_mode
                self.multi_mode = ""
            if self.mode != "in" and self.mode != "out":
                self.speed = 1
                
                self.valids = []
                for d in self.directions:
                    if d != self.lock_direction and self.can_move(d):
                        self.valids.append(d)
                if self.valids:
                    self.direction = random.choice(self.valids)
                    self.new_direction = self.direction
                if pygame.sprite.collide_rect(player, self):
                    self.time4 = pygame.time.get_ticks()
                    self.mode = "in"
                    self.multi_mode = ""
                    self.new_direction = "up"
                    self.time = self.time4
                    self.rect.center = self.position
                    self.server.clyde_color = (255,100,0)
                    self.server.clyde2_color = (255,100,0)
                    self.speed = 2

        return super().update(player)
    
class PacmanServer():
    def __init__(self, host = "127.0.0.1", port = 8002):
        self.player0_score = 0
        self.player1_score = 0
        self.winner = ""
        self.running_game = True
        self.walls = pygame.sprite.Group()
        self.pellets = pygame.sprite.Group()
        self.big_pellets = pygame.sprite.Group()
        self.pellets2 = pygame.sprite.Group()
        self.big_pellets2 = pygame.sprite.Group()
        self.ghosts = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.blinky_color = (255, 0, 0)
        self.inky_color = (0, 255, 255)
        self.pinky_color = (255,105,180)
        self.clyde_color = (255, 100, 0)
        self.blinky2_color = (255, 0, 0)
        self.inky2_color = (0, 255, 255)
        self.pinky2_color = (255,105,180)
        self.clyde2_color = (255, 100, 0)
        self.player0_color = (255,255,0)
        self.player1_color = (255,255,0)
        self.level_map = [
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWW WWWWWWWWWWWWWWWWWWWWWWWWWWWW", 
            "W............WW............W W************WW************W",
            "W.WWWW.WWWWW.WW.WWWWW.WWWW.W W*WWWW*WWWWW*WW*WWWWW*WWWW*W",
            "WoWWWW.WWWWW.WW.WWWWW.WWWWoW WOWWWW*WWWWW*WW*WWWWW*WWWWOW",
            "W.WWWW.WWWWW.WW.WWWWW.WWWW.W W*WWWW*WWWWW*WW*WWWWW*WWWW*W",
            "W..........................W W**************************W",
            "W.WWWW.WW.WWWWWWWW.WW.WWWW.W W*WWWW*WW*WWWWWWWW*WW*WWWW*W",
            "W.WWWW.WW.WWWWWWWW.WW.WWWW.W W*WWWW*WW*WWWWWWWW*WW*WWWW*W",
            "W......WW....WW....WW......W W******WW****WW****WW******W",
            "WWWWWW.WWWWW WW WWWWW.WWWWWW WWWWWW*WWWWW WW WWWWW*WWWWWW",
            "     W.WWWWW WW WWWWW.W           W*WWWWW WW WWWWW*W     ",
            "     W.WW     B    WW.W           W*WW     b    WW*W     ",
            "     W.WW WWW__WWW WW.W           W*WW WWW__WWW WW*W     ",
            "WWWWWW.WW W      W WW.WWWWWW WWWWWW*WW W      W WW*WWWWWW",
            "      .   WIP   CW   .             *   Wip   cW   *      ",
            "WWWWWW.WW W      W WW.WWWWWW WWWWWW*WW W      W WW*WWWWWW",
            "     W.WW WWWWWWWW WW.W           W*WW WWWWWWWW WW*W     ",
            "     W.WW          WW.W           W*WW          WW*W     ",
            "     W.WW WWWWWWWW WW.W           W*WW WWWWWWWW WW*W     ",
            "WWWWWW.WW WWWWWWWW WW.WWWWWW WWWWWW*WW WWWWWWWW WW*WWWWWW",
            "W............WW............W W************WW************W",
            "W.WWWW.WWWWW.WW.WWWWW.WWWW.W W*WWWW*WWWWW*WW*WWWWW*WWWW*W",
            "W.WWWW.WWWWW.WW.WWWWW.WWWW.W W*WWWW*WWWWW*WW*WWWWW*WWWW*W",
            "Wo..WW................WW..oW WO**WW****************WW**OW",
            "WWW.WW.WW.WWWWWWWW.WW.WW.WWW WWW*WW*WW*WWWWWWWW*WW*WW*WWW",
            "WWW.WW.WW.WWWWWWWW.WW.WW.WWW WWW*WW*WW*WWWWWWWW*WW*WW*WWW",
            "W......WW....WW....WW......W W******WW****WW****WW******W",
            "W.WWWWWWWWWW.WW.WWWWWWWWWW.W W*WWWWWWWWWW*WW*WWWWWWWWWW*W",
            "W.WWWWWWWWWW.WW.WWWWWWWWWW.W W*WWWWWWWWWW*WW*WWWWWWWWWW*W",
            "W..........................W W**************************W",
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWW WWWWWWWWWWWWWWWWWWWWWWWWWWWW"
        ]
        self.player_scatter = {"0": [(768, 128), (28 * TILE_SIZE, 34 * TILE_SIZE), (96, 96), (10 * TILE_SIZE, 28 * TILE_SIZE)],
                               "1": [(1664, 128), (57 * TILE_SIZE, 34 * TILE_SIZE), (32 * TILE_SIZE, 96), (40 * TILE_SIZE, 28 * TILE_SIZE)]
                                    }
        self.create_map()
        self.player_ghosts = {0 : [self.blinky, self.inky, self.pinky, self.clyde],
                              1 : [self.blinky2, self.inky2, self.pinky2, self.clyde2]
                              }
        self.player_pellets = {0 : [self.pellets, self.big_pellets],
                               1 : [self.pellets2, self.big_pellets2]}
        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host,port))
        self.server.listen(2)
        self.players = {}
        self.sockets = {}
        self.player_id = 0
        self.corrent_palayer = 0
        self.player_positions = {0 : (24 * TILE_SIZE, 30 * TILE_SIZE), 1: (52 * TILE_SIZE, 30 * TILE_SIZE)}

    def create_map(self):
        for row_idx, row in enumerate(self.level_map):
            for col_idx, tile in enumerate(row):
                x = (col_idx) * (TILE_SIZE)
                y = (row_idx+1) * (TILE_SIZE)
                if tile == "W":
                    self.wall = Wall((x, y))
                    self.walls.add(self.wall)
                    self.all_sprites.add(self.wall)
                elif tile == ".":
                    self.pellet = Pellet((x + TILE_SIZE//2, y + TILE_SIZE//2))
                    self.pellets.add(self.pellet)
                    self.all_sprites.add(self.pellet)
                elif tile == "o":
                    self.big_pellet = BigPellet((x + TILE_SIZE // 2, y + TILE_SIZE // 2))
                    self.big_pellets.add(self.big_pellet)
                    self.all_sprites.add(self.big_pellet)
                elif tile == "*":
                    self.pellet2 = Pellet((x + TILE_SIZE//2, y + TILE_SIZE//2))
                    self.pellets2.add(self.pellet2)
                    self.all_sprites.add(self.pellet2)
                elif tile == "O":
                    self.big_pellet2 = BigPellet((x + TILE_SIZE // 2, y + TILE_SIZE // 2))
                    self.big_pellets2.add(self.big_pellet2)
                    self.all_sprites.add(self.big_pellet2)
                elif tile == "B":
                    self.blinky = Ghost((x + TILE_SIZE // 2, y + TILE_SIZE // 2), self, self.player_scatter["0"], (416, 448))
                    self.ghosts.add(self.blinky)
                    self.all_sprites.add(self.blinky)
                elif tile == "I":
                    self.inky = Inky((x + TILE_SIZE // 2, y + TILE_SIZE // 2), self, self.blinky, self.player_scatter["0"], (416, 448))
                    self.ghosts.add(self.inky)
                    self.all_sprites.add(self.inky)
                elif tile == "P":
                    self.pinky = Pinky((x + TILE_SIZE // 2, y + TILE_SIZE // 2), self, self.player_scatter["0"], (416, 448))
                    self.ghosts.add(self.pinky)
                    self.all_sprites.add(self.pinky)
                elif tile == "C":
                    self.clyde = Clyde((x + TILE_SIZE // 2, y + TILE_SIZE // 2), self, self.player_scatter["0"], (416, 448))
                    self.ghosts.add(self.clyde)
                    self.all_sprites.add(self.clyde)
                elif tile == "b":
                    self.blinky2 = Ghost((x + TILE_SIZE // 2, y + TILE_SIZE // 2), self, self.player_scatter["1"], (1344, 1376))
                    self.ghosts.add(self.blinky2)
                    self.all_sprites.add(self.blinky2)
                elif tile == "i":
                    self.inky2 = Inky((x + TILE_SIZE // 2, y + TILE_SIZE // 2), self, self.blinky2, self.player_scatter["1"], (1344, 1376))
                    self.ghosts.add(self.inky2)
                    self.all_sprites.add(self.inky2)
                elif tile == "p":
                    self.pinky2 = Pinky((x + TILE_SIZE // 2, y + TILE_SIZE // 2), self, self.player_scatter["1"], (1344, 1376))
                    self.ghosts.add(self.pinky2)
                    self.all_sprites.add(self.pinky2)
                elif tile == "c":
                    self.clyde2 = Clyde((x + TILE_SIZE // 2, y + TILE_SIZE // 2), self, self.player_scatter["1"], (1344, 1376))
                    self.ghosts.add(self.clyde2)
                    self.all_sprites.add(self.clyde2)

    def ghost_state(self):
        return [
            {"type": "blinky", "rect": (self.blinky.rect.x,self.blinky.rect.y), "color": self.blinky_color},
            {"type": "blinky", "rect": (self.blinky2.rect.x,self.blinky2.rect.y), "color": self.blinky2_color},
            {"type": "inky", "rect": (self.inky.rect.x,self.inky.rect.y), "color": self.inky_color},
            {"type": "inky", "rect": (self.inky2.rect.x,self.inky2.rect.y), "color": self.inky2_color},
            {"type": "pinky", "rect": (self.pinky.rect.x,self.pinky.rect.y), "color": self.pinky_color},
            {"type": "pinky", "rect": (self.pinky2.rect.x,self.pinky2.rect.y), "color": self.pinky2_color},
            {"type": "clyde", "rect": (self.clyde.rect.x,self.clyde.rect.y), "color": self.clyde_color},
            {"type": "clyde", "rect": (self.clyde2.rect.x,self.clyde2.rect.y), "color": self.clyde2_color},
        ]
    
    def player_state(self,):
        return [{"player": "0" , "rect": (self.players[0].rect.x, self.players[0].rect.y), "color" : self.player0_color},
                {"player": "0" , "rect": (self.players[1].rect.x, self.players[1].rect.y), "color" : self.player1_color}
                ]

    def start(self) :
        while self.player_id < 2:
            client_socket, adrr = self.server.accept()
            self.sockets[self.player_id] = client_socket
            player = Pacman(self.player_positions[self.player_id], self, self.player_id)
            self.players[self.player_id] = player
            thread = threading.Thread(target=self.handle_client, args = (client_socket,self.player_id))
            thread.start()
            self.player_id += 1

    def handle_client(self, client_socket, player_id):
        while len(self.players)<2:
            pass
        player = self.players[player_id]
        ghosts = self.player_ghosts[player_id]
        pellets = self.player_pellets[player_id]
        try :
            while True:
                keys = pickle.loads(client_socket.recv(1024))
                if keys == "quit" :
                    break
                
                player.update(keys,pellets)
                for ghost in ghosts:
                    ghost.update(player)

                if self.blinky.mode != "frightened" and pygame.sprite.collide_rect(self.blinky,self.players[0]):
                    self.running_game = False
                    self.winner = "player2"
                elif self.inky.mode != "inky frightened" and pygame.sprite.collide_rect(self.inky,self.players[0]):
                    self.running_game = False
                    self.winner = "player2"
                elif self.pinky.mode != "pinky frightened" and pygame.sprite.collide_rect(self.pinky,self.players[0]):
                    self.running_game = False
                    self.winner = "player2"
                elif self.clyde.mode != "clyde frightened" and pygame.sprite.collide_rect(self.clyde,self.players[0]):
                    self.running_game = False
                    self.winner = "player2"

                elif self.blinky2.mode != "frightened" and pygame.sprite.collide_rect(self.blinky2,self.players[1]):
                    self.running_game = False
                    self.winner = "player1"
                elif self.inky2.mode != "inky frightened" and pygame.sprite.collide_rect(self.inky2,self.players[1]):
                    self.running_game = False
                    self.winner = "player1"
                elif self.pinky2.mode != "pinky frightened" and pygame.sprite.collide_rect(self.pinky2,self.players[1]):
                    self.running_game = False
                    self.winner = "player1"
                elif self.clyde2.mode != "clyde frightened" and pygame.sprite.collide_rect(self.clyde2,self.players[1]):
                    self.running_game = False
                    self.winner = "player1"

                game_state = self.get_game_state()
                client_socket.sendall(pickle.dumps(game_state))

        except Exception as e:
            print(f"Error with player {player_id}: {e}")
        finally:
            client_socket.close()

    def get_game_state(self):
        return {
            "players": [{"rect": p["rect"], "color": p["color"]} for p in self.player_state()],
            "walls" : [(w.rect.x, w.rect.y) for w in self.walls],
            "ghosts" :[{"rect": g["rect"], "color": g["color"]} for g in self.ghost_state()],
            "pellets" : [(p.rect.x, p.rect.y) for p in self.pellets],
            "pellets2" : [(p2.rect.x, p2.rect.y) for p2 in self.pellets2],
            "big_pellets" : [(b.rect.x, b.rect.y) for b in self.big_pellets],
            "big_pellets2" : [(b2.rect.x, b2.rect.y) for b2 in self.big_pellets2],
            "running_game" : self.running_game,
            "scores" : [self.player0_score, self.player1_score],
            "winner" : self.winner

        }

PacmanServer().start()
