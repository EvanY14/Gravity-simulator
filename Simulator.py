import math
from threading import Thread
from time import *
import pygame
from particle import Particle
from graphics import *
import secrets
width, height = 1600, 900
particles = []
delay_time = 0.01
critical_mass = 10000

def test():
    radius = 0.0
    RED = pygame.Color("#FF0000")
    running = True
    growing = False
    start_time = 0
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    particleImg = pygame.image.load(
        'C:\\Users\\yueva\\AppData\\Local\\Programs\\Python\\Python37-32\\gravity_simulator\\particle.gif').convert_alpha()
    screen.fill((255, 255, 255))
    pygame.display.flip()
    pygame.display.init()
    surface = pygame.display.get_surface()
    first_run = True
    run_count = 0

    while running:
        run_count += 1
        init_velocity_x = init_velocity_y = 0
        if run_count % 5 == 0:
            screen.fill((255, 255, 255))
        event = pygame.event.get()
        for e in event:
            if e.type == pygame.MOUSEBUTTONDOWN:
                color_array = [secrets.randbelow(255) + 1, secrets.randbelow(255) + 1, secrets.randbelow(255) + 1]
                growing = True
                start_time = time.time()
                begin = start_time
                start_pos = pygame.mouse.get_pos()
            if e.type == pygame.MOUSEBUTTONUP:

                growing = False
                init_velocity_x = (end_pos[0] - start_pos[0]) / 50
                init_velocity_y = (end_pos[1] - start_pos[1]) / 50
                p = Particle(radius, [start_pos[0], start_pos[1], 0], [init_velocity_x, init_velocity_y, 0], color_array, False)
                particles.append(p)

        if growing:
            if time.time() - start_time < 5:
                radius += 0.5
            end_pos = pygame.mouse.get_pos()
            pygame.draw.line(surface, color_array, start_pos, end_pos, 1)
            # screen.fill((255, 255, 255))
            # begin = time.clock_gettime(time.CLOCK_REALTIME)
            pygame.draw.circle(surface, color_array, start_pos, int(radius), 0)
            # scaled_img = pygame.transform.scale(particleImg, (int(radius), int(radius)))
            # screen.blit(scaled_img, (pygame.mouse.get_pos()[0]-(radius/2), pygame.mouse.get_pos()[1]-(radius/2)))
            # print(pygame.mouse.get_pos())
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

        for p in particles:
            sum_mass += p.get_mass()
            collision = p.get_acceleration(particles)
            if collision is not None:
                particles.remove(p)
                particles.remove(collision)

                # conservation of momentum
                velocity_x = (p.get_velocity_x() * p.get_mass() + collision.get_velocity_x() * collision.get_mass()) / (
                            math.pi * pow(p.get_radius() + collision.get_radius(), 2) * 69)
                velocity_y = (p.get_velocity_y() * p.get_mass() + collision.get_velocity_y() * collision.get_mass()) / (
                            math.pi * pow(p.get_radius() + collision.get_radius(), 2) * 69)
                larger = p if p.get_radius() > collision.get_radius() else collision

                # Create a new particle with the two original particles combined
                temp = Particle(p.get_radius() + collision.get_radius(), [larger.get_x(), larger.get_y(), 0],
                                [velocity_x, velocity_y, 0], p.get_color(), p.get_is_black_hole())

                # if temp.get_mass() > critical_mass and not temp.get_is_black_hole():
                #    temp.set_black_hole(True)
                particles.append(temp)
                break
            else:
                p.set_x(int(p.get_x() + (p.calc_velocity_x(delay_time))))
                p.set_y(int(p.get_y() + (p.calc_velocity_y(delay_time))))

                pygame.draw.circle(surface, p.get_color(), [p.get_x(), p.get_y()],
                                   int(p.get_radius()), 0)
                if p.get_x() <= 0 or p.get_x() >= width or p.get_y() <= 0 or p.get_y() >= height:
                    particles.remove(p)
                # scaled_img = pygame.transform.scale(particleImg, (int(p.get_radius()), int(p.get_radius())))
                # screen.blit(scaled_img, [p.get_x()-(radius/2.0), p.get_y()-(radius/2.0)])
                # particles.remove(p)

                # particles.append(Particle(p.get_radius(),
                #                         [p.get_x(), p.get_y(), 0],
                #                         [p.get_velocity_x(),
                #                          p.get_velocity_y(), 0]))

        pygame.display.flip()
        time.sleep(delay_time)


test()

