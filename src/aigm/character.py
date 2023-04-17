from typing import List, Dict
from collections import namedtuple
from enum import Enum, auto
from dataclasses import dataclass


class CharacterType(Enum):
    VECTOR = auto()
    PARADOX = auto()
    SPINNER = auto()


StatAttributes = namedtuple("StatAttributes", ["pool", "edge"])


class Stat(Enum):
    MIGHT = StatAttributes("Might", ["pool", "edge"])
    SPEED = StatAttributes("Speed", ["pool", "speed"])
    INTELLECT = StatAttributes("Intellect", ["pool", "edge"])


DescriptorAttributes = namedtuple("DescriptorAttributes", ["skills", "attribute_bonuses", "inabilities", "description"])


@dataclass
class Descriptor:
    name: str
    skills: List[str]
    inabilities: List[str]
    attribute_bonuses: List[Stat]
    description: str


@dataclass
class FocusAbility:
    name: str
    cost: List[Stat]
    description: str


@dataclass
class FocusAttributes:
    description: str
    equipment: List[str]
    minor_effect_suggestion: str
    major_effect_suggestion: str
    tiered_abilities: List[List[FocusAbility]]


@dataclass
class Focus:
    name: str
    description: str
    equipment: List[str]
    minor_effect_suggestion: str
    major_effect_suggestion: str
    tiered_abilities: List[List[FocusAbility]]


@dataclass
class Attributes:
    might: Stat.Might
    speed: Stat.Speed
    intellect: Stat.Intellect


@dataclass
class Skill:
    name: str
    level: int


class Range(Enum):
    IMMEDIATE = auto()
    SHORT = auto()
    LONG = auto()
    EXTREME = auto()


@dataclass
class Weapon:
    name: str
    description: str
    price: int
    damage: int
    range: Range


@dataclass
class Armor:
    name: str
    description: str
    price: int
    might_cost: int
    speed_reduction: int


@dataclass
class OtherEquipment:
    name: str
    price: int
    description: str


@dataclass
class Cypher:
    is_occultic: bool
    name: str
    level: int
    effect: str
    description: str


@dataclass
class Artifact:
    name: str
    level: int
    effect: str
    depletion_roll: int
    depletion_roll_die: int
    description: str


@dataclass
class Character:
    name: str
    tier: int
    descriptor: Descriptor
    character_type: CharacterType
    focus: Focus
    stats: Attributes
    max_effort: int
    max_allowed_cyphers: int
    skills: List[Skill]
    weapons: List[Weapon]
    armor: List[Armor]
    other_equipment: List[OtherEquipment]
    cyphers: List[Cypher]
    artifacts: List[Artifact]
