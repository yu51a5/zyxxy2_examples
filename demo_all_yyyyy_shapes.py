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

smile = build_a_smile(width=2, depth=0.5)
zigzag = build_a_zigzag(width=2, height=0.5, angle_start=-3, nb_segments=5)
zigzag += -zigzag[0] + smile[-1] + [0, 2.]
a_curve = np.concatenate((smile, zigzag), axis=0)

shape_names_params_dicts_definition_plus = {k : v for k, v in shape_names_params_dicts_definition.items()}
shape_names_params_dicts_definition_plus.update({'a_polygon' : {}, 'a_broken_line' : {}})

def draw_box_around(what):
  bb = what.get_bbox()
  draw_a_rectangle(left=bb.xmin, bottom=bb.ymin, width=bb.width, height=bb.height, outline_color='red')
  return bb

gap, text_height, shape_height = 1, 1.5, 5.5

text_height + 0.5 * shape_height

shape_positions_colors_params = { 1 : 
                            [['a_square', 'superBlue'], 
                             ['a_rectangle', 'superGold'], 
                             ['a_triangle', 'superOrange'],
                             ['a_rhombus', 'superViolet'],
                             ['a_star', 'Purple', .6, ['orchid', .8, {'ends_qty' : 8, 'radius_1' : 3}]], 
                             ['a_regular_polygon', 'red', .9, ['orangered', .9, {'vertices_qty' : 8}]],
                             ['a_polygon', 'turquoise']],  
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
                                          ['darkgray', 1.35, {'depth_2' : -2.5, 'turn' : 3}]],
                             ['a_squiggle', 'orchid', .8, ['darkorchid', .8, {'speed_x' : 5}]]],
                                  19 : 
                            [['a_segment', 'yellow'],
                             ['a_zigzag', 'LightBlue'],
                             ['a_power_curve', 'superOrange', 0.7],
                             ['an_arc', 'PastelBlue', {'diamond_color' : 'PastelBlue'}],
                             ['a_smile', 'PastelBlue', {'diamond_color' : 'PastelBlue'}],
                             ['a_wave', 'palegreen'],
                             ['a_coil', 'lightcoral'],
                             ['a_squiggle_curve', 'orchid', .7, 
                              ['darkorchid', .7, {'speed_x' : 1.5}],
                              ['Hyacinth', .7, {'speed_x' : 5/6, 'angle_end':160}]],
                             ['a_broken_line', 'turquoise']]
}

create_canvas_and_axes(canvas_width=70, canvas_height=36)
scale_default_fontsize(.36)
set_default_linewidth(5)
bg = draw_a_rectangle(bottom=18, height=get_canvas_height()-18, left=0, width=get_canvas_width(), color='black')

#######################################################
# Now let's draw the shapes!                         ##

for text_y, shapes_infos in shape_positions_colors_params.items():
  x_so_far = gap
  shape_y = text_y + text_height + 0.5 * shape_height
  for shapes_info in shapes_infos:
    x_left = x_so_far
    shapename = shapes_info[0]
    sb = draw_a_speech_bubble(text=shapename, x=x_so_far, y=text_y,
                        color=('black' if get_type_given_shapename(shapename) == 'patch' else 'white'),
              background_color=('black' if get_type_given_shapename(shapename) != 'patch' else 'white'))
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
    x_so_far += gap + shs[-1].get_bbox().width

    for sh_ in shapes_info[3:]:
        shape_params.update(sh_[2])
        shs.append(func(diamond_x=0, diamond_y=0, color=sh_[0], contour=shapename, **shape_params))
        shs[-1].stretch(sh_[1])
        shs[-1].shift_to_position(xy=[x_so_far, shape_y], position='lc')
        x_so_far += gap + shs[-1].get_bbox().width

    x_so_far = max(x_so_far, sb.get_bbox().xmax + gap)

show_and_save()