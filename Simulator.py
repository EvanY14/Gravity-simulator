import math
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
pygame.font.init()
pygame.mixer.init()
pygame.init()
font = pygame.font.SysFont('comicsansms', 32)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


def redraw_button(shape, text, color):
    shape_rectangle = pygame.Rect((shape.x, shape.y), (shape.width, shape.height))
    shape_text = font.render(text, True, (0, 0, 0))
    shape_rect = shape_text.get_rect()
    shape_rect.center = (shape_rectangle.center[0], shape_rectangle.y + (shape_rectangle.height / 2))

    pygame.draw.rect(screen, color, shape_rectangle)
    screen.blit(shape_text, (shape_rect[0], shape_rect[1]))
    pygame.display.flip()


def simulator():
    # explosion = pygame.mixer.music.load(sound_file)
    radius = 0.0
    RED = pygame.Color("#FF0000")
    running = True
    growing = False
    start_time = 0

    particleImg = pygame.image.load(
        'C:\\Users\\yueva\\AppData\\Local\\Programs\\Python\\Python37-32\\gravity_simulator\\particle.gif').convert_alpha()
    screen.fill((0, 0, 0))
    pygame.display.flip()
    pygame.display.init()
    surface = pygame.display.get_surface()
    first_run = True
    run_count = 0
    real_time_simulation = True
    ultra_graphics = True
    start_with_sun = True

    # Title Screen
    # Title text
    title_text = font.render("Gravity Simulator", True, (0, 255, 0))
    screen.blit(title_text, (
    (screen.get_width() / 2) - (title_text.get_width() / 2), (screen.get_height() / 2) - (title_text.get_height() / 2)))

    # Define buttons
    play_button = pygame.Rect((screen.get_width() / 2 - 350, screen.get_height() / 2 + 50), (300, 100))
    settings_button = pygame.Rect((screen.get_width() / 2 + 50, screen.get_height() / 2 + 50), (300, 100))

    # Define button text
    play_text = font.render("Play", True, (0, 0, 0))
    play_text_rect = play_text.get_rect()
    play_text_rect.center = (screen.get_width() / 2 - 350, (screen.get_height() / 2 + 100))

    settings_text = font.render("Settings", True, (0, 0, 0))
    settings_text_rect = settings_text.get_rect()
    settings_text_rect.center = (screen.get_width() / 2 + 150, (screen.get_height() / 2 + 100))

    # Draw buttons
    pygame.draw.rect(screen, (0, 255, 0), play_button)
    pygame.draw.rect(screen, (0, 255, 0), settings_button)
    screen.blit(play_text, (play_button[0] + 150 - (play_text.get_width() / 2), play_button[1] + 25))
    screen.blit(settings_text, (settings_button[0] + 150 - (settings_text.get_width() / 2), settings_button[1] + 25))
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
                    screen.fill((0, 0, 0))
                    # Define the Real time simulation prompt
                    real_time_text = font.render("Real time simulation", True, (255, 255, 255))
                    real_time_rect = real_time_text.get_rect()
                    real_time_rect.center = (screen.get_width() / 2, 150)
                    screen.blit(real_time_text,
                                ((screen.get_width() / 2) - (real_time_rect.width / 2),
                                 real_time_rect.y - real_time_rect.height))

                    # Define the yes button
                    yes_rectangle = pygame.Rect(
                        (screen.get_width() / 2 - 350, real_time_rect.y + real_time_rect.height + 50), (300, 100))

                    yes_text = font.render("Yes", True, (0, 0, 0))
                    yes_rect = yes_text.get_rect()
                    yes_rect.center = (screen.get_width() / 2 - 200, yes_rectangle.y + (yes_rectangle.height / 2))

                    pygame.draw.rect(screen, (255, 255, 255), yes_rectangle)
                    screen.blit(yes_text, (yes_rect[0], yes_rect[1]))

                    # Define the no button
                    no_rectangle = pygame.Rect(
                        (screen.get_width() / 2 + 50, real_time_rect.y + real_time_rect.height + 50), (300, 100))

                    no_text = font.render("No", True, (0, 0, 0))
                    no_rect = no_text.get_rect()
                    no_rect.center = (screen.get_width() / 2 + 200, no_rectangle.y + (no_rectangle.height / 2))

                    pygame.draw.rect(screen, (0, 255, 0), no_rectangle)
                    screen.blit(no_text, (no_rect[0], no_rect[1]))

                    # Define the play button on the settings screen
                    play_rectangle = pygame.Rect((screen.get_width() - 250, 100), (300, 100))
                    play_text = font.render("Play", True, (0, 0, 0))
                    play_rect = play_text.get_rect()
                    play_rect.center = (screen.get_width() - 250, 100)
                    pygame.draw.rect(screen, (0, 255, 0), play_rectangle)
                    screen.blit(play_text, (play_rect[0] + 125, play_rect[1] + 50))

                    # Define quality header
                    quality_text = font.render("Quality", True, (255, 255, 255))
                    quality_rect = quality_text.get_rect()
                    quality_rect.center = (screen.get_width() / 2, 450)

                    screen.blit(quality_text, (quality_rect[0], quality_rect[1]))

                    # Define graphics quality buttons
                    # Normal graphics
                    normal_rectangle = pygame.Rect(
                        (screen.get_width() / 2 - 350, quality_rect.y + quality_rect.height + 50), (300, 100))
                    normal_text = font.render("Normal", True, (0, 0, 0))

                    normal_rect = normal_text.get_rect()
                    normal_rect.center = (
                    screen.get_width() / 2 - 200, normal_rectangle.y + (normal_rectangle.height / 2))

                    pygame.draw.rect(screen, (0, 255, 0), normal_rectangle)
                    screen.blit(normal_text, (normal_rect[0], normal_rect[1]))

                    # Ultra graphics
                    ultra_rectangle = pygame.Rect(
                        (screen.get_width() / 2 + 50, quality_rect.y + quality_rect.height + 50),
                        (300, 100))
                    ultra_text = font.render("Ultra", True, (0, 0, 0))
                    ultra_rect = ultra_text.get_rect()
                    ultra_rect.center = (screen.get_width() / 2 + 200, ultra_rectangle.y + (ultra_rectangle.height / 2))

                    pygame.draw.rect(screen, (255, 255, 255), ultra_rectangle)
                    screen.blit(ultra_text, (ultra_rect[0], ultra_rect[1]))

                    # Start with sun title
                    start_with_sun_text = font.render("Starting configuration", True, (255, 255, 255))
                    start_with_sun_rect = start_with_sun_text.get_rect()
                    start_with_sun_rect.center = (screen.get_width() / 2, 750)

                    # Define start with sun button
                    sun_rectangle = pygame.Rect(
                        (screen.get_width() / 2 - 350, start_with_sun_rect.y + start_with_sun_rect.height + 50),
                        (300, 100))

                    sun_text = font.render("Start with sun", True, (0, 0, 0))
                    sun_rect = sun_text.get_rect()
                    sun_rect.center = (screen.get_width() / 2 - 200, sun_rectangle.y + (sun_rectangle.height / 2))

                    pygame.draw.rect(screen, (255, 255, 255), sun_rectangle)
                    screen.blit(sun_text, (sun_rect[0], sun_rect[1]))

                    # Define default button
                    default_rectangle = pygame.Rect(
                        (screen.get_width() / 2 + 50, start_with_sun_rect.y + start_with_sun_rect.height + 50),
                        (300, 100))

                    default_text = font.render("Default", True, (0, 0, 0))
                    default_rect = default_text.get_rect()
                    default_rect.center = (
                    screen.get_width() / 2 + 200, default_rectangle.y + (default_rectangle.height / 2))

                    pygame.draw.rect(screen, (0, 255, 0), default_rectangle)
                    screen.blit(default_text, (default_rect[0], default_rect[1]))

                    pygame.display.flip()
                    events_2 = pygame.event.get()
                    real_time_simulation = True
                    # while pygame.MOUSEBUTTONDOWN not in events:
                    #    sleep(0.1)
                    #    events = pygame.event.get()

                    # Wait for one of the buttons to be pressed and determine which one
                    break_out_2 = False
                    while not break_out_2:
                        for event in events_2:
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                print("mouse button down")
                                # If the yes button is pressed, set real_time_simulation to true and make it white
                                if yes_rectangle.collidepoint(event.pos):
                                    real_time_simulation = True
                                    # break_out_2 = True
                                    redraw_button(no_rectangle, "No", (0, 255, 0))
                                    redraw_button(yes_rectangle, "Yes", (255, 255, 255))

                                # If the no button is pressed, set real_time_simulation to false and make it white
                                elif no_rectangle.collidepoint(event.pos):
                                    real_time_simulation = False
                                    # break_out_2 = True
                                    redraw_button(no_rectangle, "No", (255, 255, 255))
                                    redraw_button(yes_rectangle, "Yes", (0, 255, 0))

                                # If the play button is pressed, break out and start the simulation
                                elif play_rectangle.collidepoint(event.pos):
                                    break_out = True
                                    break_out_2 = True

                                # If the normal button is pressed, set graphics to normal (no trail)
                                elif normal_rectangle.collidepoint(event.pos):
                                    # break_out_2 = True
                                    ultra_graphics = False
                                    redraw_button(ultra_rectangle, "Ultra", (0, 255, 0))
                                    redraw_button(normal_rectangle, "Normal", (255, 255, 255))
                                elif ultra_rectangle.collidepoint(event.pos):
                                    # break_out_2 = True
                                    ultra_graphics = True
                                    print('Ultra graphics')
                                    redraw_button(ultra_rectangle, "Ultra", (255, 255, 255))
                                    redraw_button(normal_rectangle, "Normal", (0, 255, 0))
                                elif sun_rectangle.collidepoint(event.pos):
                                    start_with_sun = True
                                    redraw_button(sun_rectangle, "Start with sun", (255, 255, 255))
                                    redraw_button(default_rectangle, "Default", (0, 255, 0))
                                elif default_rectangle.collidepoint(event.pos):
                                    start_with_sun = False
                                    redraw_button(sun_rectangle, "Start with sun", (0, 255, 0))
                                    redraw_button(default_rectangle, "Default", (255, 255, 255))
                                break
                        events_2 = pygame.event.get()

                    print(real_time_simulation)
                    #######
                break
        events = pygame.event.get()
    sleep(0.5)
    pygame.event.get()
    screen.fill((0, 0, 0))
    pygame.display.flip()

    # Main loop of the program
    while running:
        # Update the screen
        if real_time_simulation:
            screen.fill((0, 0, 0))

        grid_box_size = 30
        # Draw grid
        if ultra_graphics:
            for r in range(int(screen.get_width() / grid_box_size)):
                for c in range(int(screen.get_height() / grid_box_size)):
                    pygame.draw.rect(screen, (60, 60, 60), pygame.Rect((r * grid_box_size, c * grid_box_size),
                                                                       (grid_box_size, grid_box_size)), 1)

        if run_count == 0 and start_with_sun:
            particle = Particle(150,
                                [screen.get_width() / 2, screen.get_height() / 2, 0],
                                [0, 0, 0],
                                (255, 255, 0),
                                False,
                                [])
            particle.set_density(50)
            particle.set_movable(False)
            particles.append(particle)

        # If the user pressed no or the simulation is paused, set up the run simulation button in the corner
        if not real_time_simulation:
            run_rectangle = pygame.Rect((screen.get_width() - 250, 100), (300, 100))
            # event = pygame.event.get()

            run_text = font.render("Run simulation", True, (0, 0, 0))
            run_rect = run_text.get_rect()
            run_rect.center = (screen.get_width() - 250, 100)
            pygame.draw.rect(screen, (0, 255, 0), run_rectangle)
            screen.blit(run_text, (run_rect[0] + 125, run_rect[1] + 50))

        run_count += 1
        # init_velocity_x = init_velocity_y = 0

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
                p = Particle(radius,
                             [start_pos[0], start_pos[1], 0],
                             [init_velocity_x, init_velocity_y, 0],
                             color_array,
                             False,
                             [])

                particles.append(p)

        # Pause simulation
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            real_time_simulation = False
            # run_count = 0
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
            run_count = 0

        # If q is pressed, quit simulation
        if pygame.key.get_pressed()[pygame.K_q]:
            pygame.quit()
            print('Done')
            break

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
                    velocity_y = (p.get_velocity_y() * p.get_mass() + collision.get_velocity_y() * collision.get_mass()) \
                                 / (math.pi * pow(p.get_radius() + collision.get_radius(), 2) * p.get_density())
                    larger = p if p.get_radius() > collision.get_radius() else collision

                    # Create a new particle with the two original particles combined
                    temp = Particle(p.get_radius() + collision.get_radius(),
                                    [larger.get_x(), larger.get_y(), 0],
                                    [velocity_x, velocity_y, 0],
                                    larger.get_color(),
                                    p.get_is_black_hole(),
                                    larger.get_trail())
                    if p.is_movable() is False or collision.is_movable() is False:
                        temp.set_movable(False)
                    # if temp.get_mass() > critical_mass and not temp.get_is_black_hole():
                    #    temp.set_black_hole(True)
                    particles.append(temp)
                    break
                else:
                    if p.is_movable():
                        p.set_x(int(p.get_x() + (p.calc_velocity_x(delay_time))))
                        p.set_y(int(p.get_y() + (p.calc_velocity_y(delay_time))))
                    if p.get_radius() < 100:
                        p.add_to_trail((p.get_x(), p.get_y()))

                    pygame.draw.circle(surface,
                                       p.get_color(),
                                       [p.get_x(), p.get_y()],
                                       int(p.get_radius()),
                                       0)

                    if p.get_x() <= 0 or p.get_x() >= screen.get_width() or p.get_y() <= 0 or p.get_y() >= screen.get_height():
                        particles.remove(p)

                    # Draw trail
                    if ultra_graphics:
                        for t in p.get_trail():
                            pygame.draw.rect(screen,
                                             p.get_color(),
                                             pygame.Rect((t[0], t[1]),
                                                         (p.get_radius() / 10, p.get_radius() / 10)))

        else:
            for p in particles:
                pygame.draw.circle(surface,
                                   p.get_color(),
                                   [p.get_x(), p.get_y()],
                                   int(p.get_radius()),
                                   0)

        pygame.display.update()
        # time.sleep(delay_time)


simulator()
