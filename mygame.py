import arcade
import random
import math
import os

STARTING_ASTEROID_COUNT = 3
PAIN_COUNT = 5
HOUSE_COUNT = 4
CAR_COUNT = 3
SCALE = 0.5
OFFSCREEN_SPACE = 200  # 300
LEFT_LIMIT = 0  # -OFFSCREEN_SPACE
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
RIGHT_LIMIT = SCREEN_WIDTH  # + OFFSCREEN_SPACE
BOTTOM_LIMIT = -OFFSCREEN_SPACE
TOP_LIMIT = SCREEN_HEIGHT + OFFSCREEN_SPACE


# class TurningSprite(arcade.Sprite):
#     """ Sprite that sets its angle to the direction it is traveling in. """
#
#     def update(self):
#         super().update()
#         self.angle = math.degrees(math.atan2(self.change_y, self.change_x))


class ShipSprite(arcade.Sprite):
    """
    Sprite that represents our space ship.

    Derives from arcade.Sprite.
    """

    def __init__(self, filename, scale):
        """ Set up the space ship. """

        # Call the parent Sprite constructor
        super().__init__(filename, scale)

        # Info on where we are going.
        # Angle comes in automatically from the parent class.
        self.thrust = 0
        self.speed = 0
        self.max_speed = 4
        self.drag = 0.05
        self.respawning = 0

        # Mark that we are respawning.
        self.respawn()

    def respawn(self):
        """
        Called when we die and need to make a new ship.
        'respawning' is an invulnerability timer.
        """
        # If we are in the middle of respawning, this is non-zero.
        # self.respawning = 1
        self.center_x = SCREEN_WIDTH / 2
        self.center_y = 20
        self.angle = 0

    def update(self):
        """
        Update our position and other particulars.
        """
        # if self.respawning:
        #    self.respawning += 1
        #    self.alpha = self.respawning / 500.0
        #    if self.respawning > 250:
        #        self.respawning = 0
        #        self.alpha = 1
        if self.speed > 0:
            self.speed -= self.drag
            if self.speed < 0:
                self.speed = 0

        if self.speed < 0:
            self.speed += self.drag
            if self.speed > 0:
                self.speed = 0

        self.speed += self.thrust
        if self.speed > self.max_speed:
            self.speed = self.max_speed
        if self.speed < -self.max_speed:
            self.speed = -self.max_speed

        # self.change_x = -math.sin(math.radians(self.angle)) * self.speed
        # self.change_y = math.cos(math.radians(self.angle)) * self.speed

        self.center_x += self.change_x
        self.center_y += self.change_y

        """ Call the parent class. """
        super().update()


class AsteroidSprite(arcade.Sprite):
    """ Sprite that represents an asteroid. """

    def __init__(self, image_file_name, scale):
        super().__init__(image_file_name, scale=scale)
        self.size = 0
        self.bullet_list = arcade.SpriteList()

    def update(self):
        """ Move the asteroid around. """
        super().update()
        if self.center_x < LEFT_LIMIT:
            self.center_x = RIGHT_LIMIT
        if self.center_x > RIGHT_LIMIT:
            self.center_x = LEFT_LIMIT
        if self.center_y > TOP_LIMIT:
            self.center_y = BOTTOM_LIMIT
        if self.center_y < BOTTOM_LIMIT:
            self.center_y = TOP_LIMIT


class BulletSprite(arcade.Sprite):  # TurningSprite):
    """
    Class that represents a bullet.

    Derives from arcade.TurningSprite which is just a Sprite
    that aligns to its direction.
    """

    def update(self):
        super().update()
        self.angle = math.degrees(math.atan2(self.change_y, self.change_x))
        if self.center_x < -100 or self.center_x > 1500 or self.center_y > 1100 or self.center_y < -100:
            self.kill()


class CarSprite(arcade.Sprite):
    """ Sprite that represents an car. """

    def __init__(self, image_file_name, scale):
        super().__init__(image_file_name, scale=scale)
        self.max_life = 4


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "School project")

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.frame_count = 0

        self.game_over = False

        # Sprite lists
        self.all_sprites_list = None
        self.asteroid_list = None
        self.bullet_list = None
        self.enemy_bullet_list = None
        self.ship_life_list = None
        self.car_list = None

        # Set up the player
        self.score = 0
        self.player_sprite = None
        self.lives = 3

        self.shape_list = None

        # Sounds
        self.laser_sound = arcade.load_sound("sounds/laser1.wav")

        arcade.set_background_color(arcade.color.DARK_GREEN)

    def start_new_game(self):
        """ Set up the game and initialize the variables. """

        self.frame_count = 0
        self.game_over = False

        # Sprite lists
        self.all_sprites_list = arcade.SpriteList()
        self.asteroid_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()

        self.ship_life_list = arcade.SpriteList()
        self.car_list = arcade.SpriteList()

        for i in range(HOUSE_COUNT):
            house_sprite = arcade.Sprite("images/house.png")
            house_sprite.center_x = random.randrange((SCREEN_WIDTH // HOUSE_COUNT) * i + 60
                                                     , (SCREEN_WIDTH // HOUSE_COUNT) * (i + 1) - 60)
            house_sprite.center_y = random.randrange(160, SCREEN_HEIGHT - 280)
            self.all_sprites_list.append(house_sprite)

        for i in range(PAIN_COUNT):
            pain_sprite = arcade.Sprite("images/pine.png")
            pain_sprite.center_x = random.randrange((SCREEN_WIDTH // PAIN_COUNT) * i + 30
                                                    , (SCREEN_WIDTH // HOUSE_COUNT) * (i + 1) - 30)
            pain_sprite.center_y = random.randrange(120, SCREEN_HEIGHT - 300)
            self.all_sprites_list.append(pain_sprite)

        for i in range(CAR_COUNT):
            car_sprite = CarSprite("images/auto_00.png", SCALE)
            car_sprite.center_x = random.randrange((SCREEN_WIDTH // CAR_COUNT) * i + 120
                                                   , (SCREEN_WIDTH // CAR_COUNT) * (i + 1) - 120)
            car_sprite.center_y = random.randrange(65, SCREEN_HEIGHT - 265)
            self.all_sprites_list.append(car_sprite)
            self.car_list.append(car_sprite)

        # Set up the player
        self.score = 0
        self.player_sprite = ShipSprite("images/tank.png", SCALE)
        self.all_sprites_list.append(self.player_sprite)
        self.lives = 3

        # Set up the little icons that represent the player lives.
        cur_pos = 10
        for i in range(self.lives):
            life = arcade.Sprite("images/tank_mini.png", SCALE)
            life.center_x = cur_pos + life.width
            life.center_y = life.height
            cur_pos += life.width
            self.all_sprites_list.append(life)
            self.ship_life_list.append(life)

        # Make the asteroids
        for i in range(STARTING_ASTEROID_COUNT):
            enemy_sprite = AsteroidSprite("images/ufo.png", SCALE)
            enemy_sprite.guid = "Asteroid"

            enemy_sprite.center_y = TOP_LIMIT # random.randrange(BOTTOM_LIMIT, TOP_LIMIT)
            enemy_sprite.center_x = random.randrange(LEFT_LIMIT, RIGHT_LIMIT)

            enemy_sprite.change_x = random.random() * 2 - 1
            enemy_sprite.change_y = - random.randrange(1, 4)

            # enemy_sprite.change_angle = (random.random() - 0.5) * 2
            # enemy_sprite.size = 4
            self.all_sprites_list.append(enemy_sprite)
            self.asteroid_list.append(enemy_sprite)
            # self.all_sprites_list.append(life)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites.
        self.all_sprites_list.draw()
        for asteroid in self.asteroid_list:
            asteroid.bullet_list.draw()

        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 70, arcade.color.WHITE, 13)

        output = f"Asteroid Count: {len(self.asteroid_list)}"
        arcade.draw_text(output, 10, 50, arcade.color.WHITE, 13)

    def on_key_press(self, symbol, modifiers):
        """ Called whenever a key is pressed. """
        # Shoot if the player hit the space bar and we aren't respawning.
        if not self.player_sprite.respawning and symbol == arcade.key.SPACE:
            bullet_sprite = BulletSprite("images/laserBlue01.png", SCALE)
            bullet_sprite.guid = "Bullet"

            bullet_speed = 13
            bullet_sprite.change_y = \
                math.cos(math.radians(self.player_sprite.angle)) * bullet_speed
            bullet_sprite.change_x = \
                -math.sin(math.radians(self.player_sprite.angle)) \
                * bullet_speed

            bullet_sprite.center_x = self.player_sprite.center_x
            bullet_sprite.center_y = self.player_sprite.center_y
            bullet_sprite.update()

            self.all_sprites_list.append(bullet_sprite)
            self.bullet_list.append(bullet_sprite)

            # arcade.play_sound(self.laser_sound)

        if symbol == arcade.key.LEFT:
            # self.player_sprite.change_angle = 3
            self.player_sprite.change_x -= 2
        elif symbol == arcade.key.RIGHT:
            # self.player_sprite.change_angle = -3
            self.player_sprite.change_x = 2
        # elif symbol == arcade.key.UP:
        #    self.player_sprite.thrust = 0.15
        # elif symbol == arcade.key.DOWN:
        #    self.player_sprite.thrust = -.2

    def on_key_release(self, symbol, modifiers):
        """ Called whenever a key is released. """
        if symbol == arcade.key.LEFT:
            # self.player_sprite.change_angle = 0
            self.player_sprite.change_x = 0
        elif symbol == arcade.key.RIGHT:
            # self.player_sprite.change_angle = 0
            self.player_sprite.change_x = 0
        # elif symbol == arcade.key.UP:
        #    self.player_sprite.thrust = 0
        # elif symbol == arcade.key.DOWN:
        #    self.player_sprite.thrust = 0

    def update(self, x):
        """ Move everything """

        self.frame_count += 1

        if self.frame_count % 20 == 0:
            for asteroid in self.asteroid_list:
                bullet_sprite = BulletSprite("images/laserBlue01.png", SCALE)
                bullet_sprite.guid = "Bullet UFO"

                bullet_speed = 8
                bullet_sprite.change_y = -math.sin(math.radians(random.randrange(45, 135))) * bullet_speed
                bullet_sprite.change_x = math.cos(math.radians(random.randrange(45, 135))) * bullet_speed

                bullet_sprite.center_x = asteroid.center_x
                bullet_sprite.center_y = asteroid.center_y
                bullet_sprite.update()

                self.all_sprites_list.append(bullet_sprite)
                self.enemy_bullet_list.append(bullet_sprite)

        if not self.game_over:
            self.all_sprites_list.update()

            for bullet in self.bullet_list:
                self.asteroid_list.use_spatial_hash = False
                asteroids_plain = arcade.check_for_collision_with_list(bullet, self.asteroid_list)
                self.asteroid_list.use_spatial_hash = True
                asteroids_spatial = arcade.check_for_collision_with_list(bullet, self.asteroid_list)
                if len(asteroids_plain) != len(asteroids_spatial):
                    print("ERROR")

                asteroids = asteroids_spatial

                for asteroid in asteroids:
                    asteroid.kill()
                    bullet.kill()

            for bullet in self.enemy_bullet_list:
                player_shoot = arcade.check_for_collision(bullet, self.player_sprite)
                if player_shoot:
                    bullet.kill()
                    if self.lives > 0:
                        self.lives -= 1
                        self.player_sprite.respawn()
                        self.ship_life_list.pop().kill()
                        print("Crash")
                    else:
                        self.game_over = True
                        print("Game over")

            for bullet in self.enemy_bullet_list:
                cars_spatial = arcade.check_for_collision_with_list(bullet, self.car_list)

                for car in cars_spatial:
                    bullet.kill()
                    if car.max_life > 0:
                        buf = "images/auto_0%d.png" % (4 - car.max_life)
                        new_car = CarSprite(buf, SCALE)
                        new_car.center_x = car.center_x
                        new_car.center_y = car.center_y
                        new_car.max_life = car.max_life - 1
                        self.all_sprites_list.append(new_car)
                        self.car_list.append(new_car)
                        car.kill()
                    else:
                        car.kill()

            if not self.player_sprite.respawning:
                asteroids = arcade.check_for_collision_with_list(self.player_sprite, self.asteroid_list)
                if len(asteroids) > 0:
                    if self.lives > 0:
                        self.lives -= 1
                        self.player_sprite.respawn()
                        asteroids[0].kill()
                        self.ship_life_list.pop().kill()
                        print("Crash")
                    else:
                        self.game_over = True
                        print("Game over")
