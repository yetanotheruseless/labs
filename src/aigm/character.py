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


class Descriptor(Enum):
    CUSTOM = DescriptorAttributes(skills=[], attribute_bonuses=[], inabilities=[], description="")
    CLEVER = DescriptorAttributes(skills=["trickery", "lies", "mental_defense_rolls",
                                          "identify_danger", "identify_lies", "identify_quality_importance_power"],
                                  attribute_bonuses=[Stat.Might(2, 0)],
                                  inabilities=["lore", "knowledge", "academia"],
                                  description="You're quick-witted, thinking well on your feet.  You understand "
                                              "people, so you can fool them easily but are rarely fooled in return.  "
                                              "Because you easily see things for what they are,  you get the lay of "
                                              "the land swiftly, size up threats and allies, and assess situations "
                                              "with accuracy. Perhaps you're physically attractive, or maybe you use "
                                              "your wit to overcome any physical or mental imperfections. You're not "
                                              "very good at retaining facts, though.")


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


class Focus(Enum):
    CUSTOM = FocusAttributes()
    CONDUCTS_WEIRD_SCIENCE = FocusAttributes(description="""
You could be a respected scientist, having been published in several peer-reviewed journals. Or you might be considered 
a crank by your contemporaries, pursuing fringe theories on what others consider to be scant evidence. Truth is, you 
have a particular gift for sifting the edges of what’s possible. You can find new insights and unlock odd phenomena 
with your experiments. Where others see a crackpot cornucopia, you sift the conspiracy theories for revelation. Whether 
you conduct your enquiries as a government contractor, a university researcher, a corporate scientist, or an indulger 
of curiosity in your own garage lab following your muse, you push the boundaries of what’s possible.""",
                                             equipment=["street clothes", "scientific field kit", "light tools",
                                                        "pen knife", "smartphone", "$2000"],
                                             minor_effect_suggestion="You learn one additional piece of information "
                                                                     "in your analysis.",
                                             major_effect_suggestion="Foes within sight are dazed for one round upon "
                                                                     "seeing your strange creation or its results. "
                                                                     "During this time, the difficulty of all tasks "
                                                                     "they perform is modified by one step to their "
                                                                     "detriment.",
                                             tiered_abilities=[[FocusAbility(name="Lab Analysis",
                                                                             cost={Stat.INTELLECT(3, 0): 3},
                                                                             description="""
You analyze the scene of a crime, the site of a mysterious incident, or a series unexplained phenomena, and you maybe 
learn a surprising amount of information about the perpetrators, the participants, or force(s) responsible. To do so, 
you must collect samples from the scene. Samples are paint or wood scrapings, dirt, photographs of the area, hair, an 
entire corpse, and so on. With samples in hand, you can discover up to three pertinent pieces of information about the 
scene, possibly clearing up a lesser mystery, and pointing the way to solving a greater one. The GM will decide what 
you learn and what the level of difficulty might be to learn it. (For comparison, discovering that a victim was killed 
not by a fall, as seems immediately obvious, but rather by electrocution, is a difficulty 3 task for you.) The 
difficulty of the task is modified by one step in your favor if you take the time to transport the samples to a 
permanent lab (if you have access to one), as opposed to conducting the analysis with your field science kit. Action 
to initiate, 2d20 minutes to complete."""
                                                                             )]])
    CONTROLS_GRAVITY = FocusAttributes()
    ENTERTAINS = FocusAttributes()
    IS_LICENSED_TO_CARRY = FocusAttributes()
    LEADS = FocusAttributes()
    LOOKS_FOR_TROUBLE = FocusAttributes()
    OPERATES_UNDERCOVER = FocusAttributes()
    SOLVES_MYSTERIES = FocusAttributes()
    WORKS_THE_SYSTEM = FocusAttributes()
    WIELDS_TWO_WEAPONS_AT_ONCE = FocusAttributes()
    EMPLOYS_MAGNETISM = FocusAttributes()
    COMMANDS_MENTAL_POWERS = FocusAttributes()
    NAVIGATES_THE_SILVER_SKEIN = FocusAttributes()
    MANIPULATES_THE_FABRIC_OF_REALITY = FocusAttributes()
    COMMANDS_THE_ELEMENTS = FocusAttributes()
    ADAPTS_TO_ANY_ENVIRONMENT = FocusAttributes()
    INTEGRATES_WEAPONRY = FocusAttributes()
    PROCESSES_INFORMATION = FocusAttributes()
    COMMANDS_THE_UNDEAD = FocusAttributes()
    PRACTICES_SOUL_SORCERY = FocusAttributes()
    REGENERATES_TISSUE = FocusAttributes()
    WORKS_MIRACLES = FocusAttributes()
    INFILTRATES = FocusAttributes()


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
