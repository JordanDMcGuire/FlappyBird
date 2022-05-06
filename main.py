import pygame
import sys
import random


def draw_floor():  # This function will draw two copies of the floor to chase each other.  The second floor is drawn
    # off screen.
    screen.blit(floor_surface, (floor_x_pos, 450))
    screen.blit(floor_surface, (floor_x_pos + 288, 450))


def create_pipe():  # This is called from the event listener in the game loop. It sends new pipes to pipe_list
    random_pipe_pos = random.choice(pipe_height)  # The list "pipe_height" is below. It contains 3 heights.
    bottom_pipe = pipe_surface.get_rect(
        midtop=(300, random_pipe_pos))  # grab by mid-top and draw at 300 pixels. Slightly off screen.
    top_pipe = pipe_surface.get_rect(
        midbottom=(300, random_pipe_pos - 150))  # Grab it by the mid-bottom and set it 150 pixels above bottom pipe.
    return bottom_pipe, top_pipe  # sends the pipes, their rectangles, and their pos data back to the caller


def move_pipes(
        pipes):  # Called by pipe_list in the game's for loop. The parameter sent by pipe_list is pipe_list itself.
    for pipe in pipes:  # Iterates over pipe_list
        pipe.centerx -= 2.5  # center_x is an attribute of the pipe's rectangle this takes all of the existing pipes
        # and moves them 2.5 pixels to the left.
    return pipes  # sends the altered pipe_list back to the caller


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False
    if bird_rect.top <= -100:
        death_sound.play()
        return False
    if bird_rect.bottom >= 450:
        fall_sound.play()
        return False

    return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 8, 1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(144, 100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(144, 100))
        screen.blit(score_surface, score_rect)
        # high score
        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(144, 425))
        screen.blit(high_score_surface, high_score_rect)


def update_score(score_x, high_score_x):
    if score_x > high_score_x:
        high_score_x = score_x
    return high_score_x


pygame.mixer.pre_init(frequency=44100, size=32, channels=2, buffer=512)
pygame.init()  # Create an instance of pygame

screen = pygame.display.set_mode(
    (288, 512))  # Creates a variable called screen that is assigned a pygame display with a
# resolution of 576 x 1024 for easy image upscaling.

game_icon = pygame.image.load('assets/favicon.ico')
pygame.display.set_icon(game_icon)
pygame.display.set_caption('Flappy Bird')

clock = pygame.time.Clock()  # Creates a variable called clock that is assigned a pygame clock
game_font = pygame.font.Font('04B_19.ttf', 20)

# Game Variables
gravity = 0.17  # This will be used to simulate the gravity in game by using it's value to decrement the position of
# the bird
bird_movement = 0  # This will be used to impose gravity on the bird's rectangle.
game_active = True  # This is used for collisions and game overs
score = 0
high_score = 0

bg_surface = pygame.image.load(
    'assets/sprites/background-day.png').convert()  # Call the background image to a new surface variable
bg_surface = pygame.transform.scale(bg_surface, (288, 512))  # Scale the image to fit the screen

floor_surface = pygame.image.load('assets/sprites/base.png').convert()  # Call the floor image
floor_surface = pygame.transform.scale(floor_surface, (288, 62))  # scale the floor image
floor_x_pos = 0  # Variable used to move the floor

bird_downflap = pygame.image.load('assets/sprites/bluebird-downflap.png').convert_alpha()
bird_midflap = pygame.image.load('assets/sprites/bluebird-midflap.png').convert_alpha()
bird_upflap = pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(50, 256))
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

# bird_surface = pygame.image.load(
#    'assets/sprites/bluebird-midflap.png').convert_alpha()  # This loads the bird image midflap
# bird_surface = pygame.transform.scale(bird_surface, (68, 48)) *this could be used to change the size of the bird
# bird_rect = bird_surface.get_rect(center=(
#    50, 256))  # This draws a rectangle around the bird and places the center of the rectangle/bird comb at 50 x 256

pipe_surface = pygame.image.load('assets/sprites/pipe-green.png')  # load the pipe image
pipe_list = []  # Used by multiple aspects of the pipe sequence to keep track of the pipes
SPAWNPIPE = pygame.USEREVENT  # This creates an event to listen to called SPAWNPIPE
pygame.time.set_timer(SPAWNPIPE, 1200)  # This calls spawnpipe every 1.2 seconds
pipe_height = [230, 300, 400]  # Used by the create_pipe function above.

game_over_surface = pygame.image.load('assets/sprites/message.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center=(144, 256))

flap_sound = pygame.mixer.Sound('assets/audio/wing.ogg')
death_sound = pygame.mixer.Sound('assets/audio/hit.wav')
score_sound = pygame.mixer.Sound('assets/audio/point.ogg')
score_sound_countdown = 100
fall_sound = pygame.mixer.Sound('assets/audio/die.ogg')

while True:  # Initiate the loop in which the game will run

    for event in pygame.event.get():  # This is a loop that interacts with the game variables
        # Exit
        if event.type == pygame.QUIT:  # This listens for the "close" event from the user
            pygame.quit()  # End the instance of pygame
            sys.exit()  # Properly closes the program
        # Jump
        if event.type == pygame.KEYDOWN:  # Code for key listening
            if event.key == pygame.K_SPACE and game_active:  # Listen for space bar
                bird_movement = 0  # When spacebar is pressed reset the bird's gravity pull so that it doesn't get
                # too strong
                bird_movement -= 4  # Also move the bird upwards a bit as a jump!
                flap_sound.play()
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (50, 256)
                bird_movement = 0
                score = 0

        # Pipes
        if event.type == SPAWNPIPE:  # SPAWNPIPE is defined above. It is on a timer controlled by pygame and it calls
            # every 1.2 seconds.
            pipe_list.extend(create_pipe())  # Create pipe is defined above.

        # Flapping
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface, bird_rect = bird_animation()

    screen.blit(bg_surface, (0, 0))  # Apply the background surface variable to the screen

    if game_active:
        # Bird
        bird_movement += gravity  # This imposes gravity on the bird.
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement  # This moves the birds rectangle and the bird moves with it
        screen.blit(rotated_bird, bird_rect)  # This draws the bird

        # Collisions
        game_active = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(
            pipe_list)  # move_pipes(pipes) is defined above. It accepts pipe_list and moves each rectangle's centerx
        # attribute 2.5 pixels to the left.
        draw_pipes(pipe_list)

        # Score
        score += 0.01
        score_display('main_game')

        # Score sound
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

    # Floor
    floor_x_pos -= 1  # Move the floor position each time the loop repeats
    draw_floor()  # Draw 2 floors, one after another. The second is drawn off screen to the right
    if floor_x_pos <= -288:  # If the floor is out of space to the left of the screen, reset its position to 0.
        floor_x_pos = 0

    pygame.display.update()  # This allows pygame to continuously refresh the image on the screen.

    clock.tick(100)  # Sets the speed of the update. In this case 120 frames per second
