import pygame
import sys

pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.Font(None, 36)

class Button:
    def __init__(self, rect, color, text):
        self.rect = pygame.Rect(rect)
        self.color = color
        self.text = text
        self.text_surf = FONT.render(text, True, WHITE)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text_surf, self.text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

class BaseMenu:
    def __init__(self, screen, title):
        self.screen = screen
        self.title = title
        self.options = []

    def add_option(self, text, callback):
        self.options.append((text, callback))

    def display(self):
        self.screen.fill(WHITE)
        title_text = FONT.render(self.title, True, BLACK)
        self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

        for index, (option_text, _) in enumerate(self.options):
            option_surface = FONT.render(option_text, True, BLACK)
            self.screen.blit(option_surface, (SCREEN_WIDTH // 2 - option_surface.get_width() // 2, 150 + index * 50))
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for index, (_, callback) in enumerate(self.options):
                        if 150 + index * 50 <= event.pos[1] <= 150 + index * 50 + 36:
                            callback()

            self.display()
            pygame.time.Clock().tick(30)

class MainMenu(BaseMenu):
    def __init__(self, screen):
        super().__init__(screen, "Main Menu")
        self.add_option("Create Questions Set", self.create_question_set)
        self.add_option("Add a Player", self.add_player)
        self.add_option("Start the Game", self.start_game)

    def create_question_set(self):
        QuestionSetMenu(self.screen).run()

    def add_player(self):
        PlayerMenu(self.screen).run()

    def start_game(self):
        if len(game.question_sets) > 0 and len(game.players) > 0:
            print("Game started")
        else:
            print("Cannot start game: At least one question set and one player required")

class QuestionSet:
    def __init__(self):
        self.add_button = Button((300, 400, 200, 50), BLACK, "Add a new question")
        self.back_button = Button((300, 500, 200, 50), BLACK, "Back to main menu")

    def add_question_set(self, question, correct_answer, incorrect_answers):
        game.question_sets.append({
            'question': question,
            'correct_answer': correct_answer,
            'incorrect_answers': incorrect_answers
        })

    def display(self, screen):
        screen.fill(WHITE)
        if not game.question_sets:
            no_questions_text = FONT.render("No questions yet!", True, BLACK)
            screen.blit(no_questions_text, (SCREEN_WIDTH // 2 - no_questions_text.get_width() // 2, 200))
        for index, qset in enumerate(game.question_sets):
            qset_text = FONT.render(qset['question'], True, BLACK)
            screen.blit(qset_text, (50, 100 + index * 50))
        self.add_button.draw(screen)
        self.back_button.draw(screen)
        pygame.display.flip()

    def handle_event(self, event, screen, main_menu_callback):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.add_button.is_clicked(event.pos):
                self.process_add_question_set(screen)
            if self.back_button.is_clicked(event.pos):
                main_menu_callback()

    def process_add_question_set(self, screen):
        question = self.get_text_input("Enter the question: ", screen)
        correct_answer = self.get_text_input("Enter the correct answer: ", screen)
        incorrect_answers = [
            self.get_text_input("Enter incorrect answer 1: ", screen),
            self.get_text_input("Enter incorrect answer 2: ", screen),
            self.get_text_input("Enter incorrect answer 3: ", screen)
        ]
        self.add_question_set(question, correct_answer, incorrect_answers)
        print("Question set added")

    def get_text_input(self, prompt, screen):
        text = ""
        input_active = True
        while input_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

            screen.fill(WHITE)
            prompt_text = FONT.render(prompt, True, BLACK)
            input_text = FONT.render(text, True, BLACK)
            screen.blit(prompt_text, (50, 50))
            screen.blit(input_text, (50, 100))
            pygame.display.flip()
            pygame.time.Clock().tick(30)
        return text

class QuestionSetMenu(BaseMenu):
    def __init__(self, screen):
        super().__init__(screen, "Questions  Set")
        self.question_set = QuestionSet()

    def run(self):
        global main_menu_running
        main_menu_running = True
        while main_menu_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.question_set.handle_event(event, self.screen, self.go_back_to_main_menu)
            self.question_set.display(self.screen)
            pygame.time.Clock().tick(30)

    def go_back_to_main_menu(self):
        global main_menu_running
        main_menu_running = False

class PlayerSet:
    def process_add_player(self, screen):
        player_name = self.get_text_input("Enter player's name: ", screen)
        game.players.append((player_name, 0))
        print("Player added")

    def get_text_input(self, prompt, screen):
        text = ""
        input_active = True
        while input_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

            screen.fill(WHITE)
            prompt_text = FONT.render(prompt, True, BLACK)
            input_text = FONT.render(text, True, BLACK)
            screen.blit(prompt_text, (50, 50))
            screen.blit(input_text, (50, 100))
            pygame.display.flip()
            pygame.time.Clock().tick(30)
        return text

class PlayerMenu(BaseMenu):
    def __init__(self, screen):
        super().__init__(screen, "Current players")
        self.player_set = PlayerSet()
        self.add_button = Button((300, 400, 200, 50), BLACK, "Add a player")
        self.back_button = Button((300, 500, 200, 50), BLACK, "Back to main menu")

    def display(self):
        self.screen.fill(WHITE)
        if not game.players:
            no_players_text = FONT.render("No players yet!", True, BLACK)
            self.screen.blit(no_players_text, (SCREEN_WIDTH // 2 - no_players_text.get_width() // 2, 200))
        for index, player in enumerate(game.players):
            player_text = FONT.render(player[0], True, BLACK)
            self.screen.blit(player_text, (50, 100 + index * 50))
        self.add_button.draw(self.screen)
        self.back_button.draw(self.screen)
        pygame.display.flip()

    def handle_event(self, event, main_menu_callback):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.add_button.is_clicked(event.pos):
                self.player_set.process_add_player(self.screen)
            if self.back_button.is_clicked(event.pos):
                main_menu_callback()

    def run(self):
        global main_menu_running
        main_menu_running = True
        while main_menu_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.handle_event(event, self.go_back_to_main_menu)
            self.display()
            pygame.time.Clock().tick(30)

    def go_back_to_main_menu(self):
        global main_menu_running
        main_menu_running = False

class Game:
    def __init__(self):
        self.players = []
        self.question_sets = []

    def start(self):
        if len(self.question_sets) > 0 and len(self.players) > 0:
            print("Game started")
            pygame.quit()
            sys.exit()
        else:
            print("Cannot start game: At least one question set and one player required")

# Initialize Game
game = Game()

# Main Function
def main():

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Kahoot-like Game")
    main_menu = MainMenu(screen)
    main_menu.run()

if __name__ == "__main__":
    main()
