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

shape_positions_colors_params = {
                            'a_square': [1, 1, 3, 5, 'superBlue'], 
                            'a_rectangle': [7, 1, 10, 5, 'superGold'], 
                            'a_triangle': [14+1, 1, 16.5+1, 3, 'superOrange'],
                            'a_rhombus' : [20.5+2, 1, 22.5+2, 5, 'superViolet'],
                            'a_star': [32, 1, 29+2, 5, 'Purple', .6, 
                                      [36, 5, 'orchid', .8, {'ends_qty' : 8, 'radius_1' : 3}]], 
                            'a_regular_polygon': [40, 1, 42, 5, 'red', .9, 
                                      [48, 5, 'orangered', .9, {'vertices_qty' : 8}]], 

                            'a_circle': [1, 10, 3.2, 14.5, 'superPink', .8],
                            'an_ellipse': [7, 10, 10, 14.5, 'Burgundy'],                             
                            'a_drop': [17-3.5, 10, 18.5-3.5, 16.5, 'BubblePink'], 
                            'an_egg': [22-3.5, 10, 23.5-3.5, 11.5, 'BrightGreen'], 
                            'a_heart': [27-3.5, 10, 28.5-3.5, 11.5, 'RoyalBlue', 2], 
                            'a_sector': [29.5, 10, 1+27, 11.5, 'DarkTeal', .8, 
                                        [6+27, 11.5, 'SeaWave', .8, {'radius' : 0, 'angle_end' : 1}]], 
                            'an_elliptic_sector': [35.5, 10, 40.5, 14, 'Yellow', 2, 
                                      [40, 13.5, 'yellowgreen', 1.2, {'angle_start' : 3, 'angle_end' : 12}]],
                            'a_crescent': [51-4, 10, 54-4, 12.5, 'dimgray', 1., 
                                          [54-4, 13.5, 'darkgray', 1.5, {'depth_2' : -2.5, 'turn' : 1}]],
                            'a_squiggle' : [54.5, 10, 56, 14, 'orchid', .8, 
                                             [59, 14, 'darkorchid', .8, {'speed_x' : 5}]],
                            'a_polygon' : [57.5, 1, 57.5, 5, 'turquoise', 1], 
                            

                            'a_segment': [1, 19, 4, 21+1, 'yellow'],
                            'a_zigzag': [8, 19, 9, 22.5+1, 'LightBlue'],
                            'a_power_curve': [15, 19, 16, 22, 'superOrange', 0.7],
                            'an_arc': [25, 19, 25, 24.5+1, 'PastelBlue', {'diamond_color' : 'PastelBlue'}],
                            'a_smile': [31, 19, 33.5, 22+1, 'PastelBlue', {'diamond_color' : 'PastelBlue'}],
                            'a_wave' : [37, 19, 37.5, 24+1, 'palegreen'],
                            'a_coil' : [42, 19, 42, 24+1, 'lightcoral'],
                            'a_squiggle_curve' : [47, 19, 48.5, 23+1, 'orchid', .7, 
                              [51.5, 23+1, 'darkorchid', .7, {'speed_x' : 1.5}],
                              [54.5, 23+1, 'Hyacinth', .7, {'speed_x' : 5/6, 'angle_end':160}]],
                            'a_broken_line' : [57.5, 19, 57.5, 24+1, 'turquoise', 1]
}

create_canvas_and_axes(canvas_width=66, canvas_height=36)
scale_default_fontsize(.36)
set_default_linewidth(5)
bg = draw_a_rectangle(bottom=18, height=get_canvas_height()-18, left=0, width=get_canvas_width(), color='black')

#######################################################
# Now let's draw the shapes!                         ##

for shapename, long_params in shape_names_params_dicts_definition_plus.items():
  text_x, text_y, shape_x, shape_y, color = shape_positions_colors_params[shapename][:5]
  sb = draw_a_speech_bubble(text=shapename, x=text_x, y=text_y,
                       color=('black' if get_type_given_shapename(shapename) == 'patch' else 'white'),
            background_color=('black' if get_type_given_shapename(shapename) != 'patch' else 'white'))
  sbt = draw_box_around(sb)
  print(shapename, sb.get_text(), sbt.xmin, sbt.ymin)
  shape_params = {p_name : slider_range[p_slider_params][2] if isinstance(p_slider_params, str) else p_slider_params[1] 
                                                                      for p_name, p_slider_params in long_params.items()}

  func = draw_a_polygon if get_type_given_shapename(shapename) == 'patch' else draw_a_broken_line
  if len(shape_positions_colors_params[shapename]) >= 6:
    zoom_or_params = shape_positions_colors_params[shapename][5]
    if isinstance(zoom_or_params, dict):
      shape_params.update(zoom_or_params)

  sh = func(diamond_x=shape_x, diamond_y=shape_y, color=color, 
            contour=a_curve if shapename in ('a_polygon', 'a_broken_line') else shapename, 
            **shape_params)
  if len(shape_positions_colors_params[shapename]) >= 6:
    zoom_or_params = shape_positions_colors_params[shapename][5]
    if not isinstance(zoom_or_params, dict):
      sh.stretch(zoom_or_params)
  draw_box_around(sh)
  for sh_ in shape_positions_colors_params[shapename][6:]:
      shape_x, shape_y, color, zoom, param_dict = sh_[0], sh_[1], sh_[2], sh_[3], sh_[4]
      shape_params.update(param_dict)
      sh = func(diamond_x=shape_x, diamond_y=shape_y, color=color, contour=shapename, **shape_params)
      sh.stretch(zoom)
      draw_box_around(sh)

show_and_save()