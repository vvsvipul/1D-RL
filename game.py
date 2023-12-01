import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 600, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Q-Learning Game")
pygame.mixer.init()
pygame.mixer.music.load("background.mpeg")
pygame.mixer.music.play(-1)
# Load and scale background image
background_image = pygame.image.load('background.png')
background_image = pygame.transform.scale(background_image, (600, 400))
kill_sound = pygame.mixer.Sound("killi.mp3")
# Colors
purple = (128, 0, 128)  # Purple color for illustration, can be set to a transparent value for the actual game
black = (0, 0, 0)
white = (255, 255, 255)
collect=[]
# Load images
snake_image = pygame.image.load('front_p.png')
snake_image_back = pygame.image.load('back_p.png')
apple_image = pygame.image.load('p.png')
kill_image = pygame.image.load('orange_kill_1.png')

# Scale images to desired dimensions-*
kill_image = pygame.transform.scale(kill_image, (45, 45))
snake_image_back =  pygame.transform.scale(snake_image_back, (50, 50))
snake_image = pygame.transform.scale(snake_image, (50, 50))
apple_image = pygame.transform.scale(apple_image, (50, 50))

# Game variables
q_learning = {'0': [0, 0], '1': [0, 0], '2': [0, 0], '3': [0, 0], '4': [0, 0], '5': [0, 0], '6': [0,0 ], '7': [0,0 ], '8': [0, 0], '9': [0, 0]}
n_game = 0
loss = 0
win = 0
def create_platform(width):
    platform = []
    for i in range(0, 10):
        platform.append(" ")
    return platform

def display_platform(platform, score, episode,player=snake_image,target=apple_image):
    screen.blit(background_image, (0, 0))  # Set the background image
    font = pygame.font.Font(None, 36)
    for i, item in enumerate(platform):
        if item == "snake":
            screen.blit(player, (50+ i * 50, 320))
        elif item == "apple":
            screen.blit(target, (50 + i * 50, 320))
        else:
            text = font.render(str(item), True, black)
            screen.blit(text, (50 + i * 50, 300))
    score_text = font.render(f"Score: {score}", True, black)
    screen.blit(score_text, (50, 50))
    pygame.display.flip()
    if episode < 0:
        pygame.time.wait(990)

def stop(score, best_score, flag, episode):
    global n_game
    global loss
    global win
    print(flag)
    if flag:
        print("loss")
        loss+=1
    else:
        print("win")
        win+=1
    print("episodes number : ", episode)
    print(repr(q_learning))
    start()


def maxi(a, b):
    if a < b:
        return 1
    else:
        return 0

def make_move(episode, best_score, score, pos_player, pos_food, platform):
    global n_game
    flag = False  # Initialize flag
    clock = pygame.time.Clock()
    while True:
        clock.tick(30)  # Control the speed of movement
        score += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pp = pos_player
        curr_state = str(pp)

        if random.randint(0, 200) < 2 * episode or curr_state not in q_learning:
            move = random.randint(0, 10000000) % 2
            if curr_state not in q_learning:
                q_learning[curr_state] = [0, 0]
        else:
            move = maxi(q_learning[curr_state][0], q_learning[curr_state][1])
        player = snake_image
        target = apple_image
        if move == 1 and pos_player < 9: 
            player = snake_image
            pos_player += 1
        elif move == 0 and pos_player >=0:
            player = snake_image_back
            pos_player -= 1

        ahead_state = str(pos_player)
        learning_factor = 0.01
        gamma = 0.2
        if pos_player < 0:
            q_learning[curr_state][0] =((1-learning_factor)* q_learning[curr_state][0] )- ((learning_factor)*(100))
            flag = True
            print("yes")
            stop(score, best_score, flag, episode)
        elif pos_player == pos_food:
            target = kill_image
            q_learning[curr_state][1] = (1-learning_factor)* q_learning[curr_state][0] + ((learning_factor)*(100))
            flag = False
            # pygame.mixer.music.stop() 
            kill_sound.play()
            display_platform(platform, score, episode,player,target)
            stop(score, best_score, flag, episode)
        else:
            if pos_player < pp:
                q_learning[curr_state][0]=(1-learning_factor)*q_learning[curr_state][0]+((learning_factor)*(1+ gamma*(max(q_learning[ahead_state][0],q_learning[ahead_state][1]))))
            else:
                q_learning[curr_state][0]=(1-learning_factor)*q_learning[curr_state][0]+((learning_factor)*(1+ gamma*(max(q_learning[ahead_state][0],q_learning[ahead_state][1]))))

            platform[pp] = " "
            platform[pos_food] = "apple"
            platform[pos_player] = "snake"
            display_platform(platform, score, episode,player,target)

def start():
    global n_game
    n_game += 1
    width = 10
    episode = 200 - n_game
    platform = create_platform(width)
    score = 0
    display_platform(platform, score, episode)

    pos_food = 7
    pos_player = 0
    pos_food = random.randint(2, 9)
    display_platform(platform, score, episode)

    best_score =abs(pos_food - pos_player)

    make_move(episode, best_score, score, pos_player, pos_food, platform)


start()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
s
pygame.quit()
