from character import *


class Distance(Enum):
    IMMEDIATE = auto()
    SHORT = auto()
    MEDIUM = auto()
    LONG = auto()


class Laws(Enum):
    STANDARD_PHYSICS = auto()
    MAGIC = auto()
    MAD_SCIENCE = auto()
    PSIONICS = auto()
    SUBSTANDARD_PHYSICS = auto()
    EXOTIC = auto()


@dataclass
class World:
    name: str
    description: str
    level: int
    laws: List[Laws]
    foci: List[Focus]
    playable_races: List[str]
    skills: List[str]
    size_sq_miles: int
    spark_percentage: int
    connection_to_earth: str
    connection_to_strange: str
    connection_to_recursions: str
    traits: List[str]
    arrival_location: str
    is_prime: bool
    facts_players_know: List[str]
    facts_players_may_learn: List[str]


@dataclass
class Creature:
    creature_type: str
    name: str
    level: int
    health: int
    damage_inflicted: int
    combat_overview: str
    combat_actions: List[str]
    level_modifications: List[(str, int)]
    description: str
    motive: str
    interaction: str
    movement: Dict[str, Distance]
    world: World
    environment: str
    loot_currency: int
    loot_cyphers: List[Cypher]
    loot_artifacts: List[Artifact]
    loot_other: List[str]


class GateType(Enum):
    MATTER = auto()
    TRANSLATION = auto()


def narrate_translation(characters: List[Character], world: World, gate_type: GateType):
    pass


def narrate_start_of_encounter(characters: List[Character], world: World, creatures: List[Creature]):
    char_names = [char.name for char in characters]
    char_descriptors = [char.descriptor.name.lower() for char in characters]
    char_types = [char.character_type.name.lower() for char in characters]
    char_foci = [char.focus.name.lower().replace('_', ' ') for char in characters]

    world_name = world.value.name
    world_description = world.value.description

    creature_names = [creature.name for creature in creatures]
    creature_descriptions = [creature.description for creature in creatures]

    # Create the narrative for the characters
    character_narrative = "In the world of {}, {} the {} {} and friends find themselves in a {}.".format(
        world_name,
        ", ".join(["{} the {} {}".format(name, descriptor, focus) for name, descriptor, focus in zip(char_names, char_descriptors, char_foci)]),
        world_description
    )

    # Create the narrative for the encounter
    encounter_narrative = "Suddenly, they come across {}.".format(
        ", ".join(["{} ({})".format(name, description) for name, description in zip(creature_names, creature_descriptions)])
    )

    # Combine the narratives and return the result
    prompt = "{} {}".format(character_narrative, encounter_narrative)
    return prompt
