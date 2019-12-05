import math
from threading import Thread
from time import *
import pygame
from particle import Particle
from graphics import *
import secrets

width, height = 1600, 900
particles = []
particle_circles = []
delay_time = 0.01
critical_mass = 10000
sound_file = "explosion_2.wav"


def simulator():
    pygame.font.init()
    pygame.mixer.init()
    # explosion = pygame.mixer.music.load(sound_file)
    font = pygame.font.SysFont('comicsansms', 32)
    radius = 0.0
    RED = pygame.Color("#FF0000")
    running = True
    growing = False
    start_time = 0
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    particleImg = pygame.image.load(
        'C:\\Users\\yueva\\AppData\\Local\\Programs\\Python\\Python37-32\\gravity_simulator\\particle.gif').convert_alpha()
    screen.fill((0, 0, 0))
    pygame.display.flip()
    pygame.display.init()
    surface = pygame.display.get_surface()
    first_run = True
    run_count = 0
    real_time_simulation = True

    # Title Screen
    # Title text
    title_text = font.render("Gravity Simulator", True, (0, 255, 0))
    screen.blit(title_text, ((width/2) - (title_text.get_width() / 2), (height/2) - (title_text.get_height() / 2)))

    # Define buttons
    play_button = pygame.Rect((width/2 - 350, height/2 + 50), (300, 100))
    settings_button = pygame.Rect((width / 2 + 50, height / 2 + 50), (300, 100))

    # Define button text
    play_text = font.render("Play", True, (0, 0, 0))
    play_text_rect = play_text.get_rect()
    play_text_rect.center = (width / 2 - 350, height / 2 + 100)
    settings_text = font.render("Settings", True, (0,0,0))
    settings_text_rect = settings_text.get_rect()
    settings_text_rect.center = (width / 2 + 150, height / 2 + 100)

    # Draw buttons
    pygame.draw.rect(screen, (0,255,0), play_button)
    pygame.draw.rect(screen, (0,255,0), settings_button)
    screen.blit(play_text, (play_button[0] + 150 - (play_text.get_width()/2), play_button[1] + 25))
    screen.blit(settings_text, (settings_button[0] + 150 - (settings_text.get_width()/2), settings_button[1] + 25))
    pygame.display.flip()

    # Get input for buttons
    events = pygame.event.get()
    break_out = False
    while not break_out:
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                print("mouse button down")
                if play_button.collidepoint(e.pos):
                    print("play pressed")
                    break_out = True
                    break
                elif settings_button.collidepoint(e.pos):
                    print("settings pressed")
                    screen.fill((0,0,0))
                    # Define the Real time simulation prompt
                    real_time_text = font.render("Real time simulation", True, (255, 255, 255))
                    real_time_rect = real_time_text.get_rect()
                    real_time_rect.center = (width / 2, height / 2)
                    screen.blit(real_time_text,
                                ((width / 2) - (real_time_text.get_width() / 2),
                                 (height / 2) - real_time_text.get_height()))

                    # Define the yes button
                    yes_rectangle = pygame.Rect((width / 2 - 350, height / 2 + 50), (300, 100))
                    pygame.draw.rect(screen, (0, 255, 0), yes_rectangle)
                    yes_text = font.render("Yes", True, (0, 0, 0))
                    yes_rect = yes_text.get_rect()
                    yes_rect.center = (width / 2 - 350, height / 2 + 100)
                    screen.blit(yes_text, (yes_rect[0] + 150, yes_rect[1]))

                    # Define the no button
                    no_rectangle = pygame.Rect((width / 2 + 50, height / 2 + 50), (300, 100))
                    pygame.draw.rect(screen, (0, 255, 0), no_rectangle)
                    no_text = font.render("No", True, (0, 0, 0))
                    no_rect = no_text.get_rect()
                    no_rect.center = (width / 2 + 150, height / 2 + 100)
                    screen.blit(no_text, (no_rect[0] + 50, no_rect[1]))

                    pygame.display.flip()
                    events_2 = pygame.event.get()
                    real_time_simulation = False
                    # while pygame.MOUSEBUTTONDOWN not in events:
                    #    sleep(0.1)
                    #    events = pygame.event.get()

                    # Wait for one of the buttons to be pressed and determine which one
                    break_out_2 = False
                    while not break_out_2:
                        for event in events_2:
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                print("mouse button down")
                                if yes_rectangle.collidepoint(event.pos):
                                    real_time_simulation = True
                                    break_out_2 = True
                                elif no_rectangle.collidepoint(event.pos):
                                    real_time_simulation = False
                                    break_out_2 = True
                                break
                        events_2 = pygame.event.get()

                    print(real_time_simulation)
                    #######
                    break_out = True
                break
        events = pygame.event.get()
    sleep(0.5)
    pygame.event.get()
    screen.fill((0, 0, 0))
    pygame.display.flip()

    # Main loop of the program
    while running:
        # If the user pressed no, set up the run simulation button in the corner
        if not real_time_simulation:
            if run_count == 0:
                event = pygame.event.get()
                run_rectangle = pygame.Rect((width - 250, 100), (300, 100))
                run_text = font.render("Run simulation", True, (0, 0, 0))
                run_rect = run_text.get_rect()
                run_rect.center = (width - 250, 100)
            pygame.draw.rect(screen, (0, 255, 0), run_rectangle)
            screen.blit(run_text, (run_rect[0] + 125, run_rect[1] + 50))

        run_count += 1
        # init_velocity_x = init_velocity_y = 0

        # Update the screen every 5 cycles while the simulation is running to reduce flashing effect
        if run_count % 5 == 0 and real_time_simulation:
            screen.fill((0, 0, 0))

        # Get all input events and check if they are a mouse click
        event = pygame.event.get()
        for e in event:
            if e.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicks the run simulation button tell the program to run the simulation
                if not real_time_simulation and run_rectangle.collidepoint(e.pos):
                    real_time_simulation = True
                    break

                # If the simulation is running, draw a circle of a random color
                color_array = [secrets.randbelow(255) + 1, secrets.randbelow(255) + 1, secrets.randbelow(255) + 1]
                growing = True
                start_time = time.time()
                begin = start_time
                start_pos = pygame.mouse.get_pos()

            # if the user releases the mouse button, create a Particle object and pass it the radius, start position,
            # initial velocities, and color
            elif e.type == pygame.MOUSEBUTTONUP:

                growing = False
                init_velocity_x = (end_pos[0] - start_pos[0]) / 50
                init_velocity_y = (end_pos[1] - start_pos[1]) / 50
                p = Particle(radius, [start_pos[0], start_pos[1], 0], [init_velocity_x, init_velocity_y, 0],
                             color_array, False)
                particles.append(p)

        # Pause simulation
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            real_time_simulation = False
            run_count = 0
            screen.fill((0, 0, 0))
            for p in particles:
                pygame.draw.circle(surface,
                                   p.get_color(),
                                   [p.get_x(), p.get_y()],
                                   int(p.get_radius()),
                                   0)

        # Reset simulation
        if pygame.key.get_pressed()[pygame.K_r]:
            particles.clear()

        # If there is already a particle growing, increase the radius by 0.5 pixels per cycle
        if growing:
            if time.time() - start_time < 5:
                radius += 0.5

            # draw a black line over the previous line to hide it
            if not real_time_simulation and time.time() - start_time > 0.01:
                pygame.draw.line(surface,
                                 (0, 0, 0),
                                 start_pos,
                                 end_pos,
                                 1)

            # Draw the line to represent the initial velocity vector
            end_pos = pygame.mouse.get_pos()
            pygame.draw.line(surface,
                             color_array,
                             start_pos,
                             end_pos,
                             1)

            # Draw the particle
            pygame.draw.circle(surface,
                               color_array,
                               start_pos,
                               int(radius),
                               0)

        # Make sure that the object has a radius that isn't 0 to account for any division by 0
        else:
            radius = 0.5

        for e in pygame.event.get():
            if e == pygame.QUIT:
                running = False
                pygame.quit()

        # print(growing)
        sum_mass = 0
        #        if first_run:
        #            p1 = Particle(10, [800, 400, 0], [-1.0, 0, 0])
        #            p2 = Particle(10, [700, 475, 0], [1.0, 0, 0])

        #            particles.append(p1)
        #            particles.append(p2)
        #           first_run = False

        # Check if the simulation is running
        if real_time_simulation:
            for p in particles:
                sum_mass += p.get_mass()
                collision = p.get_acceleration(particles)
                if collision is not None:
                    # explosion.play()
                    particles.remove(p)
                    particles.remove(collision)

                    # conservation of momentum
                    velocity_x = (p.get_velocity_x() * p.get_mass() + collision.get_velocity_x() * collision.get_mass()) \
                                 / (math.pi * pow(p.get_radius() + collision.get_radius(), 2) * p.get_density())
                    velocity_y = (
                                             p.get_velocity_y() * p.get_mass() + collision.get_velocity_y() * collision.get_mass()) / \
                                 (math.pi * pow(p.get_radius() + collision.get_radius(), 2) * p.get_density())
                    larger = p if p.get_radius() > collision.get_radius() else collision

                    # Create a new particle with the two original particles combined
                    temp = Particle(p.get_radius() + collision.get_radius(),
                                    [larger.get_x(), larger.get_y(), 0],
                                    [velocity_x, velocity_y, 0],
                                    p.get_color(),
                                    p.get_is_black_hole())

                    # if temp.get_mass() > critical_mass and not temp.get_is_black_hole():
                    #    temp.set_black_hole(True)
                    particles.append(temp)
                    break
                else:
                    p.set_x(int(p.get_x() + (p.calc_velocity_x(delay_time))))
                    p.set_y(int(p.get_y() + (p.calc_velocity_y(delay_time))))

                    pygame.draw.circle(surface,
                                       p.get_color(),
                                       [p.get_x(), p.get_y()],
                                       int(p.get_radius()),
                                       0)

                    if p.get_x() <= 0 or p.get_x() >= width or p.get_y() <= 0 or p.get_y() >= height:
                        particles.remove(p)

        else:
            for p in particles:
                pygame.draw.circle(surface,
                                   p.get_color(),
                                   [p.get_x(), p.get_y()],
                                   int(p.get_radius()),
                                   0)

        pygame.display.flip()
        time.sleep(delay_time)


simulator()
