"""Updated Main Game Application - Integrated with Advanced Driving System"""
import sys
import os
import json

# Add engine to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from engine.core.game_engine import GameEngine, EngineConfig
from engine.physics.physics_engine import PhysicsEngine
from engine.rendering.renderer import Renderer
from engine.traffic.traffic_manager import TrafficManager
from engine.driving.advanced_driving_system import AdvancedDrivingSystem
from engine.driving.dashboard import DashboardDisplay
from engine.driving.input_controller import InputController
import pygame


class IndianTransportationSimulator:
    """Main application class for the simulator with advanced driving"""
    
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
        self.font_large = None
        self.font_medium = None
        
        # Driving system
        self.player_vehicle = None
        self.driving_system = None
        self.input_controller = None
        self.dashboard = None
        self.player_mode_enabled = False
        
    def load_config(self):
        """Load configuration from config.json"""
        try:
            with open('config.json', 'r') as f:
                config_data = json.load(f)
                return config_data
        except FileNotFoundError:
            print("⚠ config.json not found, using defaults")
            return {}
        
    def initialize(self):
        """Initialize the simulator"""
        pygame.init()
        self.engine.initialize()
        self.engine.physics_world = self.physics_engine
        self.engine.renderer = self.renderer
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_large = pygame.font.Font(None, 48)
        self.running = True
        
        # Initialize driving system
        self.driving_system = AdvancedDrivingSystem(vehicle_type="car")
        self.input_controller = InputController(self.driving_system)
        self.dashboard = DashboardDisplay(self.config.screen_width, self.config.screen_height)
        
        print("✓ Indian Transportation Simulator Initialized")
        print(f"Resolution: {self.config.screen_width}x{self.config.screen_height}")
        print(f"FPS Target: {self.config.fps}")
        print(f"Debug Mode: {self.config.debug_mode}")
        print("✓ Advanced Driving System Loaded")
        print(f"Vehicle Type: {self.driving_system.vehicle_type}")
        
    def handle_input(self):
        """Handle user input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.handle_key_press(event.key, event)
            elif event.type == pygame.KEYUP:
                self.handle_key_release(event.key)
    
    def handle_key_press(self, key: int, event):
        """Handle key press events"""
        if key == pygame.K_ESCAPE:
            self.running = False
        elif key == pygame.K_SPACE:
            self.paused = not self.paused
            print(f"Simulation {'PAUSED' if self.paused else 'RESUMED'}")
        elif key == pygame.K_TAB:
            self.player_mode_enabled = not self.player_mode_enabled
            print(f"Player Mode {'ENABLED' if self.player_mode_enabled else 'DISABLED'}")
            if self.player_mode_enabled:
                print("You are now controlling a vehicle!")
                print("Press I to start engine, W/S to accelerate/brake, Arrow keys to steer")
            else:
                self.driving_system.stop_engine()
        elif key == pygame.K_x:  # Spawn AI vehicle
            self.spawn_vehicle()
        elif key == pygame.K_c:  # Clear vehicles
            self.traffic_manager.vehicles.clear()
            print("All vehicles cleared")
        elif key == pygame.K_v:  # Show stats
            self.show_stats()
        # Pass event to input controller
        self.input_controller.handle_input(event, 0)
    
    def handle_key_release(self, key: int):
        """Handle key release"""
        self.input_controller.handle_key_release(key)
    
    def spawn_vehicle(self):
        """Spawn an AI vehicle"""
        vehicle = self.traffic_manager.spawn_vehicle()
        if vehicle:
            print(f"✓ Spawned {vehicle.vehicle_type.value}")
        else:
            print("Max vehicles reached!")
    
    def show_stats(self):
        """Show current statistics"""
        print("\n" + "="*50)
        print("VEHICLE STATISTICS")
        print("="*50)
        print(f"AI Vehicles: {self.traffic_manager.get_vehicle_count()}/50")
        print(f"Average Speed: {self.traffic_manager.get_average_speed():.2f} km/h")
        if self.player_mode_enabled:
            dashboard_info = self.driving_system.get_dashboard_info()
            print("\nPLAYER VEHICLE:")
            print(f"  Speed: {dashboard_info['speed_kmh']} km/h")
            print(f"  RPM: {dashboard_info['rpm']}")
            print(f"  Fuel: {dashboard_info['fuel_level']} L")
            print(f"  Engine Temp: {dashboard_info['engine_temp']}°C")
            print(f"  Odometer: {dashboard_info['odometer']} km")
        print("="*50 + "\n")
    
    def update(self, delta_time: float):
        """Update game state"""
        if not self.paused:
            # Update input for player vehicle
            if self.player_mode_enabled:
                self.input_controller.update_continuous_input(delta_time)
                
                # Update driving systems
                self.driving_system.update_engine(delta_time)
                self.driving_system.update_braking(delta_time)
                self.driving_system.update_steering(delta_time)
                
                # Update vehicle physics
                new_velocity = self.driving_system.update_vehicle(delta_time, self.driving_system.velocity)
                self.driving_system.velocity = new_velocity
            
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
        
        # Render player vehicle if in player mode
        if self.player_mode_enabled:
            # Draw player vehicle indicator
            player_text = self.font_medium.render("[PLAYER CONTROLLED]", True, (0, 255, 0))
            screen.blit(player_text, (self.config.screen_width // 2 - 100, 10))
        
        # Render UI
        self.render_ui(screen)
        
        # Render dashboard if player mode
        if self.player_mode_enabled:
            self.dashboard.draw_full_dashboard(screen, self.driving_system)
            self.dashboard.draw_hud(screen, self.driving_system)
        
        # Update display
        pygame.display.flip()
    
    def render_ui(self, screen):
        """Render UI overlay"""
        ui_texts = [
            f"AI Vehicles: {self.traffic_manager.get_vehicle_count()}/50",
            f"Avg Speed: {self.traffic_manager.get_average_speed():.1f} km/h",
            f"FPS: {int(self.clock.get_fps())}",
            f"Status: {'PAUSED' if self.paused else 'RUNNING'}",
            f"Player Mode: {'ON' if self.player_mode_enabled else 'OFF'}",
        ]
        
        if self.config.debug_mode:
            ui_texts.extend([
                "",
                "Controls:",
                "TAB - Toggle Player Mode",
                "SPACE - Pause/Resume",
                "X - Spawn Vehicle",
                "C - Clear Vehicles",
                "V - Show Stats",
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
        self.load_config()
        
        print("\n" + "="*60)
        print("  INDIAN TRANSPORTATION SIMULATOR - ADVANCED DRIVING")
        print("="*60)
        print("\nMAIN CONTROLS:")
        print("  TAB - Toggle Player Mode (Drive a vehicle)")
        print("  SPACE - Pause/Resume simulation")
        print("  X - Spawn AI vehicle")
        print("  C - Clear all vehicles")
        print("  V - Show statistics")
        print("  ESC - Quit\n")
        print("PLAYER MODE CONTROLS (when enabled with TAB):")
        print("  I - Start/Stop Engine")
        print("  W/UP - Accelerate        | S/DOWN - Brake")
        print("  LEFT/RIGHT - Steer      | H - Handbrake")
        print("  L - Headlights           | F - Fog Lights")
        print("  LEFT/RIGHT Arrow - Turn Indicators")
        print("  A - AC                   | W - Wipers")
        print("  U - Unlock Doors         | B - Seatbelt")
        print("  C - Cruise Control       | T - Traction Control")
        print("\n" + "="*60 + "\n")
        
        while self.running:
            delta_time = self.clock.tick(self.config.fps) / 1000.0
            
            self.handle_input()
            self.update(delta_time)
            self.render(self.engine.screen)
        
        self.shutdown()
    
    def shutdown(self):
        """Shutdown the simulator"""
        print("\nShutting down simulator...")
        print(f"Total AI vehicles spawned: {self.traffic_manager.vehicle_count}")
        if self.player_mode_enabled:
            dashboard_info = self.driving_system.get_dashboard_info()
            print(f"Player vehicle distance: {dashboard_info['odometer']} km")
        pygame.quit()
        print("Goodbye! 👋")


if __name__ == "__main__":
    simulator = IndianTransportationSimulator()
    simulator.run()
