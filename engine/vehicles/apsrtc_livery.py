"""APSRTC Bus Livery System - Authentic Andhra Pradesh bus designs"""
from enum import Enum


class LiveryStyle(Enum):
    """APSRTC livery styles"""
    CLASSIC = "classic"
    MODERN = "modern"
    HERITAGE = "heritage"


class BusLivery:
    """APSRTC Bus Livery Design"""
    
    # APSRTC Standard Livery Elements
    APSRTC_LOGO = """
    ╔════════════════════════╗
    ║  ANDHRA PRADESH        ║
    ║  STATE ROAD TRANSPORT  ║
    ║  CORPORATION           ║
    ║  A.P.S.R.T.C           ║
    ╚════════════════════════╝
    """
    
    # Bus type specific liveries
    LIVERIES = {
        "regular_ac": {
            "name": "Regular AC Bus",
            "primary_color": "Red",
            "secondary_color": "Yellow",
            "tertiary_color": "White",
            "design_elements": [
                "APSRTC Logo on side",
                "Ashoka Chakra emblem",
                "Yellow and red horizontal bands",
                "Route number display area",
                "Destination scroll area",
                "Silver/chrome bumpers",
                "Side mirrors with logos",
                "Emergency contact number",
                "Bus registration plate area"
            ],
            "text_displays": {
                "route_number": "Route: 123",
                "destination": "HYDERABAD - SECUNDERABAD",
                "emergency_contact": "Emergency: 108",
                "conductor_info": "Conductor No."
            }
        },
        "volvo_ac": {
            "name": "Volvo AC Bus",
            "primary_color": "Blue",
            "secondary_color": "White",
            "tertiary_color": "Silver",
            "design_elements": [
                "APSRTC Logo (modern)",
                "Blue and white gradient design",
                "Volvo branding",
                "LED destination display",
                "Chrome handles",
                "Tinted windows",
                "Air suspension indicator",
                "Digital route display",
                "Premium livery stripes"
            ],
            "text_displays": {
                "route_number": "Express: 100E",
                "destination": "BANGALORE - VIJAYAWADA",
                "bus_type": "VOLVO AC SEMI DELUXE",
                "facilities": "WiFi | USB Charging"
            }
        },
        "low_floor": {
            "name": "Low Floor Bus",
            "primary_color": "Orange",
            "secondary_color": "White",
            "tertiary_color": "Black",
            "design_elements": [
                "APSRTC Logo",
                "Orange and white stripes",
                "Wheelchair accessibility symbol",
                "Low floor indicator",
                "Wide door markings",
                "Handrail designs",
                "Priority seating indication",
                "Emergency exit markings",
                "Reflective safety stripes"
            ],
            "text_displays": {
                "bus_type": "LOW FLOOR BUS",
                "accessibility": "Wheelchair Accessible",
                "capacity": "70 Seater",
                "safety_info": "Emergency Exit"
            }
        },
        "super_luxury": {
            "name": "Super Luxury Bus",
            "primary_color": "Maroon",
            "secondary_color": "Gold",
            "tertiary_color": "White",
            "design_elements": [
                "Premium APSRTC Logo (gold embossed)",
                "Maroon and gold luxury design",
                "Premium livery with patterns",
                "Reclining seat indication",
                "Entertainment system marks",
                "Blanket and pillow symbols",
                "Premium carpet symbols",
                "Luxurious chrome details",
                "VIP service indicator"
            ],
            "text_displays": {
                "bus_type": "SUPER LUXURY AC",
                "features": "Reclining Seats | Entertainment",
                "slogan": "Experience Premium Comfort",
                "premium_line": "APSRTC PREMIUM SERVICE"
            }
        },
        "midi_bus": {
            "name": "Midi Bus",
            "primary_color": "Green",
            "secondary_color": "White",
            "tertiary_color": "Yellow",
            "design_elements": [
                "APSRTC Logo (smaller scale)",
                "Green and white compact design",
                "Local route markings",
                "Compact bus indicators",
                "Simple livery stripes",
                "Basic amenities symbols",
                "Local service indication",
                "Community transport mark",
                "Eco-friendly indicator"
            ],
            "text_displays": {
                "bus_type": "MIDI BUS",
                "service_type": "LOCAL SERVICE",
                "capacity": "35 Seater",
                "route_info": "City Routes"
            }
        },
        "semi_deluxe": {
            "name": "Semi Deluxe Bus",
            "primary_color": "Dark Red",
            "secondary_color": "Gold",
            "tertiary_color": "White",
            "design_elements": [
                "APSRTC Logo (standard)",
                "Dark red and gold stripes",
                "Comfortable seating indication",
                "Reclining seat symbols",
                "Entertainment facility mark",
                "Charging port indication",
                "Good quality upholstery mark",
                "Moderate luxury indicator",
                "Professional service mark"
            ],
            "text_displays": {
                "bus_type": "SEMI DELUXE AC",
                "features": "Reclining Seats | USB Charging",
                "comfort_level": "COMFORT CLASS",
                "service_quality": "QUALITY SERVICE"
            }
        },
        "express": {
            "name": "Express Bus",
            "primary_color": "Gray",
            "secondary_color": "White",
            "tertiary_color": "Red",
            "design_elements": [
                "APSRTC Logo",
                "Gray and white streamline design",
                "Speed stripes",
                "Express service marking",
                "Interstate route indication",
                "Modern aerodynamic design",
                "LED lights indication",
                "Safety feature symbols",
                "Highway service mark"
            ],
            "text_displays": {
                "bus_type": "EXPRESS AC",
                "service_type": "INTERSTATE EXPRESS",
                "features": "Fast Service | Direct Routes",
                "speed_indicator": "High Speed"
            }
        },
        "airport_shuttle": {
            "name": "Airport Shuttle",
            "primary_color": "Navy Blue",
            "secondary_color": "White",
            "tertiary_color": "Gold",
            "design_elements": [
                "Premium APSRTC Logo (gold)",
                "Navy blue and white design",
                "Airport symbol",
                "Premium travel indicator",
                "Luggage space symbols",
                "Charging stations mark",
                "WiFi facility indication",
                "Premium seating mark",
                "Executive service indicator"
            ],
            "text_displays": {
                "bus_type": "AIRPORT SHUTTLE",
                "service": "AIRPORT TRANSFER SERVICE",
                "features": "Premium Comfort | WiFi | USB",
                "route_type": "MAJOR AIRPORTS"
            }
        }
    }
    
    @staticmethod
    def get_livery_details(bus_type: str) -> dict:
        """Get livery details for a bus type"""
        return BusLivery.LIVERIES.get(bus_type, {})
    
    @staticmethod
    def render_livery_on_bus(screen, bus_x: float, bus_y: float, bus_type: str) -> None:
        """Render bus livery on screen"""
        import pygame
        
        livery = BusLivery.get_livery_details(bus_type)
        if not livery:
            return
        
        # Draw APSRTC logo area
        font = pygame.font.Font(None, 16)
        
        # Draw livery text
        livery_text = f"{livery.get('name', '')} - APSRTC"
        text_surface = font.render(livery_text, True, (255, 255, 255))
        
        # Display on bus
        if text_surface:
            screen.blit(text_surface, (int(bus_x - 50), int(bus_y - 20)))
        
        # Draw design elements as text indicators
        for i, element in enumerate(livery.get('design_elements', [])[:3]):
            small_font = pygame.font.Font(None, 12)
            element_text = small_font.render(f"• {element}", True, (200, 200, 200))
            screen.blit(element_text, (int(bus_x - 50), int(bus_y + 10 + i * 12)))
    
    @staticmethod
    def print_livery_details(bus_type: str) -> None:
        """Print livery details to console"""
        livery = BusLivery.get_livery_details(bus_type)
        if not livery:
            print(f"Livery not found for bus type: {bus_type}")
            return
        
        print("\n" + "="*60)
        print(f"APSRTC {livery['name'].upper()} - LIVERY DETAILS")
        print("="*60)
        print(f"Primary Color: {livery['primary_color']}")
        print(f"Secondary Color: {livery['secondary_color']}")
        print(f"Tertiary Color: {livery['tertiary_color']}")
        print("\nDesign Elements:")
        for element in livery['design_elements']:
            print(f"  ✓ {element}")
        print("\nText Displays:")
        for key, value in livery['text_displays'].items():
            print(f"  • {key.upper()}: {value}")
        print("="*60 + "\n")
