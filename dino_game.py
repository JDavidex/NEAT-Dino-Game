import pygame # Pygame library for game development
import os # To handle file paths
import random # For random number generation
import neat # NEAT library for neuroevolution

pygame.init()

# Constants
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dino Game - NEAT AI")

RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "run1.png")), pygame.image.load(os.path.join("Assets/Dino", "run2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "jump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "duck1.png")), pygame.image.load(os.path.join("Assets/Dino", "duck2.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "small1.png")), pygame.image.load(os.path.join("Assets/Cactus", "small2.png")), pygame.image.load(os.path.join("Assets/Cactus", "small3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "large1.png")), pygame.image.load(os.path.join("Assets/Cactus", "large2.png")), pygame.image.load(os.path.join("Assets/Cactus", "large3.png"))]
BIRD = [pygame.image.load(os.path.join("Assets/Bird", "bird1.png")), pygame.image.load(os.path.join("Assets/Bird", "bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Scenery", "cloud.png"))
BG = pygame.image.load(os.path.join("Assets/Scenery", "track.png"))

class Dinosaur:
    X_POS = 80
    Y_POS = 310
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        
        # For fitness tracking: last obstacle passed
        self.last_obstacle_passed = None

    def update(self, jump, duck):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump(duck)

        if self.step_index >= 10:
            self.step_index = 0

        # Actions based on NN output
        if jump and not self.dino_jump: 
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif duck and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or duck):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False
        
    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS + 36
        self.dino_rect.width = self.image.get_width()
        self.dino_rect.height = self.image.get_height()
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self, duck_pressed=False):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if duck_pressed and self.dino_jump:
            pass
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL
            self.dino_rect.y = self.Y_POS

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))

class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325

class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300

class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = random.choice([240, 270, 300]) 
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1

# eval_genomes is the main function that NEAT uses to evaluate each genome in the population.
# It runs the game loop and assigns fitness scores based on how well each dinosaur performs.
def eval_genomes(genomes, config):
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, high_score
    clock = pygame.time.Clock()
    
    # NEAT setup
    dinosaurs = [] # List of Dinosaur instances corresponding to each genome
    ge = [] # List of genomes for fitness assignment after each game loop iteration
    nets = [] # List of neural networks created from the genomes for decision making

    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        dinosaurs.append(Dinosaur())
        ge.append(genome)

    cloud = Cloud()
    game_speed = 16
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font('Assets/Font/PressStart2P-Regular.ttf', 20)
    stats_font = pygame.font.Font('Assets/Font/PressStart2P-Regular.ttf', 16)
    obstacles = []
    
    def score():
        global points, game_speed, high_score
        points += 1
        if points % 100 == 0:
            game_speed += 1
        
        if points > high_score:
            high_score = points
        
        hi_text = font.render("HI", True, (83, 83, 83))
        SCREEN.blit(hi_text, (SCREEN_WIDTH - 380, 30))
        
        hi_score_text = font.render(str(high_score).zfill(5), True, (83, 83, 83))
        SCREEN.blit(hi_score_text, (SCREEN_WIDTH - 300, 30))
        
        score_text = font.render(str(points).zfill(5), True, (83, 83, 83))
        SCREEN.blit(score_text, (SCREEN_WIDTH - 150, 30))
        
        # Stats for current generation
        text_dinos = stats_font.render(f'Alive: {str(len(dinosaurs))}', True, (83, 83, 83))
        SCREEN.blit(text_dinos, (50, 470))
        
        text_gen = stats_font.render(f'Generation: {p.generation}', True, (83, 83, 83))
        SCREEN.blit(text_gen, (50, 500))
        
        text_speed = stats_font.render(f'Speed: {str(game_speed)}', True, (83, 83, 83))
        SCREEN.blit(text_speed, (50, 530))

        # version info
        version_text = stats_font.render('v1.0', True, (83, 83, 83))
        SCREEN.blit(version_text, (SCREEN_WIDTH - 80, SCREEN_HEIGHT - 30))

    def draw_background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    run = True
    # The main game loop continues until all dinosaurs have died or the user quits the game.
    while run and len(dinosaurs) > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        SCREEN.fill((255, 255, 255))

        if len(obstacles) == 0:
            # Birds appear after 200 points, otherwise random cactus
            if points > 200 and random.randint(0, 9) == 0:
                obstacles.append(Bird(BIRD))
            else:
                if random.randint(0, 1) == 0:
                     obstacles.append(SmallCactus(SMALL_CACTUS))
                else:
                     obstacles.append(LargeCactus(LARGE_CACTUS))

        # Update obstacles
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            
            # Collision Check
            for i, dino in enumerate(dinosaurs):
                if dino.dino_rect.colliderect(obstacle.rect):
                    ge[i].fitness -= 10 # Hard penalty for colliding with an obstacle
                    dinosaurs.pop(i)
                    nets.pop(i)
                    ge.pop(i)

        # Update Dinosaurs
        for i, dino in enumerate(dinosaurs):
            ge[i].fitness += 0.1 # Reward for staying alive each frame
            
            # Reward for passing obstacles
            if len(obstacles) > 0:
                if obstacles[0].rect.x + obstacles[0].rect.width < dino.dino_rect.x:
                    if dino.last_obstacle_passed != id(obstacles[0]):
                        ge[i].fitness += 50  # Extra reward for passing an obstacle
                        dino.last_obstacle_passed = id(obstacles[0])
            
            dino.draw(SCREEN)
            
            # Decision making based on the closest obstacle
            if len(obstacles) > 0:
                obstacle_idx = 0
                if len(obstacles) > 1 and obstacles[0].rect.x + obstacles[0].rect.width < dino.dino_rect.x:
                    obstacle_idx = 1
                
                obs = obstacles[obstacle_idx]
                
                # Normalize inputs for the neural network to ensure consistent scaling
                inputs = (
                    dino.dino_rect.y / SCREEN_HEIGHT,                       # Dino's vertical position (normalized)
                    obs.rect.x / SCREEN_WIDTH,                              # Obstacle's horizontal position (normalized)
                    obs.rect.y / SCREEN_HEIGHT,                             # Obstacle's vertical position (normalized)
                    obs.rect.width / 200,                                   # Obstacle's width (normalized)
                    obs.rect.height / 200,                                  # Obstacle's height (normalized)
                    game_speed / 30,                                        # Current game speed (normalized)
                    1 if isinstance(obs, Bird) else 0,                      # Useful for distinguishing between birds and cacti (binary input)
                )
                
                output = nets[i].activate(inputs)
                
                # Output 0: Jump
                # Output 1: Duck
                
                jump = output[0] > 0.5
                duck = output[1] > 0.5
                
                dino.update(jump, duck)
            else:
                dino.update(False, False)

        draw_background()
        cloud.draw(SCREEN)
        cloud.update()
        score()

        pygame.display.update()
        clock.tick(60)  # Run at 120 FPS for smoother gameplay and better training performance

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)
    
    global p, high_score
    high_score = 0 # Global high score variable
    p = neat.Population(config)
    
    # Reporters
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    
    winner = p.run(eval_genomes, 24) 
    print(f'\n🏆 Best genome:\n{winner}')
    print(f'\n🎯 High Score: {high_score}')

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config_neat.txt')
    run(config_path)