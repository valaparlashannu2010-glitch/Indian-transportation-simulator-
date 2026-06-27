"""Sound System - Audio management and playback"""
import os
from enum import Enum


class SoundType(Enum):
    """Sound types"""
    ENGINE_IDLE = "engine_idle"
    ENGINE_RUNNING = "engine_running"
    ENGINE_REV = "engine_rev"
    ACCELERATION = "acceleration"
    BRAKING = "braking"
    HORN = "horn"
    TURN_SIGNAL = "turn_signal"
    COLLISION = "collision"
    SKID = "skid"
    DOOR_OPEN = "door_open"
    DOOR_CLOSE = "door_close"
    SEATBELT = "seatbelt"
    TRAFFIC_AMBIENCE = "traffic_ambience"
    RAIN = "rain"
    WIND = "wind"
    BACKGROUND_MUSIC = "background_music"


class SoundSystem:
    """Audio system for the simulator"""
    
    def __init__(self):
        self.sounds = {}  # Loaded sounds cache
        self.music_enabled = True
        self.sfx_enabled = True
        self.ambient_enabled = True
        self.master_volume = 0.8
        self.music_volume = 0.6
        self.sfx_volume = 0.8
        self.ambient_volume = 0.5
        self.current_music = None
        self.is_music_playing = False
        
        # Sound properties
        self.engine_pitch = 1.0  # Changes with RPM
        self.traffic_ambience_active = False
        self.weather_ambience_active = False
        
        print("\u2713 Sound System Initialized")
        print(f"Master Volume: {self.master_volume * 100}%")
        print(f"Music: {'ON' if self.music_enabled else 'OFF'}")
        print(f"SFX: {'ON' if self.sfx_enabled else 'OFF'}")
        print(f"Ambient: {'ON' if self.ambient_enabled else 'OFF'}")
    
    def load_sound(self, sound_type: SoundType, file_path: str = None) -> None:
        """Load a sound file"""
        # In a real implementation, this would use pygame.mixer
        # For now, we simulate it
        if file_path is None:
            file_path = f"assets/sounds/{sound_type.value}.wav"
        
        self.sounds[sound_type] = {
            'path': file_path,
            'loaded': os.path.exists(file_path) if file_path else False,
            'volume': self.sfx_volume
        }
    
    def play_sound(self, sound_type: SoundType, volume: float = None, loop: bool = False) -> None:
        """Play a sound effect"""
        if not self.sfx_enabled:
            return
        
        if volume is None:
            volume = self.sfx_volume
        
        # Adjust volume
        actual_volume = volume * self.master_volume
        
        # In real implementation, use pygame.mixer.Sound.play()
        print(f"\ud83d\udd0a Playing {sound_type.value} at {actual_volume * 100:.0f}% volume")
    
    def play_music(self, track_name: str, loop: bool = True) -> None:
        """Play background music"""
        if not self.music_enabled:
            return
        
        self.current_music = track_name
        self.is_music_playing = True
        volume = self.music_volume * self.master_volume
        
        print(f"\ud83c\udfb5 Playing music: {track_name} at {volume * 100:.0f}% volume")
    
    def stop_music(self) -> None:
        """Stop background music"""
        self.is_music_playing = False
        print("\ud83c\udfb5 Music stopped")
    
    def update_engine_sound(self, rpm: float, throttle: float) -> None:
        """Update engine sound based on RPM and throttle"""
        if not self.sfx_enabled:
            return
        
        # Calculate engine pitch based on RPM (0.5 to 2.0)
        max_rpm = 6000
        self.engine_pitch = 0.5 + (rpm / max_rpm) * 1.5
        
        # Play engine sound with calculated pitch
        if rpm > 600:  # Engine running
            volume = self.sfx_volume * (0.5 + throttle * 0.5)
            # In real implementation: play_sound_with_pitch(engine_sound, self.engine_pitch, volume)
    
    def play_horn(self) -> None:
        """Play horn sound"""
        self.play_sound(SoundType.HORN, 0.9)
    
    def play_collision_sound(self, impact_force: float) -> None:
        """Play collision sound based on impact force"""
        volume = min(1.0, impact_force / 100.0)
        self.play_sound(SoundType.COLLISION, volume)
    
    def play_skid_sound(self, intensity: float) -> None:
        """Play skid/drift sound"""
        volume = intensity * 0.8
        self.play_sound(SoundType.SKID, volume, loop=True)
    
    def set_master_volume(self, volume: float) -> None:
        """Set master volume (0.0 to 1.0)"""
        self.master_volume = max(0.0, min(1.0, volume))
        print(f"Master Volume: {self.master_volume * 100:.0f}%")
    
    def set_music_volume(self, volume: float) -> None:
        """Set music volume"""
        self.music_volume = max(0.0, min(1.0, volume))
        print(f"Music Volume: {self.music_volume * 100:.0f}%")
    
    def set_sfx_volume(self, volume: float) -> None:
        """Set SFX volume"""
        self.sfx_volume = max(0.0, min(1.0, volume))
        print(f"SFX Volume: {self.sfx_volume * 100:.0f}%")
    
    def toggle_music(self) -> None:
        """Toggle music on/off"""
        self.music_enabled = not self.music_enabled
        if not self.music_enabled:
            self.stop_music()
        print(f"Music: {'ON' if self.music_enabled else 'OFF'}")
    
    def toggle_sfx(self) -> None:
        """Toggle sound effects on/off"""
        self.sfx_enabled = not self.sfx_enabled
        print(f"SFX: {'ON' if self.sfx_enabled else 'OFF'}")
    
    def toggle_ambient(self) -> None:
        """Toggle ambient sounds on/off"""
        self.ambient_enabled = not self.ambient_enabled
        print(f"Ambient: {'ON' if self.ambient_enabled else 'OFF'}")
