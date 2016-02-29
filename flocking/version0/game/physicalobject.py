import math
import pyglet
import random

class PhysicalObject(pyglet.sprite.Sprite):
    
    def __init__(self, *args, **kwargs):
        super(PhysicalObject, self).__init__(*args, **kwargs)
        self.velocity_x = 0.0
        self.velocity_y = 0.0
 
    def update(self, dt):
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        self.check_bounds()

    def check_bounds(self):
        min_x = -self.image.width/2
        min_y = -self.image.height/2
        max_x = 800 + self.image.width/2
        max_y = 600 + self.image.height/2
        if self.x < min_x:
            self.x = max_x
        elif self.x > max_x:
            self.x = min_x
        if self.y < min_y:
            self.y = max_y
        elif self.y > max_y:
            self.y = min_y


class Boid(PhysicalObject):
    
    separationWeight = 1
    alignmentWeight = 0.01
    cohesionWeight = 0.005
    avoidanceWeight = 40
    escapeWeight = 40
     
    def __init__(self, *args, **kwargs):
        super(Boid, self).__init__(*args, **kwargs)
        self.velocity = (0, 0)

    def update(self, boids, obstacles, predators, dt):
        # Find neighbours
        neighbours = []
        for boid in boids:
            if distance(self.position, boid.position) < 60:
                neighbours.append(boid)
        
        # Forces
        sep_force = self.calculateSeparationForce(neighbours)
        sep = (self.separationWeight * sep_force[0], 
                self.separationWeight * sep_force[1])
        align_force = self.calculateAlignmentForce(neighbours)
        align = (self.alignmentWeight * align_force[0],
                self.alignmentWeight * align_force[1])
        coh_force = self.calculateCohesionForce(neighbours)
        coh = (self.cohesionWeight * coh_force[0],
                self.cohesionWeight * coh_force[1])
        avoid_force = self.calculateAvoidanceForce(obstacles)
        avoid = (self.avoidanceWeight * avoid_force[0],
                self.avoidanceWeight * avoid_force[1])
        escape_force = self.calculateEscapeForce(predators)
        escape = (self.escapeWeight * escape_force[0],
                self.escapeWeight * escape_force[1])
           
        # Velocity 
        self.velocity = (self.velocity[0] + sep[0] + align[0] + 
                        coh[0] + avoid[0] + escape[0], 
                        self.velocity[1] + sep[1] + align[1] + 
                        coh[1] + avoid[1] + escape[1])
        
        # Control max velocity
        hyp = math.sqrt(self.velocity[0]**2 + self.velocity[1]**2)
        if hyp > 50:
            self.velocity = (self.velocity[0] / hyp * 50, 
                            self.velocity[1] / hyp * 50)
        
        # Rotation, position, and 'grid wrap'
        self.rotation = -(math.atan2(self.velocity[1], self.velocity[0])
                        * 180 / math.pi)
        self.position = (self.x + self.velocity[0] * dt, 
                        self.y + self.velocity[1] * dt)
        self.check_bounds()

    def calculateSeparationForce(self, neighbours):
        sep_force = (0, 0)
        for neighbour in neighbours:
            if distance(self.position, neighbour.position) < 20:
                sep_force = (sep_force[0] + self.x - neighbour.x,
                            sep_force[1] + self.y - neighbour.y)
        return sep_force 
    
    def calculateAlignmentForce(self, neighbours):
        align_force = (0, 0)
        for neighbour in neighbours:
            align_force = (align_force[0] + neighbour.velocity[0],
                            align_force[1] + neighbour.velocity[1])
        return align_force
         
    def calculateCohesionForce(self, neighbours):
        coh_force = (0, 0)
        for neighbour in neighbours:
            coh_force = (coh_force[0] + neighbour.x - self.x,
	                   coh_force[1] + neighbour.y - self.y)
        return coh_force
	
    def calculateAvoidanceForce(self, obstacles):
        avoid_force = (0, 0)
        hyp = math.sqrt(self.velocity[0]**2 + self.velocity[1]**2)
        ahead = (self.x + self.velocity[0]/hyp * 50,
                self.y + self.velocity[1]/hyp * 50)
        ahead2 = (self.x + self.velocity[0]/hyp * 20,
				self.y + self.velocity[1]/hyp * 20)
        for obstacle in obstacles:
            if (distance(ahead, obstacle.position) < 30 or 
                distance(ahead2, obstacle.position) < 30):
                avoid_force = (ahead[0] - obstacle.x, ahead[1] - obstacle.y)
                hyp = math.sqrt(avoid_force[0]**2 + avoid_force[1]**2)
                avoid_force = (avoid_force[0]/hyp, avoid_force[1]/hyp)
                break
        return avoid_force 
        
    def calculateEscapeForce(self, predators):
        escape_force = (0, 0)
        for predator in predators:
            if distance(self.position, predator.position) < 60:
                escape_force = (escape_force[0] + self.x - predator.x,
                                escape_force[1] + self.y - predator.y)
        return escape_force

class Predator(Boid):

    separationWeight = 0.5
    cohesionWeight = 0.1
    avoidanceWeight = 10

    def __init__(self, *args, **kwargs):
        super(Boid, self).__init__(*args, **kwargs)
        self.velocity = (0, 0)

    def update(self, boids, obstacles, predators, dt):
        # Find neighbours
        neighbours = []
        for boid in boids:
            if distance(self.position, boid.position) < 80:
                neighbours.append(boid)
        
        # Forces
        sep_force = self.calculateSeparationForce(predators)
        sep = (self.separationWeight * sep_force[0], 
                self.separationWeight * sep_force[1])
        coh_force = self.calculateCohesionForce(neighbours)
        coh = (self.cohesionWeight * coh_force[0],
                self.cohesionWeight * coh_force[1])
        avoid_force = self.calculateAvoidanceForce(obstacles)
        avoid = (self.avoidanceWeight * avoid_force[0],
                self.avoidanceWeight * avoid_force[1])
           
        # Velocity 
        self.velocity = (self.velocity[0] + sep[0] + coh[0] + avoid[0], 
                        self.velocity[1] + sep[0] + coh[1] + avoid[1])
        
        # Control max velocity
        hyp = math.sqrt(self.velocity[0]**2 + self.velocity[1]**2)
        if hyp > 40:
            self.velocity = (self.velocity[0] / hyp * 40, 
                            self.velocity[1] / hyp * 40)
        
        # Rotation, position, and 'grid wrap'
        self.rotation = -(math.atan2(self.velocity[1], self.velocity[0])
                        * 180 / math.pi)
        self.position = (self.x + self.velocity[0] * dt, 
                        self.y + self.velocity[1] * dt)
        self.check_bounds()

    def calculateSeparationForce(self, predators):
        sep_force = (0, 0)
        for predator in predators:
            if distance(self.position, predator.position) < 60:
                sep_force = (sep_force[0] + self.x - predator.x,
                            sep_force[1] + self.y - predator.y)
        return sep_force 

    def calculateCohesionForce(self, neighbours):
        coh_force = (0, 0)
        for neighbour in neighbours:
            coh_force = (coh_force[0] + neighbour.x - self.x,
	                   coh_force[1] + neighbour.y - self.y)
        return coh_force
	
    def calculateAvoidanceForce(self, obstacles):
        avoid_force = (0, 0)
        hyp = math.sqrt(self.velocity[0]**2 + self.velocity[1]**2)
        ahead = (self.x + self.velocity[0]/hyp * 50,
                self.y + self.velocity[1]/hyp * 50)
        ahead2 = (self.x + self.velocity[0]/hyp * 20,
				self.y + self.velocity[1]/hyp * 20)
        for obstacle in obstacles:
            if (distance(ahead, obstacle.position) < 40 or 
                distance(ahead2, obstacle.position) < 40):
                avoid_force = (ahead[0] - obstacle.x, ahead[1] - obstacle.y)
                hyp = math.sqrt(avoid_force[0]**2 + avoid_force[1]**2)
                avoid_force = (avoid_force[0]/hyp, avoid_force[1]/hyp)
                break
        return avoid_force 

def distance(point_1=(0, 0), point_2=(0, 0)):
    return math.sqrt((point_1[0] - point_2[0]) ** 2 +
                    (point_1[1] - point_2[1]) **2)

