# Technical Architecture - Indian Bus Simulator

## Overview

- **Engine**: Unity 2022 LTS
- **Render Pipeline**: Universal Render Pipeline (URP)
- **Platforms**: iOS (14.0+), Android (8.0+)
- **Architecture Pattern**: MVC + Entity Component System elements
- **Target Resolution**: 1080p at 60 FPS

---

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    INPUT SYSTEM                             │
│        (Touch, Accelerometer, Gyro, Buttons)                │
└─────────────────────────────────────────────────────────────┘
                            |
            ┌───────────────┼───────────────┐
            |               |               |
    ┌───────▼──────┐ ┌─────▼────────┐ ┌───▼────────────┐
    │  Vehicle     │ │   Camera     │ │  UI System     │
    │  Controller  │ │   System     │ │                │
    └───────┬──────┘ └─────┬────────┘ └───┬────────────┘
            |               |               |
            └───────────────┼───────────────┘
                            |
        ┌───────────────────▼───────────────────┐
        │      PHYSICS ENGINE (Custom)          │
        │  - Vehicle Rigidbody Simulation       │
        │  - Wheel Friction & Suspension        │
        │  - Environmental Forces               │
        │  - Collision Detection                │
        └───────────────────┬───────────────────┘
                            |
        ┌───────────────────▼───────────────────┐
        │       WORLD MANAGER                   │
        │  - Traffic AI                         │
        │  - Passenger System                   │
        │  - Environmental Objects              │
        │  - Road Network                       │
        └───────────────────┬───────────────────┘
                            |
    ┌───────────────────────┼───────────────────────┐
    |                       |                       |
 n┌──▼──────────┐ ┌─────────▼────────┐ ┌───────────▼─┐
    │   Weather  │ │   Route System   │ │   Economy   │
    │   System   │ │                  │ │   System    │
    └──────┬─────┘ └────────┬────────┘ └───────┬─────┘
           |                |                  |
           └────────────────┼──────────────────┘
                            |
        ┌───────────────────▼───────────────────┐
        │    RENDERING PIPELINE (URP)           │
        │  - Scene Rendering with LOD           │
        │  - Post-Processing Stack              │
        │  - UI Overlay                         │
        │  - Minimap Rendering                  │
        └───────────────────┬───────────────────┘
                            |
                    ┌───────▼────────┐
                    │  OUTPUT: GPU   │
                    │  Display Frame │
                    └────────────────┘
```

---

## Core Systems

### 1. Vehicle Controller System

```csharp
public abstract class VehicleBase : MonoBehaviour
{
    public VehicleType vehicleType;
    public float maxSpeed;
    public float weight;
    
    public Wheel[] wheels; // 4+ wheels
    public Engine engine;
    public Transmission transmission;
    public DamageSystem damageSystem;
    public FuelTank fuel;
    
    public virtual void ApplyInput(VehicleInput input);
    public virtual void UpdatePhysics(float deltaTime);
    public virtual void ApplyDamage(DamageInfo damage);
}

public class BusController : VehicleBase
{
    // Bus-specific
    public PassengerManager passengerManager;
    public DoorSystem doors;
    public StopSystem stops;
    public ScheduleSystem schedule;
}
```

### 2. Passenger Management System

```csharp
public class PassengerManager : MonoBehaviour
{
    private List<Passenger> passengers = new();
    private List<Passenger> waitingPassengers = new();
    
    public float CalculateSatisfaction();
    public void BoardPassenger(Passenger p);
    public void AlightPassenger(int index);
    public float GetCurrentLoad();
    public float CalculateDailyRevenue();
}

public class Passenger
{
    public PassengerType type;
    public Transform destination;
    public float satisfactionScore;
    public float boardingTime;
    public Vector3 preferredSeatPosition;
    
    public void Board(Bus bus);
    public void Alight();
    public void UpdateSatisfaction();
}
```

### 3. Physics System

```csharp
public class Wheel
{
    public float radius;
    public float width;
    public float springForce;
    public float damperForce;
    public float currentFriction;
    
    public void UpdateWheel(Vector3 vehicleVelocity, float steeringInput);
    public float GetGripMultiplier(WeatherType weather);
}

public class CustomRigidbody
{
    private Vector3 velocity;
    private Vector3 angularVelocity;
    private float mass;
    
    public void AddForce(Vector3 force);
    public void AddTorque(Vector3 torque);
    public void IntegrateVelocity(float deltaTime);
    public void ResolveCollisions();
}
```

### 4. Weather System

```csharp
public class WeatherManager : Singleton<WeatherManager>
{
    private WeatherType currentWeather;
    private float weatherIntensity; // 0-1
    private ParticleSystem weatherParticles;
    
    public void SetWeather(WeatherType weather, float duration);
    public float GetGripModifier();
    public float GetVisibilityDistance();
    public Vector3 GetWindForce();
}

public enum WeatherType
{
    Clear, PartlyCloudy, LightRain, HeavyRain,
    Thunderstorm, Fog, DustStorm, Sandstorm,
    Snow, Hail, Flood, ExtremeHeat
}
```

### 5. Route & Schedule System

```csharp
public class RouteSystem : MonoBehaviour
{
    public List<BusRoute> allRoutes = new();
    
    public BusRoute GetRoute(int routeId);
    public List<BusStop> GetStopsForRoute(int routeId);
    public float GetRouteDuration(int routeId);
}

public class BusRoute
{
    public int routeId;
    public string routeName;
    public Vector3[] waypoints;
    public BusStop[] stops;
    public float distance;
    public string[] languages; // For announcements
}
```

### 6. Economy System

```csharp
public class EconomyManager : Singleton<EconomyManager>
{
    public float CalculateFare(BusRoute route, int distance, PassengerType type);
    public float CalculateDailyExpenses(Bus bus);
    public float CalculateProfit(float revenue, float expenses);
    public void UpdateFinancials(float deltaTime);
}
```

---

## Data Flow

### Frame Rendering Loop

```
Frame Start (targetDeltaTime = 16.67ms for 60 FPS)
    ↓
[INPUT PROCESSING]
- Read touch/accelerometer
- Create VehicleInput object
- Handle UI interactions
    ↓
[VEHICLE SIMULATION]
- Apply input to wheels
- Calculate forces
- Update suspension
    ↓
[PHYSICS UPDATE]
- Integrate velocity
- Handle collisions
- Update rigidbody position
    ↓
[WORLD UPDATE]
- Update traffic AI
- Update passenger animations
- Update environmental objects
    ↓
[WEATHER UPDATE]
- Apply weather modifiers
- Update particles
- Update audio effects
    ↓
[CAMERA UPDATE]
- Follow vehicle
- Apply smoothing
    ↓
[RENDERING]
- Cull objects using LOD
- Render with URP
- Apply post-processing
- Render UI
    ↓
Frame Complete (aim for consistent 60 FPS)
```

---

## Performance Optimization

### 1. Level of Detail (LOD)
- **LOD0**: 8K-16K polygons, 0-50m
- **LOD1**: 2K-4K polygons, 50-200m
- **LOD2**: 500-1K polygons, 200-500m
- **LOD3**: Billboard, 500m+

### 2. Memory Management
- Object pooling for vehicles and passengers
- Addressable assets for streaming
- Texture atlasing
- Mesh compression

### 3. Batching Strategy
- Static batching for environment
- Dynamic batching for traffic
- GPU instancing for repeated objects

### 4. CPU Optimization
- Simplified AI for distant traffic
- Async asset loading
- Fixed timestep physics (0.02s)

---

## Mobile Specific

### iOS
- Metal renderer (automatic via URP)
- 60 FPS on iPhone 12+
- 900p resolution for older devices

### Android
- Vulkan renderer support
- Adaptive quality settings
- Device-specific profiles

---

## Build Configuration

| Device | Quality | Resolution | FPS |
|--------|---------|-------------|-----|
| High-End | Ultra | 1080p | 60 |
| Mid-Range | High | 900p | 60 |
| Budget | Medium | 720p | 30-60 |
| Low-End | Low | 720p | 30 |

---

## Testing Strategy

### Unit Tests
- Physics calculations
- Fare calculations
- Weather modifiers

### Integration Tests
- Vehicle + Weather interaction
- Passenger + Bus system
- Route + Schedule system

### Performance Tests
- Frame rate profiling
- Memory usage
- Load time testing

### Device Testing
- iPhone 12, 13, 14, 15
- Galaxy S20, S21, S22
- iPad Air (tablet)

---

## Future Scalability

- **Multiplayer**: Netcode for GameObjects / Mirror
- **Cloud Saves**: PlayFab or Firebase
- **Live Events**: Server-driven system
- **PC Port**: Steam compatibility

