#!/usr/bin/env python3
"""
Samsoft Mario 64 - Peach's Castle Outdoor Area
Built with Ursina Engine - SM64 Engine Style Recreation
IndyCat-Origin Build
"""

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import math

app = Ursina()

# SM64 Color Palette
SKY_BLUE = color.rgb(140, 180, 240)
GRASS_GREEN = color.rgb(34, 177, 76)
CASTLE_WALL = color.rgb(245, 245, 220)
CASTLE_ROOF = color.rgb(220, 60, 60)
WATER_BLUE = color.rgb(64, 164, 223)
PATH_STONE = color.rgb(180, 180, 160)

# Configure window
window.title = 'Samsoft Mario 64 - Peach\'s Castle'
window.borderless = False
window.fullscreen = False
window.exit_button.visible = False
window.fps_counter.enabled = True

# Sky configuration
Sky(color=SKY_BLUE)

# Ground plane with grass texture
ground = Entity(
    model='cube',
    color=GRASS_GREEN,
    scale=(200, 0.5, 200),
    position=(0, -0.25, 0),
    texture='white_cube',
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
        
    def input(self, key):
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

# Ambient lighting
scene.ambient_light = color.rgb(200, 200, 200)

# Add directional light (sun)
sun = DirectionalLight()
sun.look_at(Vec3(1, -1, -1))

# Info text
info_text = Text(
    'WASD: Move | Mouse: Look | Space: Jump | Shift: Long Jump | Ctrl: Ground Pound',
    position=(-0.85, 0.47),
    scale=0.7,
    background=True
)

title_text = Text(
    'Samsoft Mario 64 - Peach\'s Castle',
    position=(-0.3, 0.45),
    scale=1.2,
    color=color.white,
    font='VeraMono.ttf'
)

# Camera bobbing effect
def update():
    # Simple camera bob when moving
    if player.grounded and (held_keys['w'] or held_keys['s'] or held_keys['a'] or held_keys['d']):
        player.camera_pivot.y = 1 + math.sin(time.time() * 10) * 0.05
    else:
        player.camera_pivot.y = lerp(player.camera_pivot.y, 1, time.dt * 5)
    
    # Rotate coins
    for coin in coins:
        coin.rotation_y += 100 * time.dt

# Background music placeholder
print("♪ Peach's Castle theme would play here ♪")
print("Engine: Samsoft Unix Emulator - IndyCat-Origin")
print("Build: CatKernel v0.1 with Ursina hooks")

# Run the application
app.run()
