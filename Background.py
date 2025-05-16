import pygame
import random
import math
import constants

class SamuraiBackground:
    def __init__(self, width=1920, height=1080):
        self.width = width
        self.height = height

        # Renk paleti
        self.sky_colors = constants.SKY_GRADIENT  # Günbatımı gradienti
        self.ground_color = constants.GROUND_GREEN  # Çimen yeşili
        self.tree_trunk = constants.TREE_BROWN  # Ağaç gövdesi
        self.leaves = [
            (214, 40, 40),  # Kırmızı
            (247, 127, 0),  # Turuncu
            (255, 201, 14)  # Sarı
        ]

        # Hareketli elementler
        self.petals = []  # Sakura yaprakları
        self.grass = []  # Rüzgarda hareket eden çimenler
        self.clouds = []  # Bulutlar

        # Elementleri oluştur
        self._create_petals(150)
        self._create_grass(200)
        self._create_clouds(5)
        self._create_trees(3)

        # Gradient yüzeyi
        self.sky_surface = pygame.Surface((width, height // 2))
        self._create_sky_gradient()

    def _create_sky_gradient(self):
        """Günbatımı gradienti oluşturur"""
        for y in range(self.sky_surface.get_height()):
            # Yükseklik oranına göre renk karışımı
            ratio = y / self.sky_surface.get_height()
            color = (
                int(self.sky_colors[0][0] + (self.sky_colors[1][0] - self.sky_colors[0][0]) * ratio),
                int(self.sky_colors[0][1] + (self.sky_colors[1][1] - self.sky_colors[0][1]) * ratio),
                int(self.sky_colors[0][2] + (self.sky_colors[1][2] - self.sky_colors[0][2]) * ratio)
            )
            pygame.draw.line(self.sky_surface, color, (0, y), (self.width, y))

    def _create_petals(self, count):
        """Uçuşan sakura yaprakları"""
        for _ in range(count):
            self.petals.append({
                'x': random.randint(0, self.width),
                'y': random.randint(-50, self.height),
                'speed': random.uniform(0.2, 1.5),
                'size': random.randint(2, 4),
                'angle': random.uniform(0, 6.28),
                'rot_speed': random.uniform(-0.05, 0.05)
            })

    def _create_grass(self, count):
        """Rüzgarda dalgalanan çimenler"""
        for _ in range(count):
            self.grass.append({
                'x': random.randint(0, self.width),
                'height': random.randint(5, 15),
                'width': random.randint(1, 3),
                'sway': random.uniform(0, 6.28),
                'sway_speed': random.uniform(0.02, 0.1)
            })

    def _create_clouds(self, count):
        """Yavaş hareket eden bulutlar"""
        for _ in range(count):
            self.clouds.append({
                'x': random.randint(0, self.width),
                'y': random.randint(50, 200),
                'speed': random.uniform(0.1, 0.3),
                'size': random.randint(30, 80)
            })

    def _create_trees(self, count):
        """Pixel art ağaçlar"""
        self.trees = []
        for _ in range(count):
            tree_x = random.randint(100, self.width - 100)
            self.trees.append({
                'x': tree_x,
                'trunk_height': random.randint(150, 250),
                'canopy_size': random.randint(80, 120),
                'leaves_color': random.choice(self.leaves)
            })

    def update(self):
        """Tüm hareketli elementleri günceller"""
        # Yapraklar
        for petal in self.petals:
            petal['y'] += petal['speed']
            petal['x'] += math.sin(petal['angle']) * 0.5
            petal['angle'] += petal['rot_speed']

            if petal['y'] > self.height:
                petal['y'] = random.randint(-50, -10)
                petal['x'] = random.randint(0, self.width)

        # Çimenler
        for blade in self.grass:
            blade['sway'] += blade['sway_speed']

        # Bulutlar
        for cloud in self.clouds:
            cloud['x'] += cloud['speed']
            if cloud['x'] > self.width + cloud['size']:
                cloud['x'] = -cloud['size']

    def draw(self, surface):
        """Tüm arkaplanı çizer"""
        # Gökyüzü
        surface.blit(self.sky_surface, (0, 0))

        # Güneş
        pygame.draw.circle(surface, self.sky_colors[2],
                           (int(self.width * 0.8), int(self.height * 0.2)), 40)

        # Bulutlar
        for cloud in self.clouds:
            pygame.draw.circle(surface, (255, 255, 255, 100),
                               (int(cloud['x']), cloud['y']), cloud['size'])

        # Zemin
        pygame.draw.rect(surface, self.ground_color,
                         (0, self.height // 2, self.width, self.height // 2))

        # Çimenler
        for blade in self.grass:
            sway_offset = math.sin(blade['sway']) * 5
            pygame.draw.line(surface, (blade['height'] / 20 + 50, 100, 30),
                             (blade['x'], self.height // 2),
                             (blade['x'] + sway_offset, self.height // 2 - blade['height']),
                             blade['width'])

        # Ağaçlar
        for tree in self.trees:
            # Gövde
            pygame.draw.rect(surface, self.tree_trunk,
                             (tree['x'] - 10, self.height // 2 - tree['trunk_height'],
                              20, tree['trunk_height']))

            # Taç
            pygame.draw.circle(surface, tree['leaves_color'],
                               (tree['x'], self.height // 2 - tree['trunk_height']),
                               tree['canopy_size'])

        # Yapraklar (en üst katman)
        for petal in self.petals:
            # Dönen yaprak efekti
            s = pygame.Surface((petal['size'] * 2, petal['size'] * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*self.leaves[0], 150),  # %60 opacity
                               (petal['size'], petal['size']), petal['size'])
            rotated = pygame.transform.rotate(s, petal['angle'] * 57.29)  # Radyan->Derece
            surface.blit(rotated, (petal['x'], petal['y']))