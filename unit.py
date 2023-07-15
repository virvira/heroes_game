from __future__ import annotations
from abc import ABC, abstractmethod
from equipment import Equipment, Weapon, Armor
from classes import UnitClass
from random import randint
from typing import Optional


class BaseUnit(ABC):
    """
    Базовый класс юнита
    """

    def __init__(self, name: str, unit_class: UnitClass):
        """
        При инициализации класса Unit используем свойства класса UnitClass
        """
        self.name = name
        self.unit_class = unit_class
        self.hp = unit_class.max_health
        self.stamina = unit_class.max_stamina
        self.weapon = None
        self.armor = None
        self._is_skill_used = False

    @property
    def health_points(self):
        return round(self.hp, 2)

    @property
    def stamina_points(self):
        return round(self.stamina, 2)

    def equip_weapon(self, weapon: Weapon):
        self.weapon = weapon
        return f'{self.name} экипирован оружием {self.weapon.name}'

    def equip_armor(self, armor: Armor):
        self.armor = armor
        return f'{self.name} экипирован броней {self.armor.name}'

    def _count_damage(self, target: BaseUnit) -> int:
        self.stamina -= self.weapon.stamina_per_hit
        damage = self.weapon.damage * self.unit_class.attack

        if target.stamina > target.armor.stamina_per_turn * target.unit_class.stamina:
            target.stamina -= target.armor.stamina_per_turn * target.unit_class.stamina
            damage -= target.armor.defence * target.unit_class.armor

        damage = round(damage, 1)
        target.get_damage(damage)
        return damage

    def get_damage(self, damage: int) -> Optional[int]:
        if self.hp - damage > 0:
            self.hp -= damage
        else:
            self.hp = 0

    @abstractmethod
    def hit(self, target: BaseUnit) -> str:
        """
        этот метод будет переопределен ниже
        """
        pass

    def use_skill(self, target: BaseUnit) -> str:
        """
        метод использования умения.
        если умение уже использовано возвращаем строку
        Навык использован
        Если же умение не использовано тогда выполняем функцию
        self.unit_class.skill.use(user=self, target=target)
        и уже эта функция вернем нам строку которая характеризует выполнение умения
        """
        if self._is_skill_used:
            return f'Навык использован'
        self._is_skill_used = True
        self.unit_class.skill.use(user=self, target=target)


class PlayerUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        функция удар игрока:
        здесь происходит проверка достаточно ли выносливости для нанесения удара.
        вызывается функция self._count_damage(target)
        а также возвращается результат в виде строки
        """
        if self.stamina < self.weapon.stamina_per_hit:
            return f'{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости.'

        damage = self._count_damage(target)

        if damage > 0:
            return (f'{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника и наносит '
                    f'{damage} урона.')

        return (f'{self.name} используя {self.weapon.name} наносит удар, но {target.armor.name} cоперника '
                f'его останавливает.')


class EnemyUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        функция удар соперника
        должна содержать логику применения соперником умения
        (он должен делать это автоматически и только 1 раз за бой).
        Например, для этих целей можно использовать функцию randint из библиотеки random.
        Если умение не применено, противник наносит простой удар, где также используется
        функция _count_damage(target
        """

        if not self._is_skill_used and self.unit_class.skill.stamina <= self.stamina and randint(1, 100) < 10:
            return self.use_skill(target)

        if self.stamina < self.weapon.stamina_per_hit:
            return f'{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости.'

        damage = self._count_damage(target)

        if damage > 0:
            return (f'{self.name} используя {self.weapon.name} пробивает {target.armor.name} и наносит '
                    f'Вам {damage} урона.')

        return (f'{self.name} используя {self.weapon.name} наносит удар, но Ваш(а) {target.armor.name} '
                f'его останавливает.')
