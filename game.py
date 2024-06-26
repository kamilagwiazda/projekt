import random
import sys
import time

import pygame

pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_BG_COLOR = (255, 255, 255)
BUTTON_SHADOW_COLOR = (200, 200, 200)
BUTTON_TEXT_COLOR = (0, 0, 0)
LOGO_FONT = pygame.font.Font('fonts/gooddog-plain.regular.ttf', 150)
MAIN_FONT = pygame.font.Font('fonts/Montserrat-Bold.ttf', 20)
BUTTON_FONT = pygame.font.Font('fonts/Montserrat-Bold.ttf', 20)
BACKGROUND_IMAGE = 'images/background.jpg'
BUTTON_RADIUS = 10

class Button:
    def __init__(self, rect, color, text):
        self.rect = pygame.Rect(rect)
        self.color = color
        self.text = text
        self.text_surf = BUTTON_FONT.render(text, True, BUTTON_TEXT_COLOR)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, screen):
        shadow_rect = self.rect.move(4, 4)
        pygame.draw.rect(screen, BUTTON_SHADOW_COLOR, shadow_rect, border_radius=BUTTON_RADIUS)

        pygame.draw.rect(screen, self.color, self.rect, border_radius=BUTTON_RADIUS)
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
        background = pygame.image.load(BACKGROUND_IMAGE)
        self.screen.blit(pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
        title_text = LOGO_FONT.render(self.title, True, WHITE)
        self.screen.blit(
            title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50)
        )

        for index, (option_text, callback) in enumerate(self.options):
            option_button = Button((SCREEN_WIDTH // 2 - 150, 300 + index * 70, 300, 50), BUTTON_BG_COLOR, option_text)
            option_button.draw(self.screen)

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for index, (option_text, callback) in enumerate(self.options):
                        option_button = Button((SCREEN_WIDTH // 2 - 150, 300 + index * 70, 300, 50), BUTTON_BG_COLOR,
                                               option_text)
                        if option_button.is_clicked(event.pos):
                            callback()

            self.display()
            pygame.time.Clock().tick(30)


class MainMenu(BaseMenu):
    def __init__(self, screen):
        super().__init__(screen, "Kahoot!")
        self.create_question_set_button = Button((SCREEN_WIDTH // 2 - 150, 300, 300, 50), BUTTON_BG_COLOR,
                                                 "Create Questions Set")
        self.add_player_button = Button((SCREEN_WIDTH // 2 - 150, 370, 300, 50), BUTTON_BG_COLOR, "Add a Player")
        self.start_game_button = Button((SCREEN_WIDTH // 2 - 150, 440, 300, 50), BUTTON_BG_COLOR, "Start the Game")
        self.exit_button = Button((SCREEN_WIDTH // 2 - 150, 510, 300, 50), BUTTON_BG_COLOR, "Exit")

    def display(self):
        background = pygame.image.load(BACKGROUND_IMAGE)
        self.screen.blit(pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
        title_text = LOGO_FONT.render(self.title, True, WHITE)
        self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

        self.create_question_set_button.draw(self.screen)
        self.add_player_button.draw(self.screen)
        self.start_game_button.draw(self.screen)
        self.exit_button.draw(self.screen)

        pygame.display.flip()

    def run(self):
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.create_question_set_button.is_clicked(event.pos):
                            self.create_question_set()
                        if self.add_player_button.is_clicked(event.pos):
                            self.add_player()
                        if self.start_game_button.is_clicked(event.pos):
                            self.start_game()
                        if self.exit_button.is_clicked(event.pos):
                            pygame.quit()
                            sys.exit()

                self.display()
                pygame.time.Clock().tick(30)
    def create_question_set(self):
        QuestionSetMenu(self.screen).run()

    def add_player(self):
        PlayerMenu(self.screen).run()

    def start_game(self):
        if len(game.question_sets) > 0 and len(game.players) > 0:
            GameMenu(self.screen).run()
        else:
            print(
                "Cannot start game: At least one question set and one player required"
            )


class GameMenu:
    def __init__(self, screen):
        self.screen = screen
        self.current_question_index = 0
        self.start_time = None
        self.answer_buttons = []

    def display(self, text):
        background = pygame.image.load(BACKGROUND_IMAGE)
        self.screen.blit(pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
        text_surface = MAIN_FONT.render(text, True, WHITE)
        self.screen.blit(
            text_surface,
            (
                SCREEN_WIDTH // 2 - text_surface.get_width() // 2,
                SCREEN_HEIGHT // 2 - text_surface.get_height() // 2,
            ),
        )
        pygame.display.flip()

    def run(self):
        self.current_question_index = 0
        game.current_player_index = 0
        self.ask_questions_for_current_player()

    def ask_questions_for_current_player(self):
        player = game.players[game.current_player_index][0]
        self.display_get_ready_screen(player)
        waiting_for_enter = True

        while waiting_for_enter:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting_for_enter = False

        self.ask_questions()

    def display_get_ready_screen(self, player):
        background = pygame.image.load(BACKGROUND_IMAGE)
        self.screen.blit(pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))

        logo_text = LOGO_FONT.render("Kahoot!", True, WHITE)
        logo_text = pygame.transform.scale(logo_text,
                                           (int(logo_text.get_width() * 0.5), int(logo_text.get_height() * 0.5)))
        self.screen.blit(logo_text, (SCREEN_WIDTH // 2 - logo_text.get_width() // 2, 20))

        larger_font = pygame.font.Font('fonts/Montserrat-Bold.ttf', 40)
        ready_text = larger_font.render(f"Get ready to play, {player}!", True, WHITE)
        self.screen.blit(ready_text, (SCREEN_WIDTH // 2 - ready_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))

        ready_press_text = MAIN_FONT.render("If you are ready, press ENTER.", True, WHITE)
        self.screen.blit(ready_press_text, (SCREEN_WIDTH // 2 - ready_press_text.get_width() // 2, SCREEN_HEIGHT - 100))

        pygame.display.flip()
    def ask_questions(self):
        while self.current_question_index < len(game.question_sets):
            question = game.question_sets[self.current_question_index]
            self.display_question_with_answers(question)
            waiting_for_answer = True

            self.start_time = time.time()
            while waiting_for_answer and (time.time() - self.start_time) < 30:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for i, button in enumerate(self.answer_buttons):
                            if button.is_clicked(event.pos):
                                chosen_answer = button.text
                                self.check_answer(
                                    question["correct_answer"], chosen_answer
                                )
                                waiting_for_answer = False

                self.update_timer()
                pygame.time.Clock().tick(30)

            self.current_question_index += 1

        game.current_player_index += 1
        if game.current_player_index < len(game.players):
            self.current_question_index = 0
            self.ask_questions_for_current_player()
        else:
            self.display_score()

    def update_timer(self):
                elapsed_time = time.time() - self.start_time
                remaining_time = max(0, int(30 - elapsed_time))
                timer_text = MAIN_FONT.render(str(remaining_time), True, WHITE)
                timer_circle_color = (137, 76, 192)
                pygame.draw.circle(self.screen, (0, 0, 0), (SCREEN_WIDTH - 50, 50), 30)
                pygame.draw.circle(self.screen, timer_circle_color, (SCREEN_WIDTH - 50, 50), 30)
                self.screen.blit(timer_text,
                                 (SCREEN_WIDTH - 50 - timer_text.get_width() // 2, 50 - timer_text.get_height() // 2))

                pygame.display.flip()

    def show_points(self, points=0):
        player_name = game.players[game.current_player_index][0]
        game.scores[player_name] = game.scores.get(player_name, 0) + points
    def display_question_with_answers(self, question):
        background = pygame.image.load(BACKGROUND_IMAGE)
        self.screen.blit(pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))

        qa_rect = pygame.Rect(50, 50, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100)
        pygame.draw.rect(self.screen, WHITE, qa_rect)
        question_text = MAIN_FONT.render(question["question"], True, BLACK)
        self.screen.blit(question_text, (qa_rect.x + 10, qa_rect.y + 10))

        colors = [(224, 27, 62), (22, 103, 207), (214, 158, 1), (40, 135, 13)]
        shapes = ["triangle", "diamond", "circle", "square"]
        answers = question["incorrect_answers"] + [question["correct_answer"]]
        random.shuffle(answers)

        margin = 5
        box_width = (qa_rect.width - 3 * margin) // 2
        box_height = (qa_rect.height - 120 - 3 * margin) // 2
        answer_positions = [
            (qa_rect.x + margin, qa_rect.y + 120 + margin, box_width, box_height),
            (qa_rect.x + box_width + 2 * margin, qa_rect.y + 120 + margin, box_width, box_height),
            (qa_rect.x + margin, qa_rect.y + 120 + box_height + 2 * margin, box_width, box_height),
            (qa_rect.x + box_width + 2 * margin, qa_rect.y + 120 + box_height + 2 * margin, box_width, box_height),
        ]

        self.answer_buttons = []
        for i, answer in enumerate(answers):
            color = colors[i]
            shape = shapes[i]
            pos = answer_positions[i]
            answer_rect = pygame.Rect(pos)
            pygame.draw.rect(self.screen, color, answer_rect)

            self.draw_shape(self.screen, shape, answer_rect, WHITE)

            answer_text = MAIN_FONT.render(answer, True, WHITE)
            self.screen.blit(answer_text, (answer_rect.x + 70, answer_rect.y + answer_rect.height // 2 - 10))


            answer_button = Button(answer_rect, color, answer)
            self.answer_buttons.append(answer_button)

        pygame.display.flip()

    def draw_shape(self, screen, shape, rect, color):
        text_height = MAIN_FONT.size("A")[1]
        shape_size = text_height // 2
        center_x = rect.x + 35
        center_y = rect.y + rect.height // 2
        if shape == "triangle":
            points = [
                (center_x, center_y - shape_size),
                (center_x - shape_size, center_y + shape_size),
                (center_x + shape_size, center_y + shape_size),
            ]
            pygame.draw.polygon(screen, color, points)
        elif shape == "diamond":
            points = [
                (center_x, center_y - shape_size),
                (center_x - shape_size, center_y),
                (center_x, center_y + shape_size),
                (center_x + shape_size, center_y),
            ]
            pygame.draw.polygon(screen, color, points)
        elif shape == "circle":
            pygame.draw.circle(screen, color, (center_x, center_y), shape_size)
        elif shape == "square":
            pygame.draw.rect(screen, color,
                             pygame.Rect(center_x - shape_size, center_y - shape_size, 2 * shape_size, 2 * shape_size))

    def check_answer(self, correct_answer, chosen_answer):
        end_time = time.time()
        time_taken = end_time - self.start_time

        if chosen_answer == correct_answer:
            score = max(0, 100 - int(time_taken * 10))
        else:
            score = 0

        player_name = game.players[game.current_player_index][0]
        if player_name not in game.scores:
            game.scores[player_name] = 0
        game.scores[player_name] += score

    def display_score(self):
        background = pygame.image.load(BACKGROUND_IMAGE)
        self.screen.blit(pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
        score_text = "Final Scores:\n"
        y_offset = 100
        for player, score in game.scores.items():
            player_score_text = MAIN_FONT.render(f"{player}: {score}", True, WHITE)
            self.screen.blit(
                player_score_text,
                (SCREEN_WIDTH // 2 - player_score_text.get_width() // 2, y_offset),
            )
            y_offset += 50
        pygame.display.flip()
        pygame.time.wait(5000)


class QuestionSet:
    def __init__(self):
        self.add_button = Button((SCREEN_WIDTH // 2 - 150, 400, 300, 50), BUTTON_BG_COLOR, "Add a new question")
        self.back_button = Button((SCREEN_WIDTH // 2 - 150, 500, 300, 50), BUTTON_BG_COLOR, "Back to main menu")

    def add_question_set(self, question, correct_answer, incorrect_answers):
        game.question_sets.append(
            {
                "question": question,
                "correct_answer": correct_answer,
                "incorrect_answers": incorrect_answers,
            }
        )

    def display(self, screen):
        background = pygame.image.load(BACKGROUND_IMAGE)
        screen.blit(pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
        if not game.question_sets:
            no_questions_text = MAIN_FONT.render("No questions yet!", True, WHITE)
            screen.blit(
                no_questions_text,
                (SCREEN_WIDTH // 2 - no_questions_text.get_width() // 2, 200),
            )
        for index, qset in enumerate(game.question_sets):
            qset_text = MAIN_FONT.render(qset["question"], True, WHITE)
            screen.blit(qset_text, (50, 100 + index * 70))
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
        if question is None:
            return
        correct_answer = self.get_text_input("Enter the correct answer: ", screen)
        if correct_answer is None:
            return
        incorrect_answers = []
        for i in range(3):
            incorrect_answer = self.get_text_input(f"Enter incorrect answer {i + 1}: ", screen)
            if incorrect_answer is None:
                return
            incorrect_answers.append(incorrect_answer)

        self.add_question_set(question, correct_answer, incorrect_answers)
        print("Question set added")

    def get_text_input(self, prompt, screen):
        text = ""
        input_active = True
        self.submit_button = Button((SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 150, 300, 50), BUTTON_BG_COLOR, "Submit")
        self.cancel_button = Button((SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 80, 300, 50), BUTTON_BG_COLOR, "Cancel")
        input_rect = pygame.Rect(50, 100, SCREEN_WIDTH - 100, 200)
        input_color = WHITE
        input_border_radius = 20
        max_text_width = input_rect.width - 20
        max_lines = (input_rect.height - 20) // MAIN_FONT.get_height()

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
                if event.type == pygame.MOUSEBUTTONDOWN:
                            if self.cancel_button.is_clicked(event.pos):
                                return None
                            if self.submit_button.is_clicked(event.pos):
                                input_active = False

            background = pygame.image.load(BACKGROUND_IMAGE)
            screen.blit(pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
            prompt_text = MAIN_FONT.render(prompt, True, WHITE)
            pygame.draw.rect(screen, input_color, input_rect, border_radius=input_border_radius)

            words = text.split(' ')
            lines = []
            current_line = ""
            for word in words:
                if current_line:
                    test_line = current_line + " " + word
                else:
                    test_line = word
                if MAIN_FONT.render(test_line, True, BLACK).get_width() <= max_text_width:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word + " "

            lines.append(current_line)

            lines = lines[-max_lines:]

            screen.blit(prompt_text, (50, 50))
            for i, line in enumerate(lines):
                input_text = MAIN_FONT.render(line, True, BLACK)
                screen.blit(input_text, (input_rect.x + 10, input_rect.y + 10 + i * MAIN_FONT.get_height()))
            self.draw_submit_button(screen)
            self.draw_cancel_button(screen)
            pygame.display.flip()
            pygame.time.Clock().tick(30)
        return text

    def draw_cancel_button(self, screen):
        self.cancel_button.draw(screen)

    def draw_submit_button(self, screen):
        self.submit_button.draw(screen)


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
                self.question_set.handle_event(
                    event, self.screen, self.go_back_to_main_menu
                )
            self.question_set.display(self.screen)
            pygame.time.Clock().tick(30)

    def go_back_to_main_menu(self):
        global main_menu_running
        main_menu_running = False
        main()


class PlayerSet:
    def process_add_player(self, screen):
        player_name = self.get_text_input("Enter player's name: ", screen)
        if player_name is not None:
          game.players.append((player_name, 0))
          print("Player added")
        else:
          print("Adding player was cancelled.")

    def get_text_input(self, prompt, screen):
        text = ""
        input_active = True
        self.submit_button = Button((SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 150, 300, 50), BUTTON_BG_COLOR, "Submit")
        self.cancel_button = Button((SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 80, 300, 50), BUTTON_BG_COLOR, "Cancel")
        input_rect = pygame.Rect(50, 100, SCREEN_WIDTH - 100, 50)
        input_color = WHITE
        input_border_radius = 20
        max_text_width = input_rect.width - 20
        max_lines = (input_rect.height - 20) // MAIN_FONT.get_height()

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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.cancel_button.is_clicked(event.pos):
                        return None
                    if self.submit_button.is_clicked(event.pos):
                        input_active = False

            background = pygame.image.load(BACKGROUND_IMAGE)
            screen.blit(pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
            prompt_text = MAIN_FONT.render(prompt, True, WHITE)
            pygame.draw.rect(screen, input_color, input_rect, border_radius=input_border_radius)

            words = text.split(' ')
            lines = []
            current_line = ""

            for word in words:
                test_line = current_line + word + " "
                if MAIN_FONT.render(test_line, True, BLACK).get_width() <= max_text_width:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word + " "

            lines.append(current_line)
            lines = lines[-max_lines:]

            screen.blit(prompt_text, (50, 50))
            for i, line in enumerate(lines):
                input_text = MAIN_FONT.render(line.strip(), True, BLACK)
                screen.blit(input_text, (input_rect.x + 10, input_rect.y + 10 + i * MAIN_FONT.get_height()))
            self.draw_submit_button(screen)
            self.draw_cancel_button(screen)
            pygame.display.flip()
            pygame.time.Clock().tick(30)
        return text

    def draw_cancel_button(self, screen):
        self.cancel_button.draw(screen)
    def draw_submit_button(self, screen):
        self.submit_button.draw(screen)

class PlayerMenu(BaseMenu):
    def __init__(self, screen):
        super().__init__(screen, "Current players")
        self.player_set = PlayerSet()
        self.add_button = Button((SCREEN_WIDTH // 2 - 150, 400, 300, 50), BUTTON_BG_COLOR, "Add a player")
        self.back_button = Button((SCREEN_WIDTH // 2 - 150, 500, 300, 50), BUTTON_BG_COLOR, "Back to main menu")

    def display(self):
        background = pygame.image.load(BACKGROUND_IMAGE)
        self.screen.blit(pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
        if not game.players:
            no_players_text = MAIN_FONT.render("No players yet!", True, WHITE)
            self.screen.blit(
                no_players_text,
                (SCREEN_WIDTH // 2 - no_players_text.get_width() // 2, 200),
            )
        for index, player in enumerate(game.players):
            player_text = MAIN_FONT.render(player[0], True, WHITE)
            self.screen.blit(player_text, (50, 100 + index * 70))
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
        main()


class Game:
    def __init__(self):
        self.players = []
        self.question_sets = []
        self.current_player_index = 0
        self.scores = {}

    def start(self):
        if len(self.question_sets) > 0 and len(self.players) > 0:
            print("Game started")
            pygame.quit()
            sys.exit()
        else:
            print(
                "Cannot start game: At least one question set and one player required"
            )


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
