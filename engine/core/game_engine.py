"""Main Game Engine Module - Core system for Indian Transportation Simulator"""
import pygame
import numpy as np
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class EngineConfig:
    """Configuration for the game engine"""
    screen_width: int = 1280
    screen_height: int = 720
    fps: int = 60
    gravity: float = 9.8
    physics_timestep: float = 1/60.0
    debug_mode: bool = False


class GameEngine:
    """Core game engine for Indian transportation simulator"""
    
    def __init__(self, config: EngineConfig = None):
        self.config = config or EngineConfig()
        self.running = False
        self.clock = None
        self.screen = None
        self.entities: List = []
        self.physics_world = None
        self.renderer = None
        self.input_handler = None
        
    def initialize(self):
        """Initialize the game engine"""
        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.config.screen_width, self.config.screen_height)
        )
        pygame.display.set_caption("Indian Transportation Simulator")
        self.clock = pygame.time.Clock()
        self.running = True
        print("✓ Game Engine Initialized")
        
    def update(self, delta_time: float):
        """Update game state"""
        # Update physics
        if self.physics_world:
            self.physics_world.update(delta_time)
        
        # Update entities
        for entity in self.entities:
            if hasattr(entity, 'update'):
                entity.update(delta_time)
    
    def render(self):
        """Render game state"""
        self.screen.fill((135, 206, 235))  # Sky blue
        
        # Render entities
        for entity in self.entities:
            if hasattr(entity, 'render'):
                entity.render(self.screen)
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        self.initialize()
        
        while self.running:
            delta_time = self.clock.tick(self.config.fps) / 1000.0
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            # Update and render
            self.update(delta_time)
            self.render()
        
        pygame.quit()
    
    def add_entity(self, entity):
        """Add entity to the engine"""
        self.entities.append(entity)
    
    def remove_entity(self, entity):
        """Remove entity from the engine"""
        if entity in self.entities:
            self.entities.remove(entity)
