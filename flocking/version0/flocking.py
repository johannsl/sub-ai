# Python 2

from game import load, physicalobject, resources
import pyglet

window = pyglet.window.Window(800, 600)
level_label = pyglet.text.Label(text="Flocking, M, M, M", 
                                x=400, y=575, anchor_x='center')
batch = pyglet.graphics.Batch()
boids = load.boids(200, batch)
obstacles = load.obstacles(5, batch)
predators = load.predators(1, batch)

print('''
8888888888 888                   888      d8b                   
888        888                   888      Y8P                   
888        888                   888                            
8888888    888  .d88b.   .d8888b 888  888 888 88888b.   .d88b.  
888        888 d88""88b d88P"    888 .88P 888 888 "88b d88P"88b 
888        888 888  888 888      888888K  888 888  888 888  888 
888        888 Y88..88P Y88b.    888 "88b 888 888  888 Y88b.888 
888        888  "Y88P"   "Y8888P 888  888 888 888  888  "Y88888 
                                                            888 
                                                       Y8b d88P 
                                                        "Y88P"''')
print("Controls: \n"
        "   Q-U: Modes \n"
        "   I-A: Objects \n")

@window.event
def on_draw():
    window.clear()
    batch.draw()
    level_label.draw()

def update(dt):
    for boid in boids:
        boid.update(boids, obstacles, predators, dt)
    for predator in predators:
        predator.update(boids, obstacles, predators, dt)

@window.event
def on_key_press(symbol, modifiers):
    global level_label
    global obstacles
    global predators
    if symbol == pyglet.window.key.Q:
        level_label = pyglet.text.Label(text="Flocking, L, L, H", 
                                        x=400, y=575, anchor_x="center")
        physicalobject.Boid.separationWeight = 0.1
        physicalobject.Boid.alignmentWeight = 0.001
        physicalobject.Boid.cohesionWeight = 0.1

    elif symbol == pyglet.window.key.W:
        level_label = pyglet.text.Label(text="Flocking, L, H, L", 
                                        x=400, y=575, anchor_x="center")
        physicalobject.Boid.separationWeight = 0.1
        physicalobject.Boid.alignmentWeight = 0.1
        physicalobject.Boid.cohesionWeight = 0.001
    elif symbol == pyglet.window.key.E:
        level_label = pyglet.text.Label(text="Flocking, H, L, L", 
                                        x=400, y=575, anchor_x="center")
        physicalobject.Boid.separationWeight = 10
        physicalobject.Boid.alignmentWeight = 0.001
        physicalobject.Boid.cohesionWeight = 0.001
    elif symbol == pyglet.window.key.R:
        level_label = pyglet.text.Label(text="Flocking, L, H, H", 
                                        x=400, y=575, anchor_x="center")
        physicalobject.Boid.separationWeight = 0.1
        physicalobject.Boid.alignmentWeight = 0.1
        physicalobject.Boid.cohesionWeight = 0.1
    elif symbol == pyglet.window.key.T:
        level_label = pyglet.text.Label(text="Flocking, H, L, H", 
                                        x=400, y=575, anchor_x="center")
        physicalobject.Boid.separationWeight = 10
        physicalobject.Boid.alignmentWeight = 0.001
        physicalobject.Boid.cohesionWeight = 0.1
    elif symbol == pyglet.window.key.Y:
        level_label = pyglet.text.Label(text="Flocking, H, H, H", 
                                        x=400, y=575, anchor_x="center")
        physicalobject.Boid.separationWeight = 10
        physicalobject.Boid.alignmentWeight = 0.1
        physicalobject.Boid.cohesionWeight = 0.1
    elif symbol == pyglet.window.key.U:
        level_label = pyglet.text.Label(text="Flocking, M, M, M", 
                                        x=400, y=575, anchor_x="center")
        physicalobject.Boid.separationWeight = 1
        physicalobject.Boid.alignmentWeight = 0.01
        physicalobject.Boid.cohesionWeight = 0.01
    elif symbol == pyglet.window.key.I:
        obstacles.extend(load.obstacles(1, batch))
    elif symbol == pyglet.window.key.O:
        predators.extend(load.predators(1, batch))
    elif symbol == pyglet.window.key.P:
        obstacles = []
    elif symbol == pyglet.window.key.A:
        predators = []

if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1/120.0)
    pyglet.app.run()
