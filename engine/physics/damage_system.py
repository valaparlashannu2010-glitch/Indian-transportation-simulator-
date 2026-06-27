"""Collision and Damage System - Vehicle damage physics"""
from enum import Enum
from dataclasses import dataclass
import math


class DamageType(Enum):
    """Types of damage"""
    COLLISION = "collision"
    SCRATCH = "scratch"
    DENT = "dent"
    BROKEN_WINDOW = "broken_window"
    TIRE_DAMAGE = "tire_damage"
    ENGINE_DAMAGE = "engine_damage"


@dataclass
class VehicleDamage:
    """Vehicle damage status"""
    front_bumper: float = 100.0  # 0-100 health
    rear_bumper: float = 100.0
    left_side: float = 100.0
    right_side: float = 100.0
    roof: float = 100.0
    engine: float = 100.0
    transmission: float = 100.0
    suspension: float = 100.0
    tires: list = None  # List of 4 tire healths
    windows: list = None  # List of window healths
    
    def __post_init__(self):
        if self.tires is None:
            self.tires = [100.0, 100.0, 100.0, 100.0]  # FL, FR, RL, RR
        if self.windows is None:
            self.windows = [100.0, 100.0, 100.0, 100.0]  # Front, Rear, Left, Right
    
    def get_total_damage(self) -> float:
        """Calculate total damage percentage"""
        parts = [
            self.front_bumper, self.rear_bumper,
            self.left_side, self.right_side, self.roof,
            self.engine, self.transmission, self.suspension
        ] + self.tires + self.windows
        
        avg_health = sum(parts) / len(parts)
        return 100.0 - avg_health
    
    def is_undriveable(self) -> bool:
        """Check if vehicle is undriveable"""
        return (self.engine < 20 or 
                self.transmission < 20 or 
                sum(self.tires) / 4 < 10)


class DamageSystem:
    """Vehicle damage system"""
    
    def __init__(self, vehicle_mass: float = 1000.0):
        self.damage = VehicleDamage()
        self.vehicle_mass = vehicle_mass
        self.collision_history = []
        self.smoke_particles = []
        self.fire_particles = []
        self.is_on_fire = False
        self.fire_intensity = 0.0
    
    def apply_collision_damage(self, impact_velocity: float, impact_direction: str) -> None:
        """Apply damage from collision"""
        # Impact force based on velocity and mass
        impact_force = (impact_velocity ** 2) * (self.vehicle_mass / 1000.0) / 100
        
        # Apply damage to specific parts based on direction
        if impact_direction == "front":
            self.damage.front_bumper -= impact_force * 0.5
            self.damage.engine -= impact_force * 0.3
        elif impact_direction == "rear":
            self.damage.rear_bumper -= impact_force * 0.5
            self.damage.transmission -= impact_force * 0.2
        elif impact_direction == "left":
            self.damage.left_side -= impact_force * 0.4
            self.damage.windows[2] -= impact_force * 0.2
        elif impact_direction == "right":
            self.damage.right_side -= impact_force * 0.4
            self.damage.windows[3] -= impact_force * 0.2
        
        # General damage to suspension and tires
        self.damage.suspension -= impact_force * 0.2
        for i in range(len(self.damage.tires)):
            self.damage.tires[i] -= impact_force * 0.15
        
        # Clamp all values to 0-100
        self._clamp_damage()
        
        # Record collision
        self.collision_history.append({
            'type': impact_direction,
            'force': impact_force,
            'damage': self.damage.get_total_damage()
        })
    
    def apply_tire_damage(self, tire_index: int, damage_amount: float) -> None:
        """Apply specific tire damage"""
        self.damage.tires[tire_index] -= damage_amount
        self.damage.tires[tire_index] = max(0, self.damage.tires[tire_index])
    
    def apply_engine_damage(self, damage_amount: float) -> None:
        """Apply engine damage"""
        self.damage.engine -= damage_amount
        self.damage.engine = max(0, self.damage.engine)
        
        # Engine damage can cause fire
        if self.damage.engine < 30:
            self.is_on_fire = True
            self.fire_intensity = (100 - self.damage.engine) / 100.0
    
    def _clamp_damage(self) -> None:
        """Clamp all damage values to 0-100"""
        self.damage.front_bumper = max(0, min(100, self.damage.front_bumper))
        self.damage.rear_bumper = max(0, min(100, self.damage.rear_bumper))
        self.damage.left_side = max(0, min(100, self.damage.left_side))
        self.damage.right_side = max(0, min(100, self.damage.right_side))
        self.damage.roof = max(0, min(100, self.damage.roof))
        self.damage.engine = max(0, min(100, self.damage.engine))
        self.damage.transmission = max(0, min(100, self.damage.transmission))
        self.damage.suspension = max(0, min(100, self.damage.suspension))
        
        for i in range(len(self.damage.tires)):
            self.damage.tires[i] = max(0, min(100, self.damage.tires[i]))
        
        for i in range(len(self.damage.windows)):
            self.damage.windows[i] = max(0, min(100, self.damage.windows[i]))
    
    def get_performance_modifier(self) -> dict:
        """Get performance modifiers based on damage"""
        engine_health = self.damage.engine / 100.0
        tire_health = sum(self.damage.tires) / 400.0
        
        return {
            'acceleration_modifier': engine_health * 0.8 + 0.2,
            'max_speed_modifier': engine_health * 0.7 + 0.3,
            'brake_distance_modifier': 1.0 + ((100 - tire_health * 100) / 100.0),
            'steering_precision': tire_health * 0.9 + 0.1
        }
    
    def render_damage_indicators(self, screen, vehicle_x: float, vehicle_y: float) -> None:
        """Render visual damage indicators"""
        import pygame
        
        # Smoke particles
        if self.damage.engine < 50:
            self._update_smoke()
            for particle in self.smoke_particles:
                alpha = int(particle['intensity'] * 100)
                color = (100, 100, 100)
                pygame.draw.circle(screen, color, 
                                 (int(particle['x']), int(particle['y'])), 
                                 int(particle['size']))
        
        # Fire particles
        if self.is_on_fire:
            self._update_fire()
            for particle in self.fire_particles:
                color = (255, int(255 * (1 - particle['intensity'])), 0)
                pygame.draw.circle(screen, color,
                                 (int(particle['x']), int(particle['y'])),
                                 int(particle['size']))
    
    def _update_smoke(self) -> None:
        """Update smoke particles"""
        if len(self.smoke_particles) < 20:
            self.smoke_particles.append({
                'x': 640,
                'y': 360,
                'vx': 0,
                'vy': -50,
                'size': 5,
                'intensity': 1.0
            })
        
        for particle in self.smoke_particles:
            particle['y'] += particle['vy'] * 0.016
            particle['intensity'] -= 0.02
        
        self.smoke_particles = [p for p in self.smoke_particles if p['intensity'] > 0]
    
    def _update_fire(self) -> None:
        """Update fire particles"""
        if len(self.fire_particles) < 30:
            import random
            self.fire_particles.append({
                'x': 640 + random.uniform(-10, 10),
                'y': 360 + random.uniform(-10, 10),
                'size': random.uniform(3, 8),
                'intensity': 1.0,
                'life': 0.5
            })
        
        for particle in self.fire_particles:
            particle['intensity'] -= 0.05
            particle['life'] -= 0.016
        
        self.fire_particles = [p for p in self.fire_particles if p['life'] > 0]
    
    def get_damage_info(self) -> dict:
        """Get damage information"""
        return {
            'total_damage': round(self.damage.get_total_damage(), 1),
            'front_bumper': round(self.damage.front_bumper, 1),
            'engine': round(self.damage.engine, 1),
            'tires': [round(t, 1) for t in self.damage.tires],
            'is_undriveable': self.damage.is_undriveable(),
            'on_fire': self.is_on_fire
        }
