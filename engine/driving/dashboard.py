"""Dashboard System - Real-time vehicle information display"""
import pygame
from engine.driving.advanced_driving_system import AdvancedDrivingSystem, EngineState


class DashboardDisplay:
    """Dashboard display system"""

    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        self.font_tiny = pygame.font.Font(None, 18)
        self.padding = 10

    def draw_speedometer(self, screen, driving_system: AdvancedDrivingSystem, x: int, y: int):
        """Draw speedometer gauge"""
        radius = 60
        max_speed = 200
        
        # Draw circle background
        pygame.draw.circle(screen, (50, 50, 50), (x, y), radius)
        pygame.draw.circle(screen, (100, 100, 100), (x, y), radius, 3)
        
        # Draw speed needle
        speed_angle = (driving_system.speed_kmh / max_speed) * 270 - 135
        import math
        needle_length = radius - 10
        end_x = x + needle_length * math.cos(math.radians(speed_angle))
        end_y = y + needle_length * math.sin(math.radians(speed_angle))
        pygame.draw.line(screen, (255, 0, 0), (x, y), (end_x, end_y), 3)
        
        # Draw center circle
        pygame.draw.circle(screen, (255, 0, 0), (x, y), 5)
        
        # Draw speed text
        speed_text = self.font_medium.render(f"{int(driving_system.speed_kmh)} km/h", True, (255, 255, 255))
        screen.blit(speed_text, (x - speed_text.get_width() // 2, y + radius + 10))

    def draw_rpm_gauge(self, screen, driving_system: AdvancedDrivingSystem, x: int, y: int):
        """Draw RPM gauge"""
        radius = 50
        max_rpm = driving_system.engine.max_rpm
        
        # Draw circle background
        pygame.draw.circle(screen, (50, 50, 50), (x, y), radius)
        pygame.draw.circle(screen, (100, 100, 100), (x, y), radius, 3)
        
        # Draw RPM needle
        rpm_angle = (driving_system.engine.rpm / max_rpm) * 270 - 135
        import math
        needle_length = radius - 10
        end_x = x + needle_length * math.cos(math.radians(rpm_angle))
        end_y = y + needle_length * math.sin(math.radians(rpm_angle))
        color = (255, 0, 0) if driving_system.engine.rpm > max_rpm * 0.8 else (255, 255, 255)
        pygame.draw.line(screen, color, (x, y), (end_x, end_y), 3)
        
        # Draw center circle
        pygame.draw.circle(screen, color, (x, y), 5)
        
        # Draw RPM text
        rpm_text = self.font_small.render(f"{int(driving_system.engine.rpm)} RPM", True, color)
        screen.blit(rpm_text, (x - rpm_text.get_width() // 2, y + radius + 5))

    def draw_fuel_gauge(self, screen, driving_system: AdvancedDrivingSystem, x: int, y: int, width: int = 100, height: int = 20):
        """Draw fuel gauge"""
        # Background
        pygame.draw.rect(screen, (50, 50, 50), (x, y, width, height))
        pygame.draw.rect(screen, (100, 100, 100), (x, y, width, height), 2)
        
        # Fuel level
        fuel_percentage = driving_system.fuel_level / 60.0  # Assuming 60L capacity
        fuel_width = width * max(0, min(1, fuel_percentage))
        
        # Color based on fuel level
        if fuel_percentage < 0.2:
            color = (255, 0, 0)  # Red - low fuel
        elif fuel_percentage < 0.5:
            color = (255, 165, 0)  # Orange - medium
        else:
            color = (0, 255, 0)  # Green - good
        
        pygame.draw.rect(screen, color, (x, y, fuel_width, height))
        
        # Fuel text
        fuel_text = self.font_small.render(f"Fuel: {driving_system.fuel_level:.1f}L", True, (255, 255, 255))
        screen.blit(fuel_text, (x, y - 25))

    def draw_temperature_gauge(self, screen, driving_system: AdvancedDrivingSystem, x: int, y: int, width: int = 100, height: int = 20):
        """Draw engine temperature gauge"""
        # Background
        pygame.draw.rect(screen, (50, 50, 50), (x, y, width, height))
        pygame.draw.rect(screen, (100, 100, 100), (x, y, width, height), 2)
        
        # Temperature level
        temp_percentage = driving_system.engine.temperature / driving_system.engine.max_temperature
        temp_width = width * max(0, min(1, temp_percentage))
        
        # Color based on temperature
        if temp_percentage < 0.5:
            color = (0, 100, 255)  # Blue - cool
        elif temp_percentage < 0.8:
            color = (255, 165, 0)  # Orange - warm
        else:
            color = (255, 0, 0)  # Red - hot
        
        pygame.draw.rect(screen, color, (x, y, temp_width, height))
        
        # Temperature text
        temp_text = self.font_small.render(f"Temp: {int(driving_system.engine.temperature)}°C", True, (255, 255, 255))
        screen.blit(temp_text, (x, y - 25))

    def draw_status_lights(self, screen, driving_system: AdvancedDrivingSystem, x: int, y: int):
        """Draw status indicator lights"""
        lights = []
        
        if driving_system.is_lights_on:
            lights.append(("Lights", (255, 255, 0)))
        if driving_system.is_fog_light_on:
            lights.append(("Fog", (255, 200, 0)))
        if driving_system.is_brake_light_on:
            lights.append(("Brake", (255, 0, 0)))
        if driving_system.is_reverse_light_on:
            lights.append(("Reverse", (255, 255, 255)))
        if driving_system.is_indicator_on:
            lights.append(("Indicator", (255, 165, 0)))
        if driving_system.is_handbrake_on:
            lights.append(("Handbrake", (255, 0, 0)))
        if driving_system.cruise_control_enabled:
            lights.append(("Cruise", (0, 255, 255)))
        if not driving_system.seatbelt_fastened:
            lights.append(("Seatbelt!", (255, 0, 0)))
        
        for i, (light_name, color) in enumerate(lights):
            light_text = self.font_tiny.render(light_name, True, color)
            screen.blit(light_text, (x + (i % 4) * 120, y + (i // 4) * 25))

    def draw_gear_display(self, screen, driving_system: AdvancedDrivingSystem, x: int, y: int):
        """Draw current gear display"""
        gear_map = {0: "N", 1: "D", -1: "R"}
        gear_char = gear_map.get(driving_system.transmission.current_gear, "N")
        
        # Draw gear box
        pygame.draw.rect(screen, (50, 50, 50), (x, y, 80, 80))
        pygame.draw.rect(screen, (100, 100, 100), (x, y, 80, 80), 3)
        
        # Draw gear letter
        gear_text = self.font_large.render(gear_char, True, (0, 255, 0))
        screen.blit(gear_text, (x + 40 - gear_text.get_width() // 2, y + 40 - gear_text.get_height() // 2))

    def draw_full_dashboard(self, screen, driving_system: AdvancedDrivingSystem):
        """Draw complete dashboard"""
        # Background
        dashboard_rect = pygame.Rect(0, self.screen_height - 200, self.screen_width, 200)
        pygame.draw.rect(screen, (30, 30, 30), dashboard_rect)
        pygame.draw.rect(screen, (100, 100, 100), dashboard_rect, 2)
        
        y_base = self.screen_height - 180
        x_offset = 20
        
        # Engine state and warning
        if driving_system.engine_state == EngineState.OFF:
            state_text = self.font_medium.render("ENGINE OFF", True, (255, 0, 0))
        elif driving_system.engine_state == EngineState.STARTING:
            state_text = self.font_medium.render("STARTING...", True, (255, 165, 0))
        else:
            state_text = self.font_medium.render("ENGINE RUNNING", True, (0, 255, 0))
        screen.blit(state_text, (x_offset, y_base))
        
        # Speedometer
        self.draw_speedometer(screen, driving_system, x_offset + 100, y_base + 60)
        
        # RPM Gauge
        self.draw_rpm_gauge(screen, driving_system, x_offset + 200, y_base + 60)
        
        # Gear display
        self.draw_gear_display(screen, driving_system, x_offset + 300, y_base + 20)
        
        # Fuel gauge
        self.draw_fuel_gauge(screen, driving_system, x_offset + 420, y_base + 50, 150, 20)
        
        # Temperature gauge
        self.draw_temperature_gauge(screen, driving_system, x_offset + 420, y_base + 100, 150, 20)
        
        # Status lights
        self.draw_status_lights(screen, driving_system, x_offset + 600, y_base + 20)

    def draw_hud(self, screen, driving_system: AdvancedDrivingSystem):
        """Draw heads-up display"""
        # Speed
        speed_hud = self.font_large.render(f"{int(driving_system.speed_kmh)} km/h", True, (0, 255, 0))
        screen.blit(speed_hud, (20, 20))
        
        # Fuel warning
        if driving_system.fuel_level < 10:
            fuel_warning = self.font_medium.render("⚠ LOW FUEL ⚠", True, (255, 0, 0))
            screen.blit(fuel_warning, (20, 80))
        
        # Temperature warning
        if driving_system.engine.temperature > 100:
            temp_warning = self.font_medium.render("⚠ ENGINE HOT ⚠", True, (255, 0, 0))
            screen.blit(temp_warning, (20, 120))
        
        # Seatbelt warning
        if not driving_system.seatbelt_fastened and driving_system.velocity > 5:
            seatbelt_warning = self.font_medium.render("⚠ FASTEN SEATBELT ⚠", True, (255, 165, 0))
            screen.blit(seatbelt_warning, (self.screen_width - 300, 20))
