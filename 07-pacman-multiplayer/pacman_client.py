import pygame, pickle, socket
"""writen by Zahra Gharib & Seyed Sajjad Qavami"""

pygame.init()

TILE_SIZE = 32

class PacmanClient() :
    def __init__(self, host = "127.0.0.1", port = 8002) -> None:
        self.font = pygame.font.SysFont(None, 32)
        self.screen = pygame.display.set_mode((28 * TILE_SIZE * 2 + 32, 32 * TILE_SIZE))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 32)
        self.font2 = pygame.font.SysFont(None, 50)
        self.running_game = True

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host,port))

    def send_keys(self, keys) :
        try :
            self.client.sendall(pickle.dumps(keys))
        except Exception as e:
            print(f"ERROR sending keys {e}")
            self.running_game = False

    def game_state(self) :
        data = b""
        while True:
            try :
                package = self.client.recv(8192)
                if not package :
                    break
                data += package
                try :
                    return pickle.loads(data)
                except :
                    continue
            except Exception as e :
                print(f"ERROR reciving game state {e}")
                self.running_game = False
                return None
    def draw(self, game_state) :
        self.screen.fill((0,0,0))

        for wall in game_state.get("walls", []):
            pygame.draw.rect(self.screen, (0, 0, 255), pygame.Rect(*wall, TILE_SIZE, TILE_SIZE))
        
        for pellet in game_state.get("pellets", []):
            pygame.draw.circle(self.screen, (255, 255, 255),( pellet[0] + 3, pellet[1] + 3), 3)

        for pellet2 in game_state.get("pellets2", []):
            pygame.draw.circle(self.screen, (255, 255, 255),( pellet2[0] + 3, pellet2[1] + 3), 3)
        
        for big_pellet in game_state.get("big_pellets", []):
            pygame.draw.circle(self.screen, (255, 255, 255), (big_pellet[0] + 12, big_pellet[1] + 12), 12)

        for big_pellet2 in game_state.get("big_pellets2", []):
            pygame.draw.circle(self.screen, (255, 255, 255), (big_pellet2[0] + 12, big_pellet2[1] + 12), 12)

        for player in game_state.get("players", []):
            pygame.draw.circle(self.screen, player["color"], (player["rect"][0] + 16, player["rect"][1] + 16), 16)
        
        for ghost in game_state.get("ghosts", []):
            pygame.draw.circle(self.screen, ghost["color"], (ghost["rect"][0] + 16, ghost["rect"][1] + 16), 16)

        self.score1 = game_state.get("scores", 0)[0]
        self.score2 = game_state.get("scores", 0)[1]
        self.message1 = self.font.render(f"score : {self.score1}", True, (255,255,255))
        self.screen.blit(self.message1,(10,0))
        self.message2 = self.font.render(f"score : {self.score2}", True, (255,255,255))
        self.screen.blit(self.message2,(950,0))
        self.player1 = self.font.render("player1", True, (255,0,0))
        self.screen.blit(self.player1,(400,0))
        self.player2 = self.font.render("player2", True, (255,0,0))
        self.screen.blit(self.player2,(1300,0))

        pygame.display.flip()
        
    def run(self):
        while self.running_game:
            keys_pressed = pygame.key.get_pressed()
            keys = {pygame.K_LEFT : keys_pressed[pygame.K_LEFT],
                    pygame.K_RIGHT : keys_pressed[pygame.K_RIGHT],
                    pygame.K_UP : keys_pressed[pygame.K_UP],
                    pygame.K_DOWN : keys_pressed[pygame.K_DOWN]
                    }
            self.send_keys(keys)
            game_state = self.game_state()
            if game_state is None:
                break
            

            self.draw(game_state)
            if game_state.get("running_game", "") == False:
                self.running_game = False
            
            self.winner = game_state.get("winner","")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.send_keys("quit")
                    self.running = False
            self.clock.tick(60)

        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 64)
        text = font.render(f"Game Over {self.winner} won", True, (255, 0, 0))
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(text, text_rect)
        pygame.display.update()
        pygame.time.delay(3000)

        pygame.quit()
        self.client.close()

PacmanClient().run()