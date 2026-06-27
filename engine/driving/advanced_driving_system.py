"""Advanced Driving System - Realistic vehicle control and switches"""
from enum import Enum
from dataclasses import dataclass
import math


class EngineState(Enum):
    """Engine states"""
    OFF = "off"
    STARTING = "starting"
    IDLE = "idle"
    RUNNING = "running"
    STALLING = "stalling"


class GearState(Enum):
    """Transmission gear states"""
    PARK = "P"
    REVERSE = "R"
    NEUTRAL = "N"
    DRIVE = "D"
    LOW = "L"


class SteeringMode(Enum):
    """Steering behavior modes"""
    MANUAL = "manual"
    ASSISTED = "assisted"
    AUTO = "auto"


@dataclass
class EngineStats:
    """Engine performance statistics"""
    rpm: float = 0.0
    max_rpm: float = 6000.0
    idle_rpm: float = 600.0
    torque: float = 0.0
    max_torque: float = 200.0
    fuel_consumption: float = 0.5  # L/100km
    temperature: float = 20.0  # Celsius
    max_temperature: float = 110.0


@dataclass
class TransmissionStats:
    """Transmission statistics"""
    current_gear: int = 0
    max_gears: int = 5
    gear_ratios: list = None
    clutch_engaged: bool = True
    transmission_fluid_temp: float = 20.0

    def __post_init__(self):
        if self.gear_ratios is None:
            # Standard gear ratios for a vehicle
            self.gear_ratios = [0, 3.5, 2.0, 1.3, 0.9, 0.7]


@dataclass
class BrakingSystem:
    """Braking system specifications"""
    brake_force: float = 0.0
    max_brake_force: float = 1.0
    abs_enabled: bool = True
    brake_temp: float = 20.0
    max_brake_temp: float = 800.0
    brake_fluid_pressure: float = 0.0
    brake_wear: float = 100.0  # Percentage


@dataclass
class SteeringSystem:
    """Steering system specifications"""
    steering_angle: float = 0.0
    max_steering_angle: float = 45.0  # Degrees
    steering_sensitivity: float = 1.0
    power_steering_enabled: bool = True
    steering_mode: SteeringMode = SteeringMode.ASSISTED
    wheel_alignment: float = 0.0  # Camber angle


class AdvancedDrivingSystem:
    """Complete driving system with realistic vehicle behavior"""

    def __init__(self, vehicle_type: str = "car"):
        self.vehicle_type = vehicle_type
        self.engine = EngineStats()
        self.transmission = TransmissionStats()
        self.braking = BrakingSystem()
        self.steering = SteeringSystem()
        
        # Control inputs
        self.throttle_input = 0.0  # 0-1
        self.brake_input = 0.0  # 0-1
        self.steering_input = 0.0  # -1 to 1
        self.clutch_input = 0.0  # 0-1
        
        # Vehicle state
        self.velocity = 0.0  # km/h
        self.speed_kmh = 0.0
        self.speed_mph = 0.0
        self.acceleration = 0.0
        self.fuel_level = 60.0  # Liters
        self.is_handbrake_on = False
        self.is_door_locked = True
        self.is_lights_on = False
        self.headlight_mode = 0  # 0=off, 1=parking, 2=dipped, 3=high
        self.is_fog_light_on = False
        self.is_reverse_light_on = False
        self.is_brake_light_on = False
        self.is_indicator_on = False
        self.indicator_direction = 0  # -1=left, 0=none, 1=right
        self.wiper_speed = 0  # 0=off, 1=low, 2=medium, 3=high
        self.ac_mode = 0  # 0=off, 1=low, 2=medium, 3=high
        self.ac_temperature = 22.0
        self.vehicle_temperature = 20.0
        
        # Safety systems
        self.seatbelt_fastened = False
        self.airbag_enabled = True
        self.traction_control_enabled = True
        self.stability_control_enabled = True
        self.cruise_control_enabled = False
        self.cruise_control_speed = 0.0
        
        # Odometer and trip meter
        self.odometer = 0.0  # km
        self.trip_meter = 0.0  # km
        self.trip_time = 0.0  # seconds
        
        # State tracking
        self.engine_state = EngineState.OFF
        self.is_running = False
        self.start_time = 0.0

    def start_engine(self) -> bool:
        """Start the engine (realistic startup)"""
        if self.engine_state == EngineState.OFF and self.fuel_level > 0:
            self.engine_state = EngineState.STARTING
            self.engine.rpm = 500.0
            self.start_time = 0.0
            return True
        return False

    def stop_engine(self) -> bool:
        """Stop the engine"""
        if self.engine_state != EngineState.OFF:
            self.engine_state = EngineState.OFF
            self.engine.rpm = 0.0
            self.is_running = False
            self.throttle_input = 0.0
            return True
        return False

    def engage_gear(self, gear: GearState) -> bool:
        """Engage a specific gear"""
        # Cannot engage gear if engine is off
        if self.engine_state == EngineState.OFF:
            return False
        
        # Require clutch disengagement or speed to be low
        if gear != GearState.PARK and self.velocity > 5:
            if self.clutch_input < 0.8:
                return False  # Clutch must be disengaged
        
        # Simple gear mapping
        gear_map = {
            GearState.PARK: 0,
            GearState.REVERSE: -1,
            GearState.NEUTRAL: 0,
            GearState.DRIVE: 1,
            GearState.LOW: 1
        }
        
        self.transmission.current_gear = gear_map[gear]
        return True

    def toggle_lights(self, mode: int) -> None:
        """Toggle headlights - 0=off, 1=parking, 2=dipped, 3=high beam"""
        self.headlight_mode = (self.headlight_mode + 1) % 4
        self.is_lights_on = self.headlight_mode > 0

    def toggle_fog_lights(self) -> None:
        """Toggle fog lights"""
        self.is_fog_light_on = not self.is_fog_light_on

    def toggle_indicator(self, direction: int) -> None:
        """Toggle turn indicator - -1=left, 0=none, 1=right"""
        if self.indicator_direction == direction:
            self.is_indicator_on = not self.is_indicator_on
        else:
            self.indicator_direction = direction
            self.is_indicator_on = True

    def toggle_handbrake(self) -> None:
        """Toggle handbrake"""
        if self.velocity < 1.0:  # Can only engage at very low speed
            self.is_handbrake_on = not self.is_handbrake_on

    def lock_unlock_doors(self) -> None:
        """Lock/unlock doors"""
        if self.engine_state == EngineState.OFF:
            self.is_door_locked = not self.is_door_locked

    def set_wiper_speed(self, speed: int) -> None:
        """Set wiper speed - 0=off, 1=low, 2=medium, 3=high, 4=intermittent"""
        self.wiper_speed = speed % 5

    def toggle_ac(self, mode: int = None) -> None:
        """Control air conditioning"""
        if mode is not None:
            self.ac_mode = mode
        else:
            self.ac_mode = (self.ac_mode + 1) % 4

    def set_ac_temperature(self, temp: float) -> None:
        """Set AC target temperature (16-32°C)"""
        self.ac_temperature = max(16.0, min(32.0, temp))

    def toggle_cruise_control(self) -> None:
        """Toggle cruise control"""
        if self.velocity > 40 and self.engine_state == EngineState.RUNNING:
            self.cruise_control_enabled = not self.cruise_control_enabled
            if self.cruise_control_enabled:
                self.cruise_control_speed = self.velocity

    def fastened_seatbelt(self) -> None:
        """Fasten/unfasten seatbelt"""
        self.seatbelt_fastened = not self.seatbelt_fastened

    def toggle_traction_control(self) -> None:
        """Toggle traction control"""
        self.traction_control_enabled = not self.traction_control_enabled

    def toggle_stability_control(self) -> None:
        """Toggle electronic stability control"""
        self.stability_control_enabled = not self.stability_control_enabled

    def update_engine(self, delta_time: float) -> None:
        """Update engine state and RPM"""
        if self.engine_state == EngineState.OFF:
            self.engine.rpm = 0.0
            return
        
        if self.engine_state == EngineState.STARTING:
            self.start_time += delta_time
            if self.start_time > 2.0:  # 2 seconds to start
                self.engine_state = EngineState.IDLE
                self.is_running = True
                self.engine.rpm = self.engine.idle_rpm
        
        elif self.engine_state == EngineState.IDLE:
            self.engine.rpm = self.engine.idle_rpm
            if self.throttle_input > 0:
                self.engine_state = EngineState.RUNNING
        
        elif self.engine_state == EngineState.RUNNING:
            # RPM based on throttle and gear
            target_rpm = self.engine.idle_rpm + (self.throttle_input * (self.engine.max_rpm - self.engine.idle_rpm))
            self.engine.rpm += (target_rpm - self.engine.rpm) * 0.1
            
            # Stall if RPM drops too low
            if self.engine.rpm < self.engine.idle_rpm * 0.5:
                self.engine_state = EngineState.STALLING
        
        elif self.engine_state == EngineState.STALLING:
            self.engine.rpm = 0.0
            self.engine_state = EngineState.OFF
        
        # Calculate torque
        rpm_ratio = self.engine.rpm / self.engine.max_rpm
        self.engine.torque = self.engine.max_torque * rpm_ratio * self.throttle_input
        
        # Engine temperature
        if self.is_running:
            self.engine.temperature += (self.engine.torque * 0.01 - 0.5) * delta_time
        else:
            self.engine.temperature -= 0.5 * delta_time
        self.engine.temperature = max(20.0, min(self.engine.max_temperature, self.engine.temperature))

    def update_braking(self, delta_time: float) -> None:
        """Update braking system"""
        self.braking.brake_force = self.brake_input
        
        # Brake temperature increases with use
        if self.brake_input > 0:
            self.braking.brake_temp += (self.brake_input * 10) * delta_time
        else:
            self.braking.brake_temp -= 2 * delta_time
        
        self.braking.brake_temp = max(20.0, min(self.braking.max_brake_temp, self.braking.brake_temp))
        
        # Brake wear increases with heavy braking
        if self.brake_input > 0.7:
            self.braking.brake_wear -= 0.001 * delta_time
        
        # Update brake light
        self.is_brake_light_on = self.brake_input > 0.1

    def update_steering(self, delta_time: float) -> None:
        """Update steering system"""
        # Apply steering input with sensitivity
        max_angle = self.steering.max_steering_angle
        target_angle = self.steering_input * max_angle * self.steering.steering_sensitivity
        
        # Smooth steering transition
        self.steering.steering_angle += (target_angle - self.steering.steering_angle) * 0.15

    def update_vehicle(self, delta_time: float, current_velocity: float) -> float:
        """Update vehicle dynamics"""
        self.velocity = current_velocity
        self.speed_kmh = self.velocity
        self.speed_mph = self.velocity * 0.621371
        
        # Update odometer and trip meter
        distance_traveled = (self.velocity / 3.6) * delta_time  # Convert km/h to m/s
        self.odometer += distance_traveled / 1000
        self.trip_meter += distance_traveled / 1000
        self.trip_time += delta_time
        
        # Fuel consumption
        fuel_consumption_rate = self.engine.fuel_consumption * (self.engine.rpm / self.engine.max_rpm)
        self.fuel_level -= (fuel_consumption_rate / 100) * delta_time
        self.fuel_level = max(0, self.fuel_level)
        
        # Stop engine if out of fuel
        if self.fuel_level <= 0 and self.is_running:
            self.stop_engine()
        
        # Update cabin temperature based on AC
        target_temp = self.ac_temperature if self.ac_mode > 0 else self.vehicle_temperature
        ac_efficiency = self.ac_mode * 0.25
        self.vehicle_temperature += (self.engine.temperature * 0.1 + target_temp * ac_efficiency - self.vehicle_temperature * 0.05) * delta_time
        
        # Calculate acceleration based on throttle and braking
        engine_force = (self.engine.torque / 100) * self.throttle_input if self.is_running else 0
        brake_force = -self.brake_input * self.braking.max_brake_force
        
        self.acceleration = (engine_force + brake_force) * 0.1
        
        # Handle cruise control
        if self.cruise_control_enabled and self.engine_state == EngineState.RUNNING:
            if self.velocity < self.cruise_control_speed - 1:
                self.throttle_input = 0.5
            elif self.velocity > self.cruise_control_speed + 1:
                self.throttle_input = 0.2
            else:
                self.throttle_input = 0.35
        
        # Update reverse light
        self.is_reverse_light_on = self.transmission.current_gear == -1
        
        return self.velocity + self.acceleration

    def get_dashboard_info(self) -> dict:
        """Get all dashboard information"""
        return {
            "engine_state": self.engine_state.value,
            "rpm": round(self.engine.rpm),
            "speed_kmh": round(self.speed_kmh),
            "speed_mph": round(self.speed_mph),
            "fuel_level": round(self.fuel_level, 1),
            "engine_temp": round(self.engine.temperature),
            "cabin_temp": round(self.vehicle_temperature),
            "gear": self.transmission.current_gear,
            "odometer": round(self.odometer, 1),
            "trip_meter": round(self.trip_meter, 1),
            "lights_on": self.is_lights_on,
            "fog_lights_on": self.is_fog_light_on,
            "indicators_on": self.is_indicator_on,
            "handbrake_on": self.is_handbrake_on,
            "doors_locked": self.is_door_locked,
            "seatbelt_fastened": self.seatbelt_fastened,
            "cruise_control_enabled": self.cruise_control_enabled,
            "brake_temp": round(self.braking.brake_temp),
            "brake_wear": round(self.braking.brake_wear, 1),
        }
