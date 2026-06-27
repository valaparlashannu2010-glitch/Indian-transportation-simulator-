"""APSRTC Bus Models - Authentic Andhra Pradesh State Road Transport Corporation buses"""
from enum import Enum
from dataclasses import dataclass
from engine.vehicles.vehicle import Vehicle, VehicleType, VehicleStats
from engine.rendering.renderer import Color


class APSRTCBusType(Enum):
    """APSRTC bus types"""
    REGULAR_AC = "regular_ac"
    VOLVO_AC = "volvo_ac"
    LOW_FLOOR = "low_floor"
    SUPER_LUXURY = "super_luxury"
    MIDI_BUS = "midi_bus"
    SEMI_DELUXE = "semi_deluxe"
    EXPRESS = "express"
    AIRPORT_SHUTTLE = "airport_shuttle"


@dataclass
class BusSpecifications:
    """Bus specifications"""
    name: str
    seating_capacity: int
    total_capacity: int  # Including standing
    length_m: float
    width_m: float
    height_m: float
    max_speed: float
    acceleration: float
    mass_kg: float
    fuel_tank_liters: float
    fuel_consumption_kmpl: float  # km per liter
    engine_cc: int
    color: tuple
    doors: int
    wheelchair_accessible: bool
    air_conditioned: bool
    luxury_level: str  # basic, standard, deluxe, luxury


class APSRTCBusSpecs:
    """APSRTC Bus Specifications Database"""
    
    SPECS = {
        APSRTCBusType.REGULAR_AC: BusSpecifications(
            name="Regular AC Bus",
            seating_capacity=45,
            total_capacity=55,
            length_m=9.5,
            width_m=2.5,
            height_m=3.2,
            max_speed=80.0,
            acceleration=3.0,
            mass_kg=5500,
            fuel_tank_liters=150,
            fuel_consumption_kmpl=4.5,
            engine_cc=5900,
            color=(255, 0, 0),  # Red with yellow/white bands
            doors=3,
            wheelchair_accessible=False,
            air_conditioned=True,
            luxury_level="standard"
        ),
        
        APSRTCBusType.VOLVO_AC: BusSpecifications(
            name="Volvo AC Bus",
            seating_capacity=47,
            total_capacity=55,
            length_m=10.6,
            width_m=2.5,
            height_m=3.3,
            max_speed=100.0,
            acceleration=4.5,
            mass_kg=6200,
            fuel_tank_liters=180,
            fuel_consumption_kmpl=5.2,
            engine_cc=6700,
            color=(0, 100, 200),  # Blue with white bands
            doors=3,
            wheelchair_accessible=True,
            air_conditioned=True,
            luxury_level="deluxe"
        ),
        
        APSRTCBusType.LOW_FLOOR: BusSpecifications(
            name="Low Floor Bus",
            seating_capacity=55,
            total_capacity=70,
            length_m=11.0,
            width_m=2.5,
            height_m=3.0,
            max_speed=85.0,
            acceleration=3.5,
            mass_kg=6500,
            fuel_tank_liters=200,
            fuel_consumption_kmpl=4.8,
            engine_cc=6700,
            color=(255, 150, 0),  # Orange
            doors=4,
            wheelchair_accessible=True,
            air_conditioned=True,
            luxury_level="standard"
        ),
        
        APSRTCBusType.SUPER_LUXURY: BusSpecifications(
            name="Super Luxury Bus",
            seating_capacity=38,
            total_capacity=42,
            length_m=10.8,
            width_m=2.5,
            height_m=3.4,
            max_speed=110.0,
            acceleration=5.0,
            mass_kg=6800,
            fuel_tank_liters=200,
            fuel_consumption_kmpl=5.5,
            engine_cc=7500,
            color=(100, 50, 150),  # Purple/Maroon
            doors=3,
            wheelchair_accessible=True,
            air_conditioned=True,
            luxury_level="luxury"
        ),
        
        APSRTCBusType.MIDI_BUS: BusSpecifications(
            name="Midi Bus",
            seating_capacity=28,
            total_capacity=35,
            length_m=7.5,
            width_m=2.4,
            height_m=2.9,
            max_speed=90.0,
            acceleration=4.0,
            mass_kg=3800,
            fuel_tank_liters=100,
            fuel_consumption_kmpl=6.0,
            engine_cc=4200,
            color=(0, 150, 0),  # Green
            doors=2,
            wheelchair_accessible=False,
            air_conditioned=True,
            luxury_level="basic"
        ),
        
        APSRTCBusType.SEMI_DELUXE: BusSpecifications(
            name="Semi Deluxe Bus",
            seating_capacity=42,
            total_capacity=50,
            length_m=9.8,
            width_m=2.5,
            height_m=3.2,
            max_speed=95.0,
            acceleration=3.8,
            mass_kg=5800,
            fuel_tank_liters=160,
            fuel_consumption_kmpl=4.9,
            engine_cc=6200,
            color=(200, 0, 100),  # Dark Red/Maroon
            doors=3,
            wheelchair_accessible=False,
            air_conditioned=True,
            luxury_level="deluxe"
        ),
        
        APSRTCBusType.EXPRESS: BusSpecifications(
            name="Express Bus",
            seating_capacity=48,
            total_capacity=56,
            length_m=10.5,
            width_m=2.5,
            height_m=3.3,
            max_speed=105.0,
            acceleration=4.2,
            mass_kg=6000,
            fuel_tank_liters=170,
            fuel_consumption_kmpl=5.0,
            engine_cc=6500,
            color=(100, 100, 100),  # Gray with white
            doors=3,
            wheelchair_accessible=False,
            air_conditioned=True,
            luxury_level="standard"
        ),
        
        APSRTCBusType.AIRPORT_SHUTTLE: BusSpecifications(
            name="Airport Shuttle",
            seating_capacity=32,
            total_capacity=38,
            length_m=8.5,
            width_m=2.5,
            height_m=3.1,
            max_speed=120.0,
            acceleration=5.5,
            mass_kg=5200,
            fuel_tank_liters=140,
            fuel_consumption_kmpl=5.8,
            engine_cc=5800,
            color=(0, 0, 150),  # Navy Blue
            doors=2,
            wheelchair_accessible=True,
            air_conditioned=True,
            luxury_level="luxury"
        )
    }


class APSRTCBus(Vehicle):
    """APSRTC Bus vehicle class"""
    
    def __init__(self, bus_type: APSRTCBusType, x: float, y: float):
        # Get specifications
        spec = APSRTCBusSpecs.SPECS[bus_type]
        
        # Create custom vehicle type name
        vehicle_type = VehicleType.BUS
        
        # Initialize parent with custom stats
        super().__init__(vehicle_type, x, y)
        
        # Store APSRTC-specific data
        self.bus_type = bus_type
        self.specifications = spec
        self.passengers_current = 0
        self.passengers_max = spec.total_capacity
        
        # Override vehicle stats with bus specifications
        self.stats = VehicleStats(
            max_speed=spec.max_speed,
            acceleration=spec.acceleration,
            mass=spec.mass_kg,
            friction=0.12,
            size=30,  # Larger size for buses
            color=spec.color
        )
        
        # Bus-specific features
        self.air_conditioner_on = True
        self.heater_on = False
        self.wifi_enabled = "deluxe" in spec.luxury_level or "luxury" in spec.luxury_level
        self.charging_ports = 4 if spec.wheelchair_accessible else 0
        self.usb_ports = 20 if "luxury" in spec.luxury_level else 10
        self.route_number = 0
        self.next_stop = ""
        self.is_on_schedule = True
        self.door_position = 0  # 0-100 (0 = closed, 100 = open)
        self.door_open_requested = False
        
        # Performance tracking
        self.kilometers_traveled = 0.0
        self.fuel_used = 0.0
        self.daily_revenue = 0.0
        self.maintenance_due_km = 50000
    
    def add_passenger(self, count: int = 1) -> bool:
        """Add passengers to the bus"""
        if self.passengers_current + count <= self.passengers_max:
            self.passengers_current += count
            return True
        return False
    
    def remove_passenger(self, count: int = 1) -> bool:
        """Remove passengers from the bus"""
        if self.passengers_current >= count:
            self.passengers_current -= count
            return True
        return False
    
    def open_doors(self) -> None:
        """Open bus doors"""
        self.door_open_requested = True
    
    def close_doors(self) -> None:
        """Close bus doors"""
        self.door_open_requested = False
    
    def update_doors(self, delta_time: float) -> None:
        """Update door position"""
        if self.door_open_requested:
            self.door_position = min(100, self.door_position + 50 * delta_time)
        else:
            self.door_position = max(0, self.door_position - 50 * delta_time)
    
    def calculate_fuel_consumption(self, delta_time: float) -> None:
        """Calculate fuel consumption based on weight and speed"""
        # Fuel consumption increases with passenger load
        load_factor = 1.0 + (self.passengers_current / self.passengers_max) * 0.5
        base_consumption = self.specifications.fuel_consumption_kmpl
        adjusted_consumption = base_consumption / load_factor
        
        # Calculate consumption for this delta time
        distance_traveled = (self.current_speed / 3.6) * delta_time  # Convert km/h to m/s
        fuel_consumed = (distance_traveled / 1000) / adjusted_consumption  # Liters
        
        self.fuel_used += fuel_consumed
        self.fuel_level -= fuel_consumed
    
    def get_bus_info(self) -> dict:
        """Get comprehensive bus information"""
        return {
            'bus_type': self.bus_type.value,
            'bus_name': self.specifications.name,
            'passengers': f"{self.passengers_current}/{self.passengers_max}",
            'occupancy': round((self.passengers_current / self.passengers_max) * 100),
            'speed': round(self.current_speed),
            'max_speed': self.specifications.max_speed,
            'fuel_level': round(self.fuel_level, 1),
            'fuel_tank_capacity': self.specifications.fuel_tank_liters,
            'air_con': self.air_conditioner_on,
            'wifi': self.wifi_enabled,
            'luxury_level': self.specifications.luxury_level,
            'route': self.route_number,
            'next_stop': self.next_stop,
            'on_schedule': self.is_on_schedule,
            'seating_capacity': self.specifications.seating_capacity,
            'engine_cc': self.specifications.engine_cc,
            'doors': self.specifications.doors,
        }
