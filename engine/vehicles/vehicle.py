"""Vehicle Module - Base class for all vehicles in the simulator"""
from enum import Enum
from dataclasses import dataclass
from engine.physics.physics_engine import RigidBody, Vector2D
from engine.rendering.renderer import CircleSprite, Color


class VehicleType(Enum):
    """Indian vehicle types"""
    AUTO_RICKSHAW = "auto"
    BUS = "bus"
    TRUCK = "truck"
    MOTORCYCLE = "motorcycle"
    CAR = "car"
    TATA_TEMPO = "tata_tempo"
    SCOOTER = "scooter"


@dataclass
class VehicleStats:
    """Vehicle statistics"""
    max_speed: float
    acceleration: float
    mass: float
    friction: float
    size: float
    color: tuple


class Vehicle:
    """Base vehicle class"""
    
    VEHICLE_TYPES = {
        VehicleType.AUTO_RICKSHAW: VehicleStats(
            max_speed=60.0, acceleration=5.0, mass=400, friction=0.15, size=15, color=Color.AUTO_YELLOW
        ),
        VehicleType.BUS: VehicleStats(
            max_speed=80.0, acceleration=3.0, mass=5000, friction=0.10, size=30, color=Color.BUS_RED
        ),
        VehicleType.TRUCK: VehicleStats(
            max_speed=70.0, acceleration=2.5, mass=8000, friction=0.12, size=35, color=Color.TRUCK_BROWN
        ),
        VehicleType.MOTORCYCLE: VehicleStats(
            max_speed=100.0, acceleration=7.0, mass=150, friction=0.20, size=10, color=Color.BIKE_BLACK
        ),
        VehicleType.CAR: VehicleStats(
            max_speed=120.0, acceleration=6.0, mass=1000, friction=0.14, size=18, color=(0, 0, 255)
        ),
    }
    
    def __init__(self, vehicle_type: VehicleType, x: float, y: float):
        self.vehicle_type = vehicle_type
        self.stats = self.VEHICLE_TYPES[vehicle_type]
        self.body = RigidBody(mass=self.stats.mass, friction=self.stats.friction)
        self.body.position = Vector2D(x, y)
        self.sprite = CircleSprite(x, y, self.stats.size, self.stats.color)
        self.current_speed = 0.0
        self.direction = 0.0  # Direction in degrees
        self.driver_input = {"acceleration": 0, "steering": 0, "braking": 0}
        
    def update(self, delta_time: float):
        """Update vehicle state"""
        # Apply driver input
        acceleration = self.driver_input["acceleration"] * self.stats.acceleration
        
        # Create force vector based on direction
        import math
        force_x = math.cos(math.radians(self.direction)) * acceleration
        force_y = math.sin(math.radians(self.direction)) * acceleration
        
        self.body.apply_force(Vector2D(force_x, force_y))
        
        # Update physics
        self.body.update(delta_time)
        
        # Update sprite position
        self.sprite.x = self.body.position.x
        self.sprite.y = self.body.position.y
        
        # Update speed
        self.current_speed = self.body.velocity.magnitude()
    
    def render(self, screen):
        """Render vehicle"""
        self.sprite.render(screen)
    
    def accelerate(self, amount: float = 1.0):
        """Accelerate the vehicle"""
        self.driver_input["acceleration"] = min(amount, 1.0)
    
    def brake(self, amount: float = 1.0):
        """Brake the vehicle"""
        self.driver_input["braking"] = min(amount, 1.0)
        self.body.velocity = self.body.velocity * 0.95  # Apply braking effect
    
    def steer(self, direction: float):
        """Steer the vehicle"""
        self.direction += direction
        self.driver_input["steering"] = direction
