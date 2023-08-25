import pygame
import random
import math

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Autonomous Car Race Simulator")

car_size = 30
car_rect = pygame.Rect(width // 2 - car_size // 2, height - 50, car_size, car_size)
car_speed = 2
car_rotation = 0

indicator_color = (0, 255, 0)
indicator_size = 50
proximity_distance = 100
proximity_rect = pygame.Rect(width - indicator_size, height - indicator_size, indicator_size, indicator_size)

path_width = 5
path_start_y = height // 2 - path_width // 2
path_end_y = path_start_y + path_width
path_points = [(0, path_start_y), (width, path_start_y), (width, path_end_y), (0, path_end_y)]

obstacles = []
num_obstacles = 20
for _ in range(num_obstacles):
    obstacle_rect = pygame.Rect(random.randint(0, width - 30), random.randint(0, height - 30), 30, 30)
    obstacle_speed_x = random.choice([-1, 1]) * random.uniform(1, 3)
    obstacle_speed_y = random.choice([-1, 1]) * random.uniform(1, 3)
    obstacles.append((obstacle_rect, obstacle_speed_x, obstacle_speed_y))

running = True
clock = pygame.time.Clock()
object_distance = None
path_index = 0

def check_obstacle_collision(obstacle_rect, speed_x, speed_y):
    for other_obstacle_rect, _, _ in obstacles:
        if obstacle_rect.colliderect(other_obstacle_rect) and obstacle_rect != other_obstacle_rect:
            speed_x *= -1
            speed_y *= -1
            break
    return speed_x, speed_y

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    target_x, target_y = path_points[path_index]

    dx = target_x - car_rect.centerx
    dy = target_y - car_rect.centery
    target_rotation = math.degrees(math.atan2(-dy, dx))

    if car_rotation != target_rotation:
        if abs(car_rotation - target_rotation) < 2:
            car_rotation = target_rotation
        elif car_rotation < target_rotation:
            car_rotation += 2
        else:
            car_rotation -= 2

    car_rect.x += car_speed * math.cos(math.radians(car_rotation))
    car_rect.y -= car_speed * math.sin(math.radians(car_rotation))

    if car_rect.collidepoint(target_x, target_y):
        path_index = (path_index + 1) % len(path_points)

    car_rect.x = max(car_rect.x, 0)
    car_rect.y = max(car_rect.y, 0)
    car_rect.x = min(car_rect.x, width - car_size)
    car_rect.y = min(car_rect.y, height - car_size)

    screen.fill((255, 255, 255))

    pygame.draw.polygon(screen, (0, 0, 0), path_points)

    for obstacle_rect, obstacle_speed_x, obstacle_speed_y in obstacles:
        obstacle_rect.x += obstacle_speed_x
        obstacle_rect.y += obstacle_speed_y
        
        if obstacle_rect.left < 0 or obstacle_rect.right > width:
            obstacle_speed_x *= -1
        
        if obstacle_rect.top < 0 or obstacle_rect.bottom > height:
            obstacle_speed_y *= -1
        
        obstacle_rect.x = max(obstacle_rect.x, 0)
        obstacle_rect.y = max(obstacle_rect.y, 0)
        obstacle_rect.x = min(obstacle_rect.x, width - obstacle_rect.width)
        obstacle_rect.y = min(obstacle_rect.y, height - obstacle_rect.height)
        
        pygame.draw.circle(screen, (0, 0, 255), obstacle_rect.center, obstacle_rect.width // 2)

        obstacle_speed_x, obstacle_speed_y = check_obstacle_collision(obstacle_rect, obstacle_speed_x, obstacle_speed_y)

    pygame.draw.rect(screen, (255, 0, 0), car_rect)

    rotated_car = pygame.transform.rotate(pygame.Surface((car_size, car_size)), car_rotation)
    rotated_car_rect = rotated_car.get_rect(center=car_rect.center)
    screen.blit(rotated_car, rotated_car_rect)

    nearest_obstacle_rect, _, _ = min(obstacles, key=lambda o: math.sqrt((car_rect.centerx - o[0].centerx)**2 + (car_rect.centery - o[0].centery)**2))
    object_distance = math.sqrt((car_rect.centerx - nearest_obstacle_rect.centerx)**2 + (car_rect.centery - nearest_obstacle_rect.centery)**2)

    if object_distance < proximity_distance:
        pygame.draw.rect(screen, indicator_color, proximity_rect)
    else:
        pygame.draw.polygon(screen, indicator_color, [
            (width - indicator_size, height - indicator_size),
            (width - indicator_size, height),
            (width, height - indicator_size),
            (width, height)
        ])

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
