from main import *


class GameObject:
    """Oyun objesi."""
    # parametre olarak height = ekranın yüksekliği, width ekranın genisliği, oyunun çalıştırılabilir olması (keepgoing), hangi levelden baslanılcağı, oyunun bitip bitmeyeceği ve Fps degerleri alınır
    def __init__(self, height=720, width=1080, keepgoing=True, level=1, game_over=False, FPS=120):
        # oyun init fonksiyonu cağırılarak pygamenin oyunu oluşturması sağlanır
        pygame.init()
        # beyaz rengin rgb olarak tanımlanması
        self.white = (255, 255, 255)
        # oyun ekran arayüzünün çağırılması
        pygame.mixer.init()
        # parametre değerlerinin sınıf objesi olarak girilmesi
        self.currentLevel = level
        self.fps = FPS
        self.width = width
        self.height = height
        self.keepgoing = keepgoing
        self.game_over = game_over
        # oyun başlarken atanacak ilk değerler fonksiyonlar halinde birbirinden ayırılarak guruplanmıştır
        # init screen ekran ayarlamalarını yapar
        self.initScreen()
        # arkaplanı doldurarak kullanılabilir hale getirir
        self.fillBackground()
        # oyunnun ekranının cizdirilmeye hazır hale getirilmesini sağlar (render)
        self.blit()
        # canların ilk değerlerinin atanması
        self.lives = [Lives(1), Lives(2), Lives(3)]
        # oyunda kullanılan spritelerin yani (image dosyalarının ) yüklenmesi ve gerekli olan yerlere atılması
        self.initSprites()
        # oyunda kullanılacak olan verlilerin yani harita ve highscore değerlerinin dosyalardan yüklenmesi
        self.load_data()
        # oyunun update fonksiyonu çağırılarak oyun başlatılır 
        self.update()


    def update(self):
        """Update fonksiyonu her frame de çağrılır."""
    # eğer geminin canı varsa bu döngü devam eder
        while self.spaceship.lives >= 0:
            # geminin canı bittiğinde döngü sona erer
            if self.spaceship.lives == 0:
                self.game_over = True
            # oyun içerisinde olan tüm mantık bu fonksiyondadır
            self.keepGoing()
            # colliderler yani her nesne grubunun baska bir nesne grubuna vereceği tepkiler burada ayarlanır
            # örneğin bir füze düşmanı yok eder
            # ve ya benzin deposu geminin benzinini artırır gibi
            self.colliders()
            # oyun icerisindeki tüm sprite objelerinin güncellenmesi (konum güncellemesi)
            self.spriteUpdate()
            # oyun ekranının temizlenmesi 
            self.clear()
            # oyun ekranına güncellenen resimlerin çizdirilmesi
            self.draw()
            # levelin bitip bitmediğini anlayabilmemiz için çağırılan fonksiyon
            self.isThisTheEnd()
            pygame.display.flip()

    def isThisTheEnd(self):
        """Oyun sonu"""
        # eğer oyunun sonu geldi ise bir sonraki levelin acılması örneğin level1 den level2 ye geçiş
        # eğer son level geçildiyse oyun biter.
        if self.theEndGame.end():
            try:
                self.level()
            except Exception as ex:
                pygame.quit()

    def level(self):
        """her bir level için  "-" karakteri mapteki taşları;
        "x" karakteri mapteki fuel, yani yakıt objelerini;
        "e" karakteri düşman füzeleri çağırır."""
        self.isWave1 = True
        self.wave_1()
        y = 0
        level1 = []
        world = []
        # level haritası dosyadan okunarak cizilen taslar yerine dizilir.
        level = open('levels/level' + str(self.currentLevel))
        for i in level:
            level1.append(i)
        for row in level1:
            x = 0
            for col in row:
                if col == "-":
                    self.stone = Stone()
                    world.append(self.stone)
                    self.stoneSprites.add(world)
                    self.stone.rect.x = x
                    self.stone.rect.y = y

                if col == "x":
                    self.fuel = Fuels()
                    self.fuelSprites.add(self.fuel)
                    self.fuel.rect.x = x
                    self.fuel.rect.y = y
                if col == "e":
                    self.enemy3 = Enemy3()
                    self.enemySprites.add(self.enemy3)
                    self.enemy3.rect.x = x
                    self.enemy3.rect.y = y

                if col == "]":
                    self.theEndGame = TheEndGame()
                    self.stoneSprites.add(self.theEndGame)
                    self.theEndGame.rect.x = x
                    self.theEndGame.rect.y = y
                x += 32
            y += +32
    # oyuncunun o anki benzin deposunun ekrana çizdirilmesi
    def draw_player_fuel(self, surf, x, y, pct):
        """Oyuncu karakterin yakıt seviyesi için görselleştirme."""
        if pct < 0:
            pct = 0
        BAR_LENGTH = 100
        BAR_HEIGHT = 20
        fill = pct * BAR_LENGTH
        outline_rect = pygame.Rect(x, y, BAR_LENGTH * 2, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        if pct > 0.6:
            col = (0, 255, 0)
        elif pct > 0.3:
            col = (255, 255, 0)
        else:
            col = (255, 0, 0)
        pygame.draw.rect(surf, col, fill_rect)
        pygame.draw.rect(surf, self.white, outline_rect, 2)
    # yüksek değerlerin dosyadan yüklenmesi
    def load_data(self, HS_FILE='HighScore'):
        """Oyuncu yüksek skor yaparsa bu skor kaydedilir."""
        # load high score
        self.dir = os.path.dirname(__file__)
        with open(os.path.join(self.dir, HS_FILE), 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

    def colliders(self):
        """ana karakterin, mermilerin, füzelerin ve düşmanların çarpışma ve patlama efektleri."""
        # bullet-fuel collider
        fuel_hit_by_bullet = pygame.sprite.groupcollide(self.fuelSprites, self.shootSprites, True, True)
        # eğer mermi benzin deposuna carparsa oyuncu benzin kazanır.
        for hit in fuel_hit_by_bullet:
            # eğer mermi tarafından patlatılırsa patlama efekti çalıştırılır 
            expl = Explosion(hit.rect.center, 'sm')
            self.explosionSprites.add(expl)
        # depo patlatıldığında oyuncu benzin kazanır 
        if fuel_hit_by_bullet:
            self.spaceship.fuel += 10

        # bullet-enemy collider
        # düşmana mermi değdiginde düşmanın ölmesi
        # grupcollide benzer nesne sınıflarını aynı alan altında toplayarak bu gruplara tanımladıgımız collıde değerlerini hepsi için geçerli kılar
        # örneğin düşman grubu mermi grubu ile çarpıştığında yok olur ve ya gemi her hangi bir düşman grubu ile çarpıştığında can kaybeder.
        bullethits = pygame.sprite.groupcollide(self.enemySprites, self.shootSprites, True, True)
        for hit in bullethits:
            expl = Explosion(hit.rect.center, 'sm')
            self.explosionSprites.add(expl)
        if bullethits:
            self.spaceship.score += 1

        # player-enemy collider
        # gemi ve düşman grupları arasında colliderlerin tanımlanması
        spaceshiphits = pygame.sprite.spritecollide(self.spaceship, self.enemySprites, True)
        for hit in spaceshiphits:
            expl = Explosion(hit.rect.center, 'sm')
            self.explosionSprites.add(expl)
        if spaceshiphits:
            self.spaceship.score -= 5
            self.spaceship.lives -= 1
            self.lives[-1].kill()
            del self.lives[-1]

        # spaceship-ground collider
        # gemi ve yer arasında ki colliderin tanımlanması 
        # bu collidere göre gemi her hangi bir yere çarparsa ölür 
        spaceshiphitsground = pygame.sprite.spritecollide(self.spaceship, self.stoneSprites, False)
        if spaceshiphitsground:
            self.spaceship.lives = 0

        # rocket-ground collider
        # roket ile yer arasında tanımlanan collider
        # eğer roket yere çarparsa patlar
        rockethitsground = pygame.sprite.groupcollide(self.shootSprites, self.stoneSprites, True, False)
        for hit in rockethitsground:
            expl = Explosion(hit.rect.center, 'sm')
            self.explosionSprites.add(expl)

    def initSprites(self):
        """Bütün spriteları(düşman,oyuncu,yakıt,roket,taş,patlama,can) aktifleştirir"""
        # Sprites
        self.space = Space()

        # sprite groups
        # sprite gruplarını oluşturulması
        # patlayıcılar
        self.explosionSprites = pygame.sprite.Group()
        # sistem görüntülerinin gruplanacağı alan
        self.systemSprites = pygame.sprite.Group(self.space)
        # canların gruplandığı alan 
        self.liveSprites = pygame.sprite.Group()
        # oyunda başta belirtilen can sayısı kadar gemiye can eklenir 
        for i in self.lives:
            self.liveSprites.add(i)
        # düşman grubununun tanımlanması
        self.enemySprites = pygame.sprite.Group()
        # benzin grubnunun tanımlanması
        self.fuelSprites = pygame.sprite.Group()
        # mermi grubunun tanımlanması
        self.shootSprites = pygame.sprite.Group()
        # taş yani harita objelerinin grubunun tanımlanması
        self.stoneSprites = pygame.sprite.Group()
        # Gemi objesinin oluşturulup başta tanımlanan gemiye atılması 
        self.spaceship = SpaceShip(self.shootSprites, self.width, self.height)
        # kullanıcı grubuna geminin atılması 
        self.userSprites = pygame.sprite.Group(self.spaceship)
        # roketlerin oluşturulması ve rokete atılması
        self.rocket = Rockets(self.spaceship.rect.right, self.spaceship.rect.center[1], self.spaceship.rangey)

    def keepGoing(self, isWave1=False, isWave2=False):
        """1. ve 2. düşman dalgalarını ve oyun bitiş, açılış ekranını kontrol eder."""
        self.isWave1 = isWave1
        # düşman dalgalarının gelip gelmeyeceğinin tanımlanması 
        self.isWave2 = isWave2
        # eğer devam et True ise (keepgoing) başlangıç değerlerinin atanması gerçeklestirilir.
        # örnegin start ekranının sadece oyun basında gelmesi gibi
        if self.keepgoing:
            # Başlangıç ekranını gösterme fonksiyonu calışır 
            self.show_strt_screen()
            # devam et false yapılarak 
            self.keepgoing = False
            # canlar tanımlanır 
            self.lives = [Lives(1), Lives(2), Lives(3)]
            # Spriteler tekrar tanımlanır.
            self.initSprites()
            # level fonksiyonu cagırılarak okunan levellerin suanki level olarak gelmesi saglanır.
            self.level()

        # eğer karakter öldüyse bu kod parçası çalısır.
        if self.game_over:
            # Ölüm ekranı gösterilir
            self.show_go_screen()
            # ölüm ekranı gösterildiği icin oyuncunun oyuna tekrar baslayabilmesi icin bu değişken true olarak değistirilir.
            self.game_over = False
            # biten canlar yeniden tanımlanarak yenilenir
            self.lives = [Lives(1), Lives(2), Lives(3)]
            # Spriteler yeniden atanarak başlangıca dönülmesi saglanır 
            self.initSprites()
            # değisen level değeri 1 e çekilerek oyuncunun 1. levelden baslaması saglanır
            self.currentLevel = 1
            # level fonksiyonu cagırılarak levelin 1 e esitlenmesi saglanır
            self.level()
        # oyun icinde kullanılacak olan fps basta tanımlanan fps değerine eşitlenir
        self.clock.tick(self.fps)
        # oyun icerisinde mousenin gözükmemesi icin bu değer false yapılır 
        pygame.mouse.set_visible(False)
        # oyun icindeki eventlerin yani tuşların basılmasını algılamak icin gerekli eventler kontrol edilir.
        for event in pygame.event.get():
            # eğer esc ye basıldıysa oyun kapatılır( ve ya çarpı tuşu)
            if event.type == pygame.QUIT or \
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()

    # oyun bitis ekranı fonksiyonu
    def show_go_screen(self, HS_FILE='HighScore'):
        """oyun bitiş ekranı"""
        # oyun bitisinin arkaplanı tanımlanarak cizime uygun hale getirilir
        self.screen.blit(self.background, (0, 0))
        # ekranda çıkcak yazılar yazdırılır.
        draw_text(self.screen, "SCRAMBLE!", 64, self.width / 2, self.height / 4)

        draw_text(self.screen, "Nice try, but not enough!", 22,
                  self.width / 2, self.height / 2)
        draw_text(self.screen, "your score is:" + str(self.spaceship.score), 64, self.width / 2, self.height * 3 / 4)
        draw_text(self.screen, "Press any key to play again", 18, self.width / 2, self.height * 8 / 9)
        # geminin skoru yüksek skordan yüksekse yeni yüksek skor olarak kaydedilir
        if self.spaceship.score > self.highscore:
            self.highscore = self.spaceship.score
            draw_text(self.screen, "NEW HIGH SCORE!!", 36, self.width / 2, self.height * 1 / 9)
            with open(os.path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.spaceship.score))
        else:
            draw_text(self.screen, "High Score: " + str(self.highscore), 18, self.width / 2, self.height * 1 / 9)
        pygame.display.flip()
        waiting = True
        # oyuncunun her hangi bir tusa basmasi beklenir bu tusa göre oyundan cıkılır veya yeni oyuna baslanır (esc veya üst alt )
        while waiting:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN and pygame.KEYUP:
                    waiting = False
    # başlangıç ekranının gösterilmesini sağlayan fonksiyon 
    def show_strt_screen(self):
        """oyun açılış ekranı"""
        # arka plan çizdirilerek rendere hazır hale getirilir.
        self.screen.blit(self.background, (0, 0))
        # gerekli yazılar ekrana yazdırlır 
        draw_text(self.screen, "SCRAMBLE!", 64, self.width / 2, self.height / 4)

        draw_text(self.screen, "Arrow keys move, Space to fire, R to fire rockets", 22,
                  self.width / 2, self.height / 2)
        draw_text(self.screen, "Press a key to begin", 18, self.width / 2, self.height * 8 / 9)
        draw_text(self.screen, "HighScore: " + str(self.highscore), 18, self.width / 2, self.height * 1 / 8)
        # ekrana render edilmis görüntü yansıtılır.
        pygame.display.flip()
        waiting = True
        # oyuncudan bir tusa basması beklenir.
        while waiting:
            self.clock.tick(self.fps)
            # eğer basılan tus esc ise oyundan cıkılır üst tus ise oyuna baslanır
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYUP:
                    waiting = False
    # ekaranın ilk değerlerinin atanması
    def initScreen(self):
        """ekranı, başlığı ve oyun saatini aktifleştirir."""
        # oyunun ekranının yüksekliginin ve genisliginin belirlenmesi
        self.screen = pygame.display.set_mode((self.width, self.height))
        # Ekranda title olarak  scramble game yazdırılması 
        pygame.display.set_caption('Scramble Game')
        # saatin tanımlanması fps()
        self.clock = pygame.time.Clock()
    # oyun arkaplaninin doldurulması 
    def fillBackground(self):
        """arka fonu siyahla doldurur."""
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        # rgb(0,0,0) siyah 
        self.background.fill((0, 0, 0))
    # resimlerin ekrana çizdirilmesi 
    def blit(self):
        """resimleri ekrana blitler."""
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

    def wave_1(self):
        """birinci düşman dalgası için yer ve level konfigurasyonu"""
        # Event loop
        # Burada level 1 de sadece wave1 level 2 de ise sadece wave2 aktiflesir. Level3 e geçildiğinde ise her iki dalga da aktifleserek zorluk zorlaştırılmıs olur
        # düşmanların random olarak cıkmasını saglar
        # eğer level 1 ve ya level 3 ise dalga 1 aktifleserek düsman dalgaları random olarak tanımlanır
        if self.currentLevel == 1 or self.currentLevel == 3:
            for i in range(175):
                self.enemy = Enemy1()
                self.enemy.rect.x = random.randrange(600, 8064)
                self.enemy.rect.y = random.randrange(0, self.height / 2 + 50)
                self.enemySprites.add(self.enemy)
        # eğer level 2 ve ya 3 ise wawe 2 başlar 
        if self.currentLevel == 2 or self.currentLevel == 3:
            for i in range(100):
                self.enemy2 = Enemy2()
                self.enemy2.rect.x = random.randrange(600, 8064)
                self.enemy2.rect.y = random.randrange(0, self.height / 2 + 50)
                self.enemySprites.add(self.enemy2)
    # ekranın temizlenmesi için tanımlanmış fonksiyon
    # oyun ekranı temizlenmesse ekranda cıkacak resimler üstüste gelerek görüntü bozulur bu sebeple her güncellemede ekran temizlenerek resimler tekrar cizdirilir.
    def clear(self):
        """ekranı temizler."""
        self.systemSprites.clear(self.screen, self.background)
        self.userSprites.clear(self.screen, self.background)
        self.stoneSprites.clear(self.screen, self.background)
        self.enemySprites.clear(self.screen, self.background)
        self.fuelSprites.clear(self.screen, self.background)
        self.shootSprites.clear(self.screen, self.background)
        self.explosionSprites.clear(self.screen, self.background)
        self.liveSprites.clear(self.screen, self.background)
    # resimlerin toplu olarak  güncellemnmesi 
    def spriteUpdate(self):
        """bütün spriteların update fonksiyonlarını çalıştırır."""
        self.systemSprites.update()
        self.userSprites.update()
        self.stoneSprites.update()
        self.enemySprites.update()
        self.fuelSprites.update()
        self.shootSprites.update()
        self.explosionSprites.update()
        self.liveSprites.update()
    # resimlerin ekrana cizdirilmesi 
    def draw(self):
        """bütün spriteları ekrana çizer"""
        self.systemSprites.draw(self.screen)
        self.userSprites.draw(self.screen)
        self.stoneSprites.draw(self.screen)
        self.enemySprites.draw(self.screen)
        self.fuelSprites.draw(self.screen)
        self.shootSprites.draw(self.screen)
        self.explosionSprites.draw(self.screen)
        self.liveSprites.draw(self.screen)
        self.draw_player_fuel(self.screen, self.width / 2 - 100, self.height - 50, self.spaceship.fuel / 100)
        draw_text(self.screen, "FUEL ", 18, self.width / 2, self.height - 50)
        draw_text(self.screen, str(self.spaceship.score), 24, self.width - 24, 24)
        draw_text(self.screen, str(self.spaceship.fuel), 24, self.width - 100, 24)

# bu dosya baslatıldıgında GameObject yani oyunu tanımlayarak baslatır parametre olarak girilen level ve fps degerleri tanımlanır, ek olarak diğer parametrelerde bu obje tanımlanırken değiştirilebilir
# oyunun baslaması icin her hangi bir yerde tanımlanan gameobject yeterlidir.
if __name__ == '__main__': GameObject(level=1, FPS=60)
