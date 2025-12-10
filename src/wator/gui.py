from __future__ import annotations
import random
import time
import pygame
from typing import Union
from .planet import Planet
from .fish import Fish
from .shark import Shark
from .config import grid_width, grid_height, number_fishes, number_sharks


class WatorGUI:
    def __init__(self, cell_size=20, fps=5):
        self.cell_size = cell_size
        self.fps = fps
        self.width = grid_width
        self.height = grid_height
        self.window_width = self.width * self.cell_size
        self.window_height = self.height * self.cell_size + 40

        self.bg_color = (18, 25, 38)  
        self.grid_color = (40, 55, 80)
        self.water_color = (20, 35, 60) 
        self.text_color = (220, 230, 240) 

        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Wa-Tor Simulation")
        self.clock = pygame.time.Clock()

        try:
            self.font_emoji = pygame.font.SysFont("Segoe UI Emoji", self.cell_size)
        except:
            self.font_emoji = pygame.font.SysFont(None, self.cell_size)

        self.font_text = pygame.font.SysFont(None, 30)

        self.planet = Planet(self.width, self.height)
        self.place_entities(number_fishes, number_sharks)
        self.chronon = 0
        self.simulation_active = True

    def get_free_positions(self):
        free_positions = []
        for y in range(self.height):
            for x in range(self.width):
                if self.planet.get(x, y) is None:
                    free_positions.append((x, y))
        return free_positions

    def create_entity(self, instance, free_positions):
        if not free_positions:
            return None
        x, y = free_positions.pop()
        new_entity = instance(x=x, y=y)
        self.planet.add(new_entity, x, y)
        return new_entity

    def place_entities(self, num_fish, num_sharks):
        free_positions = self.get_free_positions()
        random.shuffle(free_positions)
        
        print(f"Placement: {num_fish} poissons et {num_sharks} requins")
        
        for _ in range(num_fish):
            if free_positions:
                self.create_entity(Fish, free_positions)
        
        for _ in range(num_sharks):
            if free_positions:
                shark = self.create_entity(Shark, free_positions)

    def get_entities(self):
        entities = []
        for y in range(self.height):
            for x in range(self.width):
                e = self.planet.get(x, y)
                if e is not None:
                    entities.append(e)
        return entities

    def get_entity_counts(self):
        fish_count = 0
        shark_count = 0
        
        for y in range(self.height):
            for x in range(self.width):
                entity = self.planet.get(x, y)
                if entity is not None:
                    entity_type = type(entity).__name__
                    if entity_type == 'Fish':
                        fish_count += 1
                    elif entity_type == 'Shark':
                        shark_count += 1
        
        return fish_count, shark_count

    def move_entities(self):
        if not self.simulation_active:
            return
            
        entities = self.get_entities()
        random.shuffle(entities)
        
        for entity in entities:
            current_entity = self.planet.get(entity.x, entity.y)
            if current_entity is not entity:
                continue
                
            entity_type = type(entity).__name__
            
            if entity_type == 'Fish':
                if not entity.alive:
                    self.planet.remove(entity.x, entity.y)
                    continue
                    
                entity.search_free(self.planet)
                    
            elif entity_type == 'Shark':
                if not entity.alive:
                    self.planet.remove(entity.x, entity.y)
                    continue
                    
                entity.search_fish(self.planet)

    def check_simulation_state(self):
        fish_count, shark_count = self.get_entity_counts()
        
        print(f"Chronon {self.chronon}: 🐟={fish_count} 🦈={shark_count}")
        
        if fish_count == 0:
            print("ARRÊT: Tous les poissons sont morts")
            return False
            
        if shark_count == 0:
            print("ARRÊT: Tous les requins sont morts")
            return False
            
        return True

    def draw_grid(self):


        fish_count = 0
        shark_count = 0
        
        for y in range(self.height):
            for x in range(self.width):

                screen_y = y * self.cell_size + 40 
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
                    entity_type = type(entity).__name__
                    
                    if entity_type == 'Fish':
                        fish_count += 1
                        emoji_surface = self.font_emoji.render("🐟", True, self.text_color)
                        emoji_rect = emoji_surface.get_rect(center=rect.center)
                        self.screen.blit(emoji_surface, emoji_rect)
                        
                    elif entity_type == 'Shark':
                        shark_count += 1
                        emoji_surface = self.font_emoji.render("🦈", True, self.text_color)
                        emoji_rect = emoji_surface.get_rect(center=rect.center)
                        self.screen.blit(emoji_surface, emoji_rect)
                
                pygame.draw.rect(self.screen, self.grid_color, rect, 1)
        
        status = "ACTIVE" if self.simulation_active else "ARRÊTÉE"
        info_text = f"Chronon: {self.chronon}  |  🐟 : {fish_count}  |  🦈 : {shark_count} "
        text_surface = self.font_emoji.render(info_text, True, self.text_color)
        self.screen.blit(text_surface, (10, 5))

        wave_rect = pygame.Rect(0, self.window_height - 20, self.window_width, 20)
        pygame.draw.rect(self.screen, (15, 30, 50), wave_rect)
        
        return fish_count, shark_count

    def run(self):
        running = True
        
        print("=" * 60)
        print("DÉMARRAGE DE LA SIMULATION WA-TOR")
        print("=" * 60)
        
        while running:
            self.clock.tick(self.fps)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE:
                        self.simulation_active = not self.simulation_active
                        print(f"Simulation {'reprise' if self.simulation_active else 'en pause'}")
            
            self.screen.fill(self.bg_color)
            
            if self.simulation_active:
                should_continue = self.check_simulation_state()
                
                if not should_continue:
                    self.simulation_active = False
                else:
                    self.chronon += 1
                    self.move_entities()
            
            self.draw_grid()
            
            if not self.simulation_active:
                msg_font = pygame.font.SysFont(None, 40)
                msg_text = msg_font.render("SIMULATION TERMINÉE", True, (200, 0, 0))
                sub_text = self.font_text.render("Appuyez sur ÉCHAP pour quitter", True, (200, 200, 200))
                
                max_width = max(msg_text.get_width(), sub_text.get_width())
                frame_width = max_width + 40 
                frame_height = 80
                frame_x = self.window_width//2 - frame_width//2
                frame_y = self.window_height//2 - frame_height//2
                
                pygame.draw.rect(self.screen, (40, 40, 50), (frame_x, frame_y, frame_width, frame_height))
                pygame.draw.rect(self.screen, (200, 0, 0), (frame_x, frame_y, frame_width, frame_height), 2)
                
                msg_rect = msg_text.get_rect(center=(self.window_width//2, self.window_height//2 - 10))
                sub_rect = sub_text.get_rect(center=(self.window_width//2, self.window_height//2 + 20))
                self.screen.blit(msg_text, msg_rect)
                self.screen.blit(sub_text, sub_rect)

            pygame.display.flip()
        
        print("\n" + "=" * 60)
        print("FIN DE LA SIMULATION")
        print(f"Dernier chronon: {self.chronon}")
        final_fish, final_sharks = self.get_entity_counts()
        print(f"Poissons finaux: {final_fish}")
        print(f"Requins finaux: {final_sharks}")
        print("=" * 60)
        
        pygame.quit()