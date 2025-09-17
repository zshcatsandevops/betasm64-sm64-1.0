#!/usr/bin/env python3
"""
Samsoft Mario 64 - Peach's Castle Outdoor Area
Built with Ursina Engine - SM64 Engine Style Recreation
IndyCat-Origin Build
"""

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import math
import time as pytime

# Initialize app with specific settings
app = Ursina(
    title='Samsoft Mario 64 - Peach\'s Castle',
    borderless=False,
    fullscreen=False,
    vsync=True
)

# SM64 Color Palette - using normalized values
SKY_BLUE = color.rgb(140/255, 180/255, 240/255)
GRASS_GREEN = color.rgb(34/255, 177/255, 76/255)
CASTLE_WALL = color.rgb(245/255, 245/255, 220/255)
CASTLE_ROOF = color.rgb(220/255, 60/255, 60/255)
WATER_BLUE = color.rgb(64/255, 164/255, 223/255)
PATH_STONE = color.rgb(180/255, 180/255, 160/255)
MENU_BLUE = color.rgb(48/255, 104/255, 184/255)
MENU_YELLOW = color.rgb(248/255, 248/255, 120/255)

# Configure window
window.color = color.black
window.exit_button.visible = False
window.fps_counter.enabled = False

# Game state management
game_started = False
menu_active = True

# Spaceworld Beta Menu Class
class SpaceworldMenu(Entity):
    def __init__(self):
        super().__init__(parent=camera.ui)
        
        # Dark blue gradient background
        self.bg = Entity(
            parent=self,
            model='quad',
            color=MENU_BLUE,
            scale=(2, 1, 1),
            position=(0, 0, 10)
        )
        
        # Title text - SUPER MARIO 64
        self.title = Text(
            'SUPER MARIO 64',
            parent=self,
            position=(0, 0.35),
            scale=3,
            color=MENU_YELLOW,
            origin=(0, 0)
        )
        
        # Beta version text
        self.beta_text = Text(
            'SHOSHINKAI 1995 DEMO',
            parent=self,
            position=(0, 0.28),
            scale=1,
            color=color.white,
            origin=(0, 0)
        )
        
        # File select header
        self.select_text = Text(
            'SELECT FILE',
            parent=self,
            position=(0, 0.15),
            scale=1.5,
            color=color.white,
            origin=(0, 0)
        )
        
        # File slots
        self.file_slots = []
        self.selected_file = 0
        
        for i in range(4):
            y_pos = 0.05 - (i * 0.12)
            
            # File slot background
            slot_bg = Entity(
                parent=self,
                model='quad',
                color=color.rgba(0, 0, 0, 0.5) if i < 3 else color.rgba(128/255, 0, 0, 0.7),
                scale=(0.5, 0.08, 1),
                position=(0, y_pos, 9)
            )
            
            # File text
            if i < 3:
                file_text = Text(
                    f'FILE {i + 1}  -  NEW',
                    parent=self,
                    position=(0, y_pos),
                    scale=1.2,
                    color=color.white,
                    origin=(0, 0)
                )
                stars_text = Text(
                    '☆ × 0',
                    parent=self,
                    position=(0.2, y_pos),
                    scale=1,
                    color=MENU_YELLOW,
                    origin=(0, 0)
                )
            else:
                file_text = Text(
                    'ERASE FILE',
                    parent=self,
                    position=(0, y_pos),
                    scale=1.2,
                    color=color.rgb(255/255, 128/255, 128/255),
                    origin=(0, 0)
                )
                stars_text = None
            
            self.file_slots.append({
                'bg': slot_bg,
                'text': file_text,
                'stars': stars_text,
                'position': y_pos
            })
        
        # Selection cursor (star)
        self.cursor = Text(
            '▶',
            parent=self,
            position=(-0.28, 0.05),
            scale=1.5,
            color=MENU_YELLOW,
            origin=(0, 0)
        )
        
        # Instructions
        self.instructions = Text(
            'Press ↑↓ to select, ENTER to start',
            parent=self,
            position=(0, -0.4),
            scale=0.8,
            color=color.white,
            origin=(0, 0)
        )
        
        # Nintendo copyright
        self.copyright = Text(
            '© 1995 Nintendo / Samsoft Unix Port',
            parent=self,
            position=(0, -0.47),
            scale=0.6,
            color=color.gray,
            origin=(0, 0)
        )
        
        # Sound effect placeholder
        self.menu_sound = False
        
    def update(self):
        global game_started, menu_active
        
        if not menu_active:
            return
        
        # Animate cursor
        self.cursor.x = -0.28 + math.sin(pytime.time() * 3) * 0.01
        
        # Handle input
        if held_keys['up arrow']:
            self.selected_file = max(0, self.selected_file - 1)
            self.cursor.y = self.file_slots[self.selected_file]['position']
        
        if held_keys['down arrow']:
            self.selected_file = min(3, self.selected_file + 1)
            self.cursor.y = self.file_slots[self.selected_file]['position']
        
        if held_keys['enter'] or held_keys['space']:
            if self.selected_file < 3:  # File selection
                self.start_game()
            else:  # Erase option
                print("Erase function not implemented")
    
    def start_game(self):
        global game_started, menu_active
        
        # Fade out effect
        fade = Entity(
            parent=camera.ui,
            model='quad',
            color=color.black,
            scale=3,
            alpha=0,
            z=-1
        )
        
        # Quick fade animation
        fade.animate_color(color.rgba(0, 0, 0, 1), duration=0.5)
        
        # Hide menu after fade
        invoke(self.hide_menu, delay=0.5)
        
        print(f"Starting File {self.selected_file + 1}")
        print("♪ File select jingle ♪")
    
    def hide_menu(self):
        global game_started, menu_active
        
        # Hide all menu elements
        self.enabled = False
        menu_active = False
        game_started = True
        
        # Show game elements
        window.color = SKY_BLUE
        window.fps_counter.enabled = True
        
        # Enable player controls
        if hasattr(player, 'enabled'):
            player.enabled = True
        
        print("♪ Peach's Castle theme starts ♪")

# Create menu first
menu = SpaceworldMenu()

# Camera setup first
camera.fov = 90

# Sky configuration with texture='sky_default' to avoid white screen
sky = Sky(
    color=SKY_BLUE,
    texture=None
)

# Ground plane with grass texture
ground = Entity(
    model='plane',
    color=GRASS_GREEN,
    scale=(200, 1, 200),
    position=(0, 0, 0),
    texture='grass',
    texture_scale=(40, 40),
    collider='box'
)

# Castle base structure
class PeachCastle(Entity):
    def __init__(self):
        super().__init__()
        
        # Main castle body
        self.main_body = Entity(
            parent=self,
            model='cube',
            color=CASTLE_WALL,
            scale=(20, 25, 18),
            position=(0, 12.5, -30),
            collider='box'
        )
        
        # Central tower
        self.central_tower = Entity(
            parent=self,
            model='cylinder',
            color=CASTLE_WALL,
            scale=(8, 35, 8),
            position=(0, 17.5, -30),
            collider='box'
        )
        
        # Central tower roof (cone)
        self.tower_roof = Entity(
            parent=self,
            model='cone',
            color=CASTLE_ROOF,
            scale=(10, 8, 10),
            position=(0, 39, -30),
            rotation=(0, 0, 0)
        )
        
        # Left tower
        self.left_tower = Entity(
            parent=self,
            model='cylinder',
            color=CASTLE_WALL,
            scale=(6, 28, 6),
            position=(-15, 14, -30),
            collider='box'
        )
        
        # Left tower roof
        self.left_roof = Entity(
            parent=self,
            model='cone',
            color=CASTLE_ROOF,
            scale=(7, 6, 7),
            position=(-15, 30, -30)
        )
        
        # Right tower
        self.right_tower = Entity(
            parent=self,
            model='cylinder',
            color=CASTLE_WALL,
            scale=(6, 28, 6),
            position=(15, 14, -30),
            collider='box'
        )
        
        # Right tower roof
        self.right_roof = Entity(
            parent=self,
            model='cone',
            color=CASTLE_ROOF,
            scale=(7, 6, 7),
            position=(15, 30, -30)
        )
        
        # Castle entrance
        self.entrance = Entity(
            parent=self,
            model='cube',
            color=color.rgb(40, 30, 20),
            scale=(4, 6, 0.5),
            position=(0, 3, -20.5)
        )
        
        # Bridge to castle
        self.bridge = Entity(
            parent=self,
            model='cube',
            color=PATH_STONE,
            scale=(8, 0.3, 20),
            position=(0, 0.15, -10),
            collider='box'
        )
        
        # Decorative windows
        for i in range(3):
            for j in range(2):
                window = Entity(
                    parent=self,
                    model='cube',
                    color=color.rgb(100, 150, 200),
                    scale=(1.5, 2, 0.2),
                    position=(-5 + i*5, 8 + j*6, -20.8)
                )

# Moat around castle
moat = Entity(
    model='cube',
    color=WATER_BLUE,
    scale=(60, 0.1, 60),
    position=(0, -0.05, -30)
)

# Stone path leading to castle
main_path = Entity(
    model='cube',
    color=PATH_STONE,
    scale=(10, 0.2, 40),
    position=(0, 0.1, 0),
    collider='box'
)

# Decorative trees (simple representation)
class Tree(Entity):
    def __init__(self, x, z):
        super().__init__()
        self.trunk = Entity(
            parent=self,
            model='cylinder',
            color=color.rgb(101, 67, 33),
            scale=(1, 5, 1),
            position=(x, 2.5, z)
        )
        self.leaves = Entity(
            parent=self,
            model='sphere',
            color=color.rgb(34, 139, 34),
            scale=(5, 5, 5),
            position=(x, 6, z)
        )

# Place trees around the castle
tree_positions = [
    (-30, -10), (30, -10),
    (-35, -40), (35, -40),
    (-25, -55), (25, -55),
    (-40, 10), (40, 10),
    (-20, 15), (20, 15)
]

for pos in tree_positions:
    Tree(pos[0], pos[1])

# Hills in background
for i in range(5):
    hill = Entity(
        model='sphere',
        color=GRASS_GREEN,
        scale=(20 + i*3, 10 + i*2, 20 + i*3),
        position=(-60 + i*30, -5, -80 - i*10)
    )

# Create small decorative elements
class Coin(Entity):
    def __init__(self, position):
        super().__init__(
            model='cylinder',
            color=color.rgb(255, 215, 0),
            scale=(0.8, 0.1, 0.8),
            position=position,
            rotation=(90, 0, 0)
        )
        self.rotation_speed = 100
    
    def update(self):
        self.rotation_y += self.rotation_speed * time.dt

# Place some coins
coin_positions = [
    (5, 1, 5),
    (-5, 1, 5),
    (0, 1, 10),
    (10, 1, -5),
    (-10, 1, -5)
]

coins = [Coin(pos) for pos in coin_positions]

# Player controller (Mario-style)
class MarioController(FirstPersonController):
    def __init__(self):
        super().__init__(
            speed=8,
            jump_height=3,
            jump_duration=0.4,
            position=(0, 2, 20),
            mouse_sensitivity=Vec2(40, 40)
        )
        self.camera_pivot.y = 1
        self.enabled = False  # Disabled until menu is closed
        
    def input(self, key):
        if not game_started:
            return
        super().input(key)
        
        # Long jump (SM64 style)
        if key == 'shift' and self.grounded:
            self.jump_height = 5
            self.speed = 12
        elif key == 'shift up':
            self.jump_height = 3
            self.speed = 8
        
        # Ground pound
        if key == 'ctrl' and not self.grounded:
            self.y_velocity = -20

# Create castle instance
castle = PeachCastle()

# Create player
player = MarioController()

# Fix lighting - set ambient light first, then directional
scene.ambient_light = Vec4(0.4, 0.4, 0.4, 1.0)

# Add directional light (sun) with proper intensity
sun = DirectionalLight()
sun.look_at(Vec3(1, -1, -1))
sun.color = color.rgb(1, 0.9, 0.8)
sun.intensity = 0.6

# Info text (hidden initially)
info_text = Text(
    'WASD: Move | Mouse: Look | Space: Jump | Shift: Long Jump | Ctrl: Ground Pound',
    position=(-0.85, 0.47),
    scale=0.7,
    background=True,
    enabled=False  # Hidden until game starts
)

title_text = Text(
    'Samsoft Mario 64 - Peach\'s Castle',
    position=(-0.3, 0.45),
    scale=1.2,
    color=color.white,
    font='VeraMono.ttf',
    enabled=False  # Hidden until game starts
)

# Camera bobbing effect
def update():
    global game_started
    
    # Only update game elements if game has started
    if game_started:
        # Enable UI texts if not already enabled
        if not info_text.enabled:
            info_text.enabled = True
            title_text.enabled = True
        
        # Simple camera bob when moving
        if hasattr(player, 'grounded') and player.grounded:
            if held_keys['w'] or held_keys['s'] or held_keys['a'] or held_keys['d']:
                player.camera_pivot.y = 1 + math.sin(pytime.time() * 10) * 0.05
            else:
                player.camera_pivot.y = lerp(player.camera_pivot.y, 1, time.dt * 5)
    
    # ESC to return to menu
    if held_keys['escape'] and game_started:
        return_to_menu()

def return_to_menu():
    global game_started, menu_active
    game_started = False
    menu_active = True
    menu.enabled = True
    player.enabled = False
    info_text.enabled = False
    title_text.enabled = False
    window.color = color.black
    window.fps_counter.enabled = False

# Set background color as fallback
camera.background_color = SKY_BLUE

# Background music placeholder
print("════════════════════════════════════════")
print("  SUPER MARIO 64 - SPACEWORLD 1995     ")
print("  Samsoft Unix Emulator Port           ")
print("  Engine: IndyCat-Origin | CatKernel   ")
print("════════════════════════════════════════")
print("♪ Spaceworld menu theme playing ♪")
print("Use ↑↓ arrows to select, ENTER to start")
print("ESC returns to menu during gameplay")

# Run the application
app.run()
