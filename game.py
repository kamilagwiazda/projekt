import random
import sys
import time
import pygame

pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_BG_COLOR = (255, 255, 255)
BUTTON_SHADOW_COLOR = (200, 200, 200)
BUTTON_TEXT_COLOR = (0, 0, 0)
LOGO_FONT = pygame.font.Font("fonts/gooddog-plain.regular.ttf", 150)
MAIN_FONT = pygame.font.Font("fonts/Montserrat-Bold.ttf", 20)
BUTTON_FONT = pygame.font.Font("fonts/Montserrat-Bold.ttf", 20)
BACKGROUND_IMAGE = "images/background.jpg"
BUTTON_RADIUS = 10

class Button:
    def __init__(self, rect, color, text):
        self.rect = pygame.Rect(rect)
        self.color = color
        self.original_color = color
        self.hover_color = (200, 200, 200)
        self.text = text
        self.text_surf = BUTTON_FONT.render(text, True, BUTTON_TEXT_COLOR)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, screen):
        shadow_rect = self.rect.move(4, 4)
        pygame.draw.rect(screen, BUTTON_SHADOW_COLOR, shadow_rect, border_radius=BUTTON_RADIUS)
        pygame.draw.rect(screen, self.color, self.rect, border_radius=BUTTON_RADIUS)
        screen.blit(self.text_surf, self.text_rect)
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, self.hover_color, self.rect, border_radius=BUTTON_RADIUS)
        else:
            pygame.draw.rect(screen, self.color, self.rect, border_radius=BUTTON_RADIUS)
        screen.blit(self.text_surf, self.text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)


class BaseMenu:
    def __init__(self, screen, title=None):
        self.screen = screen
        self.title = title
        self.options = []

    def add_option(self, text, callback):
        self.options.append((text, callback))

    def display_background(self):
        background = pygame.image.load(BACKGROUND_IMAGE)
        self.screen.blit(pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))

    def display_title(self):
        if self.title:
            title_text = LOGO_FONT.render(self.title, True, WHITE)
            self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

    def display(self):
        self.display_background()
        self.display_title()
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
                        option_button = Button((SCREEN_WIDTH // 2 - 150, 300 + index * 70, 300, 50), BUTTON_BG_COLOR, option_text)
                        if option_button.is_clicked(event.pos):
                            callback()
            self.display()
            pygame.time.Clock().tick(30)


class QuestionSet:
    def __init__(self):
        self.add_button = Button((SCREEN_WIDTH // 2 - 150, 400, 300, 50), BUTTON_BG_COLOR, "Add a new question")
        self.back_button = Button((SCREEN_WIDTH // 2 - 150, 500, 300, 50), BUTTON_BG_COLOR, "Back to main menu")
        pygame.mixer.music.load('music/background.mp3')
        pygame.mixer.music.play(-1)
        self.button_click_sound = pygame.mixer.Sound('music/click.mp3')

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
        game.question_sets.append({"question": question, "correct_answer": correct_answer, "incorrect_answers": incorrect_answers})
        print("Question set added")

    def get_text_input(self, prompt, screen):
        text = ""
        input_active = True
        submit_button = Button((SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 150, 300, 50), BUTTON_BG_COLOR, "Submit")
        cancel_button = Button((SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 80, 300, 50), BUTTON_BG_COLOR, "Cancel")
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
                    if cancel_button.is_clicked(event.pos):
                        return None
                    if submit_button.is_clicked(event.pos):
                        input_active = False

            background = pygame.image.load(BACKGROUND_IMAGE)
            screen.blit(pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
            prompt_text = MAIN_FONT.render(prompt, True, WHITE)
            pygame.draw.rect(screen, input_color, input_rect, border_radius=input_border_radius)

            words = text.split(" ")
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
            submit_button.draw(screen)
            cancel_button.draw(screen)
            pygame.display.flip()
            pygame.time.Clock().tick(30)
        return text

    def display(self, screen):
        background = pygame.image.load(BACKGROUND_IMAGE)
        screen.blit(pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
        if not game.question_sets:
            no_questions_text = MAIN_FONT.render("No questions yet!", True, WHITE)
            screen.blit(no_questions_text, (SCREEN_WIDTH // 2 - no_questions_text.get_width() // 2, 200))
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


class QuestionSetMenu(BaseMenu):
    def __init__(self, screen):
        super().__init__(screen, "Question Set")
        self.question_set = QuestionSet()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.question_set.handle_event(event, self.screen, self.go_back_to_main_menu)
            self.question_set.display(self.screen)
            pygame.time.Clock().tick(30)

    def go_back_to_main_menu(self):
        main_menu = MainMenu(self.screen)
        main_menu.run()


class MainMenu(BaseMenu):
    def __init__(self, screen):
        super().__init__(screen, "Kahoot!")
        self.add_option("Create Questions Set", self.create_question_set)
        self.add_option("Add a Player", self.add_player)
        self.add_option("Start the Game", self.start_game)
        self.add_option("Exit", self.exit_game)
        pygame.mixer.music.load('music/background.mp3')
        pygame.mixer.music.play(-1)

    def create_question_set(self):
        QuestionSetMenu(self.screen).run()

    def add_player(self):
        PlayerMenu(self.screen).run()

    def start_game(self):
        if len(game.question_sets) > 0 and len(game.players) > 0:
            GameMenu(self.screen).run()
        else:
            print("Cannot start game: At least one question set and one player required")

    def exit_game(self):
        pygame.quit()
        sys.exit()


class PlayerSet:
    def __init__(self):
        self.add_button = Button((SCREEN_WIDTH // 2 - 150, 400, 300, 50), BUTTON_BG_COLOR, "Add a player")
        self.back_button = Button((SCREEN_WIDTH // 2 - 150, 500, 300, 50), BUTTON_BG_COLOR, "Back to main menu")
        self.button_click_sound = pygame.mixer.Sound('music/click.mp3')

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
        submit_button = Button((SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 150, 300, 50), BUTTON_BG_COLOR, "Submit")
        cancel_button = Button((SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 80, 300, 50), BUTTON_BG_COLOR, "Cancel")
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
                    if cancel_button.is_clicked(event.pos):
                        return None
                    if submit_button.is_clicked(event.pos):
                        input_active = False

            background = pygame.image.load(BACKGROUND_IMAGE)
            screen.blit(pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
            prompt_text = MAIN_FONT.render(prompt, True, WHITE)
            pygame.draw.rect(screen, input_color, input_rect, border_radius=input_border_radius)

            words = text.split(" ")
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
            submit_button.draw(screen)
            cancel_button.draw(screen)
            pygame.display.flip()
            pygame.time.Clock().tick(30)
        return text

    def display(self, screen):
        background = pygame.image.load(BACKGROUND_IMAGE)
        screen.blit(pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
        if not game.players:
            no_players_text = MAIN_FONT.render("No players yet!", True, WHITE)
            screen.blit(no_players_text, (SCREEN_WIDTH // 2 - no_players_text.get_width() // 2, 200))
        for index, player in enumerate(game.players):
            player_text = MAIN_FONT.render(player[0], True, WHITE)
            screen.blit(player_text, (50, 100 + index * 70))
        self.add_button.draw(screen)
        self.back_button.draw(screen)
        pygame.display.flip()

    def handle_event(self, event, screen, main_menu_callback):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.add_button.is_clicked(event.pos):
                self.process_add_player(screen)
            if self.back_button.is_clicked(event.pos):
                main_menu_callback()


class PlayerMenu(BaseMenu):
    def __init__(self, screen):
        super().__init__(screen, "Current players")
        self.player_set = PlayerSet()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.player_set.handle_event(event, self.screen, self.go_back_to_main_menu)
            self.player_set.display(self.screen)
            pygame.time.Clock().tick(30)

    def go_back_to_main_menu(self):
        main_menu = MainMenu(self.screen)
        main_menu.run()


class GameMenu(BaseMenu):
    def __init__(self, screen):
        super().__init__(screen, "Game Menu")
        self.current_question_index = 0
        self.start_time = None
        self.answer_buttons = []
        self.message = ""
        self.message_color = (102, 191, 58)
        self.correct_sound = pygame.mixer.Sound('music/correct.wav')
        self.incorrect_sound = pygame.mixer.Sound('music/wrong.wav')

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
        logo_text = pygame.transform.scale(logo_text, (int(logo_text.get_width() * 0.5), int(logo_text.get_height() * 0.5)))
        self.screen.blit(logo_text, (SCREEN_WIDTH // 2 - logo_text.get_width() // 2, 20))
        larger_font = pygame.font.Font("fonts/Montserrat-Bold.ttf", 40)
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
                                self.check_answer(question, question["correct_answer"], chosen_answer)
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
        self.screen.blit(timer_text, (SCREEN_WIDTH - 50 - timer_text.get_width() // 2, 50 - timer_text.get_height() // 2))
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
            pygame.draw.rect(screen, color, pygame.Rect(center_x - shape_size, center_y - shape_size, 2 * shape_size, 2 * shape_size))

    def check_answer(self, question, correct_answer, chosen_answer):
        end_time = time.time()
        time_taken = end_time - self.start_time
        if chosen_answer == correct_answer:
            score = max(0, 100 - int(time_taken * 10))
            self.message = f"Good job! +{score} points"
            self.message_color = (102, 191, 58)
            self.correct_sound.play()
        else:
            score = 0
            self.message = "You were close! 0 points"
            self.message_color = (224, 27, 62)
            self.incorrect_sound.play()
        player_name = game.players[game.current_player_index][0]
        if player_name not in game.scores:
            game.scores[player_name] = 0
        game.scores[player_name] += score
        self.display_feedback(question, correct_answer, chosen_answer)

    def display_feedback(self, question, correct_answer, chosen_answer):
        background = pygame.image.load(BACKGROUND_IMAGE)
        self.screen.blit(pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
        qa_rect = pygame.Rect(50, 50, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100)
        pygame.draw.rect(self.screen, WHITE, qa_rect)
        question_text = MAIN_FONT.render(question["question"], True, BLACK)
        self.screen.blit(question_text, (qa_rect.x + 10, qa_rect.y + 10))
        margin = 5
        box_width = (qa_rect.width - 3 * margin) // 2
        box_height = (qa_rect.height - 120 - 3 * margin) // 2
        answer_positions = [
            (qa_rect.x + margin, qa_rect.y + 120 + margin, box_width, box_height),
            (qa_rect.x + box_width + 2 * margin, qa_rect.y + 120 + margin, box_width, box_height),
            (qa_rect.x + margin, qa_rect.y + 120 + box_height + 2 * margin, box_width, box_height),
            (qa_rect.x + box_width + 2 * margin, qa_rect.y + 120 + box_height + 2 * margin, box_width, box_height),
        ]
        for i, button in enumerate(self.answer_buttons):
            answer_rect = button.rect
            if button.text == correct_answer:
                color = (102, 191, 58)
                alpha = 255
            elif button.text == chosen_answer:
                color = (224, 27, 62)
                alpha = 255
            else:
                color = (224, 27, 62)
                alpha = 128
            surface = pygame.Surface((answer_rect.width, answer_rect.height))
            surface.set_alpha(alpha)
            surface.fill(color)
            self.screen.blit(surface, (answer_rect.x, answer_rect.y))
            answer_text = MAIN_FONT.render(button.text, True, WHITE)
            self.screen.blit(answer_text, (answer_rect.x + 70, answer_rect.y + answer_rect.height // 2 - 10))
        message_surface = MAIN_FONT.render(self.message, True, BLACK)
        message_bg = pygame.Surface((message_surface.get_width() + 20, message_surface.get_height() + 10))
        message_bg.fill(self.message_color)
        self.screen.blit(message_bg, (qa_rect.x + 10, qa_rect.y + qa_rect.height + 20))
        self.screen.blit(message_surface, (qa_rect.x + 20, qa_rect.y + qa_rect.height + 25))
        pygame.display.flip()
        pygame.time.wait(3000)

    def display_score(self):
        background = pygame.image.load(BACKGROUND_IMAGE)
        self.screen.blit(pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
        small_logo_font = pygame.font.Font("fonts/gooddog-plain.regular.ttf", 80)
        logo_text = small_logo_font.render("Kahoot!", True, WHITE)
        self.screen.blit(logo_text, (SCREEN_WIDTH // 2 - logo_text.get_width() // 2, 20))
        title_font = pygame.font.Font("fonts/Montserrat-Bold.ttf", 40)
        scoreboard_text = title_font.render("Scoreboard", True, WHITE)
        self.screen.blit(scoreboard_text, (SCREEN_WIDTH // 2 - scoreboard_text.get_width() // 2, 120))
        sorted_scores = sorted(game.scores.items(), key=lambda item: item[1], reverse=True)
        ranking_font = pygame.font.Font("fonts/Montserrat-Bold.ttf", 25)
        y_offset = 200
        previous_score = None
        for rank, (player, score) in enumerate(sorted_scores, 1):
            rank_text = ranking_font.render(f"{rank}. {player}", True, WHITE)
            score_text = ranking_font.render(f"{score}", True, WHITE)
            self.screen.blit(rank_text, (100, y_offset))
            self.screen.blit(score_text, (SCREEN_WIDTH - 200, y_offset))
            if previous_score is not None:
                difference = previous_score - score
                diff_text = ranking_font.render(f"-{difference}", True, WHITE)
                self.screen.blit(diff_text, (SCREEN_WIDTH // 2 - diff_text.get_width() // 2, y_offset))
            previous_score = score
            y_offset += 50
        pygame.display.flip()
        pygame.time.wait(5000)
        game.reset_scores()
        main_menu = MainMenu(self.screen)
        main_menu.run()


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
            print("Cannot start game: At least one question set and one player required")

    def reset_scores(self):
        self.scores = {}


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
