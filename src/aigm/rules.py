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

WorldAttributes = namedtuple('WorldAttributes',
                             ['name', 'description', 'level', 'laws', 'foci', 'playable_races', 'skills',
                              'size', 'spark_percentage', 'connection_to_earth', 'connection_to_strange',
                              'connection_to_recursions', 'traits', 'arrival_location', 'is_prime', 'facts_players_know',
                              'facts_players_may_learn'])


class World(Enum):
    EARTH = WorldAttributes(name='Earth', description='The world you know and love.',
                            level=5, laws=[Laws.STANDARD_PHYSICS],
                            foci=[Focus.CONDUCTS_WEIRD_SCIENCE, Focus.ENTERTAINS, Focus.IS_LICENSED_TO_CARRY,
                                  Focus.LEADS, Focus.LOOKS_FOR_TROUBLE, Focus.OPERATES_UNDERCOVER,
                                  Focus.SOLVES_MYSTERIES, Focus.WORKS_THE_SYSTEM],
                            playable_races=['Human'], skills=[], size=0, spark_percentage=100,
                            connection_to_earth="is Earth", connection_to_strange="No direct connection",
                            connection_to_recursions="various gates", traits=[],
                            arrival_location="Seattle Space Needle, among the crowds", facts_players_know=[],
                            facts_players_may_learn=[], is_prime=True)
    ATLANTIS = WorldAttributes(name='Atlantis', description='The lost city of Atlantis.', level=6,
                               laws=[Laws.MAGIC, Laws.MAD_SCIENCE], playable_races=['Human', 'Atlantean'],
                               skills=['Atlantis lore'], size=20000, spark_percentage=20,
                               #foci=[Focus.ADAPTS_TO_ANY_ENVIRONMENT, Focus.CONDUCTS_WEIRD_SCIENCE, Focus.ENTERTAINS,
                               #      Focus.INTEGRATES_WEAPONRY, Focus.LEADS, Focus.OPERATES_UNDERCOVER,
                               #      Focus.PROCESSES_INFORMATION, Focus.PRACTICES_SOUL_SORCERY, Focus.REGENERATES_TISSUE,
                               #      Focus.WIELDS_TWO_WEAPONS_AT_ONCE, Focus.WORKS_MIRACLES]), skills=['Atlantis lore'],
                              connection_to_earth="at least one gate in the heart of the island",
                              connection_to_strange="deep deep underwater", connection_to_recursions="various gates")
    RUK = WorldAttributes(name='Ruk', description='The world of Ruk.', level=4, laws=[Laws.MAD_SCIENCE],
                          foci=[Focus.ADAPTS_TO_ANY_ENVIRONMENT, Focus.INFILTRATES])


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
