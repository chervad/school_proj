import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


def draw_pine(x, y):
    arcade.draw_triangle_filled(x + 40, y, x, y - 100, x + 80, y - 100, arcade.color.DARK_GREEN)
    arcade.draw_lrtb_rectangle_filled(x + 30, x + 50, y - 100, y - 140, arcade.color.DARK_BROWN)


arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, "School project")
arcade.set_background_color(arcade.color.GREEN)

arcade.start_render()
arcade.finish_render()

arcade.run()