import sys
import pygame
from game import Game

def get_difficulty(screen):
    prob = 0.1
    size_text = "Current difficulty: Low (10% bombs)"
    print(size_text)
    font = pygame.font.Font(None, 27)

    #background image
    background_image = pygame.image.load("./images/nen1.png")
    screen.blit(background_image, (0, 0))  # Draw background image

    # Render the heading text
    text_title = font.render("Welcome to Minesweeper", True, (0, 0, 0))
    text_heading = font.render("Choose game difficulty (press keys 1, 2, or 3):", True, (0, 0, 0))
    text_low = font.render("1. Low (10% bombs) (press key 1)", True, (0, 0, 0))
    text_medium = font.render("2. Medium (20% bombs) (press key 2)", True, (0, 0, 0))
    text_high = font.render("3. High (30% bombs) (press key 3)", True, (0, 0, 0))



    # Adjust the positioning of the text
    screen.blit(text_title , (50,10))
    screen.blit(text_heading, (50, 50))
    screen.blit(text_low, (50, 90))
    screen.blit(text_medium, (50, 130))
    screen.blit(text_high, (50, 170))
    
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    prob = 0.1
                    size_text = "Current difficulty: Low (10% bombs)"
                    return prob, size_text
                elif event.key == pygame.K_2:
                    prob = 0.2
                    size_text = "Current difficulty: Medium (20% bombs) "
                    return prob, size_text
                elif event.key == pygame.K_3:
                    prob = 0.3
                    size_text = "Current difficulty: High (30% bombs)"
                    return prob, size_text


def main():
    pygame.init()
    screen = pygame.display.set_mode((500, 300))
    pygame.display.set_caption("Minesweeper Difficulty")

    clock = pygame.time.Clock()  # Đối tượng clock để giới hạn tốc độ khung hình
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        prob, size_text = get_difficulty(screen)
        print(size_text)

        # Chạy trò chơi với độ khó đã chọn
        size = (10, 10)  # Kích thước mặc định, bạn có thể điều chỉnh nếu cần
        g = Game(size, prob)
        g.run()

        clock.tick(30)  # Giới hạn tốc độ khung hình

if __name__ == '__main__':
    main()
