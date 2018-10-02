import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


def draw_pine(x, y):
    arcade.draw_triangle_filled(x + 40, y - 40, x, y - 100, x + 80, y - 100, arcade.color.DARK_GREEN)
    arcade.draw_triangle_filled(x + 40, y, x, y - 60, x + 80, y - 60, arcade.color.DARK_GREEN)
    arcade.draw_lrtb_rectangle_filled(x + 30, x + 50, y - 140, y - 300, arcade.color.DARK_BLUE)


def draw_house(x, y):
    arcade.draw_triangle_filled(x + 40, y, x, y - 60, x + 80, y - 60, arcade.color.DARK_RED)
    arcade.draw_lrtb_rectangle_filled(x + 30, x + 50, y - 300, y - 140, arcade.color.DARK_BLUE)


arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, "School project")
arcade.set_background_color(arcade.color.GREEN)

arcade.start_render()

draw_pine(550, 300)

arcade.finish_render()
arcade.run()
