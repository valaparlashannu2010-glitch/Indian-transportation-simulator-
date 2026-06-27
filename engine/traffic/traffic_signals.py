"""Traffic Signals System - Traffic lights and road signs"""
from enum import Enum
from dataclasses import dataclass
import math


class TrafficLightState(Enum):
    """Traffic light states"""
    RED = "red"
    YELLOW = "yellow"
    GREEN = "green"


class SignType(Enum):
    """Road sign types"""
    STOP = "stop"
    SPEED_LIMIT = "speed_limit"
    YIELD = "yield"
    NO_ENTRY = "no_entry"
    ONE_WAY = "one_way"
    PARKING = "parking"
    NO_PARKING = "no_parking"
    PEDESTRIAN_CROSSING = "pedestrian_crossing"
    SCHOOL_ZONE = "school_zone"


@dataclass
class TrafficSignal:
    """Traffic signal/light object"""
    x: float
    y: float
    direction: str  # 'N', 'S', 'E', 'W' (which road it controls)
    state: TrafficLightState = TrafficLightState.RED
    cycle_time: float = 30.0  # Total cycle time in seconds
    red_duration: float = 15.0
    yellow_duration: float = 3.0
    green_duration: float = 12.0
    elapsed_time: float = 0.0
    
    def update(self, delta_time: float) -> None:
        """Update traffic light state"""
        self.elapsed_time += delta_time
        
        # Determine current state based on elapsed time
        if self.elapsed_time < self.red_duration:
            self.state = TrafficLightState.RED
        elif self.elapsed_time < self.red_duration + self.green_duration:
            self.state = TrafficLightState.GREEN
        elif self.elapsed_time < self.red_duration + self.green_duration + self.yellow_duration:
            self.state = TrafficLightState.YELLOW
        else:
            # Cycle complete, restart
            self.elapsed_time = 0.0
            self.state = TrafficLightState.RED
    
    def can_proceed(self) -> bool:
        """Check if vehicle can proceed through this light"""
        return self.state == TrafficLightState.GREEN
    
    def should_caution(self) -> bool:
        """Check if vehicle should be cautious (yellow light)"""
        return self.state == TrafficLightState.YELLOW


@dataclass
class RoadSign:
    """Road sign object"""
    x: float
    y: float
    sign_type: SignType
    data: dict = None  # Additional data (speed limit value, etc.)
    
    def get_instruction(self) -> str:
        """Get instruction from the sign"""
        instructions = {
            SignType.STOP: "Come to complete stop",
            SignType.SPEED_LIMIT: f"Speed limit {self.data.get('limit', 50)} km/h",
            SignType.YIELD: "Yield to other vehicles",
            SignType.NO_ENTRY: "Do not enter",
            SignType.ONE_WAY: "One way traffic only",
            SignType.PARKING: "Parking allowed",
            SignType.NO_PARKING: "No parking",
            SignType.PEDESTRIAN_CROSSING: "Pedestrian crossing ahead",
            SignType.SCHOOL_ZONE: "School zone - reduce speed"
        }
        return instructions.get(self.sign_type, "Unknown sign")


class TrafficSignalsManager:
    """Manages all traffic signals and signs on the map"""
    
    def __init__(self):
        self.traffic_lights: list = []
        self.road_signs: list = []
        self.setup_default_signals()
    
    def setup_default_signals(self) -> None:
        """Setup default traffic signals and signs"""
        # Create a 4-way intersection with traffic lights
        
        # Horizontal intersection
        self.traffic_lights.append(TrafficSignal(640, 300, 'N', TrafficLightState.RED))
        self.traffic_lights.append(TrafficSignal(640, 420, 'S', TrafficLightState.GREEN))
        
        # Vertical intersection
        self.traffic_lights.append(TrafficSignal(500, 360, 'W', TrafficLightState.GREEN))
        self.traffic_lights.append(TrafficSignal(780, 360, 'E', TrafficLightState.RED))
        
        # Add road signs
        # Speed limit signs
        self.road_signs.append(RoadSign(200, 200, SignType.SPEED_LIMIT, {'limit': 60}))
        self.road_signs.append(RoadSign(400, 400, SignType.SPEED_LIMIT, {'limit': 40}))
        
        # Stop signs
        self.road_signs.append(RoadSign(150, 150, SignType.STOP))
        self.road_signs.append(RoadSign(1100, 600, SignType.STOP))
        
        # School zone
        self.road_signs.append(RoadSign(300, 500, SignType.SCHOOL_ZONE))
        
        # Pedestrian crossings
        self.road_signs.append(RoadSign(640, 200, SignType.PEDESTRIAN_CROSSING))
        self.road_signs.append(RoadSign(640, 500, SignType.PEDESTRIAN_CROSSING))
    
    def update(self, delta_time: float) -> None:
        """Update all traffic signals"""
        for light in self.traffic_lights:
            light.update(delta_time)
    
    def add_traffic_light(self, signal: TrafficSignal) -> None:
        """Add a traffic light"""
        self.traffic_lights.append(signal)
    
    def add_road_sign(self, sign: RoadSign) -> None:
        """Add a road sign"""
        self.road_signs.append(sign)
    
    def get_nearest_traffic_light(self, x: float, y: float, max_distance: float = 100.0) -> TrafficSignal:
        """Get nearest traffic light within distance"""
        nearest = None
        nearest_distance = max_distance
        
        for light in self.traffic_lights:
            distance = math.sqrt((light.x - x)**2 + (light.y - y)**2)
            if distance < nearest_distance:
                nearest = light
                nearest_distance = distance
        
        return nearest
    
    def get_nearest_road_sign(self, x: float, y: float, max_distance: float = 150.0) -> RoadSign:
        """Get nearest road sign within distance"""
        nearest = None
        nearest_distance = max_distance
        
        for sign in self.road_signs:
            distance = math.sqrt((sign.x - x)**2 + (sign.y - y)**2)
            if distance < nearest_distance:
                nearest = sign
                nearest_distance = distance
        
        return nearest
    
    def render_traffic_signals(self, screen) -> None:
        """Render traffic lights on screen"""
        import pygame
        
        for light in self.traffic_lights:
            # Determine color
            if light.state == TrafficLightState.RED:
                color = (255, 0, 0)
            elif light.state == TrafficLightState.YELLOW:
                color = (255, 255, 0)
            else:  # GREEN
                color = (0, 255, 0)
            
            # Draw traffic light
            pygame.draw.circle(screen, color, (int(light.x), int(light.y)), 15)
            pygame.draw.circle(screen, (100, 100, 100), (int(light.x), int(light.y)), 15, 2)
    
    def render_road_signs(self, screen) -> None:
        """Render road signs on screen"""
        import pygame
        
        for sign in self.road_signs:
            if sign.sign_type == SignType.STOP:
                # Red octagon
                points = []
                for i in range(8):
                    angle = i * (2 * math.pi / 8)
                    px = sign.x + 15 * math.cos(angle)
                    py = sign.y + 15 * math.sin(angle)
                    points.append((px, py))
                pygame.draw.polygon(screen, (255, 0, 0), points)
                pygame.draw.polygon(screen, (255, 255, 255), points, 2)
            
            elif sign.sign_type == SignType.SPEED_LIMIT:
                # White circle with number
                pygame.draw.circle(screen, (255, 255, 255), (int(sign.x), int(sign.y)), 12)
                pygame.draw.circle(screen, (255, 0, 0), (int(sign.x), int(sign.y)), 12, 2)
            
            elif sign.sign_type == SignType.PEDESTRIAN_CROSSING:
                # Black and white stripes
                for i in range(3):
                    pygame.draw.line(screen, (0, 0, 0), 
                                   (sign.x - 10 + i*5, sign.y - 10),
                                   (sign.x - 10 + i*5, sign.y + 10), 2)
