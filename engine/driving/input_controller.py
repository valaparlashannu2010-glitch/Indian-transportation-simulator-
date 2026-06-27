"""Input Controller - Handles player input and vehicle control"""
import pygame
from engine.driving.advanced_driving_system import AdvancedDrivingSystem, GearState


class InputController:
    """Manages player input for vehicle control"""

    def __init__(self, driving_system: AdvancedDrivingSystem):
        self.driving_system = driving_system
        self.keys_pressed = set()
        self.indicator_blink_time = 0
        self.indicator_blink_interval = 0.5

    def handle_input(self, event, delta_time: float):
        """Handle input events"""
        if event.type == pygame.KEYDOWN:
            self.handle_key_press(event.key)
        elif event.type == pygame.KEYUP:
            self.handle_key_release(event.key)

    def handle_key_press(self, key: int):
        """Handle key press"""
        self.keys_pressed.add(key)
        
        # Engine controls
        if key == pygame.K_i:  # Start/Stop engine
            if self.driving_system.engine_state.value == "off":
                self.driving_system.start_engine()
            else:
                self.driving_system.stop_engine()
        
        # Gear controls
        elif key == pygame.K_p:  # Park
            self.driving_system.engage_gear(GearState.PARK)
        elif key == pygame.K_r:  # Reverse
            self.driving_system.engage_gear(GearState.REVERSE)
        elif key == pygame.K_n:  # Neutral
            self.driving_system.engage_gear(GearState.NEUTRAL)
        elif key == pygame.K_d:  # Drive
            self.driving_system.engage_gear(GearState.DRIVE)
        
        # Lights
        elif key == pygame.K_l:  # Toggle headlights
            self.driving_system.toggle_lights(0)
        elif key == pygame.K_f:  # Toggle fog lights
            self.driving_system.toggle_fog_lights()
        
        # Indicators
        elif key == pygame.K_LEFT:  # Left indicator
            self.driving_system.toggle_indicator(-1)
        elif key == pygame.K_RIGHT:  # Right indicator
            self.driving_system.toggle_indicator(1)
        
        # Wipers
        elif key == pygame.K_w:  # Toggle wipers
            self.driving_system.set_wiper_speed((self.driving_system.wiper_speed + 1) % 5)
        
        # AC
        elif key == pygame.K_a:  # Toggle AC
            self.driving_system.toggle_ac()
        elif key == pygame.K_UP:
            self.driving_system.set_ac_temperature(self.driving_system.ac_temperature + 1)
        elif key == pygame.K_DOWN:
            self.driving_system.set_ac_temperature(self.driving_system.ac_temperature - 1)
        
        # Handbrake
        elif key == pygame.K_h:  # Handbrake
            self.driving_system.toggle_handbrake()
        
        # Doors
        elif key == pygame.K_u:  # Unlock/Lock doors
            self.driving_system.lock_unlock_doors()
        
        # Seatbelt
        elif key == pygame.K_b:  # Fasten seatbelt
            self.driving_system.fastened_seatbelt()
        
        # Cruise control
        elif key == pygame.K_c:  # Cruise control
            self.driving_system.toggle_cruise_control()
        
        # Traction/Stability control
        elif key == pygame.K_t:  # Traction control
            self.driving_system.toggle_traction_control()
        elif key == pygame.K_s:  # Stability control
            self.driving_system.toggle_stability_control()

    def handle_key_release(self, key: int):
        """Handle key release"""
        self.keys_pressed.discard(key)

    def update_continuous_input(self, delta_time: float):
        """Update continuous input (held keys)"""
        # Throttle
        if pygame.K_UP in self.keys_pressed or pygame.K_w in self.keys_pressed:
            self.driving_system.throttle_input = min(1.0, self.driving_system.throttle_input + 0.05)
        else:
            self.driving_system.throttle_input = max(0.0, self.driving_system.throttle_input - 0.1)
        
        # Braking
        if pygame.K_DOWN in self.keys_pressed or pygame.K_s in self.keys_pressed:
            self.driving_system.brake_input = min(1.0, self.driving_system.brake_input + 0.05)
        else:
            self.driving_system.brake_input = max(0.0, self.driving_system.brake_input - 0.1)
        
        # Steering
        steering_input = 0.0
        if pygame.K_LEFT in self.keys_pressed:
            steering_input -= 1.0
        if pygame.K_RIGHT in self.keys_pressed:
            steering_input += 1.0
        self.driving_system.steering_input = steering_input
        
        # Clutch (for manual transmission)
        if pygame.K_LCTRL in self.keys_pressed or pygame.K_RCTRL in self.keys_pressed:
            self.driving_system.clutch_input = min(1.0, self.driving_system.clutch_input + 0.05)
        else:
            self.driving_system.clutch_input = max(0.0, self.driving_system.clutch_input - 0.1)
        
        # Update indicator blinking
        self.indicator_blink_time += delta_time

    def get_input_state(self) -> dict:
        """Get current input state"""
        return {
            "throttle": self.driving_system.throttle_input,
            "brake": self.driving_system.brake_input,
            "steering": self.driving_system.steering_input,
            "clutch": self.driving_system.clutch_input,
            "keys_pressed": list(self.keys_pressed)
        }
