import numpy as np
from matplotlib.colors import is_color_like, to_rgb
from MY_yyyyy_SETTINGS_general import my_color_palette
from yyyyy_utils import find_LCM, get_sign, is_the_same_point

##################################################################
## color HELPERS                                               ## 
##################################################################

def find_color_code(color_name):
  if color_name is None or color_name == 'none':
    return 'none'
  if isinstance(color_name, str) and color_name in my_color_palette:
    return to_rgb(my_color_palette[color_name])

  if not is_color_like(color_name):
    raise Exception(color_name, "is not a valid color!")
  return to_rgb(color_name)

##################################################################
def colors_are_equal(color_1, color_2):
  color_code_1 = np.array(find_color_code(color_1) if isinstance(color_1, str) else color_1)
  color_code_2 = np.array(find_color_code(color_2) if isinstance(color_2, str) else color_2)
  if color_code_1.size == 3:
    color_code_1 = np.append(color_code_1, 1.)
  if color_code_2.size == 3:
    color_code_2 = np.append(color_code_2, 1.)
  return is_the_same_point(color_code_1, color_code_2)

##################################################################
##################################################################
def create_gradient_colors(rgb_start, rgb_end, nb_steps=None): 

  rgb_start_, rgb_end_ = find_color_code(rgb_start), find_color_code(rgb_end)

  if nb_steps is None:
    nb_steps_per_channel = [int(abs(rgb_start_elem - rgb_end_elem)+1) for rgb_start_elem, rgb_end_elem in zip(rgb_start_, rgb_end_)]

    nb_steps = 1
    for nspc in nb_steps_per_channel:
      nb_steps = find_LCM(n=nspc, m=nb_steps)

    result = np.array([rgb_start_ for _ in range(nb_steps)], dtype=np.float64)
    for i, (nspc, rgb_s, rgb_e) in enumerate(zip(nb_steps_per_channel, rgb_start_, rgb_end_)):
      size_of_the_step = int(nb_steps / nspc)
      for j in range(nspc):
        result[j*size_of_the_step : (j+1)*size_of_the_step, i] += get_sign(rgb_e-rgb_s) * j

    result /= 255.
  else:
    rgb_start_np, rgb_end_np = np.array(rgb_start_, dtype=np.float64), np.array(rgb_end_, dtype=np.float64)
    result = [(i*rgb_start_np + (nb_steps-1-i)*rgb_end_np)/(nb_steps-1) for i in range(nb_steps)]
    if np.max([rgb_start_np, rgb_end_np]) > 1:
      result /= 255.

  return result
