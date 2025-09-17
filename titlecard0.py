#!/usr/bin/env python3
"""
Ultra Mario 3D 1.0x
Flames Co. Build - Mario 64 Infdev Style Start Menu
With 3D Mario Head Feature
Built with Ursina Engine
"""

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import math
import random
import time as pytime

# Initialize the app
app = Ursina(
    title='Ultra Mario 3D 1.0x - Flames Co. Infdev Build',
    borderless=False,
    fullscreen=False,
    vsync=True,
    development_mode=False
)

# Color palette - N64/Mario 64 inspired
MARIO_RED = color.rgb(230, 0, 18)
MARIO_BLUE = color.rgb(0, 92, 170)
MARIO_YELLOW = color.rgb(255, 219, 88)
MARIO_BROWN = color.rgb(115, 61, 0)
MARIO_SKIN = color.rgb(242, 195, 162)
SKY_BLUE = color.rgb(100, 149, 237)
CASTLE_GRAY = color.rgb(128, 128, 128)

# Game state
game_state = {
    'menu_active': True,
    'game_started': False,
    'mario_head_active': True,
    'selected_option': 0
}

# Configure window
window.color = SKY_BLUE
window.exit_button.visible = False
window.fps_counter.enabled = False

class MarioHead(Entity):
    """3D Mario head that reacts to cursor like in SM64"""
    def __init__(self):
        super().__init__(
            parent=scene,
            position=(0, 0, 0),
            scale=1.5
        )
        
        # Main head (sphere)
        self.head = Entity(
            parent=self,
            model='sphere',
            color=MARIO_SKIN,
            scale=1
        )
        
        # Hat (cone-ish shape using scaled sphere)
        self.hat = Entity(
            parent=self,
            model='sphere',
            color=MARIO_RED,
            position=(0, 0.5, 0),
            scale=(1.1, 0.6, 1.1)
        )
        
        # Hat brim
        self.hat_brim = Entity(
            parent=self,
            model='cube',
            color=MARIO_RED,
            position=(0, 0.3, 0.2),
            scale=(1.4, 0.1, 0.7)
        )
        
        # Eyes
        self.left_eye = Entity(
            parent=self,
            model='sphere',
            color=color.white,
            position=(-0.25, 0.15, 0.45),
            scale=0.25
        )
        
        self.right_eye = Entity(
            parent=self,
            model='sphere',
            color=color.white,
            position=(0.25, 0.15, 0.45),
            scale=0.25
        )
        
        # Eye pupils
        self.left_pupil = Entity(
            parent=self,
            model='sphere',
            color=color.black,
            position=(-0.25, 0.15, 0.55),
            scale=0.12
        )
        
        self.right_pupil = Entity(
            parent=self,
            model='sphere',
            color=color.black,
            position=(0.25, 0.15, 0.55),
            scale=0.12
        )
        
        # Nose
        self.nose = Entity(
            parent=self,
            model='sphere',
            color=MARIO_SKIN,
            position=(0, -0.05, 0.5),
            scale=(0.35, 0.4, 0.4)
        )
        
        # Mustache (two parts)
        self.mustache_left = Entity(
            parent=self,
            model='cube',
            color=MARIO_BROWN,
            position=(-0.2, -0.15, 0.45),
            scale=(0.4, 0.15, 0.2),
            rotation=(0, 0, 15)
        )
        
        self.mustache_right = Entity(
            parent=self,
            model='cube',
            color=MARIO_BROWN,
            position=(0.2, -0.15, 0.45),
            scale=(0.4, 0.15, 0.2),
            rotation=(0, 0, -15)
        )
        
        # M on hat
        self.m_logo = Text(
            'M',
            parent=self,
            position=(0, 0.5, 0.56),
            scale=5,
            color=color.white,
            origin=(0, 0)
        )
        
        # Animation variables
        self.base_rotation = Vec3(0, 0, 0)
        self.target_rotation = Vec3(0, 0, 0)
        self.blink_timer = 0
        self.blink_duration = 0.1
        self.next_blink = random.uniform(2, 5)
        
        # Interaction sounds placeholder
        self.last_interaction = 0
        
    def update(self):
        if not game_state['mario_head_active']:
            return
            
        # Follow cursor smoothly
        if mouse.point:
            # Calculate rotation based on mouse position
            target_y = (mouse.x - 0.5) * 60  # Horizontal rotation
            target_x = -(mouse.y - 0.5) * 40  # Vertical rotation
            
            self.target_rotation = Vec3(target_x, target_y, 0)
            
            # Smooth rotation
            self.rotation_x += (self.target_rotation.x - self.rotation_x) * 5 * time.dt
            self.rotation_y += (self.target_rotation.y - self.rotation_y) * 5 * time.dt
        
        # Blinking animation
        self.blink_timer += time.dt
        if self.blink_timer >= self.next_blink:
            # Blink
            self.left_eye.scale_y = 0.05
            self.right_eye.scale_y = 0.05
            self.left_pupil.visible = False
            self.right_pupil.visible = False
            
            # Schedule unblink
            invoke(self.unblink, delay=self.blink_duration)
            
            self.blink_timer = 0
            self.next_blink = random.uniform(2, 5)
    
    def unblink(self):
        self.left_eye.scale_y = 0.25
        self.right_eye.scale_y = 0.25
        self.left_pupil.visible = True
        self.right_pupil.visible = True
    
    def input(self, key):
        if not game_state['mario_head_active']:
            return
            
        # Interact with Mario's face on click
        if key == 'left mouse down':
            if mouse.hovered_entity in [self.head, self.nose, self.mustache_left, self.mustache_right]:
                # Make Mario react
                self.react_to_click()
    
    def react_to_click(self):
        # Simple reaction - stretch face
        current_time = pytime.time()
        if current_time - self.last_interaction > 0.5:
            # Random reaction
            reactions = [
                lambda: self.head.animate_scale(1.2, duration=0.1),
                lambda: self.nose.animate_scale((0.5, 0.5, 0.6), duration=0.1),
                lambda: self.shake_head(),
            ]
            random.choice(reactions)()
            
            # Reset after animation
            invoke(self.reset_face, delay=0.2)
            
            self.last_interaction = current_time
            print("♪ Boing! ♪")
    
    def shake_head(self):
        self.animate_rotation((self.rotation_x, self.rotation_y, 10), duration=0.05)
        invoke(lambda: self.animate_rotation((self.rotation_x, self.rotation_y, -10), duration=0.05), delay=0.05)
        invoke(lambda: self.animate_rotation((self.rotation_x, self.rotation_y, 0), duration=0.05), delay=0.1)
    
    def reset_face(self):
        self.head.scale = 1
        self.nose.scale = (0.35, 0.4, 0.4)

class Mario64Menu(Entity):
    """Main menu in Mario 64 style"""
    def __init__(self):
        super().__init__(parent=camera.ui)
        
        # Title text
        self.title = Text(
            'ULTRA MARIO 3D',
            parent=self,
            position=(0, 0.38),
            scale=4,
            color=MARIO_RED,
            origin=(0, 0)
        )
        
        # Version text
        self.version = Text(
            '1.0X INFDEV BUILD',
            parent=self,
            position=(0, 0.31),
            scale=1.5,
            color=MARIO_YELLOW,
            origin=(0, 0)
        )
        
        # Subtitle
        self.subtitle = Text(
            'FLAMES CO. × NINTENDO',
            parent=self,
            position=(0, 0.26),
            scale=1,
            color=color.white,
            origin=(0, 0)
        )
        
        # File select boxes (Mario 64 style)
        self.file_slots = []
        self.selected_slot = 0
        
        slot_names = [
            'NEW GAME',
            'CONTINUE',
            'OPTIONS',
            'EXIT'
        ]
        
        for i, name in enumerate(slot_names):
            y_pos = 0.05 - (i * 0.12)
            
            # Slot background
            slot_bg = Entity(
                parent=self,
                model='quad',
                color=color.rgba(0, 0, 0, 0.5),
                scale=(0.4, 0.08, 1),
                position=(0, y_pos, 1)
            )
            
            # Slot text
            slot_text = Text(
                name,
                parent=self,
                position=(0, y_pos),
                scale=1.5,
                color=color.white,
                origin=(0, 0)
            )
            
            # Star counter (for continue option)
            star_text = None
            if name == 'CONTINUE':
                star_text = Text(
                    '★ × 0',
                    parent=self,
                    position=(0.25, y_pos),
                    scale=1,
                    color=MARIO_YELLOW,
                    origin=(0, 0)
                )
            
            self.file_slots.append({
                'bg': slot_bg,
                'text': slot_text,
                'stars': star_text,
                'position': y_pos,
                'name': name
            })
        
        # Selection star cursor
        self.cursor = Text(
            '★',
            parent=self,
            position=(-0.25, 0.05),
            scale=2,
            color=MARIO_YELLOW,
            origin=(0, 0)
        )
        
        # Instructions
        self.instructions = Text(
            'Press FACE BUTTONS to select',
            parent=self,
            position=(0, -0.35),
            scale=1,
            color=color.white,
            origin=(0, 0)
        )
        
        # Controls hint
        self.controls = Text(
            '↑↓: Navigate  |  ENTER: Select  |  Click Mario!',
            parent=self,
            position=(0, -0.4),
            scale=0.8,
            color=color.gray,
            origin=(0, 0)
        )
        
        # Copyright
        self.copyright = Text(
            '© 1996-2024 Nintendo / Flames Co.',
            parent=self,
            position=(0, -0.46),
            scale=0.7,
            color=color.white,
            origin=(0, 0)
        )
        
        # Decorative stars
        self.create_background_stars()
        
        # Animation timers
        self.animation_timer = 0
        
    def create_background_stars(self):
        """Create animated background stars"""
        self.bg_stars = []
        for i in range(8):
            star = Text(
                '★',
                parent=self,
                position=(random.uniform(-0.5, 0.5), random.uniform(-0.3, 0.3)),
                scale=random.uniform(0.5, 1.5),
                color=color.rgba(255, 255, 255, 0.3),
                origin=(0, 0),
                z=10
            )
            star.base_y = star.y
            star.speed = random.uniform(0.5, 2)
            star.offset = random.uniform(0, math.pi * 2)
            self.bg_stars.append(star)
    
    def input(self, key):
        if not game_state['menu_active']:
            return
            
        if key == 'up arrow':
            self.selected_slot = max(0, self.selected_slot - 1)
            self.update_cursor()
            print("♪ Menu blip ♪")
            
        elif key == 'down arrow':
            self.selected_slot = min(len(self.file_slots) - 1, self.selected_slot + 1)
            self.update_cursor()
            print("♪ Menu blip ♪")
            
        elif key in ['enter', 'space']:
            self.select_option()
    
    def update_cursor(self):
        """Update cursor position"""
        self.cursor.y = self.file_slots[self.selected_slot]['position']
        
        # Highlight selected
        for i, slot in enumerate(self.file_slots):
            if i == self.selected_slot:
                slot['bg'].color = color.rgba(255, 255, 0, 0.3)
                slot['text'].scale = 1.6
            else:
                slot['bg'].color = color.rgba(0, 0, 0, 0.5)
                slot['text'].scale = 1.5
    
    def select_option(self):
        """Handle option selection"""
        option = self.file_slots[self.selected_slot]['name']
        
        if option == 'NEW GAME':
            self.start_game()
        elif option == 'CONTINUE':
            print("No save file found! Starting new game...")
            self.start_game()
        elif option == 'OPTIONS':
            print("Options menu not yet implemented")
        elif option == 'EXIT':
            print("Thank you so much for playing my game!")
            invoke(application.quit, delay=1)
    
    def start_game(self):
        """Start the game with transition"""
        print("♪ Let's-a-go! ♪")
        
        # Create fade transition
        fade = Entity(
            parent=camera.ui,
            model='quad',
            color=color.rgba(0, 0, 0, 0),
            scale=3,
            z=-1
        )
        
        # Fade to black
        fade.animate_color(color.black, duration=1)
        
        # Start game after fade
        invoke(self.launch_game, delay=1)
        invoke(lambda: destroy(fade), delay=2)
    
    def launch_game(self):
        """Actually start the game"""
        game_state['menu_active'] = False
        game_state['game_started'] = True
        game_state['mario_head_active'] = False
        
        # Hide menu
        self.enabled = False
        mario_head.enabled = False
        
        # Enable game elements
        player.enabled = True
        game_world.enabled = True
        hud.enabled = True
        
        # Change environment
        window.color = SKY_BLUE
        window.fps_counter.enabled = True
        
        print("Game started!")
        print("♪ Doo doo doo, doo doo DOO! ♪")
    
    def update(self):
        if not game_state['menu_active']:
            return
        
        self.animation_timer += time.dt
        
        # Animate cursor
        self.cursor.x = -0.25 + math.sin(self.animation_timer * 3) * 0.02
        self.cursor.rotation_z = math.sin(self.animation_timer * 2) * 10
        
        # Animate title
        pulse = (math.sin(self.animation_timer * 2) + 1) / 2
        self.title.scale = 4 + pulse * 0.2
        
        # Animate background stars
        for star in self.bg_stars:
            star.y = star.base_y + math.sin(self.animation_timer * star.speed + star.offset) * 0.02
            star.rotation_z = self.animation_timer * 50 * star.speed

class GameWorld(Entity):
    """Simple game world for testing"""
    def __init__(self):
        super().__init__(enabled=False)
        
        # Ground
        self.ground = Entity(
            model='cube',
            color=color.green,
            scale=(50, 1, 50),
            position=(0, -2, 0),
            texture='white_cube',
            collider='box'
        )
        
        # Castle placeholder
        self.castle = Entity(
            model='cube',
            color=CASTLE_GRAY,
            scale=(10, 15, 10),
            position=(0, 5, -20),
            texture='white_cube'
        )
        
        # Some platforms
        for i in range(5):
            platform = Entity(
                model='cube',
                color=color.brown,
                scale=(3, 0.5, 3),
                position=(random.uniform(-20, 20), random.uniform(0, 5), random.uniform(-20, 20)),
                texture='white_cube',
                collider='box'
            )

class GameHUD(Entity):
    """In-game HUD"""
    def __init__(self):
        super().__init__(parent=camera.ui, enabled=False)
        
        # Power meter placeholder
        self.power_text = Text(
            'POWER',
            position=(-0.85, 0.45),
            scale=1,
            color=color.white
        )
        
        # Star counter
        self.star_counter = Text(
            '★ × 0',
            position=(0.8, 0.45),
            scale=1.5,
            color=MARIO_YELLOW
        )
        
        # Coin counter
        self.coin_counter = Text(
            '© × 0',
            position=(0.8, 0.4),
            scale=1.2,
            color=MARIO_YELLOW
        )
        
        # Lives
        self.lives = Text(
            'MARIO × 4',
            position=(-0.85, 0.4),
            scale=1,
            color=MARIO_RED
        )

# Create game objects
mario_head = MarioHead()
menu = Mario64Menu()
player = FirstPersonController(
    enabled=False,
    speed=8,
    jump_height=3
)
game_world = GameWorld()
hud = GameHUD()

# Camera setup
camera.fov = 70

# Initial camera position for menu
camera.position = (0, 0, 5)
camera.rotation = (0, 0, 0)

# Sky
sky = Sky(color=SKY_BLUE)

def update():
    """Main update loop"""
    # Return to menu with ESC
    if held_keys['escape'] and game_state['game_started']:
        return_to_menu()

def return_to_menu():
    """Return to main menu"""
    game_state['menu_active'] = True
    game_state['game_started'] = False
    game_state['mario_head_active'] = True
    
    # Show menu elements
    menu.enabled = True
    mario_head.enabled = True
    
    # Hide game elements
    player.enabled = False
    game_world.enabled = False
    hud.enabled = False
    
    # Reset camera
    camera.position = (0, 0, 5)
    camera.rotation = (0, 0, 0)
    
    # Reset window
    window.fps_counter.enabled = False
    
    print("Returned to menu")

def input(key):
    """Global input handler"""
    # Debug commands
    if key == 'f1':
        window.fps_counter.enabled = not window.fps_counter.enabled
    elif key == 'f2':
        print(f"Mario Head Active: {game_state['mario_head_active']}")
        print(f"Menu Active: {game_state['menu_active']}")
        print(f"Game Started: {game_state['game_started']}")

# ASCII art startup
print("""
╔════════════════════════════════════════════════════╗
║                                                    ║
║          ULTRA MARIO 3D 1.0X                      ║
║                                                    ║
║            ⭐ INFDEV BUILD ⭐                      ║
║                                                    ║
║         FLAMES CO. × NINTENDO                     ║
║                                                    ║
║     IT'S-A ME, MARIO! WAHOO!                     ║
║                                                    ║
╚════════════════════════════════════════════════════╝
""")
print("♪ Super Mario 64 Title Theme ♪")
print("Controls:")
print("  • ↑↓ - Navigate menu")
print("  • ENTER - Select option")
print("  • Click on Mario's face to interact!")
print("  • ESC - Return to menu (in-game)")
print("  • F1 - Toggle FPS counter")
print("  • F2 - Debug info")
print("-" * 55)

# Run the application
app.run()
