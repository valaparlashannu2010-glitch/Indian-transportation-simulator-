"""Player vehicle module - Creates and manages player-controlled vehicle"""
from engine.vehicles.vehicle import Vehicle, VehicleType
from engine.driving.advanced_driving_system import AdvancedDrivingSystem
from engine.physics.physics_engine import RigidBody, Vector2D


class PlayerVehicle(Vehicle):
    """Player-controlled vehicle with advanced driving system"""
    
    def __init__(self, vehicle_type: VehicleType, x: float, y: float):
        super().__init__(vehicle_type, x, y)
        self.driving_system = AdvancedDrivingSystem(vehicle_type.value)
        self.is_player_controlled = True
    
    def update(self, delta_time: float, driving_system: AdvancedDrivingSystem = None):
        """Update player vehicle with driving system"""
        if driving_system is None:
            driving_system = self.driving_system
        
        # Update engine
        driving_system.update_engine(delta_time)
        
        # Update braking
        driving_system.update_braking(delta_time)
        
        # Update steering
        driving_system.update_steering(delta_time)
        
        # Get throttle and apply force
        if driving_system.is_running:
            # Calculate force based on throttle, gear, and current speed
            max_force = self.stats.acceleration * 100
            throttle_force = driving_system.throttle_input * max_force
            
            # Apply brake force
            brake_force = -driving_system.brake_input * 50
            
            import math
            # Calculate direction based on steering
            current_direction = driving_system.steering.steering_angle
            driving_system.steering.steering_angle = max(-driving_system.steering.max_steering_angle, 
                                                          min(driving_system.steering.max_steering_angle, 
                                                              current_direction))
            
            # Apply force
            force_magnitude = throttle_force + brake_force
            force_x = math.cos(math.radians(driving_system.steering.steering_angle)) * force_magnitude
            force_y = math.sin(math.radians(driving_system.steering.steering_angle)) * force_magnitude
            
            self.body.apply_force(Vector2D(force_x, force_y))
        
        # Update physics
        self.body.update(delta_time)
        
        # Update sprite position
        self.sprite.x = self.body.position.x
        self.sprite.y = self.body.position.y
        
        # Update driving system velocity
        current_velocity = self.body.velocity.magnitude()
        new_velocity = driving_system.update_vehicle(delta_time, current_velocity)
        self.current_speed = new_velocity
    
    def render(self, screen):
        """Render player vehicle with indicators"""
        super().render(screen)
        
        # Draw indicator if vehicle is in player control
        if self.is_player_controlled:
            import pygame
            pygame.draw.circle(screen, (0, 255, 0), (int(self.sprite.x), int(self.sprite.y)), self.stats.size + 5, 2)
