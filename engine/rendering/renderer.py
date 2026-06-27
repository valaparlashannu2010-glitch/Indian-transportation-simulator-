"""Rendering Engine Module - Handles graphics and visualization"""
import pygame
from typing import List, Tuple


class Color:
    """Color palette for Indian transportation simulator"""
    # Indian colors
    SAFFRON = (255, 153, 0)
    WHITE = (255, 255, 255)
    GREEN = (19, 136, 8)
    NAVY_BLUE = (0, 25, 102)
    
    # Environment
    SKY_BLUE = (135, 206, 235)
    ROAD_GRAY = (64, 64, 64)
    GRASS_GREEN = (34, 139, 34)
    
    # Vehicles
    AUTO_YELLOW = (255, 200, 0)
    BUS_RED = (255, 0, 0)
    TRUCK_BROWN = (139, 69, 19)
    BIKE_BLACK = (30, 30, 30)


class Sprite:
    """Basic sprite class for rendering game objects"""
    
    def __init__(self, x: float, y: float, width: float, height: float, color: Tuple):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rotation = 0
        
    def render(self, screen):
        """Render sprite to screen"""
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.color, rect)


class CircleSprite(Sprite):
    """Circle sprite for vehicles"""
    
    def __init__(self, x: float, y: float, radius: float, color: Tuple):
        super().__init__(x, y, radius * 2, radius * 2, color)
        self.radius = radius
        
    def render(self, screen):
        """Render circle sprite to screen"""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.radius))


class Camera:
    """Camera for viewport control"""
    
    def __init__(self, width: float, height: float, world_width: float, world_height: float):
        self.width = width
        self.height = height
        self.world_width = world_width
        self.world_height = world_height
        self.x = 0
        self.y = 0
        self.target_x = 0
        self.target_y = 0
        
    def follow(self, target_x: float, target_y: float, smoothing: float = 0.1):
        """Follow a target with smoothing"""
        self.target_x = target_x - self.width / 2
        self.target_y = target_y - self.height / 2
        
        # Clamp to world bounds
        self.target_x = max(0, min(self.target_x, self.world_width - self.width))
        self.target_y = max(0, min(self.target_y, self.world_height - self.height))
        
        # Smooth camera movement
        self.x += (self.target_x - self.x) * smoothing
        self.y += (self.target_y - self.y) * smoothing
    
    def world_to_screen(self, world_x: float, world_y: float) -> Tuple[float, float]:
        """Convert world coordinates to screen coordinates"""
        screen_x = world_x - self.x
        screen_y = world_y - self.y
        return screen_x, screen_y


class Renderer:
    """Main renderer for the game"""
    
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.camera = Camera(screen_width, screen_height, 2560, 1440)
        self.sprites: List[Sprite] = []
        
    def add_sprite(self, sprite: Sprite):
        """Add sprite to renderer"""
        self.sprites.append(sprite)
    
    def render_road(self, screen):
        """Render road network"""
        # Horizontal roads
        pygame.draw.line(screen, Color.ROAD_GRAY, (0, 360), (self.screen_width, 360), 80)
        pygame.draw.line(screen, Color.WHITE, (0, 320), (self.screen_width, 320), 2)
        pygame.draw.line(screen, Color.WHITE, (0, 400), (self.screen_width, 400), 2)
        
        # Vertical roads
        pygame.draw.line(screen, Color.ROAD_GRAY, (640, 0), (640, self.screen_height), 80)
        pygame.draw.line(screen, Color.WHITE, (600, 0), (600, self.screen_height), 2)
        pygame.draw.line(screen, Color.WHITE, (680, 0), (680, self.screen_height), 2)
    
    def render(self, screen):
        """Render all sprites"""
        # Render background
        screen.fill(Color.SKY_BLUE)
        
        # Render road network
        self.render_road(screen)
        
        # Render sprites
        for sprite in self.sprites:
            sprite.render(screen)
