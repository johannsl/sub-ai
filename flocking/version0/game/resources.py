import pyglet

pyglet.resource.path = ["../resources"]
pyglet.resource.reindex()

boid_image = pyglet.resource.image("boid.png")
obstacle_image = pyglet.resource.image("obstacle.png")
predator_image = pyglet.resource.image("predator.png")

def center_image(image):
    image.anchor_x = image.width/2
    image.anchor_y = image.height/2

def resize_image(image, w, h):
    image.width = image.width * w
    image.height = image.height * h

resize_image(boid_image, 0.5, 0.5) #8
resize_image(obstacle_image, 0.5, 0.5) #32
resize_image(predator_image, 2, 2) #32
center_image(boid_image)
center_image(obstacle_image)
center_image(predator_image)

