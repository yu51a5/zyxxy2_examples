from timeit import default_timer as timer
from zyxxy2 import nice_cat, wait_for_enter, shift_layers, stretch_layers, draw_a_circle, random_integer_number, is_the_same_point, find_color_code

canvas_width = 60
canvas_height = 39
light_radius = 10

head, ears = nice_cat(axes_params=dict(canvas_width=60, canvas_height=39, tick_step=3,), block=False)
stretch_layers(diamond=head.diamond_coords, stretch=light_radius/4, layer_nbs=[1])
light = draw_a_circle(center=(30, 30), radius=light_radius, color='yellow', opacity=0.5, layer_nb=2, diamond_color='black')
while True:
  new_light_center = (float(random_integer_number(min=light_radius, max=canvas_width-light_radius)),
                      float(random_integer_number(min=light_radius, max=canvas_height-light_radius)))
  light.shift_to(new_light_center)
  while True:
    start = timer()
    cat_shift_str = wait_for_enter(f"Light is in {light.diamond_coords}. Cat is in {head.diamond_coords}. Enter cat shift! ")
    duration = timer() - start
    cat_shift = eval("(" + cat_shift_str + ")")

    shift_layers(shift=cat_shift, layer_nbs=[1])
    if (is_the_same_point(head.diamond_coords, light.diamond_coords)):
      new_color = wait_for_enter(f"Well done! Evaluation time: {int(duration)} seconds. Optionally, enter new cat color. Then press ENTER to continue. ")
      try:
        c = find_color_code(new_color)
      except:
        print(f"`{new_color}` is an invalid color. Continuing with the same color...")
        break    
      if new_color:
        print(f"New cat color is `{new_color}`, its RGB values are {c}.")
        for bp in [head, ears[0], ears[1]]:
          bp.color = new_color
      break