"""Weather System - Dynamic weather effects"""
from enum import Enum
import random
import math


class WeatherType(Enum):
    """Weather types"""
    CLEAR = "clear"
    CLOUDY = "cloudy"
    RAINY = "rainy"
    HEAVY_RAIN = "heavy_rain"
    FOGGY = "foggy"
    SNOWY = "snowy"
    STORMY = "stormy"


class WeatherSystem:
    """Dynamic weather system"""
    
    def __init__(self):
        self.current_weather = WeatherType.CLEAR
        self.weather_timer = 0.0
        self.weather_duration = 60.0  # Seconds
        self.transition_time = 5.0
        self.visibility = 1.0  # 0-1
        self.rain_intensity = 0.0  # 0-1
        self.wind_speed = 0.0  # km/h
        self.wind_direction = 0.0  # Degrees
        self.temperature = 25.0  # Celsius
        self.road_wetness = 0.0  # 0-1
        self.snow_depth = 0.0  # cm
        self.fog_density = 0.0  # 0-1
        
        # Weather particles
        self.rain_drops = []
        self.snow_flakes = []
        self.max_rain_drops = 500
        self.max_snow_flakes = 200
        
        # Weather effects
        self.tire_grip_modifier = 1.0
        self.brake_distance_modifier = 1.0
        self.visibility_modifier = 1.0
    
    def update_weather(self, delta_time: float) -> None:
        """Update weather system"""
        self.weather_timer += delta_time
        
        # Change weather randomly
        if self.weather_timer >= self.weather_duration:
            self.change_weather()
            self.weather_timer = 0.0
        
        # Update weather effects
        self.update_weather_effects(delta_time)
        self.update_particles(delta_time)
        self.update_road_conditions(delta_time)
    
    def change_weather(self) -> None:
        """Change to random weather"""
        weathers = list(WeatherType)
        self.current_weather = random.choice(weathers)
        self.weather_duration = random.uniform(30, 120)  # 30-120 seconds
    
    def update_weather_effects(self, delta_time: float) -> None:
        """Update weather effects on driving"""
        if self.current_weather == WeatherType.CLEAR:
            self.visibility = 1.0
            self.rain_intensity = 0.0
            self.fog_density = 0.0
            self.tire_grip_modifier = 1.0
            self.brake_distance_modifier = 1.0
        
        elif self.current_weather == WeatherType.CLOUDY:
            self.visibility = 0.95
            self.rain_intensity = 0.0
            self.fog_density = 0.1
            self.tire_grip_modifier = 0.98
            self.brake_distance_modifier = 1.02
        
        elif self.current_weather == WeatherType.RAINY:
            self.visibility = 0.85
            self.rain_intensity = 0.7
            self.fog_density = 0.2
            self.tire_grip_modifier = 0.75  # 25% grip reduction
            self.brake_distance_modifier = 1.35  # 35% longer braking
            self.road_wetness = min(1.0, self.road_wetness + 0.01 * delta_time)
        
        elif self.current_weather == WeatherType.HEAVY_RAIN:
            self.visibility = 0.65
            self.rain_intensity = 1.0
            self.fog_density = 0.4
            self.tire_grip_modifier = 0.60  # 40% grip reduction
            self.brake_distance_modifier = 1.60  # 60% longer braking
            self.road_wetness = min(1.0, self.road_wetness + 0.03 * delta_time)
        
        elif self.current_weather == WeatherType.FOGGY:
            self.visibility = 0.5
            self.rain_intensity = 0.1
            self.fog_density = 0.8
            self.tire_grip_modifier = 0.85
            self.brake_distance_modifier = 1.20
        
        elif self.current_weather == WeatherType.SNOWY:
            self.visibility = 0.7
            self.rain_intensity = 0.0
            self.fog_density = 0.3
            self.tire_grip_modifier = 0.50  # 50% grip reduction
            self.brake_distance_modifier = 1.80  # 80% longer braking
            self.snow_depth = min(20.0, self.snow_depth + 0.05 * delta_time)
            self.temperature = min(self.temperature - 0.1 * delta_time, -5.0)
        
        elif self.current_weather == WeatherType.STORMY:
            self.visibility = 0.40
            self.rain_intensity = 0.95
            self.fog_density = 0.6
            self.wind_speed = random.uniform(30, 60)  # 30-60 km/h winds
            self.tire_grip_modifier = 0.55
            self.brake_distance_modifier = 1.75
            self.road_wetness = 1.0
    
    def update_particles(self, delta_time: float) -> None:
        """Update weather particles (rain, snow)"""
        # Update rain drops
        if self.current_weather in [WeatherType.RAINY, WeatherType.HEAVY_RAIN, WeatherType.STORMY]:
            while len(self.rain_drops) < int(self.max_rain_drops * self.rain_intensity):
                self.rain_drops.append({
                    'x': random.uniform(0, 1280),
                    'y': random.uniform(-50, 0),
                    'speed': random.uniform(200, 400)
                })
            
            for drop in self.rain_drops:
                drop['y'] += drop['speed'] * delta_time
            
            self.rain_drops = [d for d in self.rain_drops if d['y'] < 720]
        else:
            self.rain_drops = []
        
        # Update snow flakes
        if self.current_weather == WeatherType.SNOWY:
            while len(self.snow_flakes) < int(self.max_snow_flakes):
                self.snow_flakes.append({
                    'x': random.uniform(0, 1280),
                    'y': random.uniform(-50, 0),
                    'speed': random.uniform(20, 50),
                    'sway': random.uniform(-50, 50)
                })
            
            for flake in self.snow_flakes:
                flake['y'] += flake['speed'] * delta_time
                flake['x'] += math.sin(flake['y'] * 0.01) * flake['sway'] * delta_time
            
            self.snow_flakes = [f for f in self.snow_flakes if f['y'] < 720]
        else:
            self.snow_flakes = []
    
    def update_road_conditions(self, delta_time: float) -> None:
        """Update road conditions (wetness, slipperiness)"""
        if self.current_weather not in [WeatherType.RAINY, WeatherType.HEAVY_RAIN, WeatherType.STORMY]:
            self.road_wetness = max(0.0, self.road_wetness - 0.01 * delta_time)
    
    def render_weather(self, screen) -> None:
        """Render weather effects"""
        import pygame
        
        # Draw fog overlay
        if self.fog_density > 0:
            fog_surface = pygame.Surface((1280, 720))
            fog_surface.set_alpha(int(self.fog_density * 150))
            fog_surface.fill((200, 200, 200))
            screen.blit(fog_surface, (0, 0))
        
        # Draw rain
        for drop in self.rain_drops:
            pygame.draw.line(screen, (150, 200, 255), 
                           (int(drop['x']), int(drop['y'])),
                           (int(drop['x']), int(drop['y']) + 10), 1)
        
        # Draw snow
        for flake in self.snow_flakes:
            pygame.draw.circle(screen, (255, 255, 255), 
                            (int(flake['x']), int(flake['y'])), 2)
    
    def get_weather_info(self) -> dict:
        """Get weather information"""
        return {
            'weather': self.current_weather.value,
            'visibility': round(self.visibility, 2),
            'rain_intensity': round(self.rain_intensity, 2),
            'wind_speed': round(self.wind_speed, 1),
            'temperature': round(self.temperature, 1),
            'tire_grip': round(self.tire_grip_modifier, 2),
            'brake_distance': round(self.brake_distance_modifier, 2)
        }
