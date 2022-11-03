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

from yyyyy_shape_style import _get_renderer, _get_axes, default_text_bubble_params
from yyyyy_utils import atan, calc_Pythagoras
from yyyyy_shape_functions import draw_a_triangle

##################################################################
## SHAPE                                                        ## 
##################################################################

class WordBubble:

  text_boxes = []

  ################################################################# 
  def get_all():
    return WordBubble.text_boxes

  ################################################################# 
  def _create_params_subdictionary(param_names_dictionary, kwargs):
    result = {}
    used_argnames = []
    for dict_entry in param_names_dictionary:
      if isinstance(dict_entry, str):
        result[dict_entry] = kwargs[dict_entry] if dict_entry in kwargs else default_text_bubble_params[dict_entry]
        if dict_entry in kwargs:
          used_argnames += [dict_entry]
      else:
        result[dict_entry[0]] = kwargs[dict_entry[1]] if dict_entry[1] in kwargs else default_text_bubble_params[dict_entry[1]]
        if dict_entry[1] in kwargs:
          used_argnames += [dict_entry[1]]
    return result, used_argnames

  ################################################################## 
  def __init__(self, text, x, y, ax=None, start=None, connection=None, **kwargs):

    ax = _get_axes(ax=ax)
      
    props, used_argnames = WordBubble._create_params_subdictionary([['facecolor', 'backgroundcolor'], ['alpha', 'opacity'], 'pad', # 'rounding_size', 
    ['edgecolor', 'linecolor'], 'linewidth', ['zorder', 'layer_nb']], kwargs)
    props['boxstyle'] = 'round'
  
    text_dict, used_argnames2 = WordBubble._create_params_subdictionary(['fontsize', 'verticalalignment', 'horizontalalignment', 'multialignment', 'wrap', ['zorder', 'layer_nb'], 'fontfamily', 'color'], kwargs)
    used_argnames += used_argnames2

    _triangle = draw_a_triangle(tip=[0, 0], height=0, width=0, turn=0, color=props['facecolor'], outline_linewidth=props['linewidth'], outline_color=props['edgecolor'], layer_nb=props['zorder']-1, outline_layer_nb=props['zorder']-1)
    _triangle.set_visible(False)

    # place a text box in upper left in axes coords
    self.text_box =  ax.text(s=text, x=x, y=y, transform=ax.transData, **text_dict, bbox=props)
    WordBubble.text_boxes.append(self.text_box)

    assert (start is None) == (connection is None)
    self.connection = connection
    self.start = start
    if start is None:
      self.connector = None
    else:
      assert connection in ['bubble', 'triangle']
      if  self.connection == 'triangle':
        assert 'triangle_width' in kwargs
        self.connector = _triangle
        self.connector.shift_to(start)
        self.connector.width = kwargs['triangle_width']
        self.connector.set_visible(True)
      else:
        raise Exception("not implemented")
      self.set_text(text) # to adjust the size of the connector
    
    WordBubble.text_boxes.append(self)

  def _get_what_to_move(self):
    result = [self.text_box]
    return result

  def make_visible(self, val=True):
    self.text_box.set_visible(val)
    if self.connector is not None:
      self.connector.set_visible(val)

  def make_invisible(self):
    self.make_visible(False)

  def set_text(self, text, mid_override=None):
    self.text_box.set_text(text)
    
    
    tbb = self.text_box.get_window_extent(renderer=_get_renderer())   
    tbb_it = self.text_box.get_bbox_patch().get_bbox().transformed(self.text_box.axes.transData.inverted())#tbb.transformed(self.text_box.axes.transData.inverted())

    #print(tbb_it, self.text_box.get_position())

    mid = mid_override if mid_override is not None else [0.5*(tbb_it.x1+tbb_it.x0), 0.5*(tbb_it.y1+tbb_it.y0)]

    x, y = self.text_box.get_position()

    if self.connection is None:
      pass
    elif  self.connection == 'triangle':
      # xy is a top left corner
      triangle_height = calc_Pythagoras(self.start[0] - mid[0], self.start[1] - mid[1])
      self.connector.height = triangle_height
      triangle_turn = atan((self.start[0] - mid[0]) / (self.start[1] - mid[1]))
      if self.start[1] > mid[1]:
        triangle_turn += 6
      self.connector.turn_to(turn=triangle_turn)
    else:
      raise Exception("not implemented")

def draw_a_speech_bubble(text, x, y, **kwargs):
  wb = WordBubble(text, x, y, **kwargs)
  return wb

def draw_a_code_bubble(text, x, y, **kwargs):
  cb = WordBubble(text, x, y, fontfamily='freemono', color='white', backgroundcolor='black', **kwargs)
  return cb