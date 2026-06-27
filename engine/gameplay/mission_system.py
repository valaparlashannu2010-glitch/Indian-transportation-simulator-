"""Mission System - Objectives and challenges"""
from enum import Enum
from dataclasses import dataclass
from datetime import datetime, timedelta


class MissionType(Enum):
    """Mission types"""
    DELIVERY = "delivery"
    PASSENGER_PICKUP = "passenger_pickup"
    RACING = "racing"
    SIGHTSEEING = "sightseeing"
    PARKING = "parking"
    SAFETY = "safety"


class MissionStatus(Enum):
    """Mission status"""
    AVAILABLE = "available"
    ACCEPTED = "accepted"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Mission:
    """Mission object"""
    mission_id: str
    mission_type: MissionType
    title: str
    description: str
    start_location: tuple  # (x, y)
    end_location: tuple
    time_limit: float  # Seconds
    reward: float  # Currency reward
    difficulty: str  # easy, medium, hard
    status: MissionStatus = MissionStatus.AVAILABLE
    progress: float = 0.0  # 0-100%
    start_time: float = None
    completion_time: float = None
    bonus_criteria: list = None  # Additional objectives for bonus
    
    def __post_init__(self):
        if self.bonus_criteria is None:
            self.bonus_criteria = []


class MissionSystem:
    """Mission management system"""
    
    def __init__(self):
        self.missions = {}
        self.active_mission = None
        self.completed_missions = []
        self.total_earnings = 0.0
        self.current_mission_progress = 0.0
        self.setup_default_missions()
    
    def setup_default_missions(self) -> None:
        """Setup default missions"""
        # Delivery mission
        self.add_mission(Mission(
            mission_id="delivery_01",
            mission_type=MissionType.DELIVERY,
            title="Quick Delivery",
            description="Deliver package to the market (10km)",
            start_location=(640, 360),
            end_location=(100, 100),
            time_limit=600,  # 10 minutes
            reward=500.0,
            difficulty="easy",
            bonus_criteria=["Complete within 5 minutes", "No speeding violations"]
        ))
        
        # Passenger pickup
        self.add_mission(Mission(
            mission_id="passenger_01",
            mission_type=MissionType.PASSENGER_PICKUP,
            title="Passenger Service",
            description="Pick up 4 passengers and reach destination",
            start_location=(640, 360),
            end_location=(1100, 600),
            time_limit=900,  # 15 minutes
            reward=750.0,
            difficulty="medium"
        ))
        
        # Racing mission
        self.add_mission(Mission(
            mission_id="racing_01",
            mission_type=MissionType.RACING,
            title="Road Race",
            description="Complete the circuit in under 3 minutes",
            start_location=(640, 360),
            end_location=(640, 360),  # Circular route
            time_limit=180,
            reward=1000.0,
            difficulty="hard",
            bonus_criteria=["Maintain average speed above 80 km/h", "No collisions"]
        ))
        
        # Parking mission
        self.add_mission(Mission(
            mission_id="parking_01",
            mission_type=MissionType.PARKING,
            title="Parking Challenge",
            description="Park the vehicle in the marked spot without damage",
            start_location=(640, 360),
            end_location=(500, 300),
            time_limit=120,
            reward=300.0,
            difficulty="easy"
        ))
    
    def add_mission(self, mission: Mission) -> None:
        """Add a mission"""
        self.missions[mission.mission_id] = mission
    
    def accept_mission(self, mission_id: str) -> bool:
        """Accept a mission"""
        if mission_id not in self.missions:
            return False
        
        mission = self.missions[mission_id]
        if mission.status != MissionStatus.AVAILABLE:
            return False
        
        mission.status = MissionStatus.IN_PROGRESS
        mission.start_time = 0.0
        self.active_mission = mission
        print(f"\u2714 Mission accepted: {mission.title}")
        return True
    
    def update_mission_progress(self, delta_time: float, player_x: float, player_y: float) -> None:
        """Update mission progress"""
        if not self.active_mission:
            return
        
        mission = self.active_mission
        mission.start_time += delta_time
        
        # Calculate distance to end location
        dx = mission.end_location[0] - player_x
        dy = mission.end_location[1] - player_y
        distance = (dx**2 + dy**2)**0.5
        
        # Update progress based on distance
        max_distance = ((mission.start_location[0] - mission.end_location[0])**2 + 
                       (mission.start_location[1] - mission.end_location[1])**2)**0.5
        
        mission.progress = max(0, 100 * (1 - distance / max_distance))
        self.current_mission_progress = mission.progress
        
        # Check mission completion
        if distance < 50:  # Within 50 pixels of destination
            self.complete_mission(mission_id=mission.mission_id)
        
        # Check time limit
        if mission.start_time > mission.time_limit:
            self.fail_mission(mission_id=mission.mission_id)
    
    def complete_mission(self, mission_id: str) -> None:
        """Complete a mission"""
        if mission_id not in self.missions:
            return
        
        mission = self.missions[mission_id]
        mission.status = MissionStatus.COMPLETED
        mission.completion_time = mission.start_time
        
        # Calculate reward based on difficulty and time
        time_bonus = max(0, (mission.time_limit - mission.completion_time) / mission.time_limit) * mission.reward * 0.5
        total_reward = mission.reward + time_bonus
        
        self.total_earnings += total_reward
        self.completed_missions.append(mission)
        self.active_mission = None
        
        print(f"\u2705 Mission Completed: {mission.title}")
        print(f"Reward: ${total_reward:.2f}")
    
    def fail_mission(self, mission_id: str, reason: str = "Time limit exceeded") -> None:
        """Fail a mission"""
        if mission_id not in self.missions:
            return
        
        mission = self.missions[mission_id]
        mission.status = MissionStatus.FAILED
        self.active_mission = None
        
        print(f"\u274c Mission Failed: {mission.title}")
        print(f"Reason: {reason}")
    
    def get_available_missions(self) -> list:
        """Get list of available missions"""
        return [m for m in self.missions.values() if m.status == MissionStatus.AVAILABLE]
    
    def get_mission_info(self) -> dict:
        """Get active mission information"""
        if not self.active_mission:
            return {'active': False}
        
        mission = self.active_mission
        return {
            'active': True,
            'title': mission.title,
            'type': mission.mission_type.value,
            'progress': round(mission.progress, 1),
            'time_remaining': round(mission.time_limit - mission.start_time, 1),
            'reward': mission.reward,
            'difficulty': mission.difficulty
        }
