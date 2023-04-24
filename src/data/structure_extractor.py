from kor.extraction import create_extraction_chain
from kor.nodes import Object, Text, Number
from langchain.chat_models import ChatOpenAI


class StructureExtractors:
    def __init__(self):
        self.schemas = [
            Object(
                id="creature",
                description="An entity, being, or construct which characters can interact with, "
                            "of varying degrees of dangerousness and friendliness.",
                examples=[
                    ("AGANAR 5 (15)\n A night spent in the grip of vivid, sensual dreams might be harmless, "
                     "nothing more than the mind’s nocturnal wanderings in unexpected places. Then again, the dreams "
                     "might be manifestations brought on by an aganar’s feeding, visions and fantasies stirred to "
                     "life in sleep to nourish a weird parasitic creature that creeps from its underground lair under "
                     "night’s cover.\n" +
                     "Motive: Devour the dreams of living creatures\n" +
                     """Environment (Ardeyn | Magic): Anywhere in the Daylands at night in groups of one to three; 
                     anywhere in the Night Vault in groups of three to ten 
                     Health: 21
                     Damage Inflicted: 5 points
                     Movement: Short
                     Modifications: All tasks related to perception as level 8; 
                     all tasks related to climbing as level 6. 
                     Combat: As generally peaceful creatures, aganars do not initiate fights. 
                     They want only to feed. When one comes within short range of a sleeping creature it can see 
                     (or within immediate range of a sleeping creature it can’t see because of a solid obstacle), 
                     it begins to feed on the victim’s psychic essence. The target must make an Intellect defense roll. 
                     On a failure, the aganar inflicts 5 points of Intellect damage, and the victim treats the next 
                     recovery roll he makes within twenty-four hours as if he had rolled a 1. After inflicting this 
                     damage, an aganar usually scuttles off. Once a victim takes this damage, he does not dream for 
                     several days.
                     Interaction: Aganars communicate by flashing stolen dream images at each other on their 
                     bioluminescent hides in complex patterns. 
                     Use: If the PCs descend into the Night Vault to find a spirit or seek out something else in that 
                     dark and foreboding place, they might gain the service of an aganar as a guide - provided they 
                     discern the meaning of its bioluminescent images and come up with some way of flashing images back 
                     in turn.
                     """, [{"type": "Aganar"},
                           {"motive": "Devour the dreams of living creatures"},
                           {"environment": "Ardeyn | Magic"},
                           {"level": "5"},
                           {"health": "21"},
                           {"damage_inflicted": "5"}]),
                ],
                attributes=[
                    Text(
                        id="type",
                        description="The kind of creature this is.",
                    ),
                    Text(
                        id="motive",
                        description="This entry is a way to help the GM understand what a creature or NPC wants.  "
                                    "Every creature wants something, even if it's just to be left alone."
                    ),
                    Text(
                        id="environment",
                        description="Lists the Recursions of Origin | Laws of Origin.  This entry describes whether a"
                                    " creature tends to be solitary or travel in groups and what kind of terrain it"
                                    "inhabits.  This entry also lists the creature's recursion of origin and the law"
                                    "that it operates under. If no recursion of origin is listed, the creature might"
                                    "be found in any recursion that includes the given law"
                    ),
                    Number(
                        id="level",
                        description="All creatures (and NPCs) have a level.  The level determines the target number"
                                    "a PC must reach to attack or defend agasint the opponent,  In each entry, the"
                                    "target number for the creature or NPC is listed in parentheses after the level."
                                    "The target number is three times the level"
                    ),
                    Number(
                        id="health",
                        description="The number of health points a creature has.  This is usually equal to its target"
                                    "number, and is the amount of damage a creature can take before it is killed or"
                                    "incapacitated."
                    ),
                    Number(
                        id="damage_inflicted",
                        description="The amount of damage a creature inflicts with a successful attack.  This is"
                    )
                ],
                many=True,
            )
        ]
