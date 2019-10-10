import os
import random

import pygame


class SpaceShip(pygame.sprite.Sprite):
    """oyuncu karakteri uzay gemisi, skor,yakıt,can,ateşleme ve hareket fonksiyonları"""

    def __init__(self, collide, rangex=500, rangey=500):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('images/spaceship.png')
        """Toplam oyun skorunun tutulabilmesi için tanımlanmış parametre skor """
        self.score = 0
        self.fuel = 200
        # Uzay gemisinin can değeri
        self.lives = 3
        # geminin koordinatları
        self.x = 200
        self.y = 250
        # geminin çarpısma değiskeni bu değer tanımlandığında geminin diğer objelerle gireceği tepkimelerde reaksiyonları tanımlanır
        self.collide = collide
        # geminin lazer atabilmesi icin tanımlanan boş bir lazer objesi
        self.laser = None
        # geminin roket atabilmesi icin tanımlanan boş bir roket objesi
        self.rocket = None
        # roketlerin atılabilir veya atılamaz oldugunu kontrol etmek icin kullanılan boolean değişkeni
        self.rocketready = False
        # ates edilebilir olunup olunmadıgını kontrol etmek icin tanımlanan değisken
        self.shootable = False
        self.maxTick = 10
        # tick = oyun içi saat FPS değerini dogrudan etkiler
        self.tick = self.maxTick
        # maksimum atılabilecek roket sayısı
        self.maxRocket = 30
        # gidilebilecek bölgelerin sınırları
        self.rangex = rangex
        self.rangey = rangey
        self.rockettick = self.maxRocket

        # obje(gemi) tanımlandıktan (init) sonra sürekli devam eden döngüsel fonksiyon burada sürekli olarak devam eden tepkiler tanımlanmıstır hareket tuş kombinasyonları gibi 
    def update(self, *args):
        # baslangıctaki hız 0 a sabitlendi
        self.speedx = 0
        self.speedy = 0
        # eğer oyun devam ediyorsa ve yakıt varsa
        if self.tick == 0 and self.fuel >= 1:
            # gemi ates edebilir
            self.shootable = True
            # ve frame güncellenebilir
            self.tick = self.maxTick
        else:
            self.tick -= 1
            # eger roket framesı yok sa ve yeterli yakıt varsa 
        if self.rockettick == 0 and self.fuel >= 2:
            # roket kullanılabilir olur 
            self.rocketready = True
            # roketin framesi güncellenebilir 
            self.rockettick = self.maxRocket
        else:
            self.rockettick -= 1
        # oyunda basılan tusların sürekli algılanabilmesi icin gerekli olan fonksiyon
        pygame.event.get()
        # oyun icerisinde basılı olan tusların alınması
        keystate = pygame.key.get_pressed()
        # sol tusa basılınca gemi x ekseninde -8 hızlanır yani sol yönde hız kazanır
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        # gemi eger ates edebilir halde ise shoot fonkisonu sayesinde ates eder. Ve gemi daha yeni ates ettigi icin ates etme durumu false yapılır ki belirlenen aralıklarda ates edebilsin
        if keystate[pygame.K_SPACE]:
            if self.shootable:
                self.shoot()
                self.shootable = False
        # gemi eğer roket atabilir halde ise missile fonksiyonu ile roket yollar.
        if keystate[pygame.K_r]:
            if self.rocketready:
                self.missile()
                self.rocketready = False
        # karakter hareketi sağa doğru hızlanma
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        # karaketerin hız değerini karakterin konumuna eklenerek sağa sola kayması saglanır
        self.rect.x += self.speedx
        # eger karakter belirlenen sınırların dısına cıkıyorsa bu engellenir
        if self.rect.right > self.rangex:
            self.rect.right = self.rangex
        if self.rect.left < 0:
            self.rect.left = 0
        if keystate[pygame.K_UP]:
            self.speedy = -8
        if keystate[pygame.K_DOWN]:
            self.speedy = 8
        # karakterin yukari ve asagı yönde harket etmesi saglanır
        self.rect.y += self.speedy
        # üst ve alt sınırlar 
        if self.rect.y > self.rangey:
            self.rect.y = self.rangey
        if self.rect.y < 0:
            self.rect.y = 0

    # geminin ateş edebilmesini sağlayan fonksiyon
    def shoot(self):
        # baslangıcta boş olarak tanımlanan lazer objesine yeni bir lazer objesi olusturulur.Bu obje olusturulurken başlangıç konumu olarak geminin burnunun koordinatlarını parametre olarak alır
        laser = Shoot(self.rect.right, self.rect.center[1], self.rangex)
        # lazer collidere eklenir yani artık lazer görüntü olarak gelmiş ve başka nesnelerle çarpıstıgında tepkime vermesi sağlanmıştır
        self.collide.add(laser)
        # lazer kullanıldıgında geminin yakıtı bir miktar düşer
        self.fuel -= 1
    # geminin roket atabilmesini sağlayan fonksiyon
    def missile(self):
        # gemide boş olarak tanımlanmış roket objesine yeni bir roket olusturulup eşitlenir. Konum olarak geminin burnu parametre olarak verilir
        rocket = Rockets(self.rect.right, self.rect.center[1], self.rangey)
        # roket collidere eklenir yani artık roket görüntü olarak gelmiş ve başka nesnelerle çarpıstıgında tepkime vermesi sağlanmıştır
        self.collide.add(rocket)
        # roket kullanıldıgında geminin yakıtı bir miktar düşer
        self.fuel -= 2

# karakterin canının ekranda gözükebilmesi için tanımlanan Can sınıfı
class Lives(pygame.sprite.Sprite):
    # başlangıç değerlerinin tanımlanması ve parametre olarak maximum canı alır
    def __init__(self, lives=3):
        # bu sınıf bir sprite(oyun resmi) olduğu icin sprite olarak ilk değerlerinin atılması gerekmektedir.
        pygame.sprite.Sprite.__init__(self)
        # karakterin resmi ve bu resmin boyutları image ve rect değişkenlerine load_png fonksiyonu sayesinde atılır.(Parametre olarak image klasöründeki gemi resmi secilmistir)
        self.image, self.rect = load_png('images/spaceship.png')
        # canların hizzalanması icin her canın kapladığı alan baz alınarak canların yanyana dizilebilmesi saglanır
        self.rect.x = (lives - 1) * 64
        # ekranın üst bölmesinden 10 birim aşagısı
        self.rect.y = 10

# Haritada çıkan ve kullanılabilir olan Yakıt depolarının oluşabilmesi için tanımlanan sınıf 
class Fuels(pygame.sprite.Sprite):
    # ilk değerlerin tanımlanması için kullanılan fonksiyon(constructure)
    def __init__(self):
        # sprite ilk degerlerinin atanması 
        pygame.sprite.Sprite.__init__(self)
        # image ve boyutların atılması
        self.image, self.rect = load_png('images/fuel.png')
    # oyun her kendini güncellediğinde bu fonksiyon calısır. ve bu depoların gemiye doğru ilerlemesi icin x lerin 1 azalması gerekmektedir (map karaktere doğru geliyor aynı şekilde benzin depoları da gelmeli)
    def update(self, *args):
        self.rect.x += -1

# Ateş edildiğinde çıkan lazerin resminin ve nasıl davranıcağının belirlenmesi için oluşturulan class
class Shoot(pygame.sprite.Sprite):
    # ilk değerlerin atanması icin constructure, merminin nereden çıkacağını belirlemek için x,y değerleri parametre olarak alınır.
    # With parametresi ise merminin gidebilecegi maksimum uzaklıgı belirler
    def __init__(self, x, y, width):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('images/shot.gif')
        self.rect.x = x
        self.rect.y = y
        self.width = width
        # self.sndHit1 = pygame.mixer.Sound('data/laser.wav')
        # hit

    def update(self):
        # merminin hızı 25 yani her frame güncellemesinde mermi 25 birim sağa kayar
        self.rect.x += 25
        # eğer mermi belirlenen sınırın dışına çıktıysa kendini kill() fonksiyonuyla öldürür.
        if self.rect.x > self.width:
            self.kill()

# Roket sınıfı 
class Rockets(pygame.sprite.Sprite):
    # ilk değer ataması mermi ile tek farkı burada güncellemenin hem x hemde y ekseninde olmasıdır yani roket her güncellendiğinde sağa ve aşağıya doğru düşer
    def __init__(self, x, y, width):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('images/rocket.png')
        self.rect.x = x
        self.rect.y = y
        self.width = width
        # self.rcktHit1 = pygame.mixer.Sound('data/boom.wav')

    def update(self):
        # self.count = 0
        # self.rect.x = 20
        self.rect.x += 2
        self.rect.y += 10
        # sınır dığına cıkıldığında kill ile kendini öldürür
        if self.rect.y > self.width:
            self.kill()
        # if self.count > 8:
        #     self.rect.x +=0

# bölümün bitip bitmediğini anlayabilmek için olusturulan taş sınıfı
class TheEndGame(pygame.sprite.Sprite):
    """oyun sonu için bitiş bayrağı olan taş."""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('images/stone.png')
    # her map objesinin yaptığı gibi sola doğru kayarak karakterin ilerliyormuş gibi görünmesini sağlar
    def update(self, *args):
        self.rect.x += -1

    # eğer bu sınıfın konumu x ekseninde 200 ün altına inerse bu bölüm bitmiş demektir
    # her levelde 1 adet tanımlanması yeterlidir.
    def end(self):
        if self.rect.x < 200:
            return True
        return False

# Haritada kullanılan taş objesi 
class Stone(pygame.sprite.Sprite):
    """mapi oluşturan taş sınıfı"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('images/stone.png')
    # taşların kaymasi için
    def update(self, *args):
        self.rect.x += -1

# Düşman sınıfı
class Enemy1(pygame.sprite.Sprite):
    """1.düşman, 1.25 ve 2.5 arasında rastgele bir hızla ilerler"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('images/enemy1.png')
    # random hızlanma fonksiyonu güncelleme ile çalısır
    def update(self, *args):
        self.rect.x -= random.uniform(1.25, 2.5)

# Düşman sınıfı 2 
class Enemy2(pygame.sprite.Sprite):
    """ateş topu, 2.düşman"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('images/fireball.png')

    def update(self, *args):
        self.rect.x += -5


class Enemy3(pygame.sprite.Sprite):
    """3.düşman (roket) sınıfı, ve karakter rokete yaklaşınca ateşleme fonksiyonu"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('images/enemy3.png')

    def update(self):
        self.rect.x -= 1
        # eğer 0 ile 300 arasında bir rakamdan düşük ise kendisini yukarıya doğru atar
        if self.rect.x < random.randrange(0, 300):
            self.rect.y -= 5

# uzay boşluğu sınıfı
class Space(pygame.sprite.Sprite):
    """arka plandaki uzay fonu ve hareket etme fonksiyonu"""
    def __init__(self, width=800):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('images/space.png')
        self.x = 0
        self.y = 250
        self.dx = 5
        self.width = width
        self.reset()

    def update(self):
        self.rect.center = (self.x, self.y)
        self.x -= self.dx
        if self.x < -self.width:
            self.reset()

    def reset(self):
        self.x = self.width

# patlama efektinin tanımlanması için oluşturulan sınıf
class Explosion(pygame.sprite.Sprite):
    """Patlama sınıfı."""
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.explosion_anim = self.explosionAnim()
        self.image = self.explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
    # animasyonların işlenmesi ve patlama efektinin verilmesi 
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
    # patlama efektinin başlaması için oluşturulan fonksiyon
    def explosionAnim(self):
        """Patlama efektlerini gif haline getirir."""
        explosion_anim = {}
        explosion_anim['sm'] = []

        WHITE = (255, 255, 255)
        # animasyon efektlerinnin ayrı ayrı olduğu için gif olarak çalıştırılacak 9 adet image dosyası okunur ve birleştirilir
        for i in range(9):
            filename = 'regularExplosion0{}.png'.format(i)
            img_dir = os.path.join(os.path.dirname(__file__), 'data/images')
            img = pygame.image.load(os.path.join(img_dir, filename))
            img.set_colorkey(WHITE)
            img_sm = pygame.transform.scale(img, (32, 32))
            explosion_anim['sm'].append(img_sm)

        return explosion_anim
# Resim dosyalarının oyuna aktarılması için yazılmış png aktarıcı parametre olarak dosya yolu alır. Ve image dosyası+boyut bilgisi döndürür
def load_png(name):
    """ Image dosyalarini okumat"""
    fullname = os.path.join('data', name)

    try:
        image = pygame.image.load(fullname)
        if image.get_alpha is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error as error:
        print('Cannot load image:', fullname)
        raise (SystemExit, error)
    return image, image.get_rect()


def draw_text(surf, text, size, x, y):
    """Ekrana Yazi yazdirma"""
    font_name = pygame.font.match_font('arial')
    # beyaz yazının rgb değerleri ile tanımlanması
    WHITE = (255, 255, 255)
    # font olarak parametre de girilen değerlerin işlenmesi
    font = pygame.font.Font(font_name, size)
    # image haline getirilme ve cizdirilme
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    # ekrana eklenmesi
    surf.blit(text_surface, text_rect)


