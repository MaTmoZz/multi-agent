import pygame
import random
import math

# Initialize pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
ENTITY_RADIUS = 5
SPEED = 3
DETECTION_RADIUS = 100
CONVERSION_RADIUS = 20
EDGE_AVOID_RADIUS = 50
REPULSION_RADIUS = 20
ICON_WIDTH = 30
ICON_HEIGHT = 30
OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 50

# Load and scale the background image
background_image = pygame.image.load('field.jpg')
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

# Load and scale entity icons
snake_icon = pygame.image.load('snake.png')
snake_icon = pygame.transform.scale(snake_icon, (ICON_WIDTH, ICON_HEIGHT))

chicken_icon = pygame.image.load('chicken.png')
chicken_icon = pygame.transform.scale(chicken_icon, (ICON_WIDTH, ICON_HEIGHT))

fox_icon = pygame.image.load('fox.png')
fox_icon = pygame.transform.scale(fox_icon, (ICON_WIDTH, ICON_HEIGHT))

# Load and scale obstacle image
obstacle_image = pygame.image.load('roche.png')
obstacle_image = pygame.transform.scale(obstacle_image, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))

class Entity:
    def __init__(self, x, y, tribe):
        self.x = x
        self.y = y
        self.tribe = tribe
        self.jail = False
        self.frozen = False


    def check_prison_reach(self):
        if self.tribe == 'chicken' and self.frozen == False and is_within_rect(self.x, self.y, rect2_pos[0] - 100, rect2_pos[0] + 100, rect2_pos[1] - 100, rect2_pos[1] + 100):
            return True
        if self.tribe == 'fox' and self.frozen == False and is_within_rect(self.x, self.y, rect3_pos[0] - 100, rect3_pos[0] + 100, rect3_pos[1] - 100, rect3_pos[1] + 100):
            return True
        if self.tribe == 'snake' and self.frozen == False and is_within_rect(self.x, self.y, rect1_pos[0] - 100, rect1_pos[0] + 100, rect1_pos[1] - 100, rect1_pos[1] + 100):
            return True
        return False

    def move_towards(self, target_x, target_y):
        if not self.frozen:
            angle = math.atan2(target_y - self.y, target_x - self.x)
            self.x += (SPEED + random.uniform(-0.3, 0.3)) * math.cos(angle)
            self.y += (SPEED + random.uniform(-0.3, 0.3)) * math.sin(angle)
            self.avoid_edges_and_restricted_areas()

    def move_away_from(self, target_x, target_y):
        if not self.frozen:
            angle = math.atan2(target_y - self.y, target_x - self.x)
            self.x -= (SPEED + random.uniform(-0.3, 0.3)) * math.cos(angle)
            self.y -= (SPEED + random.uniform(-0.3, 0.3)) * math.sin(angle)
            self.avoid_edges_and_restricted_areas()

    def distance_to(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def repel_from(self, other):
        if self.distance_to(other) < REPULSION_RADIUS:
            self.move_away_from(other.x, other.y)

    def draw(self):
        if self.tribe == 'snake':
            screen.blit(snake_icon, (self.x - ICON_WIDTH // 2, self.y - ICON_HEIGHT // 2))
        elif self.tribe == 'chicken':
            screen.blit(chicken_icon, (self.x - ICON_WIDTH // 2, self.y - ICON_HEIGHT // 2))
        else:
            screen.blit(fox_icon, (self.x - ICON_WIDTH // 2, self.y - ICON_HEIGHT // 2))

    def avoid_edges_and_restricted_areas(self):
        # Avoid edges
        if self.x < EDGE_AVOID_RADIUS:
            self.x = EDGE_AVOID_RADIUS
        elif self.x > WINDOW_WIDTH - EDGE_AVOID_RADIUS:
            self.x = WINDOW_WIDTH - EDGE_AVOID_RADIUS
        if self.y < EDGE_AVOID_RADIUS:
            self.y = EDGE_AVOID_RADIUS
        elif self.y > WINDOW_HEIGHT - EDGE_AVOID_RADIUS:
            self.y = WINDOW_HEIGHT - EDGE_AVOID_RADIUS

        # Avoid restricted areas
        self.avoid_restricted_area()

    def avoid_restricted_area(self):
        # Carré 1 (pour les poules et les renards)
        if self.tribe in ['chicken', 'fox']:
            rect1_left = 500
            rect1_right = 700
            rect1_top = 0
            rect1_bottom = 200

            if rect1_left < self.x < rect1_right and rect1_top < self.y < rect1_bottom:
                if self.x < (rect1_left + rect1_right) / 2:
                    self.x = rect1_left - EDGE_AVOID_RADIUS
                else:
                    self.x = rect1_right + EDGE_AVOID_RADIUS

                if self.y < (rect1_top + rect1_bottom) / 2:
                    self.y = rect1_top - EDGE_AVOID_RADIUS
                else:
                    self.y = rect1_bottom + EDGE_AVOID_RADIUS

        # Carré 2 (pour les serpents et les renards)
        if self.tribe in ['snake', 'fox']:
            rect2_left = 0
            rect2_right = 200
            rect2_top = 500
            rect2_bottom = 700

            if rect2_left < self.x < rect2_right and rect2_top < self.y < rect2_bottom:
                if self.x < (rect2_left + rect2_right) / 2:
                    self.x = rect2_left - EDGE_AVOID_RADIUS
                else:
                    self.x = rect2_right + EDGE_AVOID_RADIUS

                if self.y < (rect2_top + rect2_bottom) / 2:
                    self.y = rect2_top - EDGE_AVOID_RADIUS
                else:
                    self.y = rect2_bottom + EDGE_AVOID_RADIUS

        # Carré 3 (pour les serpents et les poules)
        if self.tribe in ['snake', 'chicken']:
            rect3_left = 1000
            rect3_right = 1200
            rect3_top = 500
            rect3_bottom = 700

            if rect3_left < self.x < rect3_right and rect3_top < self.y < rect3_bottom:
                if self.x < (rect3_left + rect3_right) / 2:
                    self.x = rect3_left - EDGE_AVOID_RADIUS
                else:
                    self.x = rect3_right + EDGE_AVOID_RADIUS

                if self.y < (rect3_top + rect3_bottom) / 2:
                    self.y = rect3_top - EDGE_AVOID_RADIUS
                else:
                    self.y = rect3_bottom + EDGE_AVOID_RADIUS

    def avoid_obstacles(self):
        for obstacle in obstacles:
            if self.distance_to(obstacle) < OBSTACLE_WIDTH:
                self.move_away_from(obstacle.x, obstacle.y)

class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        screen.blit(obstacle_image, (self.x - OBSTACLE_WIDTH // 2, self.y - OBSTACLE_HEIGHT // 2))

def is_within_rect(x, y, rect_left, rect_right, rect_top, rect_bottom):
    return rect_left < x < rect_right and rect_top < y < rect_bottom

def generate_valid_position():
    while True:
        x = random.randint(0, WINDOW_WIDTH)
        y = random.randint(0, WINDOW_HEIGHT)
        
        # Vérifiez si la position est à l'extérieur des carrés restreints
        if not is_within_rect(x, y, 500, 700, 0, 200) and \
           not is_within_rect(x, y, 0, 200, 500, 700) and \
           not is_within_rect(x, y, 1000, 1200, 500, 700):
            return x, y

# Create obstacles
obstacles = [Obstacle(random.randint(OBSTACLE_WIDTH, WINDOW_WIDTH - OBSTACLE_WIDTH), 
                      random.randint(OBSTACLE_HEIGHT, WINDOW_HEIGHT - OBSTACLE_HEIGHT)) for _ in range(10)]

# Create entities
entities = []
for _ in range(10):
    x, y = generate_valid_position()
    entities.append(Entity(x, y, 'snake'))

for _ in range(10):
    x, y = generate_valid_position()
    entities.append(Entity(x, y, 'chicken'))

for _ in range(10):
    x, y = generate_valid_position()
    entities.append(Entity(x, y, 'fox'))

# Define circle positions
rect1_pos = (600, 100)
rect2_pos = (100, 600)
rect3_pos = (1100, 600)

def adjust_movement():
    for entity in entities:
        if entity.tribe == 'snake':
            targets = [e for e in entities if e.tribe == 'fox']
            threats = [e for e in entities if e.tribe == 'chicken']
        elif entity.tribe == 'chicken':
            targets = [e for e in entities if e.tribe == 'snake']
            threats = [e for e in entities if e.tribe == 'fox']
        else:
            targets = [e for e in entities if e.tribe == 'chicken']
            threats = [e for e in entities if e.tribe == 'snake']

        for other in entities:
            if entity != other and entity.tribe == other.tribe:
                entity.repel_from(other)

        closest_target = min(targets, key=entity.distance_to, default=None)
        closest_threat = min(threats, key=entity.distance_to, default=None)

        if closest_threat and entity.distance_to(closest_threat) < DETECTION_RADIUS:
            entity.move_away_from(closest_threat.x, closest_threat.y)
        elif closest_target and entity.distance_to(closest_target) < DETECTION_RADIUS and not closest_target.jail:
            entity.move_towards(closest_target.x, closest_target.y)
            if entity.distance_to(closest_target) < CONVERSION_RADIUS:
                closest_target.jail = True
                if closest_target.tribe == "chicken":
                    closest_target.x = random.randint(rect2_pos[0] - 100, rect2_pos[0] + 100)
                    closest_target.y = random.randint(rect2_pos[1] - 100, rect2_pos[1] + 100)
                    closest_target.frozen = True
                elif closest_target.tribe == "snake":
                    closest_target.x = random.randint(rect1_pos[0] - 100, rect1_pos[0] + 100)
                    closest_target.y = random.randint(rect1_pos[1] - 100, rect1_pos[1] + 100)
                    closest_target.frozen = True
                elif closest_target.tribe == "fox":
                    closest_target.x = random.randint(rect3_pos[0] - 100, rect3_pos[0] + 100)
                    closest_target.y = random.randint(rect3_pos[1] - 100, rect3_pos[1] + 100)
                    closest_target.frozen = True

        else:
            entity.move_towards(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT))

        entity.draw()

# Initialize pygame display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Fox Chicken Snake Simulation")
clock = pygame.time.Clock()
running = True

# Game loop
while running:
    screen.blit(background_image, (0, 0))
    adjust_movement()

    # Draw squares
    pygame.draw.rect(screen, (244, 227, 206), (rect1_pos[0] - 100, rect1_pos[1] - 100, 200, 200), 2)  # Square 1
    pygame.draw.rect(screen, (211, 102, 1), (rect2_pos[0] - 100, rect2_pos[1] - 100, 200, 200), 2)  # Square 2
    pygame.draw.rect(screen, (135, 165, 114), (rect3_pos[0] - 100, rect3_pos[1] - 100, 200, 200), 2)  # Square 3

    # Draw obstacles
    for obstacle in obstacles:
        obstacle.draw()

    # Check if any chicken reaches its prison and unfreeze all chickens
    for entity in entities:
        if entity.check_prison_reach():
            for e in entities:
                if entity.tribe == e.tribe:
                    e.frozen = False
                    e.jail = False


    # Check victory conditions
    snakes_movable = any(not entity.jail and not entity.frozen for entity in entities if entity.tribe == 'snake')
    chickens_movable = any(not entity.jail and not entity.frozen for entity in entities if entity.tribe == 'chicken')
    foxes_movable = any(not entity.jail and not entity.frozen for entity in entities if entity.tribe == 'fox')

    if not foxes_movable:
        winner_text = "Snake"
    elif not chickens_movable:
        winner_text = "Fox"
    elif not snakes_movable:
        winner_text = "Chicken"
    else:
        winner_text = None
        

    # Display winner if exists
    if winner_text:
        pygame.font.init()
        font_large = pygame.font.Font(None, 100)
        font_small = pygame.font.Font(None, 74)

        winner_title_surface = font_large.render("Winner!", True, pygame.Color("#6aff9b"))
        tribe_name_surface = font_small.render(winner_text, True, (255, 255, 255))

        padding = 20
        box_width = max(winner_title_surface.get_width(), tribe_name_surface.get_width()) + 2 * padding
        box_height = winner_title_surface.get_height() + tribe_name_surface.get_height() + 3 * padding

        # Draw the black box
        pygame.draw.rect(screen, (0, 0, 0), (WINDOW_WIDTH // 2 - box_width // 2, WINDOW_HEIGHT // 2 - box_height // 2, box_width, box_height))

        # Blit the texts onto the screen
        screen.blit(winner_title_surface, (WINDOW_WIDTH // 2 - winner_title_surface.get_width() // 2, WINDOW_HEIGHT // 2 - box_height // 2 + padding))
        screen.blit(tribe_name_surface, (WINDOW_WIDTH // 2 - tribe_name_surface.get_width() // 2, WINDOW_HEIGHT // 2 + padding))

        pygame.display.flip()
        pygame.time.wait(10000)
        running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
