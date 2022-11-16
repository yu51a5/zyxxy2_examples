########################################################################
## Draw With yyyyy (or yyyyy Drawings, or Drawing With yyyyy)
## (C) 2021 by Yulia Voevodskaya (draw.with.zyxxy@outlook.com)
##
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.
##  See <https://www.gnu.org/licenses/> for the specifics.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
########################################################################

from yyyyy_canvas import create_canvas_and_axes, show_and_save
from yyyyy_shape_functions import draw_a_rectangle, draw_a_broken_line, draw_a_polygon
from yyyyy_word_bubbles import draw_a_speech_bubble
from yyyyy_shape_style import scale_default_fontsize, get_canvas_height, get_canvas_width, set_default_linewidth
from yyyyy_coordinates import shape_names_params_dicts_definition, get_type_given_shapename, build_a_smile, build_a_zigzag
from demo_yyyyy_shape_helper import slider_range
import numpy as np
from random import random, randint
from yyyyy_layers import new_layer, shift_layers

smile = build_a_smile(width=3, depth=0.5)
zigzag = build_a_zigzag(width=3, height=0.5, angle_start=-3, nb_segments=6)
zigzag += -zigzag[0] + smile[-1] + [0, 3.5]
a_curve = np.concatenate((smile, zigzag), axis=0)
a_random_curve = [[random()*3.5, random()*3.5] for _ in range(randint(15, 25))]

shape_names_params_dicts_definition_plus = {k : v for k, v in shape_names_params_dicts_definition.items()}
shape_names_params_dicts_definition_plus.update({'a_polygon' : {}, 'a_broken_line' : {}})

gap, text_height, shape_height = 1, 1.5, 5.5

shape_positions_colors_params = { 1 : 
                            [['a_square', 'superBlue'], 
                             ['a_rectangle', 'superGold'], 
                             ['a_triangle', 'superOrange'],
                             ['a_rhombus', 'superViolet'],
                             ['a_star', 'Purple', .6, ['orchid', .8, {'ends_qty' : 8, 'radius_1' : 3}]], 
                             ['a_regular_polygon', 'red', .9, ['orangered', .9, {'vertices_qty' : 8}]],
                             ['a_polygon', 'turquoise', 1.0, ['darkturquoise', 1.]]],  
                                  10 : 
                            [['a_circle', 'superPink', .8],
                             ['an_ellipse', 'Burgundy'],                             
                             ['a_drop', 'BubblePink'], 
                             ['an_egg', 'BrightGreen'], 
                             ['a_heart', 'RoyalBlue', 3.5], 
                             ['a_sector', 'DarkTeal', .8, ['SeaWave', .8, {'radius' : 0, 'angle_end' : 1}]], 
                             ['an_elliptic_sector', 'Yellow', 2, 
                                      ['yellowgreen', 1.2, {'angle_start' : 3, 'angle_end' : 12}]],
                             ['a_crescent', 'dimgray', 1., 
                                          ['darkgray', 1.35, {'depth_2' : -2.5, 'turn' : -3}]],
                             ['a_squiggle', 'orchid', .8, ['darkorchid', .8, {'speed_x' : 5}]]],
                                  28 : 
                            [['a_segment', 'yellow'],
                             ['a_zigzag', 'LightBlue'],
                             ['a_power_curve', 'red', 0.7],
                             ['an_arc', 'PastelBlue', {'diamond_color' : 'PastelBlue'}],
                             ['a_smile', 'PastelBlue', {'diamond_color' : 'PastelBlue'}],
                             ['a_wave', 'palegreen'],
                             ['a_coil', 'lightcoral', 1., 
                              ['coral', .075, {'speed_x' : 0, 'speed_out' : 3.5}]],
                             ['a_squiggle_curve', 'orchid', .7, 
                              ['darkorchid', .7, {'speed_x' : 1.5}],
                              ['Hyacinth', .7, {'speed_x' : 5/6, 'angle_end':160}]],
                             ['a_broken_line', 'turquoise', 1., ['darkturquoise', 1.]]]
}

create_canvas_and_axes(canvas_width=70, canvas_height=36)
draw_a_rectangle(bottom=18+1.5, height=get_canvas_height(), left=0, width=get_canvas_width(), color='black', layer_nb=-2)
draw_a_rectangle(bottom=18, height=28-1-18-1.5, left=0, width=get_canvas_width()/2, color='white', layer_nb=-2)
for i, text_ in enumerate(['patches', 'lines']):
  sb = draw_a_speech_bubble(text=text_, x=get_canvas_width()/2*i, y=18, fontsize=30,
                       color='black' if i == 0 else 'white', 
                       background_color='black' if i == 1 else 'white')
  sb.shift_to_position((get_canvas_width() * (.25 + .5 * i), 18 + 4.5), 'cc')
scale_default_fontsize(.36)
set_default_linewidth(5)

#######################################################
# Now let's draw the shapes!                         ##

for text_y, shapes_infos in shape_positions_colors_params.items():
  layer_nb_bg = new_layer()
  layer_nb = new_layer()
  x_so_far = 0
  shape_y = text_y + text_height + 0.5 * shape_height
  for nb_shape, shapes_info in enumerate(shapes_infos):
    x_so_far += gap
    shapename = shapes_info[0]

    text_color = 'black' if text_y < 18 else 'white'
    bg_color = ('black' if nb_shape%2 else 0.2) if text_y > 18 else ('white' if nb_shape%2 else 0.8)

    sb = draw_a_speech_bubble(text=shapename, x=x_so_far, y=text_y, color=text_color, background_color=bg_color, layer_nb=layer_nb)
    long_params = shape_names_params_dicts_definition_plus[shapename]

    shape_params = {p_name : slider_range[p_slider_params][2] if isinstance(p_slider_params, str) else p_slider_params[1] 
                                                                        for p_name, p_slider_params in long_params.items()}

    func = draw_a_polygon if get_type_given_shapename(shapename) == 'patch' else draw_a_broken_line
    if len(shapes_info) >= 3:
      zoom_or_params = shapes_info[2]
      if isinstance(zoom_or_params, dict):
        shape_params.update(zoom_or_params)

    shs = [func(diamond_x=0, diamond_y=0, color=shapes_info[1], **shape_params,
              contour=a_curve if shapename in ('a_polygon', 'a_broken_line') else shapename)]

    if len(shapes_info) >= 3:
      zoom_or_params = shapes_info[2]
      if not isinstance(zoom_or_params, dict):
        shs[-1].stretch(zoom_or_params)

    shs[-1].shift_to_position(xy=[x_so_far, shape_y], position='lc')
    x_so_far += shs[-1].get_bbox().width

    for sh_ in shapes_info[3:]:
      x_so_far += gap
      if len(sh_) > 2:
        shape_params.update(sh_[2])
      shs.append(func(diamond_x=0, diamond_y=0, color=sh_[0], **shape_params,
                      contour=a_random_curve if shapename in ('a_polygon', 'a_broken_line') else shapename))
      shs[-1].stretch(sh_[1])
      shs[-1].shift_to_position(xy=[x_so_far, shape_y], position='lc')
      x_so_far += shs[-1].get_bbox().width
    
    center_shapes = (shs[0].get_bbox().xmin + shs[-1].get_bbox().xmax) / 2
    center_text = (sb.get_bbox().xmin + sb.get_bbox().xmax) / 2
    if center_shapes > center_text:
      sb.shift_to_position(xy=[center_shapes, text_y], position='ct')
    else:
      for sh_ in shs:
        sh_.shift_x(center_text - center_shapes)
      x_so_far = sb.get_bbox().xmax

    left, right = min(shs[0].get_bbox().xmin, sb.get_bbox().xmin), max(shs[-1].get_bbox().xmax, sb.get_bbox().xmax)
    draw_a_rectangle(left=left-gap/2, width=right-left+gap, bottom=text_y-gap/2, height=text_height+shape_height+gap,
                     outline_color=text_color, layer_nb=layer_nb_bg, color=bg_color) 
  shift_layers(shift=[get_canvas_width() / 2 - (x_so_far + gap) / 2, 0], layer_nbs=[layer_nb_bg, layer_nb])

show_and_save()