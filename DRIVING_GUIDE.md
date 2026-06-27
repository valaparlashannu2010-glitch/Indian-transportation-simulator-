"""Advanced Driving System User Guide"""

## Keyboard Controls

### Engine and Transmission
- **I** - Start/Stop Engine
- **P** - Park
- **R** - Reverse
- **N** - Neutral
- **D** - Drive
- **Ctrl** - Clutch (hold for manual transmission)

### Movement
- **W / UP Arrow** - Accelerate
- **S / DOWN Arrow** - Brake
- **LEFT/RIGHT Arrow** - Steer Left/Right
- **H** - Handbrake (emergency brake)

### Lighting
- **L** - Toggle Headlights (Off → Parking → Dipped → High Beam)
- **F** - Toggle Fog Lights
- **LEFT Arrow** - Left Turn Indicator
- **RIGHT Arrow** - Right Turn Indicator

### Vehicle Features
- **W** - Toggle Wipers (Off → Low → Medium → High → Intermittent)
- **A** - Toggle Air Conditioning
- **UP/DOWN** - AC Temperature (16-32°C)
- **U** - Lock/Unlock Doors
- **B** - Fasten/Unfasten Seatbelt
- **C** - Toggle Cruise Control
- **T** - Toggle Traction Control
- **S** - Toggle Stability Control

## Dashboard Information

### Main Gauges
1. **Speedometer** - Current speed in km/h
2. **RPM Gauge** - Engine revolutions per minute
3. **Fuel Gauge** - Remaining fuel (0-60L)
4. **Temperature Gauge** - Engine temperature

### Status Lights
- **Lights** - Yellow (headlights active)
- **Fog** - Orange (fog lights active)
- **Brake** - Red (brakes applied)
- **Reverse** - White (reverse gear engaged)
- **Indicator** - Orange (turn signal active)
- **Handbrake** - Red (handbrake engaged)
- **Cruise** - Cyan (cruise control active)
- **Seatbelt!** - Red warning (seatbelt not fastened)

### Engine States
- **ENGINE OFF** - Red (engine not running)
- **STARTING...** - Orange (engine starting)
- **ENGINE RUNNING** - Green (engine active)

## Vehicle Systems

### Engine System
- **RPM Range**: 600 - 6000 RPM
- **Idle Speed**: 600 RPM
- **Max Torque**: 200 Nm
- **Fuel Consumption**: 0.5 L/100km base rate
- **Temperature Range**: 20-110°C
- **Stalling**: Engine stalls if RPM drops below 300

### Transmission
- **Gears**: Park, Reverse, Neutral, Drive, Low
- **Gear Ratios**: 3.5, 2.0, 1.3, 0.9, 0.7
- **Clutch Required**: Yes (Ctrl key)
- **Auto Shift**: Enabled (automatic gear changes)

### Braking System
- **ABS (Anti-lock Braking)**: Enabled by default
- **Brake Temperature**: 20-800°C
- **Brake Wear**: Degrades with heavy braking
- **Brake Force**: Max 100%
- **Emergency Brake**: Handbrake (H key)

### Steering
- **Steering Angle**: ±45 degrees
- **Power Steering**: Enabled (assists steering)
- **Steering Modes**: Manual, Assisted, Auto
- **Sensitivity**: Adjustable (1.0 default)

### Fuel System
- **Tank Capacity**: 60 Liters
- **Consumption Rate**: Based on engine load
- **Range**: ~6000 km (theoretical)
- **Warning**: Low fuel at <10L

### Cooling System
- **Operating Temperature**: 80-95°C (optimal)
- **Overheat Warning**: 100°C+
- **Coolant Failure**: Stalls at 110°C

### Climate Control (AC)
- **Temperature Range**: 16-32°C
- **Modes**: Off, Low, Medium, High
- **Efficiency**: Increases with mode

### Lights System
- **Headlights**: 4 states (Off, Parking, Dipped, High Beam)
- **Fog Lights**: On/Off toggle
- **Brake Lights**: Auto-engage when braking
- **Reverse Lights**: Auto-engage in reverse gear
- **Indicators**: Left/Right turn signals with auto-cancel

### Wiper System
- **Speeds**: Off, Low, Medium, High, Intermittent
- **Auto-off**: When car stops for 5 seconds

## Safety Features

### Active Safety
- **Traction Control (TC)**: Prevents wheel slip
- **Electronic Stability Control (ESC)**: Maintains vehicle stability
- **Anti-lock Braking (ABS)**: Prevents brake lock-up
- **Cruise Control**: Maintains constant speed

### Passive Safety
- **Seatbelt System**: Must be fastened
- **Airbag System**: Enabled by default
- **Door Locks**: Manual/automatic locking

## Performance Monitoring

### Odometer
- Tracks total distance traveled
- Stored permanently
- Used for maintenance scheduling

### Trip Meter
- Resets manually
- Tracks distance for current trip
- Tracks time for current trip
- Calculates average speed

### Warning System
- **Low Fuel**: <10L
- **Engine Hot**: >100°C
- **Seatbelt**: Not fastened at speed >5 km/h
- **Door Unlocked**: At speed >10 km/h

## Advanced Driving Tips

1. **Smooth Acceleration**: Gradually increase throttle for better fuel economy
2. **Engine Braking**: Release throttle before braking to cool engine
3. **Gear Selection**: Use lower gears for climbing or heavy loads
4. **Fuel Efficiency**: Maintain 60-80 km/h for best efficiency
5. **Brake Maintenance**: Avoid excessive braking to reduce wear
6. **Temperature Management**: Monitor engine temperature, let it cool after heavy use
7. **Cruise Control**: Use on highways for fuel savings
8. **Indicators**: Always signal turns for safety

## Emergency Procedures

### Engine Stall
- **Cause**: RPM drops below 300 (usually from releasing throttle suddenly)
- **Recovery**: Press I to restart engine

### Overheating
- **Warning**: Temperature gauge in red zone (>100°C)
- **Action**: Stop vehicle and let cool, check AC efficiency
- **Prevention**: Avoid prolonged high throttle

### Low Fuel
- **Warning**: Red fuel gauge and warning message
- **Action**: Refuel immediately
- **Note**: Engine stops at 0L fuel

### Brake Wear
- **Indicator**: Brake wear percentage on dashboard
- **Action**: Consider repairs when <20%
- **Performance**: Decreases as wear increases

## Customization

Edit `config.json` to customize:
- Vehicle stats (mass, max speed, acceleration)
- Engine parameters (RPM range, torque)
- Steering sensitivity
- Fuel consumption rates
- Temperature thresholds
