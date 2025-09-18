#!/usr/bin/env python3
"""
Ultra Mario 64 - STABLE EDITION
Optimized for performance and stability
All areas working without crashes
"""

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import math
import random

# Initialize app with optimized settings
app = Ursina(
    title='Ultra Mario 64 - Stable Edition',
    borderless=False,
    fullscreen=False,
    vsync=True,
    development_mode=False,
    size=(1280, 720)
)

# Optimize texture loading
Text.default_resolution = 1080 * Text.size

# Color constants
MARIO_RED = color.rgb(230, 0, 18)
MARIO_BLUE = color.rgb(0, 92, 170)
MARIO_YELLOW = color.rgb(255, 219, 88)
SKY_BLUE = color.rgb(100, 149, 237)

# Game state
game_state = {
    'menu_active': True,
    'game_started': False,
    'current_area': 'menu',
    'stars_collected': 0,
    'coins': 0,
    'lives': 4,
    'current_course': None
}

# Set window properties
window.color = SKY_BLUE
window.fps_counter.enabled = False

class SimplifiedMarioHead(Entity):
    """Simplified Mario head for menu - less entities"""
    def __init__(self):
        super().__init__(
            model='sphere',
            color=color.rgb(242, 195, 162),
            scale=1.5,
            position=(0, 0, 0)
        )
        
        # Simple hat
        self.hat = Entity(
            parent=self,
            model='sphere',
            color=MARIO_RED,
            position=(0, 0.5, 0),
            scale=(1.1, 0.6, 1.1)
        )
        
        # Simple M logo
        self.logo = Text(
            'M',
            parent=self,
            position=(0, 0.5, 0.55),
            scale=5,
            color=color.white
        )
        
    def update(self):
        # Simple rotation following mouse
        if mouse.x:
            self.rotation_y = (mouse.x - 0.5) * 60
            self.rotation_x = -(mouse.y - 0.5) * 30

class SimplifiedMenu(Entity):
    """Simplified menu system"""
    def __init__(self):
        super().__init__(parent=camera.ui)
        
        self.title = Text(
            'ULTRA MARIO 64',
            position=(0, 0.35),
            scale=3,
            color=MARIO_RED,
            origin=(0, 0)
        )
        
        self.subtitle = Text(
            'STABLE EDITION',
            position=(0, 0.28),
            scale=1.5,
            color=MARIO_YELLOW,
            origin=(0, 0)
        )
        
        # Menu options
        self.options = []
        self.selected = 0
        
        menu_items = ['START GAME', 'CONTINUE', 'EXIT']
        
        for i, item in enumerate(menu_items):
            option = Text(
                item,
                position=(0, 0.05 - i * 0.1),
                scale=1.5,
                color=color.white,
                origin=(0, 0)
            )
            self.options.append(option)
        
        # Selection indicator
        self.cursor = Text(
            '►',
            position=(-0.15, 0.05),
            scale=2,
            color=MARIO_YELLOW,
            origin=(0, 0)
        )
        
        self.controls = Text(
            'Arrow Keys: Navigate | Enter: Select',
            position=(0, -0.4),
            scale=0.8,
            color=color.gray,
            origin=(0, 0)
        )
    
    def input(self, key):
        if not game_state['menu_active']:
            return
            
        if key == 'down arrow':
            self.selected = min(self.selected + 1, len(self.options) - 1)
            self.update_cursor()
        elif key == 'up arrow':
            self.selected = max(self.selected - 1, 0)
            self.update_cursor()
        elif key == 'enter':
            self.select_option()
    
    def update_cursor(self):
        self.cursor.y = 0.05 - self.selected * 0.1
        
        # Highlight selected
        for i, opt in enumerate(self.options):
            opt.color = MARIO_YELLOW if i == self.selected else color.white
    
    def select_option(self):
        if self.selected == 0:  # Start Game
            self.start_game()
        elif self.selected == 1:  # Continue
            self.start_game()
        elif self.selected == 2:  # Exit
            application.quit()
    
    def start_game(self):
        game_state['menu_active'] = False
        game_state['game_started'] = True
        game_state['current_area'] = 'castle_grounds'
        
        self.enabled = False
        mario_head.enabled = False
        
        # Enable game elements
        player.enabled = True
        castle.enabled = True
        hud.enabled = True
        
        # Position player
        player.position = Vec3(0, 1, 0)
        
        print("Game Started! Welcome to Peach's Castle!")

class OptimizedCastle(Entity):
    """Optimized castle with fewer entities"""
    def __init__(self):
        super().__init__(enabled=False)
        
        # Castle grounds
        self.ground = Entity(
            parent=self,
            model='cube',
            color=color.green,
            scale=(100, 1, 100),
            position=(0, -0.5, 0),
            texture='white_cube',
            collider='box'
        )
        
        # Main castle building (simplified)
        self.castle_building = Entity(
            parent=self,
            model='cube',
            color=color.rgb(180, 120, 80),
            scale=(30, 30, 20),
            position=(0, 15, -30),
            texture='white_cube',
            collider='box'
        )
        
        # Castle entrance
        self.entrance = Entity(
            parent=self,
            model='cube',
            color=color.dark_gray,
            scale=(4, 6, 1),
            position=(0, 3, -19),
            collider='box'
        )
        
        # Create course paintings
        self.create_paintings()
        
        # Simple trees
        for i in range(10):
            tree = Entity(
                parent=self,
                model='cube',
                color=color.brown,
                scale=(1, 5, 1),
                position=(
                    random.uniform(-40, 40),
                    2.5,
                    random.uniform(-40, 40)
                ),
                collider='box'
            )
            
            leaves = Entity(
                parent=tree,
                model='sphere',
                color=color.green,
                scale=(3, 2, 3),
                position=(0, 0.6, 0)
            )
    
    def create_paintings(self):
        """Create course entrance paintings"""
        self.paintings = []
        
        # Bob-omb Battlefield
        painting1 = CourseEntrance(
            name='BOB-OMB\nBATTLEFIELD',
            course_id='bob_omb',
            position=(-10, 3, -19.5),
            color=color.green,
            parent=self
        )
        self.paintings.append(painting1)
        
        # Whomp's Fortress
        painting2 = CourseEntrance(
            name="WHOMP'S\nFORTRESS",
            course_id='whomps',
            position=(10, 3, -19.5),
            color=color.brown,
            parent=self
        )
        self.paintings.append(painting2)
        
        # Cool Cool Mountain
        painting3 = CourseEntrance(
            name='COOL COOL\nMOUNTAIN',
            course_id='cool_cool',
            position=(-15, 3, -25),
            rotation_y=90,
            color=color.white,
            parent=self
        )
        self.paintings.append(painting3)
        
        # Jolly Roger Bay
        painting4 = CourseEntrance(
            name='JOLLY ROGER\nBAY',
            course_id='jolly_roger',
            position=(15, 3, -25),
            rotation_y=-90,
            color=color.blue,
            parent=self
        )
        self.paintings.append(painting4)
        
        # Bowser Stage
        painting5 = CourseEntrance(
            name='BOWSER\nDARK WORLD',
            course_id='bowser1',
            position=(0, 8, -29.5),
            color=color.red,
            parent=self
        )
        self.paintings.append(painting5)

class CourseEntrance(Entity):
    """Optimized painting entrance"""
    def __init__(self, name, course_id, **kwargs):
        super().__init__(
            model='cube',
            scale=(3, 4, 0.2),
            collider='box',
            **kwargs
        )
        
        self.course_id = course_id
        self.course_name = name
        
        # Simple text label
        self.label = Text(
            name,
            parent=self,
            position=(0, 0, -0.11),
            scale=6,
            color=color.white,
            origin=(0, 0)
        )
        
        # Ripple effect
        self.ripple_time = 0
        self.is_rippling = False
        
    def update(self):
        if self.is_rippling:
            self.ripple_time += time.dt * 5
            self.scale_x = 3 + math.sin(self.ripple_time) * 0.1
            self.scale_y = 4 + math.cos(self.ripple_time) * 0.1
            
            if self.ripple_time > math.pi * 2:
                self.is_rippling = False
                self.ripple_time = 0
                self.scale = (3, 4, 0.2)

class SimpleCourse(Entity):
    """Base class for simplified courses"""
    def __init__(self, name):
        super().__init__(enabled=False)
        self.course_name = name
        
        # Basic ground
        self.ground = Entity(
            parent=self,
            model='cube',
            color=color.green,
            scale=(60, 1, 60),
            position=(0, -0.5, 0),
            texture='white_cube',
            collider='box'
        )
        
        # Add some platforms
        self.create_platforms()
        
        # Add stars
        self.create_stars()
        
        # Exit portal
        self.exit_portal = Entity(
            parent=self,
            model='cube',
            color=color.rgba(255, 255, 0, 128),
            scale=(2, 3, 0.5),
            position=(0, 1.5, 25),
            collider='box'
        )
        
        exit_text = Text(
            'EXIT',
            parent=self.exit_portal,
            position=(0, 0, -0.3),
            scale=8,
            color=color.white,
            origin=(0, 0)
        )
    
    def create_platforms(self):
        # Create some simple platforms
        for i in range(5):
            platform = Entity(
                parent=self,
                model='cube',
                color=color.brown,
                scale=(5, 1, 5),
                position=(
                    random.uniform(-20, 20),
                    random.uniform(1, 8),
                    random.uniform(-20, 20)
                ),
                texture='white_cube',
                collider='box'
            )
    
    def create_stars(self):
        # Add collectible stars
        self.stars = []
        for i in range(3):
            star = SimpleStar(
                position=(
                    random.uniform(-20, 20),
                    random.uniform(2, 10),
                    random.uniform(-20, 20)
                ),
                parent=self
            )
            self.stars.append(star)

class BobOmbBattlefield(SimpleCourse):
    """Simplified Bob-omb Battlefield"""
    def __init__(self):
        super().__init__("Bob-omb Battlefield")
        
        # Mountain in center
        self.mountain = Entity(
            parent=self,
            model='cone',
            color=color.brown,
            scale=(15, 20, 15),
            position=(0, 10, 0),
            collider='box'
        )
        
        # Some cannons
        for pos in [(15, 0, 15), (-15, 0, -15)]:
            cannon = Entity(
                parent=self,
                model='cylinder',
                color=color.black,
                scale=(2, 3, 2),
                position=pos,
                rotation=(30, 0, 0),
                collider='box'
            )
        
        # Simple enemies (just decorative spheres)
        for i in range(5):
            bobomb = Entity(
                parent=self,
                model='sphere',
                color=color.black,
                scale=1,
                position=(
                    random.uniform(-20, 20),
                    0.5,
                    random.uniform(-20, 20)
                )
            )

class WhompsFortress(SimpleCourse):
    """Simplified Whomp's Fortress"""
    def __init__(self):
        super().__init__("Whomp's Fortress")
        
        # Stone fortress
        self.fortress = Entity(
            parent=self,
            model='cube',
            color=color.gray,
            scale=(20, 15, 20),
            position=(0, 7.5, 0),
            texture='white_cube',
            collider='box'
        )
        
        # Tower
        self.tower = Entity(
            parent=self,
            model='cylinder',
            color=color.gray,
            scale=(5, 25, 5),
            position=(0, 12.5, -15),
            collider='box'
        )

class CoolCoolMountain(SimpleCourse):
    """Simplified Cool Cool Mountain"""
    def __init__(self):
        super().__init__("Cool Cool Mountain")
        
        # Snow ground
        self.ground.color = color.white
        
        # Mountain
        self.mountain = Entity(
            parent=self,
            model='cone',
            color=color.white,
            scale=(20, 30, 20),
            position=(0, 15, 0),
            collider='box'
        )
        
        # Slide entrance
        self.cabin = Entity(
            parent=self,
            model='cube',
            color=color.brown,
            scale=(5, 4, 5),
            position=(0, 25, 0),
            collider='box'
        )

class JollyRogerBay(SimpleCourse):
    """Simplified Jolly Roger Bay"""
    def __init__(self):
        super().__init__("Jolly Roger Bay")
        
        # Water effect
        self.ground.color = color.rgba(0, 100, 200, 128)
        
        # Sunken ship
        self.ship = Entity(
            parent=self,
            model='cube',
            color=color.brown,
            scale=(10, 5, 20),
            position=(0, 2, 0),
            rotation=(0, 0, 15),
            collider='box'
        )

class BowserStage(SimpleCourse):
    """Simplified Bowser Stage"""
    def __init__(self):
        super().__init__("Bowser's Dark World")
        
        # Dark platform
        self.ground.color = color.dark_gray
        self.ground.scale = (30, 1, 30)
        
        # Boss arena
        self.arena = Entity(
            parent=self,
            model='cylinder',
            color=color.gray,
            scale=(15, 0.5, 15),
            position=(0, 0, 0),
            collider='box'
        )
        
        # Simple Bowser
        self.bowser = Entity(
            parent=self,
            model='sphere',
            color=color.rgb(200, 150, 0),
            scale=(3, 4, 3),
            position=(0, 2, -8)
        )
        
        # Bowser shell
        shell = Entity(
            parent=self.bowser,
            model='sphere',
            color=color.green,
            scale=(1.2, 1.1, 1.3),
            position=(0, 0, -0.3)
        )

class SimpleStar(Entity):
    """Simple collectible star"""
    def __init__(self, **kwargs):
        super().__init__(
            model='sphere',
            color=MARIO_YELLOW,
            scale=1,
            **kwargs
        )
        
        self.collected = False
        
    def update(self):
        if not self.collected:
            self.rotation_y += 100 * time.dt
            self.y += math.sin(time.time() * 2) * 0.01

class SimpleHUD(Entity):
    """Simplified HUD"""
    def __init__(self):
        super().__init__(parent=camera.ui, enabled=False)
        
        # Star counter
        self.star_text = Text(
            f'★ × {game_state["stars_collected"]}',
            position=(0.8, 0.45),
            scale=1.5,
            color=MARIO_YELLOW
        )
        
        # Coin counter
        self.coin_text = Text(
            f'© × {game_state["coins"]}',
            position=(0.8, 0.4),
            scale=1.2,
            color=MARIO_YELLOW
        )
        
        # Lives
        self.lives_text = Text(
            f'MARIO × {game_state["lives"]}',
            position=(-0.8, 0.45),
            scale=1,
            color=MARIO_RED
        )
        
        # Current area
        self.area_text = Text(
            '',
            position=(0, 0.35),
            scale=2,
            color=color.white
        )
    
    def update_display(self):
        self.star_text.text = f'★ × {game_state["stars_collected"]}'
        self.coin_text.text = f'© × {game_state["coins"]}'
        self.lives_text.text = f'MARIO × {game_state["lives"]}'
    
    def show_area(self, name):
        self.area_text.text = name
        self.area_text.enabled = True
        invoke(setattr, self.area_text, 'enabled', False, delay=3)

class MarioController(FirstPersonController):
    """Simplified Mario controller"""
    def __init__(self):
        super().__init__(
            speed=8,
            jump_height=2,
            jump_duration=0.3,
            enabled=False
        )
        
        self.jump_count = 0
        self.last_jump_time = 0
        
    def input(self, key):
        super().input(key)
        
        # Triple jump timing
        if key == 'space':
            current_time = time.time()
            if current_time - self.last_jump_time < 0.5:
                self.jump_count += 1
                if self.jump_count >= 3:
                    self.jump_height = 4
                    print("Triple Jump!")
                    self.jump_count = 0
            else:
                self.jump_count = 1
                self.jump_height = 2
            self.last_jump_time = current_time

# Create game objects
print("Loading game objects...")
mario_head = SimplifiedMarioHead()
menu = SimplifiedMenu()
player = MarioController()
castle = OptimizedCastle()
hud = SimpleHUD()

# Course instances (created on demand)
courses = {}

# Camera setup
camera.fov = 60
camera.position = (0, 0, 5)

# Simple sky
sky = Entity(
    model='sphere',
    color=SKY_BLUE,
    scale=500,
    double_sided=True
)

def load_course(course_id):
    """Load a course on demand"""
    if course_id not in courses:
        print(f"Loading {course_id}...")
        if course_id == 'bob_omb':
            courses[course_id] = BobOmbBattlefield()
        elif course_id == 'whomps':
            courses[course_id] = WhompsFortress()
        elif course_id == 'cool_cool':
            courses[course_id] = CoolCoolMountain()
        elif course_id == 'jolly_roger':
            courses[course_id] = JollyRogerBay()
        elif course_id == 'bowser1':
            courses[course_id] = BowserStage()
        else:
            courses[course_id] = SimpleCourse(f"Course {course_id}")
    
    return courses[course_id]

def enter_course(course_id):
    """Enter a course"""
    castle.enabled = False
    
    course = load_course(course_id)
    course.enabled = True
    
    game_state['current_course'] = course
    game_state['current_area'] = course_id
    
    player.position = Vec3(0, 2, 0)
    
    hud.show_area(course.course_name)
    print(f"Entered {course.course_name}!")

def exit_course():
    """Exit current course"""
    if game_state['current_course']:
        game_state['current_course'].enabled = False
        game_state['current_course'] = None
    
    castle.enabled = True
    game_state['current_area'] = 'castle_grounds'
    
    player.position = Vec3(0, 1, 0)
    
    print("Returned to castle!")

def update():
    """Main update loop"""
    # Check for painting collisions
    if game_state['game_started'] and castle.enabled:
        for painting in castle.paintings:
            dist = distance(player.position, painting.world_position)
            if dist < 3:
                # Show prompt
                if held_keys['e']:
                    painting.is_rippling = True
                    invoke(enter_course, painting.course_id, delay=0.5)
    
    # Check for exit portal in courses
    if game_state['current_course']:
        course = game_state['current_course']
        if distance(player.position, course.exit_portal.world_position) < 2:
            if held_keys['e']:
                exit_course()
        
        # Check star collection
        for star in course.stars:
            if not star.collected and distance(player.position, star.world_position) < 2:
                star.collected = True
                star.enabled = False
                game_state['stars_collected'] += 1
                hud.update_display()
                print(f"Star collected! Total: {game_state['stars_collected']}")

def input(key):
    """Global input handler"""
    # Return to menu
    if key == 'escape':
        if game_state['game_started']:
            if game_state['current_course']:
                exit_course()
            else:
                # Return to menu
                game_state['menu_active'] = True
                game_state['game_started'] = False
                
                menu.enabled = True
                mario_head.enabled = True
                
                player.enabled = False
                castle.enabled = False
                hud.enabled = False
                
                camera.position = (0, 0, 5)
                camera.rotation = (0, 0, 0)
    
    # Debug keys
    if key == 'f1':
        window.fps_counter.enabled = not window.fps_counter.enabled
    
    if key == 'f2' and game_state['game_started']:
        print(f"Area: {game_state['current_area']}")
        print(f"Stars: {game_state['stars_collected']}")
        print(f"Position: {player.position}")
    
    if key == 'f3' and game_state['game_started']:
        game_state['stars_collected'] += 10
        hud.update_display()
        print(f"Debug: Added 10 stars!")

# Startup message
print("""
═══════════════════════════════════════════════════════════
           ULTRA MARIO 64 - STABLE EDITION
═══════════════════════════════════════════════════════════

CONTROLS:
  • WASD/Arrows - Move
  • Mouse - Look around  
  • SPACE - Jump (Triple jump with timing!)
  • E - Enter paintings / Exit course
  • ESC - Menu/Back
  
DEBUG:
  • F1 - Toggle FPS
  • F2 - Show position
  • F3 - Add stars

COURSES AVAILABLE:
  ★ Bob-omb Battlefield
  ★ Whomp's Fortress  
  ★ Cool Cool Mountain
  ★ Jolly Roger Bay
  ★ Bowser's Dark World

Ready to play!
═══════════════════════════════════════════════════════════
""")

# Run the game
app.run()
