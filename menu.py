import pygame, sys, time, random
from button import Button
from main import main  # Import the main function from main.py
from checkers.constants import get_font, SCREEN, fanfare_sound, sad_trombone

pygame.init()

pygame.display.set_caption("Main Menu")

BG1 = pygame.image.load("assets/background_new.png") #background for the start screen- pink with flowers
BG2 = pygame.image.load("assets/rules.png") #background for the rules screen
BG3 = pygame.image.load("assets/baby.png") #baby image for the loser screen
settings_background = pygame.image.load("assets/settings_background.png") #background for the settings screen

celebration1 = pygame.image.load("assets/celebration1.png") #for winner
celebration2 = pygame.image.load("assets/celebration2.png")

tear = pygame.image.load("assets/tear.png")
tear_img = pygame.transform.scale(tear, (30, 45)) #resizes the tear to match size of baby

confetti = pygame.image.load("assets/confetti.png")
confetti_img = pygame.transform.scale(confetti, (200, 300))

LEFT_EYE_X, LEFT_EYE_Y = 330, 455 #coordinates for the left eye of baby
RIGHT_EYE_X, RIGHT_EYE_Y = 450, 455 #coordinates for the right eye

class Tear:
    def __init__(self, x, y):
        self.x = x + random.randint(-3, 3)  #adds some slight variation for where the tears appear, so individual tears are visible when they fall
        self.y = y
        self.speed = random.uniform(2, 5)  #random speed to create a natural effect

    def update(self):
        self.y += self.speed  #moves the tear down the screen
        if self.y > 800:  #reset when it reaches bottom of the screen
            self.y = random.randint(LEFT_EYE_Y, LEFT_EYE_Y + 20)

    def draw(self, screen):
        screen.blit(tear_img, (self.x, self.y))

class Confetti:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = random.uniform(2, 5)

    def update(self):
        self.y += self.speed
        if self.y > 800:
            self.y = random.randint(0, 800)

    def draw(self, screen):
        screen.blit(confetti_img, (self.x, self.y))

#creates multiple tears from both eyes
tears = [Tear(LEFT_EYE_X, LEFT_EYE_Y) for _ in range(5)] + [Tear(RIGHT_EYE_X, RIGHT_EYE_Y) for _ in range(5)]
confettis = [Confetti(random.randint(0, 800), random.randint(0, 200)) for _ in range(10)]

def loser():
    pygame.display.set_caption("Loser")

    start_time = time.time()
    clock = pygame.time.Clock()

    #creates the text message for the screen
    LOSER_TEXT = get_font(70).render("YOU LOSE!", True, "White")
    LOSER_RECT = LOSER_TEXT.get_rect(center=(400, 100))

    #tracks how long the tears have been falling
    tears_start_time = time.time()

    while True:
        sad_trombone.play(-1)

        #draws background with baby image
        SCREEN.blit(BG3, (0, 0)) 

        SCREEN.blit(LOSER_TEXT, LOSER_RECT)

        if time.time() - tears_start_time < 6:
            for tear in tears:
                tear.update()
                tear.draw(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q): #so that the player can quit the game more quickly, than going through the start menu
                pygame.quit() 
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                sad_trombone.stop()
                main_menu()
                return

        pygame.display.update()
        clock.tick(30)  #smooth 30 FPS animation

        #after 6 seconds of tears, the screen will clear and return to the main menu
        if time.time() - tears_start_time >= 6:
            SCREEN.fill("black")
            time.sleep(0.3)
            sad_trombone.stop()
            main_menu()
            return

def winner():
    pygame.display.set_caption("Winner")

    SCREEN.blit(celebration1, (0, 0))

    
    confetti_start_time = time.time()

    #defines the  colors for the text
    colors = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (51, 255, 51), (0, 191, 0), (57, 229, 225), (51, 51, 255), (168, 37, 255), (238, 130, 238)]

    start_time = time.time()
    last_background_switch = time.time()  #tracks last background switch time
    background_switch_interval = 0.2  #so that the background switches every 0.2 seconds

    j = 0  #for alternating the background
    clock = pygame.time.Clock()  #controls frame rate

    while True:
        fanfare_sound.play(-1)

        elapsed_time = time.time() - start_time  #updates elapsed time

        if elapsed_time >= 6:  #stops after 4 seconds
            break

        if time.time() - confetti_start_time < 6:
            for confetti in confettis:
                confetti.update()
                confetti.draw(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                fanfare_sound.stop()
                main_menu()
                return

        #in order to switch the background every 0.2 seconds
        if time.time() - last_background_switch >= background_switch_interval:
            if j % 2 == 0:
                SCREEN.blit(celebration1, (0, 0))  #celebration1
            else:
                SCREEN.blit(celebration2, (0, 0))  #celebration2
            last_background_switch = time.time()  # update the last background switch time
            j += 1  #increment j to alternate between backgrounds

        #cycle through colors for the text every 0.2 seconds
        color_change_time = time.time() - start_time  #track time for color changes
        color_index = int(color_change_time / 0.2) % len(colors)  #determines the color based on time
        current_color = colors[color_index]

        #draw text with the current color
        WINNER_TEXT = get_font(70).render("YOU WIN!", True, current_color)
        WINNER_RECT = WINNER_TEXT.get_rect(center=(400, 100))
        SCREEN.blit(WINNER_TEXT, WINNER_RECT)  #draw text with changing colors
        pygame.display.update()

        clock.tick(30)  #limit the frame rate to 30 FPS for smooth animation
    fanfare_sound.stop()
    main_menu()  #switches to main_menu after 4 seconds

def play():
    settings()
    
def options():
    pygame.display.set_caption("Rules")

    while True:
        SCREEN.blit(BG2, (0, 0))

        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        OPTIONS_BACK = Button(image=None, pos=(600, 690), 
                            text_input="BACK", font=get_font(40), base_color="#455946", hovering_color="#5c0603ff")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                pygame.quit()
                sys.exit()
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_b):
                    main_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def settings():
    global difficulty
    pygame.display.set_caption("Settings")
    while True:
            board_background = pygame.image.load("assets/board_background.png")
            SCREEN.blit(board_background, (0, 0)) 
            
            settings_rect = settings_background.get_rect(center=(400, 400))
            SCREEN.blit(settings_background, settings_rect.topleft)

            SETTINGS_MOUSE_POS = pygame.mouse.get_pos()
            
            SETTINGS_TEXT = get_font(70).render("SETTINGS", True, "White")
            SETTINGS_RECT = SETTINGS_TEXT.get_rect(center=(400, 100))

            LV1_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(400, 250), 
                                text_input="EASY", font=get_font(75), base_color="#D8FCFF", hovering_color="White")
            LV2_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(400, 400), 
                                text_input="MEDIUM", font=get_font(68), base_color="#D8FCFF", hovering_color="White")
            LV3_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(400, 550), 
                                text_input="HARD", font=get_font(75), base_color="#D8FCFF", hovering_color="White")
            
            settings_BACK = Button(image=None, pos=(655, 710), 
                            text_input="BACK", font=get_font(40), base_color="White", hovering_color="#D8FCFF")
            
            settings_BACK.changeColor(SETTINGS_MOUSE_POS)
            settings_BACK.update(SCREEN)


            SCREEN.blit(SETTINGS_TEXT, SETTINGS_RECT)

            for button in [LV1_BUTTON, LV2_BUTTON, LV3_BUTTON]:
                button.changeColor(SETTINGS_MOUSE_POS)
                button.update(SCREEN)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                    pygame.quit()
                    sys.exit()
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_b):
                    main_menu()
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if LV1_BUTTON.checkForInput(SETTINGS_MOUSE_POS):
                        difficulty = "easy"
                        main()
                    if LV2_BUTTON.checkForInput(SETTINGS_MOUSE_POS):
                        difficulty = "medium"
                        main()
                    if LV3_BUTTON.checkForInput(SETTINGS_MOUSE_POS):
                        difficulty = "hard"
                        main()
                    if settings_BACK.checkForInput(SETTINGS_MOUSE_POS):
                        main_menu()

            pygame.display.update()


def main_menu():
    while True:
        SCREEN.blit(BG1, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(70).render("START MENU", True, "#ff0000")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(400, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#D8FCFF", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(400, 400), 
                            text_input="RULES", font=get_font(75), base_color="#D8FCFF", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(400, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#D8FCFF", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
