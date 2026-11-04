import ursina
from ursina import *
from ursina import camera
from ursina.prefabs.first_person_controller import FirstPersonController
x_size = 20
z_size = 20
y_size = 5
app = Ursina()
Sky(texture='sky_sunset')
mouse.locked = True
for y in range(y_size):
    for z in range(z_size):
        for x in range(x_size):
            cube = Entity(model="cube", scale=(1, 1, 1), position=(x, y, z), texture='grass', collider='box')
player = FirstPersonController(
    position=(5, 4, 5),
    speed=8,
    jump_height=2,
    mouse_sensitivity=Vec2(40, 40),)
def input(key):
    global ray
    if key == 'escape':
        if mouse.locked:
            mouse.locked = False
        else:
            mouse.locked = True
    if key == 'right mouse down':
        if mouse.hovered_entity:
            place_pos = mouse.world_point + mouse.normal * 0.5
            grid_pos = Vec3(round(place_pos.x), round(place_pos.y), round(place_pos.z))
            Entity(
                model="cube",
                scale=(1, 1, 1),
                position=grid_pos,
                texture='grass',
                collider='box',            )
    if key == 'left mouse down':
        if mouse.hovered_entity:
            destroy(mouse.hovered_entity)
app.run()
