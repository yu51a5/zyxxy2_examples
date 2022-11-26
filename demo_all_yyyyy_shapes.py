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
from yyyyy_shape_functions import draw_a_rectangle, draw_a_broken_line, draw_a_polygon, clone_a_shape
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
extention, extention2 = 4.5, 12
transf_y = 36+gap/2+extention
canvas_height = 36+gap/2+extention+extention2
create_canvas_and_axes(canvas_width=71, canvas_height=canvas_height)

shape_positions_colors_params = { 1 + gap/2 + extention: 
                            [['a_square', 'superBlue'], 
                             ['a_rectangle', 'superGold'], 
                             ['a_triangle', 'superOrange'],
                             ['a_rhombus', 'superViolet'],
                             ['a_star', 'Purple', .6, ['orchid', .8, {'ends_qty' : 8, 'radius_1' : 3}]], 
                             ['a_regular_polygon', 'red', .9, ['orangered', .9, {'vertices_qty' : 8}]],
                             ['a_polygon', 'turquoise', 1.0, ['darkturquoise', 1.]]],  
                                  10 + gap/2 + extention: 
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
                                  28 + extention: 
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
                             ['a_broken_line', 'turquoise', 1., ['darkturquoise', 1.]]],
                                  canvas_height - (gap + text_height + shape_height) : 

                              [['a_star', 'superBlue', 'shift', (3, .5), 0.5], 
                               ['a_square', 'superBlue', 'turn', 2], 
                               ['a_rhombus', 'superBlue', 'stretch', 1.8], 
                               ['a_drop', 'aquamarine', 'stretch_x', 1.5], 
                               ['a_crescent', 'turquoise', 'stretch_y', 1.5]]
}

draw_a_rectangle(bottom=19.5+extention, height=get_canvas_height(), left=0, width=get_canvas_width(), color='black', layer_nb=-2)
draw_a_rectangle(top=2 + 28, height=get_canvas_height(), left=0, width=get_canvas_width()/2, color='white', layer_nb=-2)
draw_a_rectangle(height= gap + text_height + shape_height + 2, top=get_canvas_height(), 
                 left=0, width=get_canvas_width(), color='plum', layer_nb=-2)

set_default_linewidth(5)
title_bboxes = [None, None]
c1, c2 = 2, 1
for i, text_ in enumerate(['patches', 'lines']):
  text_color = 'black' if i == 0 else 'white'
  title = draw_a_speech_bubble(text=text_, fontsize=30,
                       x=get_canvas_width() * (.25 + .5 * i), y=22.5 + extention, position='cc',
                       color=text_color, background_color='black' if i == 1 else 'white')
  title_bboxes[i] = title.get_bbox()
  if i == 0:
    y1, y2 = title_bboxes[i].ymax + gap/2, title_bboxes[i].ymin-gap/2
  else:
    y2, y1 = title_bboxes[i].ymax+gap/2, title_bboxes[i].ymin-gap/2
  draw_a_broken_line([[title_bboxes[i].xmin-gap*(c1+c2), y2], [title_bboxes[i].xmin-gap*c1, y1], 
                      [title_bboxes[i].xmax+gap*c1, y1], [title_bboxes[i].xmax+gap*(c1+c2), y2]], color=text_color)
  draw_a_broken_line([[title_bboxes[i].xmin-gap*(c1-c2), y2], [title_bboxes[i].xmin-gap*c1, y1], 
                      [title_bboxes[i].xmax+gap*c1, y1], [title_bboxes[i].xmax+gap*(c1-c2), y2]], color=text_color)
scale_default_fontsize(.36)


draw_a_rectangle(bottom=0, height=extention-gap/2, left=0, width=get_canvas_width(), color='plum')
draw_a_speech_bubble(text='Run demo_yyyyy_shape.py to see how the shape parameters work!', 
                          x=get_canvas_width()/2, y=(extention-gap/2)/2, position='cc', 
                          fontsize=15, background_color='plum')
#######################################################
# Now let's draw the shapes!                         ##

for text_y, shapes_infos in shape_positions_colors_params.items():
  layer_nb_bg = new_layer()
  layer_nb = new_layer()

  x_so_far = gap
  shape_y = text_y + text_height + 0.5 * shape_height
  for nb_shape, shapes_info in enumerate(shapes_infos):
    shapename = shapes_info[0]

    text_color = 'white' if 40 > text_y > 18 else 'black'
    
    sb = draw_a_speech_bubble(text=shapename if 40 > text_y else shapes_info[2], 
                              x=x_so_far, y=text_y, color=text_color, background_color='none')
    long_params = shape_names_params_dicts_definition_plus[shapename]

    shape_params = {p_name : slider_range[p_slider_params][2] 
                               if isinstance(p_slider_params, str) else p_slider_params[1] 
                                          for p_name, p_slider_params in long_params.items()}

    func = draw_a_polygon if get_type_given_shapename(shapename) == 'patch' else draw_a_broken_line
    if len(shapes_info) >= 3:
      zoom_or_params = shapes_info[2]
      if isinstance(zoom_or_params, dict):
        shape_params.update(zoom_or_params)

    shs = [func(diamond_x=0, diamond_y=0, color=shapes_info[1], **shape_params,
              contour=a_curve if shapename in ('a_polygon', 'a_broken_line') else shapename)]

    zoom_factor = 1.
    if (len(shapes_info) >= 3 and 40 > text_y) or (len(shapes_info) == 5 and 40 < text_y):
      zoom_or_params = shapes_info[2 if 40 > text_y else -1]
      if not isinstance(zoom_or_params, dict):
        zoom_factor = zoom_or_params
    shs[0].stretch(zoom_factor)
    shs[0].shift_to_position(xy=[x_so_far, shape_y], position='lc')

    if 40 > text_y:
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
       
    else:
      shs[0].shift_to_position(xy=[x_so_far, shape_y], position='lc')
      shs.append(clone_a_shape(shs[0]))
      an_attr = getattr(shs[0], shapes_info[2])
      an_attr(shapes_info[3])

      for sh in shs:
        sh.left += x_so_far - min([sh2.left for sh2 in shs])
      shs[0].color = 'Purple'
      shs[0].opacity = .5
      shs[1].color = 'superPink'

    center_shapes = (min([sh.left for sh in shs]) + max([sh.right for sh in shs])) / 2
    center_text = sb.center_x
    if center_shapes > center_text:
      sb.shift_to_position(xy=[center_shapes, text_y], position='cb')
    else:
      for sh_ in shs:
        sh_.shift_x(center_text - center_shapes)
    
    left, right = min([sh.left for sh in shs + [sb]]), max([sh.right for sh in shs + [sb]])
    draw_a_rectangle(left=left-gap/2, width=right-left+gap, bottom=text_y-gap/2, height=text_height+shape_height+gap,
                     outline_color=text_color, layer_nb=layer_nb_bg, color='none')
    x_so_far = right+gap

  shift_layers(shift=[get_canvas_width() / 2 - (x_so_far + gap) / 2, 0], layer_nbs=[layer_nb_bg, layer_nb])

show_and_save()