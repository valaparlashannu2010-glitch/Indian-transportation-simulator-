"""Advanced Steering System - Realistic steering with tilt and lean mechanics"""
import math
from dataclasses import dataclass
from enum import Enum


class SteeringType(Enum):
    """Steering system types"""
    MANUAL = "manual"
    POWER_STEERING = "power_steering"
    HYDRAULIC = "hydraulic"
    ELECTRIC = "electric"


class SuspensionType(Enum):
    """Vehicle suspension types"""
    INDEPENDENT = "independent"
    DEPENDENT = "dependent"
    MULTI_LINK = "multi_link"
    AIR_SUSPENSION = "air_suspension"


@dataclass
class WheelData:
    """Individual wheel data"""
    position: str  # FL, FR, RL, RR
    grip: float = 1.0  # 0-1 grip coefficient
    temperature: float = 20.0
    wear: float = 100.0  # Percentage
    slip_angle: float = 0.0  # Degrees
    suspension_compression: float = 0.0  # 0-1
    brake_force: float = 0.0


class AdvancedSteeringSystem:
    """Advanced steering system with realistic mechanics"""
    
    def __init__(self, steering_type: SteeringType = SteeringType.POWER_STEERING,
                 suspension_type: SuspensionType = SuspensionType.MULTI_LINK):
        self.steering_type = steering_type
        self.suspension_type = suspension_type
        
        # Steering parameters
        self.steering_angle = 0.0  # Current steering angle
        self.steering_input = 0.0  # Raw input (-1 to 1)
        self.steering_sensitivity = 1.0
        self.steering_dead_zone = 0.05
        self.steering_response_time = 0.15  # Seconds to reach target
        self.max_steering_angle = 45.0  # Degrees
        self.steering_wheel_angle = 0.0  # Steering wheel rotation (540 degrees typical)
        
        # Power steering parameters
        self.power_steering_pressure = 0.0  # PSI (0-3000)
        self.power_steering_enabled = True
        self.power_steering_ratio = 1.0  # Steering reduction ratio
        
        # Vehicle tilt parameters
        self.roll_angle = 0.0  # Roll (left-right tilt) in degrees
        self.pitch_angle = 0.0  # Pitch (forward-backward tilt) in degrees
        self.yaw_angle = 0.0  # Yaw (rotation) in degrees
        self.max_roll_angle = 15.0  # Maximum lean angle
        self.max_pitch_angle = 8.0
        
        # Suspension parameters
        self.suspension_stiffness = 1.0
        self.suspension_damping = 0.8
        self.suspension_height = 1.0  # Normalized height
        self.center_of_gravity_height = 0.6  # Normalized height
        
        # Wheels
        self.wheels = {
            'FL': WheelData('FL'),
            'FR': WheelData('FR'),
            'RL': WheelData('RL'),
            'RR': WheelData('RR')
        }
        
        # Turn indicators
        self.left_indicator_active = False
        self.right_indicator_active = False
        self.hazard_lights_active = False
        self.indicator_blink_state = False
        self.indicator_blink_time = 0.0
        self.indicator_blink_frequency = 0.5  # Seconds per blink
        self.auto_cancel_distance = 50.0  # Meters
        self.distance_traveled_with_indicator = 0.0
        
        # Tire marks
        self.tire_marks = []
        self.max_tire_marks = 1000
        
        # Vehicle stability
        self.slip_ratio = 0.0
        self.lateral_acceleration = 0.0
        self.understeer_factor = 0.0
        self.oversteer_factor = 0.0
    
    def update_steering_input(self, raw_input: float, delta_time: float) -> None:
        """Update steering with realistic response"""
        # Apply dead zone
        if abs(raw_input) < self.steering_dead_zone:
            raw_input = 0.0
        
        self.steering_input = raw_input
        
        # Calculate target steering angle
        target_angle = raw_input * self.max_steering_angle * self.steering_sensitivity
        
        # Apply steering response time (smooth steering)
        steering_diff = target_angle - self.steering_angle
        max_change = (self.max_steering_angle * 2) * delta_time / self.steering_response_time
        
        if abs(steering_diff) > max_change:
            self.steering_angle += math.copysign(max_change, steering_diff)
        else:
            self.steering_angle = target_angle
        
        # Clamp steering angle
        self.steering_angle = max(-self.max_steering_angle, min(self.max_steering_angle, self.steering_angle))
        
        # Update steering wheel angle (540 degrees for typical steering wheel)
        self.steering_wheel_angle = (self.steering_angle / self.max_steering_angle) * 540.0
    
    def update_power_steering(self, vehicle_speed: float, delta_time: float) -> None:
        """Update power steering assistance based on speed"""
        if not self.power_steering_enabled:
            return
        
        # Power steering pressure increases with steering angle and decreases with speed
        base_pressure = abs(self.steering_angle) * 100
        speed_factor = max(0.5, 1.0 - (vehicle_speed / 200.0))  # Reduce at high speed
        
        target_pressure = base_pressure * speed_factor
        
        # Smooth pressure change
        self.power_steering_pressure += (target_pressure - self.power_steering_pressure) * 0.1
        self.power_steering_pressure = max(0, min(3000, self.power_steering_pressure))
    
    def update_vehicle_tilt(self, lateral_acceleration: float, longitudinal_acceleration: float, 
                           vehicle_speed: float, delta_time: float) -> None:
        """Update vehicle tilt (roll and pitch) based on acceleration"""
        # Calculate roll angle from lateral acceleration
        # Roll increases with lateral acceleration and decreases with speed (stability)
        max_lateral_g = 1.2
        normalized_lateral_accel = min(abs(lateral_acceleration) / max_lateral_g, 1.0)
        
        # Speed reduces tilting effect
        tilt_factor = max(0.3, 1.0 - (vehicle_speed / 300.0))
        
        target_roll = normalized_lateral_accel * self.max_roll_angle * tilt_factor
        if lateral_acceleration < 0:
            target_roll = -target_roll
        
        # Smooth roll transition
        self.roll_angle += (target_roll - self.roll_angle) * 0.15
        
        # Calculate pitch angle from longitudinal acceleration
        max_long_g = 0.8
        normalized_long_accel = min(abs(longitudinal_acceleration) / max_long_g, 1.0)
        
        target_pitch = normalized_long_accel * self.max_pitch_angle
        if longitudinal_acceleration < 0:  # Braking
            target_pitch = -target_pitch
        
        # Smooth pitch transition
        self.pitch_angle += (target_pitch - self.pitch_angle) * 0.15
    
    def update_suspension(self, delta_time: float, load: float = 1.0) -> None:
        """Update suspension compression based on vehicle load and tilt"""
        # Calculate suspension compression
        base_compression = load / 2.0
        tilt_effect = abs(self.roll_angle) / self.max_roll_angle * 0.3
        
        # Update each wheel compression
        if self.roll_angle > 0:  # Tilting right
            self.wheels['FR'].suspension_compression = base_compression + tilt_effect
            self.wheels['RR'].suspension_compression = base_compression + tilt_effect
            self.wheels['FL'].suspension_compression = base_compression - tilt_effect
            self.wheels['RL'].suspension_compression = base_compression - tilt_effect
        else:  # Tilting left
            self.wheels['FL'].suspension_compression = base_compression + abs(tilt_effect)
            self.wheels['RL'].suspension_compression = base_compression + abs(tilt_effect)
            self.wheels['FR'].suspension_compression = base_compression - abs(tilt_effect)
            self.wheels['RR'].suspension_compression = base_compression - abs(tilt_effect)
        
        # Clamp compression values
        for wheel in self.wheels.values():
            wheel.suspension_compression = max(0, min(1.0, wheel.suspension_compression))
    
    def update_wheel_grip(self, vehicle_speed: float, delta_time: float) -> None:
        """Update wheel grip based on speed and conditions"""
        # Grip decreases with speed
        speed_factor = max(0.6, 1.0 - (vehicle_speed / 250.0))
        
        # Grip also affected by tire wear
        for wheel in self.wheels.values():
            wear_factor = wheel.wear / 100.0
            wheel.grip = speed_factor * wear_factor
            
            # Temperature effects on grip
            if wheel.temperature < 40:
                wheel.grip *= 0.7  # Cold tires have less grip
            elif wheel.temperature > 100:
                wheel.grip *= 0.8  # Hot tires lose grip (tire degradation)
            
            # Update tire temperature
            if abs(self.steering_angle) > 10:
                wheel.temperature += 2.0 * delta_time
            else:
                wheel.temperature -= 0.5 * delta_time
            
            wheel.temperature = max(20, min(120, wheel.temperature))
    
    def update_indicators(self, delta_time: float, distance_delta: float) -> None:
        """Update turn indicators with blinking and auto-cancel"""
        # Update blink state
        self.indicator_blink_time += delta_time
        if self.indicator_blink_time >= self.indicator_blink_frequency:
            self.indicator_blink_state = not self.indicator_blink_state
            self.indicator_blink_time = 0.0
        
        # Track distance for auto-cancel
        self.distance_traveled_with_indicator += distance_delta
        
        # Auto-cancel indicators after turning
        if self.distance_traveled_with_indicator > self.auto_cancel_distance:
            if abs(self.steering_angle) < 5.0:  # Steering returned to center
                self.left_indicator_active = False
                self.right_indicator_active = False
                self.distance_traveled_with_indicator = 0.0
    
    def toggle_left_indicator(self) -> None:
        """Toggle left turn indicator"""
        if self.left_indicator_active:
            self.left_indicator_active = False
        else:
            self.left_indicator_active = True
            self.right_indicator_active = False  # Can't have both active
        self.distance_traveled_with_indicator = 0.0
    
    def toggle_right_indicator(self) -> None:
        """Toggle right turn indicator"""
        if self.right_indicator_active:
            self.right_indicator_active = False
        else:
            self.right_indicator_active = True
            self.left_indicator_active = False  # Can't have both active
        self.distance_traveled_with_indicator = 0.0
    
    def toggle_hazard_lights(self) -> None:
        """Toggle hazard lights (both indicators on)"""
        self.hazard_lights_active = not self.hazard_lights_active
        if self.hazard_lights_active:
            self.left_indicator_active = False
            self.right_indicator_active = False
    
    def add_tire_mark(self, x: float, y: float, intensity: float = 1.0) -> None:
        """Add tire mark at position"""
        if len(self.tire_marks) >= self.max_tire_marks:
            self.tire_marks.pop(0)  # Remove oldest mark
        
        self.tire_marks.append({
            'x': x,
            'y': y,
            'intensity': intensity,
            'age': 0.0
        })
    
    def update_tire_marks(self, delta_time: float) -> None:
        """Update tire marks (fade over time)"""
        for mark in self.tire_marks:
            mark['age'] += delta_time
            mark['intensity'] = max(0, 1.0 - mark['age'] / 5.0)  # Fade in 5 seconds
        
        # Remove faded marks
        self.tire_marks = [m for m in self.tire_marks if m['intensity'] > 0.01]
    
    def calculate_stability(self, vehicle_speed: float) -> dict:
        """Calculate vehicle stability metrics"""
        # Understeer: front tires lose grip first
        understeer_threshold = 0.15
        self.understeer_factor = max(0, self.steering_angle - understeer_threshold) / self.max_steering_angle
        
        # Oversteer: rear tires lose grip first
        oversteer_threshold = 0.25
        self.oversteer_factor = max(0, abs(self.yaw_angle) - oversteer_threshold) / 30.0
        
        # Calculate total stability (0-1, higher is more stable)
        stability = 1.0 - (self.understeer_factor * 0.5 + self.oversteer_factor * 0.5)
        stability = max(0, min(1.0, stability))
        
        return {
            'stability': stability,
            'understeer': self.understeer_factor,
            'oversteer': self.oversteer_factor,
            'grip_available': min([w.grip for w in self.wheels.values()]),
            'avg_tire_temp': sum([w.temperature for w in self.wheels.values()]) / 4
        }
    
    def get_steering_info(self) -> dict:
        """Get current steering system information"""
        return {
            'steering_angle': round(self.steering_angle, 2),
            'steering_wheel_angle': round(self.steering_wheel_angle, 2),
            'roll_angle': round(self.roll_angle, 2),
            'pitch_angle': round(self.pitch_angle, 2),
            'left_indicator': self.left_indicator_active and self.indicator_blink_state,
            'right_indicator': self.right_indicator_active and self.indicator_blink_state,
            'hazard_lights': self.hazard_lights_active and self.indicator_blink_state,
            'power_steering_pressure': round(self.power_steering_pressure, 0),
            'suspension_height': round(self.suspension_height, 2),
            'tire_marks_count': len(self.tire_marks)
        }
