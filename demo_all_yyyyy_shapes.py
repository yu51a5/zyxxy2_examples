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
from yyyyy_coordinates import shape_names_params_dicts_definition, get_type_given_shapename
from demo_yyyyy_shape_helper import slider_range


#                      'LightPink',
#                      ''   : "#b66dff",
#                      'PastelBlue' : "#6db6ff",
#                      'LightBlue'  : "#b6dbff",

shape_positions_colors_params = {
                            'a_square': [1, 1, 3, 5, 'superBlue'], 
                            'a_rectangle': [7, 1, 10, 5, 'superGold'], 
                            'a_triangle': [14+1, 1, 16.5+1, 3, 'superOrange'],
                            'a_rhombus' : [20.5+2, 1, 22.5+2, 5, 'superViolet'],
                            'a_star': [27+2, 1, 29+2, 5, 'Purple', .6], 
                            'a_regular_polygon': [32+2, 1, 36.5+2, 5, 'red'], 

                            'a_circle': [1, 10, 3.2, 14.5, 'superPink', .8],
                            'an_ellipse': [7, 10, 10, 14.5, 'Burgundy'],                             
                            'a_drop': [17-3.5, 10, 18.5-3.5, 16.5, 'BubblePink'], 
                            'an_egg': [22-3.5, 10, 23.5-3.5, 11.5, 'BrightGreen'], 
                            'a_heart': [27-3.5, 10, 28.5-3.5, 11.5, 'RoyalBlue', 2], 
                            'a_sector': [29.5, 10, 1+27, 11.5, 'DarkTeal', .8, 
                                        [6+27, 11.5, 'SeaWave', .8, {'radius' : 0, 'angle_end' : 1}]], 
                            'an_elliptic_sector': [36.4, 10, 40.4, 11.5, 'Yellow', 2],
                            'a_crescent': [51, 10, 54, 12.5, 'dimgray', 1., 
                                          [54, 13.5, 'darkgray', 1.5, {'depth_2' : -2.5, 'turn' : 1}]],

                            'a_segment': [1, 19, 4, 21, 'Hyacinth'],
                            'a_zigzag': [8, 19, 9, 22.5, 'LightBlue'],
                            'a_power_curve': [15, 19, 16, 22, 'LightPink', 0.7],
                            'an_arc': [25, 19, 25, 24.5, 'PastelBlue'],
                            'a_smile': [31, 19, 33.5, 22, 'PastelBlue'],
                            'a_wave': [38, 19, 38.5, 24, 'palegreen'],

                            # ''
                            # 'a_coil'
                            # 'a_squiggle'
                            # '' : [], 
                            #  : [],  
}

create_canvas_and_axes(canvas_width=60, canvas_height=36)
scale_default_fontsize(.4)
set_default_linewidth(5)
draw_a_rectangle(bottom=18, height=get_canvas_height()-18, left=0, width=get_canvas_width(), color='black')

#######################################################
# Now let's draw the shapes!                         ##

for shapename, long_params in shape_names_params_dicts_definition.items():
  if shapename not in shape_positions_colors_params:
    continue
  text_x, text_y, shape_x, shape_y, color = shape_positions_colors_params[shapename][:5]
  draw_a_speech_bubble(text=shapename, x=text_x, y=text_y,
                       color=('black' if get_type_given_shapename(shapename) == 'patch' else 'white'))
  shape_params = {p_name : slider_range[p_slider_params][2] if isinstance(p_slider_params, str) else p_slider_params[1] 
                                                                      for p_name, p_slider_params in long_params.items()}

  func = draw_a_polygon if get_type_given_shapename(shapename) == 'patch' else draw_a_broken_line
  sh = func(diamond_x=shape_x, diamond_y=shape_y, color=color, contour=shapename,  **shape_params)
  if len(shape_positions_colors_params[shapename]) >= 6:
    sh.stretch(shape_positions_colors_params[shapename][5])
  if len(shape_positions_colors_params[shapename]) > 6:
    shape_x, shape_y, color, zoom, param_dict = shape_positions_colors_params[shapename][6]
    shape_params.update(param_dict)
    sh = func(diamond_x=shape_x, diamond_y=shape_y, color=color, contour=shapename, **shape_params)
    sh.stretch(zoom)

show_and_save()