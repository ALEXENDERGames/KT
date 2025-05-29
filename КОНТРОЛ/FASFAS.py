import arcade
import random

SCREEN_W = 800
SCREEN_H = 600
WORLD_W = 1250
WORLD_H = 600

PLAYER_SCALE = 0.15
TILE_SCALE = 0.5
COIN_SCALE = 0.1
COIN_TOTAL = 10
MOVE_SPEED = 5
JUMP_POWER = 20
GRAVITY_FORCE = 1


class GameCharacter(arcade.Sprite):
    def __init__(self):
        super().__init__(
            r"C:\Users\Overlord\Desktop\КОНТРОЛ\Андрей.png",
            PLAYER_SCALE,
        )
        self.x = 64
        self.y = 128
        self.dx = 0
        self.dy = 0
        self.coins = 0

    def update_position(self):
        self.x += self.dx
        self.y += self.dy
        self.dy -= GRAVITY_FORCE

        if self.y < 64:
            self.y = 64


class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_W, SCREEN_H, "Приключения Андрея")
        self.game_scene = None
        self.player = None
        self.physics = None
        self.view_camera = None
        self.ui_camera = None
        self.coins_group = None
        self.game_background = None

    def initialize_game(self):
        self.game_background = arcade.load_texture(r"C:\Users\Overlord\Desktop\КОНТРОЛ\background.png")

        self.view_camera = arcade.Camera(self.width, self.height)
        self.ui_camera = arcade.Camera(self.width, self.height)

        self.game_scene = arcade.Scene()
        self.game_scene.add_sprite_list("MainCharacter")
        self.game_scene.add_sprite_list("Environment", use_spatial_hash=True)
        self.coins_group = arcade.SpriteList()

        self.player = GameCharacter()
        self.game_scene.add_sprite("MainCharacter", self.player)

        for ground_x in range(0, WORLD_W, 64):
            ground_tile = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALE)
            ground_tile.position = (ground_x, 32)
            self.game_scene.add_sprite("Environment", ground_tile)

        platform_positions = [
            (512, 96), (256, 96), (768, 96),
            (400, 200), (600, 300), (200, 400),
            (700, 400), (300, 250), (500, 350), (900, 200)
        ]

        for pos in platform_positions:
            platform = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", TILE_SCALE)
            platform.position = pos
            self.game_scene.add_sprite("Environment", platform)

        for _ in range(COIN_TOTAL):
            coin = arcade.Sprite(
                r"C:\Users\Overlord\Desktop\КОНТРОЛ\free-icon-dollar-1490853.png",
                COIN_SCALE
            )

            coin.x = random.randint(100, WORLD_W - 100)
            coin.y = random.randint(150, WORLD_H - 50)

            while arcade.check_for_collision_with_list(coin, self.game_scene["Environment"]):
                coin.x = random.randint(100, WORLD_W - 100)
                coin.y = random.randint(150, WORLD_H - 50)

            self.coins_group.append(coin)

        self.physics = arcade.PhysicsEnginePlatformer(
            self.player,
            gravity_constant=GRAVITY_FORCE,
            walls=self.game_scene["Environment"]
        )

    def draw_frame(self):
        self.clear()

        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            self.width, self.height,
                                            self.game_background)

        self.view_camera.use()
        self.game_scene.draw()
        self.coins_group.draw()

        self.ui_camera.use()
        arcade.draw_text(f"Монеты: {self.player.coins}",
                         20, self.height - 40,
                         arcade.color.GOLD, 24, bold=True)

    def process_key_press(self, key, modifiers):
        if key in (arcade.key.UP, arcade.key.W):
            if self.physics.can_jump():
                self.player.dy = JUMP_POWER
        elif key in (arcade.key.LEFT, arcade.key.A):
            self.player.dx = -MOVE_SPEED
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.player.dx = MOVE_SPEED

    def process_key_release(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.A, arcade.key.RIGHT, arcade.key.D):
            self.player.dx = 0

    def update_game_state(self, delta_time):
        self.physics.update()
        self.player.update_position()

        collected_coins = arcade.check_for_collision_with_list(self.player, self.coins_group)
        for coin in collected_coins:
            coin.kill()
            self.player.coins += 1

        target_x = self.player.x - self.width / 2
        target_y = self.player.y - self.height / 2

        if target_x < 0: target_x = 0
        if target_y < 0: target_y = 0
        if target_x > WORLD_W - self.width: target_x = WORLD_W - self.width
        if target_y > WORLD_H - self.height: target_y = WORLD_H - self.height

        self.view_camera.move_to((target_x, target_y))


if __name__ == "__main__":
    game_app = GameWindow()
    game_app.initialize_game()
    arcade.run()