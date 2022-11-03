
from yyyyy_canvas import create_canvas_and_axes, show_and_save
from yyyyy_shape_functions import draw_a_square

#######################################################
# Creating the canvas!                               ##
create_canvas_and_axes(canvas_width=10, canvas_height=10, tick_step=1)

#######################################################
# Now let's draw the shapes!                         ##
draw_a_square(left=0, bottom=0, side=1, color='black')

show_and_save()