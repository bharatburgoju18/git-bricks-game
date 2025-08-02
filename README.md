# 🧱 Brick Breaker Game

A classic arcade-style Brick Breaker game built with HTML5 Canvas and JavaScript, featuring intelligent auto-play AI and exciting power-up mechanics.

## 🎮 Features

### Core Gameplay
- **Classic Brick Breaking**: Destroy colorful bricks arranged in a 5x10 grid
- **Physics-Based Ball Movement**: Realistic ball bouncing with angle-based paddle hits
- **Lives System**: Start with 3 lives, lose one when the ball falls below the paddle
- **Progressive Scoring**: Earn 10 points per brick destroyed

### Advanced Features
- **🤖 Auto-Play AI**: Intelligent paddle movement that automatically tracks and catches the ball
- **💰 Power-Up System**: Golden bonus boxes that fall from destroyed bricks
  - Worth +20 points when caught
  - Cost 1 life if missed (risk/reward mechanic)
  - 30% spawn chance from destroyed bricks
- **🎛️ Flexible Controls**: Switch between manual control (keyboard/mouse) and auto-play mode

### Visual & UI
- **Colorful Design**: Each brick row has a different vibrant color
- **Real-time Status**: Live score and lives counter
- **Auto-play Indicator**: Visual feedback showing current control mode
- **Responsive Controls**: Smooth paddle movement with multiple input methods

## 🚀 Installation & Setup

### Prerequisites
- Any modern web browser (Chrome, Firefox, Safari, Edge)
- No additional software or dependencies required

### Quick Start
1. **Download** or clone the project files
2. **Navigate** to the project directory
3. **Open** `index.html` in your web browser
4. **Play** immediately - no installation needed!

```bash
# If using git
git clone <repository-url>
cd "bricks game"
open index.html  # macOS
# or double-click index.html in file explorer
```

## 🎯 How to Play

### Game Objective
Destroy all bricks to win the game while keeping the ball in play and collecting bonus power-ups.

### Starting the Game
1. Open the game in your browser
2. Press **SPACEBAR** to start
3. The game begins in auto-play mode by default

### Control Modes

#### Auto-Play Mode (Default)
- Paddle automatically follows the ball
- Perfect for watching or learning game mechanics
- Toggle ON/OFF with the **'A'** key

#### Manual Control
- **Arrow Keys**: Move paddle left/right
- **Mouse**: Move mouse to control paddle position
- Using arrow keys automatically disables auto-play

### Power-Up System
- **Golden Boxes** fall from destroyed bricks (30% chance)
- **Catch them** with the paddle for **+20 bonus points**
- **Miss them** and **lose 1 life** - high risk, high reward!

### Winning & Losing
- **Win**: Destroy all 50 bricks
- **Lose**: Run out of lives (ball falls below paddle or miss power-ups)

## 🎮 Controls Reference

| Key/Action | Function |
|------------|----------|
| **SPACEBAR** | Start/Restart game |
| **Left Arrow** | Move paddle left (disables auto-play) |
| **Right Arrow** | Move paddle right (disables auto-play) |
| **Mouse Movement** | Control paddle position |
| **'A' Key** | Toggle auto-play mode ON/OFF |

## 🛠️ Technical Specifications

### Technology Stack
- **HTML5**: Game structure and UI
- **CSS3**: Styling and responsive design
- **JavaScript (ES6+)**: Game logic and mechanics
- **Canvas API**: 2D graphics rendering

### Game Architecture
- **Object-oriented design** with separate game entities
- **Game loop** using `requestAnimationFrame` for smooth 60fps gameplay
- **Collision detection** system for ball, paddle, bricks, and power-ups
- **State management** for different game phases (ready, playing, game over, won)

### Performance Features
- **Efficient rendering** with selective drawing
- **Optimized collision detection** algorithms
- **Memory management** for dynamic power-up objects
- **Smooth animations** with consistent frame timing

## 📁 Project Structure

```
bricks-game/
├── index.html          # Main HTML file with game canvas and UI
├── game.js            # Core game logic and mechanics
└── README.md          # Project documentation
```

### File Descriptions

#### `index.html`
- Game container and canvas setup
- UI elements (score, lives, controls)
- Responsive styling with dark theme
- Instructions and game information

#### `game.js`
- Game constants and configuration
- Paddle, ball, brick, and power-up objects
- AI logic for auto-play mode
- Collision detection algorithms
- Game state management
- Event handlers for user input
- Rendering and animation loop

## 🎨 Game Mechanics Deep Dive

### Ball Physics
- **Speed**: Constant velocity with direction changes
- **Bouncing**: Angle-based reflection off paddle surface
- **Wall Collision**: Perfect elastic collision with screen boundaries

### Auto-Play AI
- **Tracking Algorithm**: Calculates optimal paddle position
- **Smooth Movement**: Gradual approach to target position
- **Collision Avoidance**: Boundary checking and constraint handling

### Power-Up System
- **Spawning**: Random generation based on probability
- **Physics**: Gravity-based falling motion
- **Collision**: Rectangle-based intersection detection
- **Risk Management**: Balance between reward and penalty

### Scoring System
- **Bricks**: 10 points each (base game)
- **Power-ups**: 20 points each (bonus)
- **Total Possible**: 500 base points + unlimited bonus points

## 🔮 Future Enhancements

### Planned Features
- **Multiple Levels**: Progressive difficulty with different brick layouts
- **Power-up Varieties**: Different types of bonuses (multi-ball, bigger paddle, etc.)
- **Sound Effects**: Audio feedback for collisions and achievements
- **Particle Effects**: Visual flair for brick destruction and power-up collection
- **High Score System**: Local storage for best scores
- **Mobile Support**: Touch controls for mobile devices

### Technical Improvements
- **Webpack Build System**: Module bundling and optimization
- **TypeScript**: Enhanced type safety and development experience
- **Unit Tests**: Automated testing for game logic
- **Performance Monitoring**: FPS tracking and optimization

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines
- Follow existing code style and conventions
- Test thoroughly on multiple browsers
- Update documentation for new features
- Keep commits focused and descriptive

## 📝 License

This project is open source and available under the [MIT License](https://opensource.org/licenses/MIT).

## 🎯 Game Statistics

- **Total Bricks**: 50 (5 rows × 10 columns)
- **Starting Lives**: 3
- **Base Points per Brick**: 10
- **Bonus Points per Power-up**: 20
- **Power-up Spawn Rate**: 30%
- **Maximum Possible Score**: Unlimited (due to power-ups)

---

**Enjoy playing Brick Breaker! 🎮**

*Built with ❤️ using HTML5 Canvas and JavaScript*