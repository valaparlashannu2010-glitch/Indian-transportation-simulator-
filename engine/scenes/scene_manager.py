"""Game Scene Manager - Manages different game scenes/modes"""
from enum import Enum
from engine.driving.advanced_driving_system import AdvancedDrivingSystem
from engine.driving.dashboard import DashboardDisplay
from engine.driving.input_controller import InputController


class GameScene(Enum):
    """Different game scenes"""
    MAIN_MENU = "main_menu"
    DRIVING = "driving"
    TRAFFIC_VIEW = "traffic_view"
    PAUSE_MENU = "pause_menu"
    SETTINGS = "settings"


class SceneManager:
    """Manages game scenes and transitions"""
    
    def __init__(self):
        self.current_scene = GameScene.MAIN_MENU
        self.previous_scene = None
        self.driving_system = None
        self.input_controller = None
        self.dashboard = None
    
    def switch_scene(self, new_scene: GameScene):
        """Switch to a new scene"""
        self.previous_scene = self.current_scene
        self.current_scene = new_scene
        print(f"Scene changed: {self.previous_scene.value} -> {new_scene.value}")
    
    def initialize_driving_scene(self, vehicle_type: str = "car"):
        """Initialize driving scene with a vehicle"""
        self.driving_system = AdvancedDrivingSystem(vehicle_type)
        self.input_controller = InputController(self.driving_system)
        self.current_scene = GameScene.DRIVING
    
    def get_current_scene(self) -> GameScene:
        """Get current game scene"""
        return self.current_scene
    
    def is_driving_scene(self) -> bool:
        """Check if currently in driving scene"""
        return self.current_scene == GameScene.DRIVING
    
    def is_traffic_view(self) -> bool:
        """Check if currently in traffic view"""
        return self.current_scene == GameScene.TRAFFIC_VIEW
