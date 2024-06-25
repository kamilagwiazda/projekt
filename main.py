import pygame
import sys
import time
from pygame.locals import (QUIT, MOUSEBUTTONDOWN)

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 30
FONT_SIZE = 32

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Kahoot-like Game')
clock = pygame.time.Clock()
font = pygame.font.Font(None, FONT_SIZE)

class Button():
    def __init__(self, rect, color, text):
        self.rect = pygame.Rect(rect)
        self.color = color
        self.text = text
        self.text_surf = font.render(text, True, (255, 255, 255))
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text_surf, self.text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

    def add_score(self, points):
        self.score += points

class Question:
    def __init__(self, question, choices, correct_choice):
        self.question = question
        self.choices = choices
        self.correct_choice = correct_choice

class QuestionSet:
    def __init__(self, name):
        self.name = name
        self.questions = []

    def add_question(self, question, choices, correct_choice):
        self.questions.append(Question(question, choices, correct_choice))

class QuestionManager:
    def __init__(self):
        self.question_sets = {}
        self.current_question_set = None
        self.current_question_index = 0

    def add_question_set(self, name):
        self.question_sets[name] = QuestionSet(name)

    def add_question_to_set(self, set_name, question, choices, correct_choice):
        if set_name in self.question_sets:
            self.question_sets[set_name].add_question(question, choices, correct_choice)

    def load_question_set(self, set_name):
        if set_name in self.question_sets:
            self.current_question_set = self.question_sets[set_name]
            self.current_question_index = 0

    def get_current_question(self):
        if self.current_question_set and self.current_question_index < len(self.current_question_set.questions):
            return self.current_question_set.questions[self.current_question_index]
        return None

    def next_question(self):
        self.current_question_index += 1

class Menu:
    def __init__(self, game):
        self.game = game
        self.buttons = []
        self.create_menu()

    def create_menu(self):
        self.buttons = [
            Button((300, 100, 200, 50), (0, 128, 0), 'Create Question Set'),
            Button((300, 200, 200, 50), (0, 128, 0), 'Add Question'),
            Button((300, 300, 200, 50), (0, 128, 0), 'Add Player'),
            Button((300, 400, 200, 50), (0, 128, 0), 'Start Game')
        ]

    def display_menu(self):
        screen.fill((0, 0, 0))
        for button in self.buttons:
            button.draw(screen)
        pygame.display.update()

    def handle_menu_click(self, mouse_pos):
        if self.buttons[0].is_clicked(mouse_pos):
            self.game.create_question_set()
        elif self.buttons[1].is_clicked(mouse_pos):
            self.game.add_question()
        elif self.buttons[2].is_clicked(mouse_pos):
            self.game.add_player()
        elif self.buttons[3].is_clicked(mouse_pos):
            self.game.load_question_set("Set1")
            self.game.run()

class Game:
    def __init__(self):
        self.players = []
        self.question_manager = QuestionManager()
        self.current_player = None
        self.buttons = []
        self.start_time = 0
        self.answering = False
        self.menu = Menu(self)

    def add_player(self):
        name = input("Enter player name: ")
        self.players.append(Player(name))
        if not self.current_player:
            self.current_player = self.players[0]

    def create_question_set(self):
        set_name = input("Enter question set name: ")
        self.question_manager.add_question_set(set_name)

    def add_question(self):
        set_name = input("Enter question set name to add question to: ")
        question = input("Enter the question: ")
        choices = []
        for i in range(4):
            choices.append(input(f"Enter choice {i + 1}: "))
        correct_choice = input("Enter the correct choice: ")
        self.question_manager.add_question_to_set(set_name, question, choices, correct_choice)

    def load_question_set(self, set_name):
        self.question_manager.load_question_set(set_name)

    def setup_ui(self):
        # Create UI elements like buttons for answers
        question = self.question_manager.get_current_question()
        if question:
            self.buttons = []
            for i, choice in enumerate(question.choices):
                button = Button(
                    (100, 300 + i * 50, 600, 40),
                    (0, 128, 0),
                    choice
                )
                self.buttons.append(button)

    def run(self):
        running = True
        self.setup_ui()
        while running:
            screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if self.answering:
                        mouse_pos = event.pos
                        for button in self.buttons:
                            if button.is_clicked(mouse_pos):
                                self.handle_answer(button.text)

            # Draw current question and buttons
            question = self.question_manager.get_current_question()
            if question:
                question_surf = font.render(question.question, True, (255, 255, 255))
                screen.blit(question_surf, (50, 100))

                if not self.answering:
                    pygame.display.update()
                    time.sleep(2)  # Wait for 2 seconds before showing answers
                    self.answering = True
                    self.start_time = time.time()
                else:
                    for button in self.buttons:
                        button.draw(screen)

                    elapsed_time = time.time() - self.start_time
                    if elapsed_time >= 5:
                        self.handle_answer(None)  # Time out, no answer given

            else:
                self.show_final_scores()
                running = False

            pygame.display.update()
            clock.tick(FPS)

    def handle_answer(self, answer):
        question = self.question_manager.get_current_question()
        if question:
            if answer == question.correct_choice:
                elapsed_time = time.time() - self.start_time
                points = 1000 * (5 - elapsed_time)
                self.current_player.add_score(max(points, 0))
        self.question_manager.next_question()
        self.setup_ui()
        self.answering = False

    def show_final_scores(self):
        screen.fill((0, 0, 0))
        for i, player in enumerate(self.players):
            score_text = f"{player.name}: {player.score}"
            score_surf = font.render(score_text, True, (255, 255, 255))
            screen.blit(score_surf, (50, 50 + i * 40))
        pygame.display.update()
        pygame.time.wait(5000)

# Sample questions for demonstration
sample_questions = [
    ("Set1", "What is 2 + 2?", ["3", "4", "5", "6"], "4"),
    ("Set1", "What is the capital of France?", ["Berlin", "London", "Paris", "Madrid"], "Paris"),
]

# Game setup
game = Game()

# Add sample questions
game.question_manager.add_question_set("Set1")
for set_name, question, choices, correct_choice in sample_questions:
    game.question_manager.add_question_to_set(set_name, question, choices, correct_choice)

# Display menu
running = True
while running:
    screen.fill((0, 0, 0))
    game.menu.display_menu()
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            game.menu.handle_menu_click(event.pos)
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()
