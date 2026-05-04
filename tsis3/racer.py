import random
from pathlib import Path

import pygame
from pygame import *
import time
from pygame.sprite import Sprite, Group, spritecollide, spritecollideany

from persistence import add_score


ENI = 500
BIK = 700
FPS = 60

ZHOL = [100, 200, 300, 400]
FIN = 3000
QAZYNA = Path("/Users/medinameirambek/Desktop/meow/tsis3/assets")

QIYIN = {
    "easy":   {"zhan_jyl": 5, "kol": 1000, "tosqan": 1600},
    "normal": {"zhan_jyl": 7, "kol": 800,  "tosqan": 1200},
    "hard":   {"zhan_jyl": 9, "kol": 600,  "tosqan": 900}
}

draw_rect = pygame.draw.rect
draw_ellipse = pygame.draw.ellipse
draw_circle = pygame.draw.circle
get_ticks = pygame.time.get_ticks
get_pressed = pygame.key.get_pressed
Sound = pygame.mixer.Sound


def suret(at, olshem=None):
    img = pygame.image.load(str(QAZYNA / at)).convert_alpha()
    if olshem:
        img = transform.scale(img, olshem)
    return img


def qauipsiz(oz_rect):
    qol = [z for z in ZHOL if abs(z - oz_rect.centerx) > 70]
    if not qol:
        qol = ZHOL[:]
    return random.choice(qol)


class Oz(Sprite):
    def __init__(self, sozder):
        super().__init__()
        self.image = suret("Player.png", (50, 90))
        renmap = {
            "blue":   (0, 0, 220, 90),
            "red":    (220, 0, 0, 90),
            "green":  (0, 180, 0, 90),
            "yellow": (255, 215, 0, 90)
        }
        ren = renmap.get(sozder.get("car_color", "blue"), (0, 0, 220, 90))
        overlay = Surface((50, 90), SRCALPHA)
        overlay.fill(ren)
        self.image.blit(overlay, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = ENI // 2
        self.rect.bottom = BIK - 20
        self.jyl = 6

    def jylt(self):
        bas = get_pressed()
        if bas[K_LEFT]:  self.rect.move_ip(-self.jyl, 0)
        if bas[K_RIGHT]: self.rect.move_ip(self.jyl, 0)
        if bas[K_UP]:    self.rect.move_ip(0, -self.jyl)
        if bas[K_DOWN]:  self.rect.move_ip(0, self.jyl)
        if self.rect.left < 35:      self.rect.left = 35
        if self.rect.right > ENI-35: self.rect.right = ENI-35
        if self.rect.top < 0:        self.rect.top = 0
        if self.rect.bottom > BIK:   self.rect.bottom = BIK


class Zhan(Sprite):
    def __init__(self, oz_rect, jyl):
        super().__init__()
        self.image = suret("Enemy.png", (50, 90))
        self.rect = self.image.get_rect()
        self.rect.centerx = qauipsiz(oz_rect)
        self.rect.bottom = -random.randint(40, 300)
        self.jyl = jyl

    def jylt(self, zjyl):
        self.rect.y += self.jyl + zjyl//3
        if self.rect.top > BIK: self.kill()


class Tenge(Sprite):
    def __init__(self, oz_rect):
        super().__init__()
        tan = random.choice([("20tg.png",20),("50tg.png",50),("100tg.png",100)])
        self.kun = tan[1]
        self.image = suret(tan[0], (38, 38))
        self.rect = self.image.get_rect()
        self.rect.centerx = qauipsiz(oz_rect)
        self.rect.y = -random.randint(60, 450)
        self.jyl = 4

    def jylt(self, zjyl):
        self.rect.y += self.jyl + zjyl//3
        if self.rect.top > BIK: self.kill()


class Tosqan(Sprite):
    def __init__(self, oz_rect):
        super().__init__()
        self.tur = random.choice(["barrier","oil","pothole","speed_bump"])
        self.image = Surface((65, 35), SRCALPHA)
        if self.tur == "barrier":
            draw_rect(self.image, (255,140,0), (0,0,65,35))
            draw_rect(self.image, (0,0,0), (0,0,65,35), 2)
        elif self.tur == "oil":
            draw_ellipse(self.image, (0,0,0), (6,7,53,22))
        elif self.tur == "pothole":
            draw_ellipse(self.image, (90,90,90), (5,5,55,25))
            draw_ellipse(self.image, (0,0,0), (12,9,40,16))
        elif self.tur == "speed_bump":
            draw_rect(self.image, (255,215,0), (0,12,65,12))
            draw_rect(self.image, (0,0,0), (0,12,65,12), 1)
        self.rect = self.image.get_rect()
        self.rect.centerx = qauipsiz(oz_rect)
        self.rect.y = -random.randint(80, 500)
        self.jyl = 5

    def jylt(self, zjyl):
        self.rect.y += self.jyl + zjyl//3
        if self.rect.top > BIK: self.kill()


class QozTosqan(Sprite):
    def __init__(self):
        super().__init__()
        self.image = Surface((90, 28), SRCALPHA)
        draw_rect(self.image, (255,140,0), (0,0,90,28))
        draw_rect(self.image, (0,0,0), (0,0,90,28), 2)
        self.rect = self.image.get_rect()
        self.rect.x = random.choice([55, ENI-145])
        self.rect.y = -60
        self.jyl_y = 5
        self.jyl_x = random.choice([-2, 2])

    def jylt(self, zjyl):
        self.rect.y += self.jyl_y + zjyl//4
        self.rect.x += self.jyl_x
        if self.rect.left < 35 or self.rect.right > ENI-35:
            self.jyl_x *= -1
        if self.rect.top > BIK: self.kill()


class Kuch(Sprite):
    def __init__(self, oz_rect):
        super().__init__()
        self.tur = random.choice(["nitro","shield","repair"])
        self.tuu = time.time()
        self.omer = 6
        self.image = Surface((40, 40), SRCALPHA)
        ren_harf = {"nitro": ((0,200,255),"N"), "shield": ((0,0,220),"S"), "repair": ((0,180,0),"R")}
        ren, harf = ren_harf[self.tur]
        draw_circle(self.image, ren, (20,20), 19)
        draw_circle(self.image, (0,0,0), (20,20), 19, 2)
        qalam = font.SysFont("Verdana", 18, bold=True)
        mat = qalam.render(harf, True, (255,255,255))
        self.image.blit(mat, mat.get_rect(center=(20,20)))
        self.rect = self.image.get_rect()
        self.rect.centerx = qauipsiz(oz_rect)
        self.rect.y = -random.randint(120, 550)
        self.jyl = 4

    def jylt(self, zjyl):
        self.rect.y += self.jyl + zjyl//3
        if self.rect.top > BIK: self.kill()
        if time.time() - self.tuu > self.omer: self.kill()


def fon_sal(ekran, fony):
    ekran.fill((30,120,45))
    zsol = 40
    zen = ENI - 80
    zbos = zen // 4
    draw_rect(ekran, (190,190,190), (zsol,0,zen,BIK))
    draw_rect(ekran, (255,215,0), (zsol,0,4,BIK))
    draw_rect(ekran, (255,215,0), (zsol+zen-4,0,4,BIK))
    for sx in [zsol+zbos, zsol+zbos*2, zsol+zbos*3]:
        for y in range(-100, BIK+100, 150):
            sy = (y + fony) % (BIK+150) - 100
            draw_rect(ekran, (255,255,255), (sx-4,sy,8,70))


def hud_sal(ekran, qalam, bal, tng, ara, active_p, kuaqyt, qalqan):
    sheild = max(0, FIN - int(ara))
    matndar = [
        f"Score: {int(bal)}",
        f"Coins: {tng}",
        f"Distance: {int(ara)}m",
        f"Remaining: {sheild}m",
        f"Power: {active_p if active_p else 'None'}",
        f"Time: {kuaqyt:.1f}s" if active_p== "nitro" else "",
        f"Shield: {'ON' if qalqan else 'OFF'}"
    ]
    y = 10
    for mat in matndar:
        if mat:
            ekran.blit(qalam.render(mat, True, (0,0,0)), (10, y))
            y += 24


def oyyn(ekran, qold, sozder):
    saat = pygame.time.Clock()
    qalam = font.SysFont("Verdana", 18)

    urys = Sound(str(QAZYNA/"crash.wav"))
    aqsha = Sound(str(QAZYNA/"money.wav"))
    bip = Sound(str(QAZYNA/"bip.wav"))

    if sozder["sound"]:
        mixer.music.load(str(QAZYNA/"background.wav"))
        mixer.music.play(-1)

    qiyin = QIYIN[sozder.get("difficulty","normal")]
    oz = Oz(sozder)

    barlyq = Group()
    zhandar = Group()
    tengeler = Group()
    tosqandar = Group()
    kuchter = Group()
    barlyq.add(oz)

    juryp = True
    utyp = False
    fony = 0
    zjyl = 5
    ara = 0
    bal = 0
    tng = 0
    sheild = False
    active_p = None
    ksonu = 0

    son_zhan = son_tenge = son_tosqan = son_kuch = son_oqiga = get_ticks()

    while juryp:
        qazir = get_ticks()
        deng = 1 + int(ara // 600)
        kol = max(250, qiyin["kol"] - deng*70)
        tkol = max(350, qiyin["tosqan"] - deng*70)
        zj = qiyin["zhan_jyl"] + deng

        if active_p == "nitro":
            zjyl = (5+deng) if time.time() > ksonu else (10+deng)
            if time.time() > ksonu: active_p = None
        else:
            zjyl = 5 + deng

        for ev in pygame.event.get():
            if ev.type == QUIT:
                mixer.music.stop()
                return "quit", {"score":int(bal),"distance":int(ara),"coins":tng}

        if qazir-son_zhan > kol:
            z = Zhan(oz.rect, zj); zhandar.add(z); barlyq.add(z); son_zhan = qazir
        if qazir-son_tenge > 1050:
            t = Tenge(oz.rect); tengeler.add(t); barlyq.add(t); son_tenge = qazir
        if qazir-son_tosqan > tkol:
            tq = Tosqan(oz.rect); tosqandar.add(tq); barlyq.add(tq); son_tosqan = qazir
        if qazir-son_kuch > 6500:
            k = Kuch(oz.rect); kuchter.add(k); barlyq.add(k); son_kuch = qazir
        if qazir-son_oqiga > 5000:
            qt = QozTosqan(); tosqandar.add(qt); barlyq.add(qt); son_oqiga = qazir

        oz.jylt()
        for s in list(zhandar): s.jylt(zjyl)
        for s in list(tengeler): s.jylt(zjyl)
        for s in list(tosqandar): s.jylt(zjyl)
        for s in list(kuchter): s.jylt(zjyl)

        fony = (fony + zjyl) % BIK
        ara += zjyl * 0.08
        bal += zjyl * 0.03

        for t in spritecollide(oz, tengeler, True):
            tng += 1; bal += t.kun
            if sozder["sound"]: aqsha.play()

        for k in spritecollide(oz, kuchter, True):
            if active_p is None and not sheild:
                if sozder["sound"]: bip.play()
                if k.tur == "nitro":    active_p = "nitro"; ksonu = time.time()+4
                elif k.tur == "shield": sheild= True
                elif k.tur == "repair":
                    bal += 50
                    for tq in list(tosqandar): tq.kill(); break

        uz = spritecollideany(oz, zhandar)
        ut = spritecollideany(oz, tosqandar)
        if uz or ut:
            if sheild:
                sheild = False
                if uz: uz.kill()
                if ut: ut.kill()
            else:
                if sozder["sound"]: urys.play()
                juryp = False

        if ara >= FIN: utyp = True; juryp = False

        fon_sal(ekran, fony)
        for ent in barlyq: ekran.blit(ent.image, ent.rect)
        hud_sal(ekran, qalam, bal, tng, ara, active_p, max(0, ksonu-time.time()), sheild)
        display.flip()
        saat.tick(FPS)

    mixer.music.stop()
    sonbal = int(bal + ara*0.5 + tng*20)
    add_score(qold, sonbal, ara, tng)
    return "game_over", {"score":sonbal,"distance":int(ara),"coins":tng,"won":utyp}