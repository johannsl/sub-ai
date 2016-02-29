import math
import physicalobject
import pyglet
import random
import resources

def boids(num_boids, batch):
    boids = []
    for boid in range(num_boids):
        boid_x = random.randint(0, 800)
        boid_y = random.randint(0, 600)
        new_boid = physicalobject.Boid(img=resources.boid_image, 
                                        x=boid_x, y=boid_y, batch=batch)
        new_boid.velocity = (random.uniform(-1, 1)*50, random.uniform(-1, 1)*50)
        new_boid.rotation = -(math.atan2(new_boid.velocity[1], 
                            new_boid.velocity[0]) * 180 / math.pi)
        boids.append(new_boid)
    return boids

def obstacles(num_obstacles, batch):
    obstacles = []
    for obstacle in range(num_obstacles):
        obstacle_x = random.randint(0, 800)
        obstacle_y = random.randint(0, 600)
        new_obstacle = physicalobject.PhysicalObject(
            img=resources.obstacle_image, x=obstacle_x, y=obstacle_y, 
            batch=batch)
        obstacles.append(new_obstacle)
    return obstacles

def predators(num_predators, batch):
    predators = []
    for predator in range(num_predators):
        predator_x = random.randint(0, 800)
        predator_y = random.randint(0, 600)
        new_predator = physicalobject.Predator(img=resources.predator_image, 
                                        x=predator_x, y=predator_y, batch=batch)
        new_predator.velocity = (random.uniform(-1, 1)*50, random.uniform(-1, 1)*50)
        new_predator.rotation = -(math.atan2(new_predator.velocity[1], 
                            new_predator.velocity[0]) * 180 / math.pi)
        predators.append(new_predator)
    return predators
