"""Traffic Manager Module - Manages traffic flow and AI behavior"""
from typing import List
import random
import math
from engine.vehicles.vehicle import Vehicle, VehicleType
from engine.physics.physics_engine import Vector2D


class TrafficManager:
    """Manages all traffic in the simulator"""
    
    def __init__(self, max_vehicles: int = 100):
        self.vehicles: List[Vehicle] = []
        self.max_vehicles = max_vehicles
        self.spawn_points = [
            (100, 360),
            (1280, 360),
            (640, 100),
            (640, 720)
        ]
        self.vehicle_count = 0
        
    def spawn_vehicle(self, vehicle_type: VehicleType = None, x: float = None, y: float = None) -> Vehicle:
        """Spawn a new vehicle"""
        if len(self.vehicles) >= self.max_vehicles:
            return None
        
        if vehicle_type is None:
            vehicle_type = random.choice(list(VehicleType))
        
        if x is None or y is None:
            spawn_point = random.choice(self.spawn_points)
            x, y = spawn_point
        
        vehicle = Vehicle(vehicle_type, x, y)
        self.vehicles.append(vehicle)
        self.vehicle_count += 1
        return vehicle
    
    def update(self, delta_time: float):
        """Update all vehicles and traffic behavior"""
        for vehicle in self.vehicles:
            # Simple AI: move forward with occasional steering changes
            if random.random() < 0.01:  # 1% chance per frame
                vehicle.steer(random.uniform(-5, 5))
            
            if random.random() < 0.02:  # 2% chance per frame
                if random.random() < 0.5:
                    vehicle.accelerate(random.uniform(0.5, 1.0))
                else:
                    vehicle.brake(random.uniform(0.2, 0.5))
            
            vehicle.update(delta_time)
        
        # Remove vehicles that went off-screen
        self.vehicles = [v for v in self.vehicles if -100 < v.body.position.x < 1380 and -100 < v.body.position.y < 820]
    
    def render(self, screen):
        """Render all vehicles"""
        for vehicle in self.vehicles:
            vehicle.render(screen)
    
    def get_vehicle_count(self) -> int:
        """Get current vehicle count"""
        return len(self.vehicles)
    
    def get_average_speed(self) -> float:
        """Calculate average speed of all vehicles"""
        if not self.vehicles:
            return 0.0
        total_speed = sum(v.current_speed for v in self.vehicles)
        return total_speed / len(self.vehicles)
