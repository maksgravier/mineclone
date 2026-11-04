import numpy as np
from ursina import *
import ursina as game_time
from my_library import *
app = Ursina()
size_of_1_block = (1, 1, 1)
all_the_block_not_in_inventory_list = []
n = 0
n2 = 0
n3 = 0
gravity = 35
velocity = 0
jump_hight = 12
speed = 5
jumping = False
camera.z = 10
camera.y =  5
sky = Sky(color=color.azure)
mouse_sensitivity = 150.0
size_of_world = [50, 3, 50]
start_x = 0
start_z = 0
flat_backwards_ray = False
flat_forward_ray = False
start_y = 0
in_menu = False
pointer = Text(text='+', origin=(0, 0), scale=2, color=color.white)
mouse.locked = True
for y in range(size_of_world[1]):
    for x in range(size_of_world[0]):
        for z in range(size_of_world[2]):
            block = Entity(
                model="cube",
                color=color.green,
                texture="white_cube",
                scale=size_of_1_block,
                position=(start_x + x, start_y + y, start_z + z),
                collider="box"
            )
            all_the_block_not_in_inventory_list.append(block)
            n += 1
        n3 += 1




def update():
    global velocity, jumping, jump_hight, in_menu, flat_forward_ray, pointer_ray, flat_backwards_ray
    if not in_menu:
        dt = game_time.time.dt
        flat_forward = Vec3(camera.forward.x, 0, camera.forward.z).normalized()
        collision_ray_1 = raycast(Vec3(camera.position[0], camera.position[1] - 1, camera.position[2]), flat_forward, distance=1, ignore=(camera,))
        collision_ray_2 = raycast(Vec3(camera.position[0], camera.position[1] - 1, camera.position[2]), Vec3(flat_forward[0] * -1, flat_forward[1], flat_forward[2] * -1), distance=1, ignore=(camera,))
        if collision_ray_1.hit:
            flat_forward_ray = True
            print("l")
        else:
            flat_forward_ray = False
        if collision_ray_2.hit:
            flat_backwards_ray = True
            print("b")
        else:
            flat_backwards_ray = False
        if held_keys['a'] or held_keys['left arrow']:
            camera.rotation_y -= speed * dt
        if held_keys['d'] or held_keys['right arrow']:
            camera.rotation_y += speed * dt
        if (held_keys['w'] or held_keys['up arrow']) and not flat_forward_ray:
            if held_keys['shift']:
                camera.position += flat_forward * (speed * 3) * dt
            else:
                camera.position += flat_forward * speed * dt
        if (held_keys['s'] or held_keys['down arrow']) and not flat_backwards_ray:
            if held_keys['shift']:
                camera.position -= flat_forward * (speed * 3) * dt
            else:
                camera.position -= flat_forward * speed * dt
        camera.rotation_x -= mouse.velocity[1] * mouse_sensitivity
        camera.rotation_y += mouse.velocity[0] * mouse_sensitivity
        camera.rotation_x = clamp(camera.rotation_x, -80, 80)
        hit_info = raycast(camera.world_position, Vec3(0, -1, 0), distance=1.5, ignore=(camera,))
        pointer_ray = raycast(camera.position, camera.forward, distance=12, ignore=(camera,))



        if hit_info.hit and hit_info.world_normal.y > 0:
            jumping = False
            velocity = 0
            if held_keys['space']:
                velocity = jump_hight
                jumping = True
            else:
                camera.y = hit_info.world_point.y + 1.2
        else:
            velocity -= gravity * dt
        camera.y += velocity * dt
def input(key):
    global in_menu
    if key == 'escape':
        if not in_menu:
            in_menu = True
            mouse.locked = False
        else:
            in_menu = False
            mouse.locked = True
    if key == 'right mouse down' and pointer_ray.hit:
        Entity(model="cube",
               scale=size_of_1_block,
               color=color.green,
               position=pointer_ray.entity.position + pointer_ray.world_normal,
               texture="white_cube",
               collider="box"
               )
    if key == "left mouse down":
        if pointer_ray.hit:
            destroy(pointer_ray.entity)
        else:
            pass
app.run()
