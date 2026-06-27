# Indian Transportation Simulator

A comprehensive Python-based transportation simulator featuring Indian vehicles, realistic physics, and dynamic traffic management.

## 🎮 Features

- **Custom Game Engine** - Built from scratch with physics and rendering
- **Indian Vehicles** - Auto Rickshaw, Bus, Truck, Motorcycle, Car, Tata Tempo, and more
- **Physics Simulation** - Realistic vehicle dynamics with collision detection
- **Traffic Management** - AI-controlled vehicles with automatic spawn and behavior
- **Dynamic Rendering** - Real-time graphics with camera system
- **Configuration System** - Easily customize game parameters

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/valaparlashannu2010-glitch/Indian-transportation-simulator-.git
   cd Indian-transportation-simulator-
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the simulator**
   ```bash
   python main.py
   ```

## 🎮 Controls

| Key | Action |
|-----|--------|
| **SPACE** | Pause/Resume |
| **S** | Spawn Vehicle |
| **C** | Clear Vehicles |
| **R** | Show Stats |
| **ESC** | Quit |

## 📁 Project Structure

```
engine/
├── core/          # Game engine core
├── physics/       # Physics simulation
├── rendering/     # Graphics rendering
├── vehicles/      # Vehicle classes
└── traffic/       # Traffic management
main.py           # Application entry point
config.json       # Game configuration
requirements.txt  # Dependencies
```

## 🚗 Vehicle Types

- **Auto Rickshaw** - Yellow, lightweight, agile
- **Bus** - Red, heavy, public transport
- **Truck** - Brown, cargo transport
- **Motorcycle** - Black, fast, manoeuvrable
- **Car** - Blue, balanced performance
- **Tata Tempo** - Orange, commercial vehicle

## ⚙️ Configuration

Edit `config.json` to customize:
- Display resolution and FPS
- Physics parameters
- Traffic density
- Vehicle properties
- Debug settings

## 📚 Documentation

- [Development Guide](DEVELOPMENT.md) - Architecture and development workflow
- [Contributing Guide](CONTRIBUTING.md) - How to contribute

## 🔧 Technologies

- **Pygame** - Graphics and input handling
- **Python 3** - Core language
- **NumPy** - Mathematical operations
- **Pytest** - Testing framework

## 📊 Features Coming Soon

- Advanced AI pathfinding
- Traffic signals and lanes
- Weather effects
- Day/night cycle
- Sound effects
- Multiplayer support
- Map editor
- Performance analytics

## 🤝 Contributing

Contributions are welcome! Please see [DEVELOPMENT.md](DEVELOPMENT.md) for guidelines.

## 📄 License

MIT License - See LICENSE file for details

## 👤 Author

**valaparlashannu2010-glitch**

---

## 🌟 Support

If you find this project helpful, please give it a star! ⭐

For issues and questions, please open a GitHub issue.

**Happy Simulating!** 🚗🚕🚌
