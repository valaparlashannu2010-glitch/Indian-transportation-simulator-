"""Main Game Application - Entry point for Indian Transportation Simulator"""
import sys
import os

# Add engine to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from engine.core.game_engine import GameEngine, EngineConfig
from engine.physics.physics_engine import PhysicsEngine
from engine.rendering.renderer import Renderer
from engine.traffic.traffic_manager import TrafficManager
import pygame


class IndianTransportationSimulator:
    """Main application class for the simulator"""
    
    def __init__(self):
        self.config = EngineConfig(
            screen_width=1280,
            screen_height=720,
            fps=60,
            debug_mode=True
        )
        self.engine = GameEngine(self.config)
        self.physics_engine = PhysicsEngine(gravity=9.8)
        self.renderer = Renderer(self.config.screen_width, self.config.screen_height)
        self.traffic_manager = TrafficManager(max_vehicles=50)
        self.running = False
        self.paused = False
        self.clock = None
        self.font = None
        
    def initialize(self):
        """Initialize the simulator"""
        pygame.init()
        self.engine.initialize()
        self.engine.physics_world = self.physics_engine
        self.engine.renderer = self.renderer
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.running = True
        print("✓ Indian Transportation Simulator Initialized")
        print(f"Resolution: {self.config.screen_width}x{self.config.screen_height}")
        print(f"FPS Target: {self.config.fps}")
        print(f"Debug Mode: {self.config.debug_mode}")
        
    def handle_input(self):
        """Handle user input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                    print(f"Simulation {'PAUSED' if self.paused else 'RESUMED'}")
                elif event.key == pygame.K_s:
                    self.spawn_vehicle()
                elif event.key == pygame.K_c:
                    self.traffic_manager.vehicles.clear()
                    print("All vehicles cleared")
                elif event.key == pygame.K_r:
                    print(f"Vehicles: {self.traffic_manager.get_vehicle_count()}")
                    print(f"Average Speed: {self.traffic_manager.get_average_speed():.2f} km/h")
    
    def spawn_vehicle(self):
        """Spawn a vehicle"""
        vehicle = self.traffic_manager.spawn_vehicle()
        if vehicle:
            print(f"Spawned {vehicle.vehicle_type.value}")
        else:
            print("Max vehicles reached!")
    
    def update(self, delta_time: float):
        """Update game state"""
        if not self.paused:
            # Update traffic
            self.traffic_manager.update(delta_time)
            
            # Update physics for all vehicles
            for vehicle in self.traffic_manager.vehicles:
                self.physics_engine.add_body(vehicle.body)
            
            # Update physics engine
            self.physics_engine.update(delta_time)
            
            # Spawn new vehicles occasionally
            if len(self.traffic_manager.vehicles) < 30:
                import random
                if random.random() < 0.02:  # 2% chance per frame
                    self.spawn_vehicle()
    
    def render(self, screen):
        """Render game state"""
        # Clear screen
        screen.fill((135, 206, 235))  # Sky blue
        
        # Render road
        self.renderer.render_road(screen)
        
        # Render traffic
        self.traffic_manager.render(screen)
        
        # Render UI
        self.render_ui(screen)
        
        # Update display
        pygame.display.flip()
    
    def render_ui(self, screen):
        """Render UI overlay"""
        ui_texts = [
            f"Vehicles: {self.traffic_manager.get_vehicle_count()}/50",
            f"Avg Speed: {self.traffic_manager.get_average_speed():.1f} km/h",
            f"FPS: {int(self.clock.get_fps())}",
            f"Status: {'PAUSED' if self.paused else 'RUNNING'}",
        ]
        
        if self.config.debug_mode:
            ui_texts.extend([
                "",
                "Controls:",
                "SPACE - Pause/Resume",
                "S - Spawn Vehicle",
                "C - Clear All Vehicles",
                "R - Show Stats",
                "ESC - Quit",
            ])
        
        y_offset = 10
        for text in ui_texts:
            if text:
                surface = self.font.render(text, True, (0, 0, 0))
                screen.blit(surface, (10, y_offset))
            y_offset += 25
    
    def run(self):
        """Main simulation loop"""
        self.initialize()
        
        print("\n" + "="*50)
        print("Indian Transportation Simulator")
        print("="*50)
        print("Press SPACE to pause/resume simulation")
        print("Press S to spawn a vehicle")
        print("Press C to clear all vehicles")
        print("Press R to show statistics")
        print("Press ESC to quit")
        print("="*50 + "\n")
        
        while self.running:
            delta_time = self.clock.tick(self.config.fps) / 1000.0
            
            self.handle_input()
            self.update(delta_time)
            self.render(self.engine.screen)
        
        self.shutdown()
    
    def shutdown(self):
        """Shutdown the simulator"""
        print("\nShutting down simulator...")
        print(f"Total vehicles spawned: {self.traffic_manager.vehicle_count}")
        pygame.quit()
        print("Goodbye! 👋")


if __name__ == "__main__":
    simulator = IndianTransportationSimulator()
    simulator.run()
