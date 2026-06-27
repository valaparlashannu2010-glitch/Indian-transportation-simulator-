# Development Setup Guide

## Prerequisites

### Required Software

1. **Unity 2022 LTS**
   - Download: https://unity.com/download
   - Install with iOS and Android modules

2. **Git & GitHub**
   - Git: https://git-scm.com/
   - GitHub Desktop (optional): https://desktop.github.com/

3. **IDE**
   - Visual Studio Code or Visual Studio 2022
   - C# Dev Kit extension

4. **Mobile Build Tools**
   - **iOS**: Xcode 13+ (macOS only)
   - **Android**: Android Studio with SDK

5. **3D Tools** (Optional)
   - Blender (Free): https://blender.org/
   - Substance Painter (Paid): https://www.adobe.com/products/substance/painter.html

---

## Project Setup

### Step 1: Clone Repository

```bash
git clone https://github.com/valaparlashannu2010-glitch/Indian-transportation-simulator-
cd Indian-transportation-simulator-
git checkout game-development
```

### Step 2: Create Unity Project

1. Open Unity Hub
2. Click "New project"
3. Select "3D (URP)" template
4. Name: "Indian-Bus-Simulator"
5. Create in cloned repository directory

### Step 3: Configure Project Settings

```
Edit → Project Settings
```

**Player Settings**:
- Company Name: "Indian Bus Simulator"
- Product Name: "IBS"
- Bundle ID: `com.yourcompany.ibs`

**Quality Settings** (Create 4 tiers):
- Ultra, High, Medium, Low
- Adjust shadows, particles, draw distance per tier

**Time Settings**:
- Fixed Timestep: 0.02 (50 physics updates/sec)

### Step 4: Install Packages

```
Window → Package Manager
```

Install:
- Input System (com.unity.inputsystem)
- Post Processing (com.unity.postprocessing)
- TextMesh Pro (usually pre-installed)
- ProBuilder (com.unity.probuilder)

### Step 5: Create Folder Structure

```bash
mkdir -p Assets/Scripts/{Vehicles,Passengers,World,Routes,Physics,Weather,Traffic,Economy,Audio,UI,Core}
mkdir -p Assets/{Prefabs,Models,Textures,Materials,Shaders,Audio,Scenes,Data,Maps,Animations}
```

### Step 6: Configure Git

Create `.gitattributes`:

```
* text=auto
*.cs diff=csharp
*.shader diff=csharp
*.meta merge=unityyamlmerge eol=lf
*.prefab merge=unityyamlmerge eol=lf
*.unity merge=unityyamlmerge eol=lf
```

---

## Development Workflow

### Creating a Feature

```bash
# Create feature branch
git checkout -b feature/bus-physics

# Make changes
# Commit frequently
git add Assets/Scripts/Vehicles/BusPhysics.cs
git commit -m "Implement bus physics engine"

# Push to GitHub
git push origin feature/bus-physics

# Create Pull Request on GitHub
# Request review
# Merge after approval
```

---

## First Scene Setup

### Create Main Scene

1. New scene: `Assets/Scenes/MainGame.unity`
2. Add to Build Settings (Scene 0)

### Scene Components

1. **Main Camera**
   - Right-click → 3D Object → Camera
   - Tag: "MainCamera"

2. **Game Manager** (Empty GameObject)
   - Add script: `Scripts/Core/GameManager.cs`
   - Don't Destroy On Load

3. **Bus (Test)**
   - Create simple cube for testing
   - Add component: BusController.cs

4. **Canvas**
   - Right-click → UI → Canvas
   - For HUD elements

---

## Building for Mobile

### Android Build

```
File → Build Settings
Select: Android

Edit → Project Settings → Player
- Package Name: com.yourcompany.ibs
- Target API: 30+
- Minimum API: 26+

File → Build and Run
```

### iOS Build

```
File → Build Settings
Select: iOS

Edit → Project Settings → Player
- Bundle Identifier: com.yourcompany.ibs
- Target iOS: 14.0+

File → Build
Open Xcode project
Product → Run
```

---

## Performance Profiling

### In-Editor

```
Window → Analysis → Profiler
```

Monitor:
- CPU Usage
- Memory
- GPU
- Rendering

### On Device

```
Window → Analysis → Frame Debugger
```

Check:
- Draw calls
- Batch counts
- Memory

---

## Common Issues

### "Assembly has invalid references"
```bash
rm -rf Library/
```

### Android Build Fails
- Check SDK/NDK paths
- Ensure JDK is installed
- Update build tools

### iOS Build Fails
- Set development team in Xcode
- Check provisioning profiles
- Update Xcode

---

## Useful Commands

```bash
# View status
git status

# View recent commits
git log --oneline -10

# Clean build cache
rm -rf Library/ Temp/ Logs/

# Stash changes
git stash

# Pull latest
git pull origin develop
```

---

## Next Steps

1. ✅ Repository cloned
2. ✅ Unity project created
3. → Start Phase 1: Bus Physics
4. → Create basic vehicle controller
5. → Implement passenger spawning
6. → Build first demo scene

---

## Resources

- [Unity Manual](https://docs.unity3d.com/Manual/)
- [Unity Learn](https://learn.unity.com/)
- [GitHub Guides](https://guides.github.com/)

Happy coding! 🚌🎮
