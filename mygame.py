import arcade
import random
import math
import os

STARTING_UFO_COUNT = 3
PAIN_COUNT = 5
HOUSE_COUNT = 4
CAR_COUNT = 3
SCALE = 0.5
OFFSCREEN_SPACE = 200
LEFT_LIMIT = 0
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
RIGHT_LIMIT = SCREEN_WIDTH
BOTTOM_LIMIT = -OFFSCREEN_SPACE
TOP_LIMIT = SCREEN_HEIGHT + OFFSCREEN_SPACE


class TankSprite(arcade.Sprite):
    # Спрайт танка игрока

    def __init__(self, filename, scale):
        super().__init__(filename, scale)
        self.respawning = 0
        # устанвливаем танк внизу в центре
        self.respawn()

    def update(self):
        # Обновление позиции танка
        self.center_x += self.change_x
        self.center_y += self.change_y

        super().update()

    def respawn(self):
        # устанвливаем танк внизу в центре
        self.center_x = SCREEN_WIDTH / 2
        self.center_y = 20
        self.angle = 0


class UfoSprite(arcade.Sprite):
    # Спрайт вражеской тарелки

    def __init__(self, image_file_name, scale):
        super().__init__(image_file_name, scale=scale)
        self.size = 0
        self.bullet_list = arcade.SpriteList()
        

    def update(self):
        super().update()
        # Если тарелка выходит за пределы экрана, то появится с другой стороны
        if self.center_x < LEFT_LIMIT:
            self.center_x = RIGHT_LIMIT
        if self.center_x > RIGHT_LIMIT:
            self.center_x = LEFT_LIMIT
        if self.center_y > TOP_LIMIT:
            self.center_y = BOTTOM_LIMIT
        if self.center_y < BOTTOM_LIMIT:
            self.center_y = TOP_LIMIT


class BulletSprite(arcade.Sprite):
    # спрайт бластера

    def update(self):
        super().update()
        self.angle = math.degrees(math.atan2(self.change_y, self.change_x))
        if self.center_x < -100 or self.center_x > 1500 or self.center_y > 1100 or self.center_y < -100:
            self.kill()


class CarSprite(arcade.Sprite):
    # Спрайт машины горожан

    def __init__(self, image_file_name, scale):
        super().__init__(image_file_name, scale=scale)
        self.max_life = 4


class MyGame(arcade.Window):
    # Главный класс игры

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "School project")

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.frame_count = 0

        self.game_over = False

        # Список всех спрайтов
        self.all_sprites_list = None
        self.ufo_list = None
        self.bullet_list = None
        self.enemy_bullet_list = None
        self.tank_life_list = None
        self.car_list = None

        # Очки игрока
        self.score = 0
        self.player_sprite = None
        self.lives = 3

        self.shape_list = None

        arcade.set_background_color(arcade.color.DARK_GREEN)

    def start_new_game(self):
        # старт новой игры

        self.frame_count = 0
        self.game_over = False

        self.all_sprites_list = arcade.SpriteList()
        self.ufo_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()
        self.tank_life_list = arcade.SpriteList()
        self.car_list = arcade.SpriteList()

        # растановка домиков в случайном порядке
        for i in range(HOUSE_COUNT):
            house_sprite = arcade.Sprite("images/house.png")
            house_sprite.center_x = random.randrange((SCREEN_WIDTH // HOUSE_COUNT) * i + 60
                                                     , (SCREEN_WIDTH // HOUSE_COUNT) * (i + 1) - 60)
            house_sprite.center_y = random.randrange(160, SCREEN_HEIGHT - 280)
            self.all_sprites_list.append(house_sprite)

        # растановка ёлочек в случайном порядке
        for i in range(PAIN_COUNT):
            pain_sprite = arcade.Sprite("images/pine.png")
            pain_sprite.center_x = random.randrange((SCREEN_WIDTH // PAIN_COUNT) * i + 30
                                                    , (SCREEN_WIDTH // HOUSE_COUNT) * (i + 1) - 30)
            pain_sprite.center_y = random.randrange(120, SCREEN_HEIGHT - 300)
            self.all_sprites_list.append(pain_sprite)

        # растановка машинок в случайном порядке
        for i in range(CAR_COUNT):
            car_sprite = CarSprite("images/auto_00.png", SCALE)
            car_sprite.center_x = random.randrange((SCREEN_WIDTH // CAR_COUNT) * i + 120
                                                   , (SCREEN_WIDTH // CAR_COUNT) * (i + 1) - 120)
            car_sprite.center_y = random.randrange(65, SCREEN_HEIGHT - 265)
            self.all_sprites_list.append(car_sprite)
            self.car_list.append(car_sprite)

        # ставим танк игрока
        self.score = 0
        self.player_sprite = TankSprite("images/tank.png", SCALE)
        self.all_sprites_list.append(self.player_sprite)
        self.lives = 3

        # иконки жизней игрока
        cur_pos = 10
        for i in range(self.lives):
            life = arcade.Sprite("images/tank_mini.png", SCALE)
            life.center_x = cur_pos + life.width
            life.center_y = life.height
            cur_pos += life.width
            self.all_sprites_list.append(life)
            self.tank_life_list.append(life)

        # создание вражеских тарелок
        for i in range(STARTING_UFO_COUNT):
            enemy_sprite = UfoSprite("images/ufo.png", SCALE)
            enemy_sprite.guid = "Ufo"

            enemy_sprite.center_y = TOP_LIMIT
            enemy_sprite.center_x = random.randrange(LEFT_LIMIT, RIGHT_LIMIT)

            enemy_sprite.change_x = random.random() * 2 - 1
            enemy_sprite.change_y = - random.randrange(1, 4)

            self.all_sprites_list.append(enemy_sprite)
            self.ufo_list.append(enemy_sprite)

    def on_draw(self):
        # отрисовка экрана

        arcade.start_render()

        # отрисовка всех спрайтов
        self.all_sprites_list.draw()

        # написаьт очки игрока на экране
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 70, arcade.color.WHITE, 13)

        output = f"Ufo Count: {len(self.ufo_list)}"
        arcade.draw_text(output, 10, 50, arcade.color.WHITE, 13)

    def on_key_press(self, symbol, modifiers):
        # обработчики нажатий клавиш

        # Игрок нажал на пробел - выстрелд из танка
        if not self.player_sprite.respawning and symbol == arcade.key.SPACE:
            bullet_sprite = BulletSprite("images/laserBlue01.png", SCALE)
            bullet_sprite.guid = "Bullet"

            bullet_speed = 13
            bullet_sprite.change_y = math.cos(math.radians(self.player_sprite.angle)) * bullet_speed
            bullet_sprite.change_x = -math.sin(math.radians(self.player_sprite.angle)) * bullet_speed

            bullet_sprite.center_x = self.player_sprite.center_x
            bullet_sprite.center_y = self.player_sprite.center_y
            bullet_sprite.update()

            self.all_sprites_list.append(bullet_sprite)
            self.bullet_list.append(bullet_sprite)

        # Игрок нажал влево
        if symbol == arcade.key.LEFT:
            self.player_sprite.change_x -= 2
        # игрок нажал вправо
        elif symbol == arcade.key.RIGHT:
            self.player_sprite.change_x = 2

    def on_key_release(self, symbol, modifiers):
        # игрок отжал клавишу влево или вправо - танк остановился
        if symbol == arcade.key.LEFT:
            self.player_sprite.change_x = 0
        elif symbol == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def update(self, x):
        # движение всех объектов игры
        self.frame_count += 1

        if self.frame_count % 20 == 0:
            for ufo in self.ufo_list:
                bullet_sprite = BulletSprite("images/laserBlue01.png", SCALE)
                bullet_sprite.guid = "Bullet UFO"

                bullet_speed = 8
                bullet_sprite.change_y = -math.sin(math.radians(random.randrange(45, 135))) * bullet_speed
                bullet_sprite.change_x = math.cos(math.radians(random.randrange(45, 135))) * bullet_speed

                bullet_sprite.center_x = ufo.center_x
                bullet_sprite.center_y = ufo.center_y
                bullet_sprite.update()

                self.all_sprites_list.append(bullet_sprite)
                self.enemy_bullet_list.append(bullet_sprite)

        if not self.game_over:
            self.all_sprites_list.update()

            for bullet in self.bullet_list:
                self.ufo_list.use_spatial_hash = False
                ufos_plain = arcade.check_for_collision_with_list(bullet, self.ufo_list)
                self.ufo_list.use_spatial_hash = True
                ufos_spatial = arcade.check_for_collision_with_list(bullet, self.ufo_list)
                if len(ufos_plain) != len(ufos_spatial):
                    print("ERROR")

                ufos = ufos_spatial

                for ufo in ufos:
                    ufo.kill()
                    bullet.kill()

            for bullet in self.enemy_bullet_list:
                player_shoot = arcade.check_for_collision(bullet, self.player_sprite)
                if player_shoot:
                    bullet.kill()
                    if self.lives > 0:
                        self.lives -= 1
                        self.player_sprite.respawn()
                        self.tank_life_list.pop().kill()
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
                ufos = arcade.check_for_collision_with_list(self.player_sprite, self.ufo_list)
                if len(ufos) > 0:
                    if self.lives > 0:
                        self.lives -= 1
                        self.player_sprite.respawn()
                        ufos[0].kill()
                        self.tank_life_list.pop().kill()
                        print("Crash")
                    else:
                        self.game_over = True
                        print("Game over")
