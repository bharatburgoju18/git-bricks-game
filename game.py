import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Game constants
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
BALL_RADIUS = 8
BRICK_ROWS = 5
BRICK_COLS = 10
BRICK_WIDTH = 75
BRICK_HEIGHT = 20
BRICK_PADDING = 5
BRICK_OFFSET_TOP = 60
POWERUP_WIDTH = 20
POWERUP_HEIGHT = 20
POWERUP_SPEED = 3
POWERUP_SPAWN_CHANCE = 0.3

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 149, 221)
GOLD = (255, 215, 0)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class GameState:
    READY = "ready"
    PLAYING = "playing"
    GAME_OVER = "game_over"
    WON = "won"

class Paddle:
    def __init__(self):
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.x = (CANVAS_WIDTH - self.width) // 2
        self.y = CANVAS_HEIGHT - self.height - 10
        self.speed = 7
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def update_position(self):
        self.rect.x = self.x
        self.rect.y = self.y
    
    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, self.rect)

class Ball:
    def __init__(self):
        self.x = CANVAS_WIDTH // 2
        self.y = CANVAS_HEIGHT - 30
        self.dx = 5
        self.dy = -5
        self.radius = BALL_RADIUS
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, 
                               self.radius * 2, self.radius * 2)
    
    def update_position(self):
        self.rect.center = (int(self.x), int(self.y))
    
    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius)

class Brick:
    def __init__(self, x, y, row):
        self.x = x
        self.y = y
        self.width = BRICK_WIDTH
        self.height = BRICK_HEIGHT
        self.status = 1  # 1 = visible, 0 = destroyed
        self.color = self.get_color_by_row(row)
        self.rect = pygame.Rect(x, y, self.width, self.height)
    
    def get_color_by_row(self, row):
        """Generate rainbow colors similar to HSL in JavaScript"""
        colors = [
            (255, 100, 100),  # Red-ish
            (255, 165, 0),    # Orange
            (255, 255, 0),    # Yellow
            (0, 255, 0),      # Green
            (0, 100, 255),    # Blue
        ]
        return colors[row % len(colors)]
    
    def draw(self, screen):
        if self.status == 1:
            pygame.draw.rect(screen, self.color, self.rect)
            pygame.draw.rect(screen, WHITE, self.rect, 1)  # White border

class PowerUp:
    def __init__(self, x, y):
        self.x = x - POWERUP_WIDTH // 2
        self.y = y
        self.width = POWERUP_WIDTH
        self.height = POWERUP_HEIGHT
        self.speed = POWERUP_SPEED
        self.points = 20
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def update(self):
        self.y += self.speed
        self.rect.y = self.y
    
    def draw(self, screen, font):
        pygame.draw.rect(screen, GOLD, self.rect)
        pygame.draw.rect(screen, ORANGE, self.rect, 2)
        
        # Draw "+20" text
        text = font.render("+20", True, BLACK)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT))
        pygame.display.set_caption("Brick Breaker")
        self.clock = pygame.time.Clock()
        
        # Fonts
        self.large_font = pygame.font.Font(None, 48)
        self.medium_font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 12)
        
        # Game state
        self.state = GameState.READY
        self.score = 0
        self.lives = 3
        self.auto_play = True
        self.control_mode = 'keyboard'
        
        # Game objects
        self.paddle = Paddle()
        self.ball = Ball()
        self.bricks = []
        self.power_ups = []
        
        # Input tracking
        self.keys_pressed = {}
        self.mouse_x = CANVAS_WIDTH // 2
        
        self.init_bricks()
    
    def init_bricks(self):
        """Initialize the brick grid"""
        self.bricks = []
        for c in range(BRICK_COLS):
            column = []
            for r in range(BRICK_ROWS):
                brick_x = (c * (BRICK_WIDTH + BRICK_PADDING)) + BRICK_PADDING
                brick_y = (r * (BRICK_HEIGHT + BRICK_PADDING)) + BRICK_OFFSET_TOP
                brick = Brick(brick_x, brick_y, r)
                column.append(brick)
            self.bricks.append(column)
    
    def draw_bricks(self):
        """Draw all visible bricks"""
        for column in self.bricks:
            for brick in column:
                brick.draw(self.screen)
    
    def draw_score(self):
        """Draw score and lives"""
        score_text = self.medium_font.render(f"Score: {self.score}", True, WHITE)
        lives_text = self.medium_font.render(f"Lives: {self.lives}", True, WHITE)
        
        self.screen.blit(score_text, (10, CANVAS_HEIGHT - 50))
        self.screen.blit(lives_text, (10, CANVAS_HEIGHT - 25))
    
    def draw_auto_play_status(self):
        """Draw auto-play status"""
        color = GREEN if self.auto_play else RED
        status_text = self.small_font.render(f"Auto-play: {'ON' if self.auto_play else 'OFF'} (Press 'A' to toggle)", True, color)
        self.screen.blit(status_text, (10, 10))
    
    def draw_game_message(self, message):
        """Draw overlay message for game states"""
        # Semi-transparent overlay
        overlay = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Main message
        main_text = self.large_font.render(message, True, WHITE)
        main_rect = main_text.get_rect(center=(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2))
        self.screen.blit(main_text, main_rect)
        
        # Instructions
        instruction_text = self.medium_font.render("Press SPACE to start", True, WHITE)
        instruction_rect = instruction_text.get_rect(center=(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2 + 60))
        self.screen.blit(instruction_text, instruction_rect)
    
    def collision_detection(self):
        """Check ball-brick collisions"""
        for column in self.bricks:
            for brick in column:
                if brick.status == 1 and self.ball.rect.colliderect(brick.rect):
                    self.ball.dy = -self.ball.dy
                    brick.status = 0
                    self.score += 10
                    
                    # Spawn power-up with chance
                    if random.random() < POWERUP_SPAWN_CHANCE:
                        self.spawn_power_up(brick.x + brick.width // 2, 
                                          brick.y + brick.height)
                    
                    # Check win condition
                    if self.score == BRICK_ROWS * BRICK_COLS * 10:
                        self.state = GameState.WON
                    
                    return  # Only handle one collision per frame
    
    def move_paddle(self):
        """Handle paddle movement with different control modes"""
        if self.auto_play:
            # AI follows ball
            paddle_center = self.paddle.x + self.paddle.width // 2
            ball_center = self.ball.x
            
            if abs(ball_center - paddle_center) > 5:
                if ball_center > paddle_center and self.paddle.x < CANVAS_WIDTH - self.paddle.width:
                    self.paddle.x += self.paddle.speed
                elif ball_center < paddle_center and self.paddle.x > 0:
                    self.paddle.x -= self.paddle.speed
            
            # Keep paddle in bounds
            self.paddle.x = max(0, min(CANVAS_WIDTH - self.paddle.width, self.paddle.x))
        else:
            # Manual control
            if self.keys_pressed.get(pygame.K_RIGHT, False) and self.paddle.x < CANVAS_WIDTH - self.paddle.width:
                self.paddle.x += self.paddle.speed
                self.control_mode = 'keyboard'
            elif self.keys_pressed.get(pygame.K_LEFT, False) and self.paddle.x > 0:
                self.paddle.x -= self.paddle.speed
                self.control_mode = 'keyboard'
            elif self.control_mode == 'mouse':
                # Mouse control
                self.paddle.x = max(0, min(CANVAS_WIDTH - self.paddle.width, 
                                         self.mouse_x - self.paddle.width // 2))
        
        self.paddle.update_position()
    
    def move_ball(self):
        """Update ball position and handle collisions"""
        self.ball.x += self.ball.dx
        self.ball.y += self.ball.dy
        
        # Wall collisions
        if (self.ball.x + self.ball.dx > CANVAS_WIDTH - self.ball.radius or 
            self.ball.x + self.ball.dx < self.ball.radius):
            self.ball.dx = -self.ball.dx
        
        # Ceiling collision
        if self.ball.y + self.ball.dy < self.ball.radius:
            self.ball.dy = -self.ball.dy
        
        # Floor collision (check paddle hit)
        elif self.ball.y + self.ball.dy > CANVAS_HEIGHT - self.ball.radius:
            if self.ball.rect.colliderect(self.paddle.rect):
                # Calculate angle based on hit position
                hit_pos = (self.ball.x - self.paddle.x) / self.paddle.width
                angle = (hit_pos - 0.5) * math.pi / 3
                speed = math.sqrt(self.ball.dx**2 + self.ball.dy**2)
                self.ball.dx = math.sin(angle) * speed
                self.ball.dy = -math.cos(angle) * speed
            else:
                # Ball missed paddle
                self.lives -= 1
                if self.lives == 0:
                    self.state = GameState.GAME_OVER
                else:
                    self.reset_ball()
        
        self.ball.update_position()
    
    def reset_ball(self):
        """Reset ball to starting position"""
        self.ball.x = CANVAS_WIDTH // 2
        self.ball.y = CANVAS_HEIGHT - 30
        self.ball.dx = 5 * (1 if random.random() > 0.5 else -1)
        self.ball.dy = -5
        self.ball.update_position()
    
    def spawn_power_up(self, x, y):
        """Create a new power-up"""
        power_up = PowerUp(x, y)
        self.power_ups.append(power_up)
    
    def update_power_ups(self):
        """Update power-up positions and remove off-screen ones"""
        for power_up in self.power_ups[:]:  # Copy list to avoid modification during iteration
            power_up.update()
            
            if power_up.y > CANVAS_HEIGHT:
                self.lives -= 1
                self.power_ups.remove(power_up)
                if self.lives == 0:
                    self.state = GameState.GAME_OVER
    
    def check_power_up_collisions(self):
        """Check if paddle caught any power-ups"""
        for power_up in self.power_ups[:]:
            if power_up.rect.colliderect(self.paddle.rect):
                self.score += power_up.points
                self.power_ups.remove(power_up)
    
    def draw_power_ups(self):
        """Draw all power-ups"""
        for power_up in self.power_ups:
            power_up.draw(self.screen, self.small_font)
    
    def reset_game(self):
        """Reset game to initial state"""
        self.score = 0
        self.lives = 3
        self.state = GameState.PLAYING
        self.paddle.x = (CANVAS_WIDTH - PADDLE_WIDTH) // 2
        self.paddle.update_position()
        self.reset_ball()
        self.init_bricks()
        self.power_ups = []
    
    def handle_events(self):
        """Process keyboard and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                self.keys_pressed[event.key] = True
                
                if event.key == pygame.K_SPACE:
                    if self.state != GameState.PLAYING:
                        self.reset_game()
                
                elif event.key == pygame.K_a:
                    self.auto_play = not self.auto_play
                    self.control_mode = 'auto' if self.auto_play else 'keyboard'
                
                elif event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    self.auto_play = False
            
            elif event.type == pygame.KEYUP:
                self.keys_pressed[event.key] = False
            
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_x = event.pos[0]
                if not self.auto_play:
                    self.control_mode = 'mouse'
        
        return True
    
    def draw(self):
        """Draw all game elements"""
        self.screen.fill(BLACK)
        
        self.draw_bricks()
        self.ball.draw(self.screen)
        self.paddle.draw(self.screen)
        self.draw_power_ups()
        self.draw_score()
        self.draw_auto_play_status()
        
        if self.state == GameState.READY:
            self.draw_game_message("BRICK BREAKER")
        elif self.state == GameState.GAME_OVER:
            self.draw_game_message("GAME OVER")
        elif self.state == GameState.WON:
            self.draw_game_message("YOU WIN!")
    
    def update(self):
        """Update game logic"""
        if self.state == GameState.PLAYING:
            self.collision_detection()
            self.move_ball()
            self.move_paddle()
            self.update_power_ups()
            self.check_power_up_collisions()
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            # Handle events
            running = self.handle_events()
            
            # Update game logic
            self.update()
            
            # Draw everything
            self.draw()
            
            pygame.display.flip()
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()

def main():
    """Entry point"""
    game = Game()
    game.run()

if __name__ == "__main__":
    main()