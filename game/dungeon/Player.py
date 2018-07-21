import sys, time, random, math, pygame
from pygame.locals import *
from library import *
from Dungeon import *


def Die(faces):
    """
    :return: 返回一个 1 到 faces 的随机数
    """
    roll = random.randint(1, faces)
    return roll


class Player():
    def __init__(self, dungeon, level, name):
        """

        :param dungeon:传入地图
        :param level:传入等级
        :param name:传入名称
        """
        self.dungeon = dungeon
        self.alive = True
        self.x = 0
        self.y = 0
        self.name = name
        self.gold = 0
        self.experience = 0
        self.level = level
        self.weapon = level
        self.weapon_name = "Club"
        self.armor = level
        self.armor_name = "Rags"
        self.roll()

    def roll(self):
        """
        str：力量
        dex：敏捷
        con：体质
        int：智力
        """
        self.str = 6 + Die(6) + Die(6)
        self.dex = 6 + Die(6) + Die(6)
        self.con = 6 + Die(6) + Die(6)
        self.int = 6 + Die(6) + Die(6)
        self.cha = 6 + Die(6) + Die(6)
        self.max_health = 10 + Die(self.con)
        self.health = self.max_health

    def levelUp(self):
        """
        升级之后，各个属性增加
        """
        self.str += Die(6)
        self.dex += Die(6)
        self.con += Die(6)
        self.int += Die(6)
        self.cha += Die(6)
        self.max_health += Die(6)
        self.health = self.max_health

    def draw(self, surface, char):
        self.dungeon.draw_char(surface, self.x, self.y, char)

    def move(self, movex, movey):
        """
        :param movex:横移坐标
        :param movey: 纵移坐标
        :return: 是否可以移动
        """
        char = self.dungeon.getCharAt(self.x + movex, self.y + movey)
        if char not in (self.dungeon.roomChar, self.dungeon.hallChar):
            return False
        else:
            self.x += movex
            self.y += movey
            return True

    def moveUp(self):
        return self.move(0, -1)

    def moveDown(self):
        return self.move(0, 1)

    def moveLeft(self):
        return self.move(-1, 0)

    def moveRight(self):
        return self.move(1, 0)

    def addHealth(self, amount):
        """
        :param amount:增加的量
        """
        self.health += amount
        if self.health < 0:
            self.health = 0
        elif self.health > self.max_health:
            self.health = self.max_health

    def addExperience(self, xp):
        """
        :param xp: 增加的量
        """
        cap = math.pow(10, self.level)
        self.experience += xp
        if self.experience > cap:
            self.levelUp()

    def getAttack(self):
        """
        :return:攻击力
        """
        attack = self.str + Die(20)
        return attack

    def getDefense(self):
        """
        :return:防御力
        """
        defense = self.dex + self.armor
        return defense

    def getDamage(self, defense):
        """
        :return:毁灭值
        """
        damage = Die(8) + self.str + self.weapon - defense
        return damage


class Monster(Player):
    def __init__(self, dungeon, level, name):
        Player.__init__(self, dungeon, level, name)
        self.gold = random.randint(1, 4) * level
        self.str = 1 + Die(6) + Die(6)
        self.dex = 1 + Die(6) + Die(6)
