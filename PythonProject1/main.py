import pygame
import math
import random
from pygame.math import Vector2

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1200, 800
FPS = 60
DOT_RADIUS = 2
NUM_ROWS = 15
DOTS_PER_ROW = 80
AMPLITUDE = 40
FREQUENCY = 0.008  # Reduced from 0.02 (slower wave formation)
PHASE_SHIFT = 0.03  # Reduced from 0.1 (slower wave movement)
TRAIL_ALPHA = 25
MOUSE_INFLUENCE_RADIUS = 150
MOUSE_INFLUENCE_RADIUS_SQ = MOUSE_INFLUENCE_RADIUS ** 2
MAX_DISPLACEMENT = 30
PULSE_AMPLITUDE = 1
STAR_COUNT = 200
STAR_TWINKLE_SPEED = 2

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("White Gradient Wave Dots with Mouse Interaction")
clock = pygame.time.Clock()

# Trail surface
trail_surface = pygame.Surface((WIDTH, HEIGHT))
trail_surface.set_alpha(TRAIL_ALPHA)


class WaveRow:
    def __init__(self, y_pos, phase_offset):
        self.y_base = y_pos
        self.phase = phase_offset
        self.dots = [(x * (WIDTH // DOTS_PER_ROW), y_pos)
                     for x in range(DOTS_PER_ROW)]

    def update(self, time, mouse_x, mouse_y):
        self.phase += PHASE_SHIFT

        for i, (x, y) in enumerate(self.dots):
            angle = x * FREQUENCY + self.phase
            new_y = self.y_base + math.sin(angle) * AMPLITUDE

            # Calculate mouse influence
            dx = x - mouse_x
            dy = new_y - mouse_y
            distance_sq = dx ** 2 + dy ** 2

            if distance_sq < MOUSE_INFLUENCE_RADIUS_SQ:
                if distance_sq == 0:
                    new_y += MAX_DISPLACEMENT
                else:
                    distance = math.sqrt(distance_sq)
                    if distance < MOUSE_INFLUENCE_RADIUS:
                        factor = (MOUSE_INFLUENCE_RADIUS - distance) / MOUSE_INFLUENCE_RADIUS
                        displacement = factor * MAX_DISPLACEMENT
                        dir_y = dy / distance
                        new_y += dir_y * displacement

            self.dots[i] = (x, new_y)


# Create wave rows
vertical_spacing = HEIGHT // (NUM_ROWS + 1)
wave_rows = [WaveRow(i * vertical_spacing, i * math.pi / NUM_ROWS)
             for i in range(1, NUM_ROWS + 1)]

# Initialize stars
stars = [{
    'x': random.randint(0, WIDTH),
    'y': random.randint(0, HEIGHT),
    'brightness': random.randint(100, 255)
} for _ in range(STAR_COUNT)]

running = True
time = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Trail effect
    screen.blit(trail_surface, (0, 0))
    trail_surface.fill((0, 0, 0, 255))

    # Update and draw stars
    for star in stars:
        # Twinkle brightness
        star['brightness'] += random.uniform(-STAR_TWINKLE_SPEED, STAR_TWINKLE_SPEED)
        star['brightness'] = max(50, min(255, star['brightness']))
        brightness = int(star['brightness'])
        pygame.draw.circle(screen, (brightness, brightness, brightness), (star['x'], star['y']), 1)

    # Update and draw waves
    time += 1
    for row in wave_rows:
        row.update(time, mouse_x, mouse_y)
        for x, y in row.dots:
            # Calculate white gradient based on y position
            gradient_value = int((y / HEIGHT) * 255)
            color = (gradient_value, gradient_value, gradient_value)

            # Calculate pulse effect
            angle = x * FREQUENCY + row.phase
            pulse = abs(math.sin(angle)) * PULSE_AMPLITUDE
            current_radius = int(DOT_RADIUS + pulse)

            pygame.draw.circle(screen, color,
                               (int(x), int(y)), current_radius)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()