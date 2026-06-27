# Development Guide - Indian Transportation Simulator

## Project Structure

```
Indian-transportation-simulator/
├── engine/
│   ├── core/
│   │   └── game_engine.py          # Main game engine
│   ├── physics/
│   │   └── physics_engine.py       # Physics simulation
│   ├── rendering/
│   │   └── renderer.py             # Graphics rendering
│   ├── vehicles/
│   │   └── vehicle.py              # Vehicle classes
│   └── traffic/
│       └── traffic_manager.py      # Traffic management
├── main.py                          # Application entry point
├── config.json                      # Game configuration
├── requirements.txt                 # Python dependencies
├── README.md                        # Project overview
├── DEVELOPMENT.md                   # Development guide
├── tests/                           # Unit tests
├── docs/                            # Documentation
└── .gitignore                       # Git ignore rules
```

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/valaparlashannu2010-glitch/Indian-transportation-simulator-.git
cd Indian-transportation-simulator-
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Simulator
```bash
python main.py
```

## Game Controls

| Key | Action |
|-----|--------|
| **SPACE** | Pause/Resume simulation |
| **S** | Spawn a new vehicle |
| **C** | Clear all vehicles |
| **R** | Show statistics |
| **ESC** | Quit game |

## Engine Architecture

### Core Components

1. **GameEngine** - Main game loop and entity management
2. **PhysicsEngine** - Rigid body dynamics and collision detection
3. **Renderer** - Graphics rendering and camera system
4. **TrafficManager** - Vehicle spawning and AI behavior
5. **Vehicle** - Vehicle class with physics and rendering

### Game Loop Flow

```
Initialize
    ↓
Handle Input → Update Physics → Update Traffic → Render
    ↓
    └→ Repeat until exit
```

## Vehicle Types

- **Auto Rickshaw** - Yellow, lightweight, agile
- **Bus** - Red, heavy, slow acceleration
- **Truck** - Brown, very heavy, cargo transport
- **Motorcycle** - Black, light, high acceleration
- **Car** - Blue, medium, balanced
- **Tata Tempo** - Orange, commercial, medium-heavy
- **Scooter** - Green, very light, agile

## Physics System

### Features
- Rigid body dynamics
- Force-based movement
- Friction simulation
- Elastic collision detection and response
- Customizable mass and acceleration

### Key Equations
- **Force**: F = m × a
- **Velocity**: v = v + a × Δt
- **Position**: p = p + v × Δt
- **Friction**: f = -c × v

## Configuration

Edit `config.json` to customize:
- Display resolution and FPS
- Physics parameters (gravity, timestep)
- Traffic density and spawn rate
- Vehicle properties and colors
- Debug settings

## Development Workflow

### Adding a New Feature

1. Create a feature branch
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make changes and test
   ```bash
   python main.py
   ```

3. Run tests
   ```bash
   pytest tests/
   ```

4. Commit and push
   ```bash
   git add .
   git commit -m "Add your feature description"
   git push origin feature/your-feature-name
   ```

5. Create a Pull Request

### Code Style

We follow PEP 8 style guide. Use Black for formatting:

```bash
black engine/ main.py
```

Lint with Flake8:

```bash
flake8 engine/ main.py
```

## Testing

Run unit tests:

```bash
pytest tests/ -v
```

Run with coverage:

```bash
pytest tests/ --cov=engine --cov-report=html
```

## Performance Tips

1. **Limit max vehicles** - Adjust `max_vehicles` in config.json
2. **Physics iterations** - Increase `max_iterations` for better accuracy
3. **Frame rate** - Lower FPS for slower systems
4. **Render optimization** - Use sprite batching for many objects

## Common Issues

### Issue: ImportError for pygame
**Solution**: Install pygame correctly
```bash
pip install pygame --upgrade
```

### Issue: Slow performance with many vehicles
**Solution**: Reduce max_vehicles in config.json or optimize physics

### Issue: Vehicles spawning outside screen
**Solution**: Check spawn_points in traffic_manager.py

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests
5. Submit a pull request

## Future Enhancements

- [ ] Advanced AI with pathfinding
- [ ] Traffic signals and lane system
- [ ] Weather effects (rain, fog)
- [ ] Day/night cycle
- [ ] Sound effects and music
- [ ] Multiplayer support
- [ ] Map editor
- [ ] Vehicle damage system
- [ ] Traffic rules enforcement
- [ ] Performance analytics

## Resources

- [Pygame Documentation](https://www.pygame.org/docs/)
- [Physics Engine Guide](https://www.gamedev.net/tutorials/)
- [Game Development Best Practices](https://www.gamedev.net/)

## License

MIT License - See LICENSE file for details

## Support

For issues and questions:
- Open an issue on GitHub
- Check existing discussions
- Read the documentation

## Credits

Created by: valaparlashannu2010-glitch

---

**Last Updated**: June 27, 2026
