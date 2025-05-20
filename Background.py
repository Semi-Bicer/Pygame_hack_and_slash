import pygame
import random
import math
import constants

class SamuraiBackground:
    def __init__(self, width=1920, height=1080):
        self.width = width
        self.height = height

        # Renk paleti - Sakura vadisi için
        self.sky_colors = constants.SKY_GRADIENT  # Pastel günbatımı gradienti
        self.ground_color = (45, 85, 45)  # Eski yeşil zemin rengi
        self.tree_trunk = constants.TREE_BROWN  # Ağaç gövdesi
        self.leaves = constants.SAKURA_COLORS  # Sakura yaprak renkleri

        # Hareketli elementler
        self.petals = []  # Sakura yaprakları
        self.fallen_petals = []  # Yere düşmüş çiçekler
        self.mist = []  # Hafif sis efekti
        self.clouds = []  # Bulutlar
        self.mountains = []  # Dağ siluetleri
        self.grass = []  # Rüzgarda hareket eden çimenler

        # Elementleri oluştur
        self._create_petals(300)  # Daha az uçuşan yaprak
        self._create_fallen_petals(300)  # Yere düşmüş çiçekler
        self._create_mist(20)  # Hafif sis efekti
        self._create_clouds(8)  # Daha fazla bulut
        self._create_mountains()  # Dağ siluetleri
        self._create_grass(200)  # Çimenler
        self._create_trees(0)  # Parametre artık kullanılmıyor, içeride rastgele sayıda ağaç oluşuyor

        # Gradient yüzeyi
        self.sky_surface = pygame.Surface((width, height // 2))
        self._create_sky_gradient()

    def _create_sky_gradient(self):
        """Pastel gün batımı gökyüzü gradienti oluşturur"""
        height = self.sky_surface.get_height()

        # Üç bölgeli gradient - üst (mor-pembe), orta (pembe-turuncu), alt (turuncu-sarı)
        for y in range(height):
            # Yükseklik oranına göre renk karışımı
            ratio = y / height

            if ratio < 0.5:  # Üst yarı - mor-pembe'den pembe-turuncu'ya
                sub_ratio = ratio * 2  # 0-0.5 aralığını 0-1'e normalize et
                color = (
                    int(self.sky_colors[0][0] + (self.sky_colors[1][0] - self.sky_colors[0][0]) * sub_ratio),
                    int(self.sky_colors[0][1] + (self.sky_colors[1][1] - self.sky_colors[0][1]) * sub_ratio),
                    int(self.sky_colors[0][2] + (self.sky_colors[1][2] - self.sky_colors[0][2]) * sub_ratio)
                )
            else:  # Alt yarı - pembe-turuncu'dan turuncu-sarı'ya
                sub_ratio = (ratio - 0.5) * 2  # 0.5-1 aralığını 0-1'e normalize et
                color = (
                    int(self.sky_colors[1][0] + (self.sky_colors[2][0] - self.sky_colors[1][0]) * sub_ratio),
                    int(self.sky_colors[1][1] + (self.sky_colors[2][1] - self.sky_colors[1][1]) * sub_ratio),
                    int(self.sky_colors[1][2] + (self.sky_colors[2][2] - self.sky_colors[1][2]) * sub_ratio)
                )

            # Yatay çizgi çiz
            pygame.draw.line(self.sky_surface, color, (0, y), (self.width, y))

        # Güneş efekti - daha büyük ve yumuşak
        sun_x = int(self.width * 0.75)  # Güneş biraz sağda
        sun_y = int(height * 0.4)  # Güneş biraz aşağıda

        # Güneş ışık halesi - daha büyük ve yumuşak
        for radius in range(120, 60, -10):
            alpha = 255 - (radius - 60) * 5  # Dışa doğru azalan opasite
            if alpha < 0: alpha = 0
            if alpha > 255: alpha = 255

            # Yarı saydam halka
            s = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*constants.SUNSET_YELLOW, alpha), (radius, radius), radius)
            self.sky_surface.blit(s, (sun_x - radius, sun_y - radius))

        # Güneş
        pygame.draw.circle(self.sky_surface, constants.SUN_YELLOW, (sun_x, sun_y), 60)

        # Hafif sis efekti - tüm gökyüzüne
        mist_surface = pygame.Surface((self.width, height), pygame.SRCALPHA)
        for _ in range(15):
            mist_x = random.randint(0, self.width)
            mist_y = random.randint(0, height)
            mist_width = random.randint(200, 500)
            mist_height = random.randint(50, 150)
            mist_color = random.choice(constants.MIST_COLORS)

            # Yarı saydam sis yüzeyi
            pygame.draw.ellipse(mist_surface, mist_color,
                              (mist_x, mist_y, mist_width, mist_height))

        # Sisi gökyüzüne ekle
        self.sky_surface.blit(mist_surface, (0, 0))

    def _create_mountains(self):
        """Arka planda dağ siluetleri oluşturur"""
        # Üç katmanlı dağ silueti
        for layer in range(3):
            # Her katman için farklı yükseklik ve renk
            height_factor = 0.15 - layer * 0.03  # Uzaktaki dağlar daha alçak
            mountain_height = int(self.height * height_factor)
            mountain_color = constants.MOUNTAIN_COLORS[layer]

            # Dağ noktaları
            points = []
            points.append((0, self.height // 2))  # Sol alt köşe

            # Dağ tepeleri
            segments = 10 + layer * 5  # Uzaktaki dağlar daha detaylı
            for i in range(segments):
                x = int(self.width * i / segments)
                # Rastgele yükseklik - orta kısımda daha yüksek
                height_variation = abs((i / segments) - 0.5) * 2  # 0-1 arası
                y = int(self.height // 2 - mountain_height * (1 - height_variation * 0.7))
                points.append((x, y))

            points.append((self.width, self.height // 2))  # Sağ alt köşe

            # Dağ siluetini kaydet
            self.mountains.append({
                'points': points,
                'color': mountain_color
            })

    def _create_fallen_petals(self, count):
        """Yere düşmüş sakura çiçekleri oluşturur"""
        ground_y = self.height // 2  # Zemin seviyesi

        for _ in range(count):
            self.fallen_petals.append({
                'x': random.randint(0, self.width),
                'y': random.randint(ground_y, self.height),
                'size': random.randint(2, 6),
                'color': random.choice(constants.SAKURA_COLORS),
                'rotation': random.uniform(0, 6.28)
            })

    def _create_mist(self, count):
        """Hafif sis efekti oluşturur"""
        for _ in range(count):
            self.mist.append({
                'x': random.randint(0, self.width),
                'y': random.randint(self.height // 4, self.height // 2),
                'width': random.randint(200, 600),
                'height': random.randint(50, 150),
                'color': random.choice(constants.MIST_COLORS),
                'speed': random.uniform(0.1, 0.3)
            })

    def _create_petals(self, count):
        for _ in range(count):
            self.petals.append({
                'x': random.randint(0, self.width),
                'y': random.randint(-100, self.height),  # Daha yüksekten başla
                'speed': random.uniform(0.3, 2.0),  # Biraz daha hızlı
                'size': random.randint(2, 5),  # Biraz daha büyük yapraklar
                'angle': random.uniform(0, 6.28),
                'rot_speed': random.uniform(-0.08, 0.08),  # Daha hızlı dönüş
                'color': random.choice(constants.SAKURA_COLORS)  # Sakura renkleri
            })

    def _create_grass(self, count):
        # Çok daha fazla çimen ekle - tüm oynanabilir alan boyunca
        for _ in range(count * 10):  # Çimen sayısını 10 kat artır
            # Rastgele y pozisyonu - TÜM yeşillik alanı boyunca (sadece üst kısım değil)
            y_pos = random.randint(self.height // 2, self.height - 20)  # Zemin seviyesinden ekranın altına kadar

            self.grass.append({
                'x': random.randint(0, self.width),
                'y': y_pos,  # Rastgele y pozisyonu
                'height': random.randint(3, 10),  # Daha kısa çimenler
                'width': random.randint(1, 3),
                'sway': random.uniform(0, 6.28),
                'sway_speed': random.uniform(0.02, 0.1),
                # Daha açık yeşil tonlar
                'color': (random.randint(25, 40), random.randint(70, 90), random.randint(25, 40))
            })

    def _create_clouds(self, count):
        for _ in range(count):
            self.clouds.append({
                'x': random.randint(0, self.width),
                'y': random.randint(50, 200),
                'speed': random.uniform(0.1, 0.3),
                'size': random.randint(30, 80)
            })

    def _create_trees(self, count):
        self.trees = []
        # Daha fazla ağaç oluştur - sakura vadisi için
        tree_count = random.randint(7, 9)  # 7-9 arası rastgele sayıda ağaç

        # Ağaçları eşit aralıklarla yerleştir, ama hafif rastgelelik ekle
        spacing = self.width / (tree_count + 1)  # Eşit aralıklar

        for i in range(tree_count):
            # Temel pozisyon (eşit aralıklı)
            base_x = spacing * (i + 1)

            # Hafif rastgele sapma ekle (benzer ama tam aynı olmayan mesafeler için)
            random_offset = random.randint(-int(spacing * 0.15), int(spacing * 0.15))
            tree_x = int(base_x + random_offset)

            # Orta bölgeyi boş bırak (oyun alanı için)
            if tree_x > self.width * 0.4 and tree_x < self.width * 0.6:
                # Orta bölgedeyse, kenarlara doğru it
                if tree_x < self.width / 2:
                    tree_x = int(self.width * 0.35)  # Sol tarafa it
                else:
                    tree_x = int(self.width * 0.65)  # Sağ tarafa it

            # Ağaç boyutlarını rastgele belirle - daha uzun sakura ağaçları
            trunk_height = random.randint(250, 400)  # Daha uzun gövdeler
            canopy_size = random.randint(120, 200)   # Daha büyük taçlar

            # Sakura renkleri kullan
            self.trees.append({
                'x': tree_x,
                'trunk_height': trunk_height,
                'canopy_size': canopy_size,
                'leaves_color': random.choice(constants.SAKURA_COLORS),  # Sakura renkleri
                'trunk_bend': random.randint(-20, 20),  # Gövde eğikliği
                'texture_seed': random.randint(0, 1000),  # Doku için rastgele tohum
                'branch_count': random.randint(6, 10)  # Daha fazla dal
            })

    def update(self):
        # Yapraklar
        for petal in self.petals:
            petal['y'] += petal['speed']
            petal['x'] += math.sin(petal['angle']) * 0.5
            petal['angle'] += petal['rot_speed']

            if petal['y'] > self.height:
                petal['y'] = random.randint(-50, -10)
                petal['x'] = random.randint(0, self.width)

        # Yere düşmüş çiçekler - hafif hareket
        for petal in self.fallen_petals:
            # Hafif rastgele hareket
            if random.random() < 0.01:  # %1 olasılıkla
                petal['x'] += random.uniform(-0.5, 0.5)
                petal['rotation'] += random.uniform(-0.1, 0.1)

        # Çimenler
        for blade in self.grass:
            blade['sway'] += blade['sway_speed']

        # Sis - yavaş hareket
        for mist in self.mist:
            mist['x'] += mist['speed']
            if mist['x'] > self.width + mist['width']:
                mist['x'] = -mist['width']

        # Bulutlar
        for cloud in self.clouds:
            cloud['x'] += cloud['speed']
            if cloud['x'] > self.width + cloud['size']:
                cloud['x'] = -cloud['size']



    def draw(self, surface):
        # Gökyüzü
        surface.blit(self.sky_surface, (0, 0))

        # Dramatik güneş - kırmızı gün batımı güneşi
        sun_x = int(self.width * 0.8)
        sun_y = int(self.height * 0.2)

        # Güneş ışık halesi
        for radius in range(60, 40, -5):
            alpha = 255 - (radius - 40) * 10  # Dışa doğru azalan opasite
            if alpha < 0: alpha = 0
            if alpha > 255: alpha = 255

            # Yarı saydam halka
            s = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*self.sky_colors[2], alpha), (radius, radius), radius)
            surface.blit(s, (sun_x - radius, sun_y - radius))

        # Güneş
        pygame.draw.circle(surface, (255, 100, 50), (sun_x, sun_y), 40)

        # Atmosferik bulutlar
        for cloud in self.clouds:
            # Yarı saydam bulut yüzeyi
            cloud_surface = pygame.Surface((cloud['size'] * 3, cloud['size'] * 1.5), pygame.SRCALPHA)

            # Bulut rengi - hafif gri-mavi
            cloud_color = (220, 220, 230, 120)  # Yarı saydam

            # Daha doğal bulut şekli
            pygame.draw.ellipse(cloud_surface, cloud_color,
                               (0, 0, cloud['size'] * 3, cloud['size'] * 1.5))

            # Bulutun üst kısmına daha küçük yuvarlaklar ekle
            pygame.draw.ellipse(cloud_surface, cloud_color,
                               (cloud['size'] * 0.5, 0, cloud['size'] * 1.5, cloud['size']))

            pygame.draw.ellipse(cloud_surface, cloud_color,
                               (cloud['size'] * 1.2, 0, cloud['size'] * 1.5, cloud['size'] * 0.8))

            # Bulut gölgelendirme
            pygame.draw.ellipse(cloud_surface, (200, 200, 210, 150),
                               (cloud['size'] * 0.8, cloud['size'] * 0.3, cloud['size'] * 1.5, cloud['size'] * 0.7))

            surface.blit(cloud_surface, (int(cloud['x']), cloud['y']))

        # Dağ siluetleri
        for mountain in self.mountains:
            pygame.draw.polygon(surface, mountain['color'], mountain['points'])

        # Zemin - daha doğal ama sabit üst kısım ile
        ground_color = (45, 85, 45)  # Açık yeşil zemin rengi

        # Zemin polygon'unu çiz - önceden hesaplanmış sabit noktalar
        if not hasattr(self, 'ground_points'):
            # İlk çağrıda noktaları hesapla ve sakla
            self.ground_points = []
            ground_y = self.height // 2

            # Sol alt köşe - daha yukarıda
            self.ground_points.append((0, ground_y - 15))  # 15 piksel yukarı

            # Üst kısım için dalgalı noktalar - sabit seed ile
            random.seed(42)  # Sabit seed - her zaman aynı rastgele sayılar
            segment_count = 20
            for i in range(segment_count + 1):
                x = self.width * i / segment_count
                # Dalgalı üst kısım - sabit pattern, daha yukarıda
                height_variation = math.sin(i * 0.5) * 6 + random.randint(-2, 2)  # Daha az dalgalanma
                y = ground_y - 15 + height_variation  # 15 piksel yukarı
                self.ground_points.append((x, y))

            # Sağ alt ve sol alt köşeler
            self.ground_points.append((self.width, self.height))
            self.ground_points.append((0, self.height))

            # Seed'i sıfırla
            random.seed()

        # Sabit polygon'u çiz
        pygame.draw.polygon(surface, ground_color, self.ground_points)

        # Yere düşmüş çiçekler - daha az belirgin
        for petal in self.fallen_petals:
            # Yere düşmüş çiçek yüzeyi - daha saydam
            s = pygame.Surface((petal['size'] * 2, petal['size'] * 2), pygame.SRCALPHA)

            # Çiçek şekli - 5 yapraklı çiçek
            center_x, center_y = petal['size'], petal['size']
            radius = petal['size']

            # Oval yaprak çiz - daha saydam
            pygame.draw.ellipse(s, (*petal['color'], 100),  # Daha saydam (180 -> 100)
                              (center_x - radius/2, center_y - radius/2, radius, radius))

            # Döndür ve ekrana çiz
            rotated = pygame.transform.rotate(s, petal['rotation'] * 57.29)
            surface.blit(rotated, (petal['x'], petal['y']))

        # Çimenler - TÜM yeşillik alanı boyunca sallanan çimenler
        for blade in self.grass:
            sway_offset = math.sin(blade['sway']) * 5
            # Kendi rengi ve kendi y pozisyonu ile çiz
            pygame.draw.line(surface, blade['color'],
                             (blade['x'], blade['y']),  # Çimenin tabanı
                             (blade['x'] + sway_offset, blade['y'] - blade['height']),  # Çimenin ucu
                             blade['width'])

        # Uzun sakura ağaçları
        for tree in self.trees:
            # Ağaç gövdesi - hafif eğik
            trunk_base_x = tree['x']
            trunk_top_x = tree['x'] + tree['trunk_bend']  # Hafif eğik gövde
            trunk_base_y = self.height // 2 - 5  # Ağaç kökleri çimen üstünde kalsın
            trunk_top_y = self.height // 2 - 5 - tree['trunk_height']
            trunk_width = 20  # İnce gövde

            # Gövde çiz - eğik dikdörtgen
            trunk_points = [
                (trunk_base_x - trunk_width//2, trunk_base_y),  # Sol alt
                (trunk_base_x + trunk_width//2, trunk_base_y),  # Sağ alt
                (trunk_top_x + trunk_width//3, trunk_top_y),    # Sağ üst
                (trunk_top_x - trunk_width//3, trunk_top_y)     # Sol üst
            ]
            pygame.draw.polygon(surface, self.tree_trunk, trunk_points)

            # Gövde detayları - ağaç kabuğu dokusu
            darker_trunk = (60, 35, 25)  # Daha açık kahverengi

            # Yatay çizgiler - ağaç kabuğu
            for i in range(5, tree['trunk_height'], 40):
                y_pos = trunk_top_y + i
                pygame.draw.line(surface, darker_trunk,
                               (trunk_base_x - trunk_width//2 + (trunk_top_x - trunk_base_x) * i / tree['trunk_height'], y_pos),
                               (trunk_base_x + trunk_width//2 + (trunk_top_x - trunk_base_x) * i / tree['trunk_height'], y_pos),
                               1)

            # Ağaç dalları - daha sabit ve düzenli
            branch_count = tree['branch_count']
            for i in range(branch_count):
                # Dal pozisyonu - gövde boyunca düzenli dağılım
                rel_y = 0.2 + 0.6 * i / (branch_count - 1)  # 0.2-0.8 arası dağılım
                rel_x = 0.3 if i % 2 == 0 else -0.3  # Sağ ve sol dallar

                # Dal başlangıç noktası
                branch_base_x = trunk_base_x + (trunk_top_x - trunk_base_x) * rel_y
                branch_base_y = trunk_top_y + rel_y * tree['trunk_height']

                # Dal uzunluğu ve açısı - daha sabit
                branch_length = trunk_width * 3
                branch_angle = math.pi/4 if rel_x > 0 else math.pi*3/4  # 45 veya 135 derece

                # Dal bitiş noktası
                branch_end_x = branch_base_x + math.cos(branch_angle) * branch_length
                branch_end_y = branch_base_y + math.sin(branch_angle) * branch_length

                # Dal çiz - daha kalın
                pygame.draw.line(surface, self.tree_trunk,
                               (branch_base_x, branch_base_y),
                               (branch_end_x, branch_end_y),
                               3)

            # Ağaç taçı - büyük sakura çiçekleri kümesi
            leaf_color = tree['leaves_color']
            canopy_x = trunk_top_x
            canopy_y = trunk_top_y
            canopy_size = tree['canopy_size']

            # Sakura ağacı taçı - daha sade ve daha kırmızı
            # Ana yaprak kümesi için yarı saydam yüzey
            leaf_surface = pygame.Surface((canopy_size*2.5, canopy_size*2.5), pygame.SRCALPHA)

            # Doku için rastgele tohum kullan
            random.seed(tree['texture_seed'])

            # Ana yaprak kümesi - daha kırmızı ve daha sade
            # Daha koyu kırmızı ana renk
            main_color = (255, 30, 60)  # Daha koyu kırmızı

            # Ana yaprak kümesi - büyük oval
            pygame.draw.ellipse(leaf_surface, (*main_color, 180),
                              (canopy_size*0.5, canopy_size*0.5, canopy_size*1.5, canopy_size*1.5))

            # Daha az sayıda yaprak kümesi oluştur
            for _ in range(40):  # Daha az yaprak kümesi
                # Rastgele konum - daha küçük bir alana yayılım
                angle = random.uniform(0, 6.28)
                distance = random.uniform(0, canopy_size * 0.9)
                x = canopy_size*1.25 + math.cos(angle) * distance
                y = canopy_size*1.25 + math.sin(angle) * distance

                # Daha küçük yapraklar
                size = random.randint(canopy_size//10, canopy_size//5)

                # Daha kırmızı tonlar
                r = 255
                g = random.randint(20, 50)
                b = random.randint(40, 70)
                color = (r, g, b, random.randint(150, 200))  # Daha kırmızı ve yarı saydam

                # Basit oval yapraklar
                pygame.draw.ellipse(leaf_surface, color,
                                  (x - size/2, y - size/2, size, size*1.2))

            # Yaprak kümesini ekrana ekle
            surface.blit(leaf_surface, (canopy_x - canopy_size*1.25, canopy_y - canopy_size*1.25))

            # Rastgele tohumu sıfırla
            random.seed()

        # Sakura yaprakları (en üst katman)
        for petal in self.petals:
            # Dönen yaprak efekti - sakura yaprağı şeklinde
            s = pygame.Surface((petal['size'] * 2, petal['size'] * 2), pygame.SRCALPHA)

            # Sakura yaprağı şekli - 5 yapraklı çiçek
            center_x, center_y = petal['size'], petal['size']
            radius = petal['size']

            # Yaprak rengi
            color = petal['color']

            # 5 yapraklı çiçek çiz
            for i in range(5):
                angle = i * (2 * math.pi / 5)
                x = center_x + math.cos(angle) * radius * 0.8
                y = center_y + math.sin(angle) * radius * 0.8

                # Oval yaprak çiz
                pygame.draw.ellipse(s, (*color, 200),  # %80 opacity
                                  (center_x - radius/2, center_y - radius/2, radius, radius))
                pygame.draw.ellipse(s, (*color, 180),  # %70 opacity
                                  (x - radius/2, y - radius/2, radius, radius))

            # Yaprağın ortasına küçük sarı merkez ekle
            pygame.draw.circle(s, (255, 255, 150, 220), (center_x, center_y), radius/5)

            # Döndür ve ekrana çiz
            rotated = pygame.transform.rotate(s, petal['angle'] * 57.29)  # Radyan->Derece
            surface.blit(rotated, (petal['x'], petal['y']))