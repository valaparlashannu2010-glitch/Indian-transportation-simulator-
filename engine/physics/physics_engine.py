"""Physics Engine Module - Handles vehicle dynamics and collisions"""
import numpy as np
from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class Vector2D:
    """2D Vector for physics calculations"""
    x: float = 0.0
    y: float = 0.0
    
    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)
    
    def __mul__(self, scalar):
        return Vector2D(self.x * scalar, self.y * scalar)
    
    def magnitude(self):
        return (self.x**2 + self.y**2)**0.5
    
    def normalize(self):
        mag = self.magnitude()
        if mag > 0:
            return Vector2D(self.x / mag, self.y / mag)
        return Vector2D(0, 0)


class RigidBody:
    """Rigid body for physics simulation"""
    
    def __init__(self, mass: float = 1.0, friction: float = 0.1):
        self.mass = mass
        self.friction = friction
        self.position = Vector2D(0, 0)
        self.velocity = Vector2D(0, 0)
        self.acceleration = Vector2D(0, 0)
        self.forces = Vector2D(0, 0)
        self.rotation = 0.0
        self.angular_velocity = 0.0
        
    def apply_force(self, force: Vector2D):
        """Apply force to the rigid body"""
        self.forces = self.forces + force
    
    def update(self, delta_time: float):
        """Update rigid body physics"""
        # F = ma => a = F/m
        self.acceleration = self.forces * (1.0 / self.mass)
        
        # Apply friction
        friction_force = self.velocity * (-self.friction)
        self.velocity = self.velocity + (friction_force + self.forces) * (delta_time / self.mass)
        
        # Update position
        self.position = self.position + self.velocity * delta_time
        
        # Reset forces
        self.forces = Vector2D(0, 0)


class Collider:
    """Collision detection and response"""
    
    @staticmethod
    def check_collision(body1: RigidBody, body2: RigidBody, radius1: float, radius2: float) -> bool:
        """Check if two circular bodies collide"""
        dx = body2.position.x - body1.position.x
        dy = body2.position.y - body1.position.y
        distance = (dx**2 + dy**2)**0.5
        return distance < (radius1 + radius2)
    
    @staticmethod
    def resolve_collision(body1: RigidBody, body2: RigidBody):
        """Resolve collision between two bodies"""
        # Simple elastic collision
        dx = body2.position.x - body1.position.x
        dy = body2.position.y - body1.position.y
        distance = (dx**2 + dy**2)**0.5
        
        if distance == 0:
            return
        
        # Normalize collision vector
        nx = dx / distance
        ny = dy / distance
        
        # Relative velocity
        dvx = body2.velocity.x - body1.velocity.x
        dvy = body2.velocity.y - body1.velocity.y
        
        # Relative velocity along collision normal
        dvn = dvx * nx + dvy * ny
        
        # Don't collide if moving apart
        if dvn >= 0:
            return
        
        # Impulse
        impulse = 2 * dvn / (body1.mass + body2.mass)
        
        # Apply impulse
        body1.velocity.x -= impulse * body2.mass * nx
        body1.velocity.y -= impulse * body2.mass * ny
        body2.velocity.x += impulse * body1.mass * nx
        body2.velocity.y += impulse * body1.mass * ny


class PhysicsEngine:
    """Main physics engine for the simulator"""
    
    def __init__(self, gravity: float = 9.8):
        self.gravity = gravity
        self.bodies: List[RigidBody] = []
        self.colliders: List[Tuple] = []
        
    def add_body(self, body: RigidBody):
        """Add a rigid body to the physics engine"""
        self.bodies.append(body)
    
    def update(self, delta_time: float):
        """Update physics simulation"""
        # Update all bodies
        for body in self.bodies:
            body.update(delta_time)
        
        # Check collisions
        for i in range(len(self.bodies)):
            for j in range(i + 1, len(self.bodies)):
                if self.check_collision(self.bodies[i], self.bodies[j]):
                    Collider.resolve_collision(self.bodies[i], self.bodies[j])
    
    def check_collision(self, body1: RigidBody, body2: RigidBody) -> bool:
        """Check if two bodies collide"""
        # Default radius for circular collision
        return Collider.check_collision(body1, body2, 0.5, 0.5)
