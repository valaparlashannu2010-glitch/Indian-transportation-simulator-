"""Lane System - Multi-lane road system with lane detection"""
from enum import Enum
from dataclasses import dataclass
import math


class LaneType(Enum):
    """Types of lanes"""
    REGULAR = "regular"
    BUS_ONLY = "bus_only"
    BIKE_LANE = "bike_lane"
    PARKING = "parking"
    EMERGENCY = "emergency"
    CARPOOL = "carpool"


@dataclass
class Lane:
    """Individual lane on a road"""
    lane_id: int
    lane_type: LaneType
    x_start: float
    y_start: float
    x_end: float
    y_end: float
    width: float = 3.5  # Standard lane width in meters
    speed_limit: float = 60.0  # km/h
    direction: str = "forward"  # forward, backward
    left_boundary: str = "solid"  # solid, dashed, none
    right_boundary: str = "solid"
    
    def get_lane_center(self) -> tuple:
        """Get center of the lane"""
        return (
            (self.x_start + self.x_end) / 2,
            (self.y_start + self.y_end) / 2
        )
    
    def get_lane_length(self) -> float:
        """Get length of the lane"""
        return math.sqrt(
            (self.x_end - self.x_start)**2 + (self.y_end - self.y_start)**2
        )
    
    def is_position_in_lane(self, x: float, y: float, tolerance: float = 2.0) -> bool:
        """Check if position is within this lane"""
        # Simple check based on proximity to lane center
        center_x, center_y = self.get_lane_center()
        distance = math.sqrt((x - center_x)**2 + (y - center_y)**2)
        return distance < (self.width / 2) + tolerance


class RoadNetwork:
    """Network of roads and lanes"""
    
    def __init__(self):
        self.lanes: list = []
        self.intersections: list = []
        self.setup_default_road_network()
    
    def setup_default_road_network(self) -> None:
        """Setup default road network"""
        # Horizontal main road (North-South)
        self.lanes.append(Lane(
            lane_id=1,
            lane_type=LaneType.REGULAR,
            x_start=0, y_start=340,
            x_end=1280, y_end=340,
            width=3.5,
            speed_limit=60,
            direction="forward",
            left_boundary="solid",
            right_boundary="dashed"
        ))
        
        self.lanes.append(Lane(
            lane_id=2,
            lane_type=LaneType.REGULAR,
            x_start=0, y_start=380,
            x_end=1280, y_end=380,
            width=3.5,
            speed_limit=60,
            direction="backward",
            left_boundary="dashed",
            right_boundary="solid"
        ))
        
        # Vertical main road (East-West)
        self.lanes.append(Lane(
            lane_id=3,
            lane_type=LaneType.REGULAR,
            x_start=620, y_start=0,
            x_end=620, y_end=720,
            width=3.5,
            speed_limit=50,
            direction="forward"
        ))
        
        self.lanes.append(Lane(
            lane_id=4,
            lane_type=LaneType.REGULAR,
            x_start=660, y_start=0,
            x_end=660, y_end=720,
            width=3.5,
            speed_limit=50,
            direction="backward"
        ))
        
        # Bus-only lane
        self.lanes.append(Lane(
            lane_id=5,
            lane_type=LaneType.BUS_ONLY,
            x_start=0, y_start=360,
            x_end=1280, y_end=360,
            width=4.0,
            speed_limit=70,
            direction="forward",
            left_boundary="solid",
            right_boundary="solid"
        ))
        
        # Bike lane
        self.lanes.append(Lane(
            lane_id=6,
            lane_type=LaneType.BIKE_LANE,
            x_start=0, y_start=400,
            x_end=1280, y_end=400,
            width=2.0,
            speed_limit=25,
            left_boundary="dashed",
            right_boundary="dashed"
        ))
        
        # Emergency lane
        self.lanes.append(Lane(
            lane_id=7,
            lane_type=LaneType.EMERGENCY,
            x_start=0, y_start=320,
            x_end=1280, y_end=320,
            width=3.0,
            speed_limit=80,
            left_boundary="solid",
            right_boundary="none"
        ))
    
    def add_lane(self, lane: Lane) -> None:
        """Add a lane to the network"""
        self.lanes.append(lane)
    
    def find_lanes_near_position(self, x: float, y: float, search_distance: float = 50.0) -> list:
        """Find all lanes near a position"""
        nearby_lanes = []
        for lane in self.lanes:
            if lane.is_position_in_lane(x, y, search_distance):
                nearby_lanes.append(lane)
        return nearby_lanes
    
    def get_current_lane(self, x: float, y: float) -> Lane:
        """Get current lane for a position"""
        nearby_lanes = self.find_lanes_near_position(x, y, 5.0)
        if nearby_lanes:
            return nearby_lanes[0]
        return None
    
    def can_change_lane(self, vehicle_x: float, vehicle_y: float, 
                       target_lane_id: int, is_bus: bool = False) -> bool:
        """Check if vehicle can change to target lane"""
        current_lane = self.get_current_lane(vehicle_x, vehicle_y)
        target_lane = None
        
        for lane in self.lanes:
            if lane.lane_id == target_lane_id:
                target_lane = lane
                break
        
        if not target_lane:
            return False
        
        # Bus can only use bus-only lanes or regular lanes
        if is_bus and target_lane.lane_type == LaneType.BIKE_LANE:
            return False
        
        # Cars cannot use bus-only lanes
        if not is_bus and target_lane.lane_type == LaneType.BUS_ONLY:
            return False
        
        return True
    
    def render_lanes(self, screen) -> None:
        """Render all lanes on screen"""
        import pygame
        
        for lane in self.lanes:
            # Draw lane
            if lane.lane_type == LaneType.BUS_ONLY:
                lane_color = (255, 200, 0)  # Yellow
            elif lane.lane_type == LaneType.BIKE_LANE:
                lane_color = (100, 200, 100)  # Green
            elif lane.lane_type == LaneType.EMERGENCY:
                lane_color = (255, 0, 0)  # Red
            else:
                lane_color = (200, 200, 200)  # Gray
            
            # Draw lane background
            pygame.draw.line(
                screen,
                lane_color,
                (int(lane.x_start), int(lane.y_start)),
                (int(lane.x_end), int(lane.y_end)),
                int(lane.width)
            )
            
            # Draw lane markings
            if lane.left_boundary == "dashed":
                self.draw_dashed_line(screen, (255, 255, 255),
                                    (lane.x_start, lane.y_start - lane.width/2),
                                    (lane.x_end, lane.y_end - lane.width/2), 1)
            elif lane.left_boundary == "solid":
                pygame.draw.line(screen, (255, 255, 255),
                               (int(lane.x_start), int(lane.y_start - lane.width/2)),
                               (int(lane.x_end), int(lane.y_end - lane.width/2)), 2)
    
    @staticmethod
    def draw_dashed_line(screen, color, start_pos, end_pos, width, dash_length=10):
        """Draw a dashed line"""
        import pygame
        x1, y1 = start_pos
        x2, y2 = end_pos
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        
        if distance == 0:
            return
        
        num_dashes = int(distance / (dash_length * 2))
        for i in range(num_dashes):
            start = (
                x1 + (x2 - x1) * (i * dash_length * 2) / distance,
                y1 + (y2 - y1) * (i * dash_length * 2) / distance
            )
            end = (
                x1 + (x2 - x1) * (i * dash_length * 2 + dash_length) / distance,
                y1 + (y2 - y1) * (i * dash_length * 2 + dash_length) / distance
            )
            pygame.draw.line(screen, color, start, end, width)
