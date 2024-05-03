import pygame
from piece import Piece
from board import Board
import os
from solver import Solver
from window import GameWindow
from blinktext import BlinkText

class Game:
    def __init__(self, size, prob):
        pygame.init()
        pygame.mixer.init()
        
        self.board = Board(size, prob)
        self.screen = pygame.display.set_mode((800, 600))
        self.pieceSize = (self.screen.get_width() / size[1], self.screen.get_height() / size[0])
        self.loadPictures()
        self.solver = Solver(self.board)
        self.window = GameWindow()
        print("Actual screen size:", pygame.display.Info().current_w, pygame.display.Info().current_h)
    
        self.window.game = self
        self.win_message = BlinkText("YOU WIN!", font_size=40)
        self.lose_message = BlinkText("YOU LOSE!", font_size=40)
        self.replay_button_rect = pygame.Rect(self.screen.get_width() // 2 - 75, self.screen.get_height() // 2 - 25, 150, 50)
        self.exit_button_rect = pygame.Rect(self.screen.get_width() // 2 - 75, self.screen.get_height() // 2 + 50, 150, 50)
        self.buttons_visible = False
        self.clock = pygame.time.Clock()
        self.time_elapsed = 0
        self.game_over = False
        self.first_click_done = False 


    def run(self):
        self.window.draw_start_menu()
        self.window.handle_start_menu()

    def reset(self):
        self.board.reset()
        self.buttons_visible = False
        self.win_message.visible = False
        self.lose_message.visible = False

    def loadPictures(self):
        self.images = {}
        imagesDirectory = "images"
        for fileName in os.listdir(imagesDirectory):
            if not fileName.endswith(".png"):
                continue
            path = os.path.join(imagesDirectory, fileName)
            img = pygame.image.load(path)
            img = img.convert()
            img = pygame.transform.scale(img, (int(self.pieceSize[0]), int(self.pieceSize[1])))
            self.images[fileName.split(".")[0]] = img

    def run_game(self):
        running = True
        while running:
            self.clock.tick(60)
            if not self.game_over:
                self.time_elapsed += self.clock.get_time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause_game()

                elif event.type == pygame.MOUSEBUTTONDOWN and not (self.board.getWon() or self.board.getLost()):
                    rightClick = pygame.mouse.get_pressed(num_buttons=3)[2]
                    if not self.first_click_done:
                        index = tuple(int(pos // size) for pos, size in zip(pygame.mouse.get_pos(), self.pieceSize))[::-1]
                        piece = self.board.getPiece(index)
                        while piece.getHasBomb():
                            self.board.reset()
                            piece = self.board.getPiece(index)
                        self.first_click_done = True
                        self.board.handleClick(piece, rightClick)
                    else:
                        self.handleClick(pygame.mouse.get_pos(), rightClick)

            self.screen.fill((0, 0, 0))
            self.draw()
            pygame.display.flip()

            if self.board.getWon() or self.board.getLost():
                self.handle_game_end()

            self.win_message.update()
            self.lose_message.update()

        pygame.quit()


    def draw(self):
        topLeft = (0, 0)
        for row in self.board.getBoard():
            for piece in row:
                if topLeft[0] + self.pieceSize[0] <= self.screen.get_width() and topLeft[1] + self.pieceSize[1] <= self.screen.get_height():
                    rect = pygame.Rect(topLeft, self.pieceSize)
                    image = self.images[self.getImageString(piece)]
                    self.screen.blit(image, topLeft)
                topLeft = topLeft[0] + self.pieceSize[0], topLeft[1]
            topLeft = (0, topLeft[1] + self.pieceSize[1])

        if self.board.getWon():
            self.win_message.visible = True
            pygame.draw.rect(self.screen, (0, 255, 0), self.replay_button_rect)
            pygame.draw.rect(self.screen, (255, 0, 0), self.exit_button_rect)
            replay_text = pygame.font.Font(None, 36).render("Replay", True, (255, 255, 255))
            exit_text = pygame.font.Font(None, 36).render("Exit", True, (255, 255, 255))
            replay_text_rect = replay_text.get_rect(center=self.replay_button_rect.center)
            exit_text_rect = exit_text.get_rect(center=self.exit_button_rect.center)
            self.screen.blit(replay_text, replay_text_rect)
            self.screen.blit(exit_text, exit_text_rect)
            if self.win_message.visible:
                win_message_rect = self.win_message.surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 50))
                self.screen.blit(self.win_message.surface, win_message_rect)

        elif self.board.getLost():
            self.lose_message.visible = True
            pygame.draw.rect(self.screen, (0, 255, 0), self.replay_button_rect)
            pygame.draw.rect(self.screen, (255, 0, 0), self.exit_button_rect)
            replay_text = pygame.font.Font(None, 36).render("Replay", True, (255, 255, 255))
            exit_text = pygame.font.Font(None, 36).render("Exit", True, (255, 255, 255))
            replay_text_rect = replay_text.get_rect(center=self.replay_button_rect.center)
            exit_text_rect = exit_text.get_rect(center=self.exit_button_rect.center)
            self.screen.blit(replay_text, replay_text_rect)
            self.screen.blit(exit_text, exit_text_rect)
            if self.lose_message.visible:
                lose_message_rect = self.lose_message.surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 50))
                self.screen.blit(self.lose_message.surface, lose_message_rect)

        elif not self.board.getWon() and not self.board.getLost():
            if self.buttons_visible:
                pygame.draw.rect(self.screen, (0, 255, 0), self.replay_button_rect)
                pygame.draw.rect(self.screen, (255, 0, 0), self.exit_button_rect)
                replay_text = pygame.font.Font(None, 36).render("Replay", True, (255, 255, 255))
                exit_text = pygame.font.Font(None, 36).render("Exit", True, (255, 255, 255))
                replay_text_rect = replay_text.get_rect(center=self.replay_button_rect.center)
                exit_text_rect = exit_text.get_rect(center=self.exit_button_rect.center)
                self.screen.blit(replay_text, replay_text_rect)
                self.screen.blit(exit_text, exit_text_rect)
                if self.win_message.visible:
                    win_message_rect = self.win_message.surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 50))
                    self.screen.blit(self.win_message.surface, win_message_rect)
                elif self.lose_message.visible:
                    lose_message_rect = self.lose_message.surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 50))
                    self.screen.blit(self.lose_message.surface, lose_message_rect)

        time_text = pygame.font.Font(None, 24).render(f"Time: {self.time_elapsed // 1000} s", True, (255, 255, 255))
        self.screen.blit(time_text, (10, 10))
                        
    def getImageString(self, piece):
        if piece.getClicked():
            return str(piece.getNumAround()) if not piece.getHasBomb() else 'bomb-at-clicked-block'
        if self.board.getLost():
            if piece.getHasBomb():
                return 'unclicked-bomb'
            return 'wrong-flag' if piece.getFlagged() else 'empty-block'
        return 'flag' if piece.getFlagged() else 'empty-block'

    def handleClick(self, position, flag):
        index = tuple(int(pos // size) for pos, size in zip(position, self.pieceSize))[::-1]
        piece = self.board.getPiece(index)
        if piece.getClicked():
            return
        if flag:
            piece.toggleFlag()
        else:
            self.board.handleClick(piece, flag)

    def handle_game_end(self):
        if self.board.getWon() or self.board.getLost():
            mouse_pos = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0]:
                if self.replay_button_rect.collidepoint(mouse_pos):
                    self.board.reset()
                    self.time_elapsed = 0
                    self.game_over = False
                elif self.exit_button_rect.collidepoint(mouse_pos):
                    self.window.draw_start_menu()
                    self.window.handle_start_menu()

            if self.board.getWon():
                self.win()
                if not self.game_over:
                    self.save_record()

            elif self.board.getLost():
                self.lose()

    def win(self):
        sound = pygame.mixer.Sound('win.wav')
        sound.play()
        if not self.game_over:
            self.save_record()
        self.game_over = True

    def save_record(self):

        records = []
        try:
            with open('records.txt', 'r') as f:
                records = f.readlines()
        except FileNotFoundError:
            pass

        if len(records) >= 11:
            max_time_index = max(range(len(records)), key=lambda i: int(records[i].split()[1]))
            
            if self.time_elapsed // 1000 < int(records[max_time_index].split()[1]):
                records[max_time_index] = f"Time: {self.time_elapsed // 1000} s\n"
        else:
            records.append(f"Time: {self.time_elapsed // 1000} s\n")

        records.sort(key=lambda x: int(x.split()[1]))

        with open('records.txt', 'w') as f:
            f.writelines(records)

        print("Record saved successfully!")


    def lose(self):
        sound = pygame.mixer.Sound('lose.wav')
        sound.play()
        self.game_over = True

    def pause_game(self):
        self.window.draw_start_menu()
        self.window.handle_start_menu()
        pygame.time.wait(500)  # Tạm dừng trò chơi trong 500ms để tránh trạng thái Esc bị nhầm lẫn
