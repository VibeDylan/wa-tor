from __future__ import annotations
import pygame
from .planet import Planet
from .fish import Fish
from .shark import Shark
from .config import grid_width, grid_height, number_fishes, number_sharks
from .simulation import count_entities, place_entities, move_entities, get_entities
from .database import display_history, archive_simulation, create_database
from pathlib import Path



class WatorGUI:
    def __init__(self, cell_size=20, fps=5):
        self.cell_size = cell_size
        self.fps = fps
        self.width = grid_width
        self.height = grid_height
        
        self.grid_width = self.width * self.cell_size
        self.grid_height = self.height * self.cell_size
        self.menu_width = 250
        self.window_width = self.grid_width + self.menu_width
        self.window_height = self.grid_height

        self.bg_color = (18, 25, 38)  
        self.grid_color = (40, 55, 80)
        self.water_color = (20, 35, 60) 
        self.text_color = (220, 230, 240)
        
        self.menu_bg_color = (30, 40, 55)
        self.button_color = (50, 70, 100)
        self.button_hover_color = (70, 90, 120)  
        self.button_text_color = (220, 230, 240)

        pygame.init()

        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Wa-Tor Simulation")
        self.clock = pygame.time.Clock()

        assets_dir = Path(__file__).parent.parent / "assets"
        fish_sprite_path = assets_dir / "fish_sprite.png"
        shark_sprite_path = assets_dir / "shark_sprite.png"
        
        fish_sprite_raw = pygame.image.load(str(fish_sprite_path))
        shark_sprite_raw = pygame.image.load(str(shark_sprite_path))
        
        self.fish_sprite = pygame.transform.scale(fish_sprite_raw, (self.cell_size, self.cell_size))
        self.shark_sprite = pygame.transform.scale(shark_sprite_raw, (self.cell_size, self.cell_size))

        self.font_text = pygame.font.SysFont(None, 30)
        self.font_menu = pygame.font.SysFont(None, 28)
        self.font_button = pygame.font.SysFont(None, 24)

        self.planet = Planet(self.width, self.height)
        place_entities(self.planet, number_fishes, number_sharks)
        self.chronon = 0
        self.simulation_active = True
        
        self.buttons = {
            'pause': pygame.Rect(self.grid_width + 30, 200, 190, 40),
            'history': pygame.Rect(self.grid_width + 30, 250, 190, 40),
            'reset': pygame.Rect(self.grid_width + 30, 300, 190, 40)
        }
        
        self.mouse_pos = (0, 0)
        self.mouse_clicked = False
        self.showing_history = False
        self.simulation_ended = False  
        self.end_message_displayed = False 
        create_database()



    def check_simulation_state(self):
        entities = get_entities(self.planet)
        shark_count, fish_count = count_entities(entities)

        if fish_count == 0:
            if self.simulation_active:  
                return False
            
        if shark_count == 0:
            if self.simulation_active: 
                return False
            
        return True
        


    def reset_simulation(self):
            self.planet = Planet(self.width, self.height)
            place_entities(self.planet, number_fishes, number_sharks)
            
            self.chronon = 0
            self.simulation_active = True


    def display_history_interface(self):
        history_rect = pygame.Rect(0, 0, self.grid_width, self.grid_height)
        pygame.draw.rect(self.screen, (240, 240, 240), history_rect)
        
        title = pygame.font.Font(None, 30).render("DERNIÈRES SIMULATIONS", True, (0, 0, 0))
        self.screen.blit(title, (self.grid_width//2 - title.get_width()//2, 30))
        
        history_text = display_history()
        
        font = pygame.font.Font(None, 28)
        y = 100
        max_y = self.grid_height - 50 
        
        for line in str(history_text).split('\n'):
            if y < max_y:  
                text = font.render(line, True, (0, 0, 0))
                self.screen.blit(text, (50, y))
                y += 35
            else:
                break  
        

    def draw_menu(self):
        menu_rect = pygame.Rect(self.grid_width, 0, self.menu_width, self.window_height)
        pygame.draw.rect(self.screen, self.menu_bg_color, menu_rect)
        
        if not self.simulation_active and not self.check_simulation_state():
            msg_font = pygame.font.SysFont(None, 24) 
            msg_text = msg_font.render("SIMULATION TERMINÉE", True, (200, 0, 0))
            self.screen.blit(msg_text, (self.grid_width + 20, 40))
            
        stats_y = 80
        entities = get_entities(self.planet)
        shark_count, fish_count = count_entities(entities)
        
        stats = [
            f"Chronon: {self.chronon}",
            f"Poissons: {fish_count}",
            f"Requins: {shark_count}"
        ]
        
        for i, stat in enumerate(stats):
            text = self.font_menu.render(stat, True, self.text_color)
            self.screen.blit(text, (self.grid_width + 20, stats_y + i * 30))
        
        button_labels = {
            'pause': "PAUSE" if self.simulation_active else "REPRENDRE",
            'history': "HISTORIQUE",
            'reset': "RÉINITIALISER"
        }
        
        for button_name, button_rect in self.buttons.items():
            color = self.button_hover_color if button_rect.collidepoint(self.mouse_pos) else self.button_color
            
            pygame.draw.rect(self.screen, color, button_rect, border_radius=8)
            pygame.draw.rect(self.screen, self.text_color, button_rect, 2, border_radius=8)
            
            text = self.font_button.render(button_labels[button_name], True, self.button_text_color)
            text_rect = text.get_rect(center=button_rect.center)
            self.screen.blit(text, text_rect)
        
        instructions = [
            "ESPACE: Pause/Reprise",
            "ÉCHAP: Quitter"
        ]
        
        instructions_y = 380
        for i, instruction in enumerate(instructions):
            text = self.font_button.render(instruction, True, (180, 190, 210))
            self.screen.blit(text, (self.grid_width + 20, instructions_y + i * 25))



    def draw_grid(self):

        fish_count = 0
        shark_count = 0
        
        for y in range(self.height):
            for x in range(self.width):
                screen_y = y * self.cell_size 
                rect = pygame.Rect(x * self.cell_size, screen_y,
                                self.cell_size, self.cell_size)
                
                cell_color = (
                    self.water_color[0] + (x % 2) * 5, 
                    self.water_color[1] + (y % 2) * 5,
                    self.water_color[2]
                )
                pygame.draw.rect(self.screen, cell_color, rect)
                
                entity = self.planet.get(x, y)
                
                if entity is not None:                    
                    if type(entity) is Fish:
                        fish_count += 1
                        sprite_rect = self.fish_sprite.get_rect(center=rect.center)
                        self.screen.blit(self.fish_sprite, sprite_rect)
                        
                    elif type(entity) is Shark:
                        shark_count += 1
                        sprite_rect = self.shark_sprite.get_rect(center=rect.center)
                        self.screen.blit(self.shark_sprite, sprite_rect)

                pygame.draw.rect(self.screen, self.grid_color, rect, 1)
        
        wave_rect = pygame.Rect(0, self.grid_height + 40 - 20, self.grid_width, 20)
        pygame.draw.rect(self.screen, (15, 30, 50), wave_rect)
        
        return fish_count, shark_count
    
        
    def run(self):
        running = True

        while running:
            self.mouse_pos = pygame.mouse.get_pos()
            self.mouse_clicked = False
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE:
                        self.simulation_active = not self.simulation_active
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: 
                        self.mouse_clicked = True
                        
                        if self.buttons['pause'].collidepoint(self.mouse_pos):
                            self.simulation_active = not self.simulation_active
                        elif self.buttons['history'].collidepoint(self.mouse_pos):
                            self.showing_history = not self.showing_history
                        elif self.buttons['reset'].collidepoint(self.mouse_pos):
                            self.reset_simulation()

            self.screen.fill(self.bg_color)
            
            self.draw_menu()
            

            if self.showing_history:
                self.display_history_interface()
            else:
                self.draw_grid()
                
                if self.simulation_active:
                    should_continue = self.check_simulation_state()
                    
                    if not should_continue:
                        self.simulation_active = False        
                        entities = get_entities(self.planet)
                        shark_count, fish_count = count_entities(entities)
                        archive_simulation(self.chronon, fish_count, shark_count)

                    else:
                        self.chronon += 1
                        entities = get_entities(self.planet)
                        entities = move_entities(self.planet, entities)


            pygame.display.flip()
            self.clock.tick(self.fps)

        final_entities = get_entities(self.planet)
        final_fish, final_sharks = count_entities(final_entities)

        archive_simulation(self.chronon, final_fish, final_sharks)

        
        pygame.quit()