expmultiplier = 1

commonSpirits = ("Tiger", "Eagle", "Boar", "Snake", "Lion", "Fox", "Horse", "Peacock", "Swan", "Octopus", "Hedgehog", "Wolf", "Cat")
rareSpirits = ("Dolphin", "Shark", "Elephant", "Rhino", "Gorilla", "Ox", "Bear", "Whale", "Crocodile")
legendarySpirits = ("Dodo", "T_Rex", "Sauropod", "Mammoth")
mythicalSpirits = ("Leviathan", "Unicorn", "Phoenix", "Dragon")
adminSpirits = ("True Phoenix")

spiritEmoji = {
    "dragon": ":dragon:",
    "unicorn": ":unicorn:",
    "phoenix": "<:phoenixspirit:790707708185280542>",
    "leviathan": "<:leviathanspirit:790715462908379167>",
    "true phoenix": "<a:phoenixflap:790698766880997377>",
}

for i in commonSpirits:
    spiritEmoji.update({i.lower(): ":"+i.lower()+":"})
for i in rareSpirits:
    spiritEmoji.update({i.lower(): ":"+i.lower()+":"})
for i in legendarySpirits:
    spiritEmoji.update({i.lower(): ":"+i.lower()+":"})

#stats are: (HP, ATK, DEF, EVA)
spiritStats = {
    "Bear": (700, 120, 20, 10),
    "Tiger": (550, 130, 25, 20),
    "Eagle": (400, 105, 20, 55),
    "Boar": (450, 115, 20, 25),
    "Snake": (350, 130, 20, 50),
    "Gorilla": (675, 120, 20, 10),
    "Rhino": (600, 120, 25, 15),
    "Lion": (550, 130, 30, 15),
    "Ox": (700, 110, 25, 10),
    "Fox": (450, 110, 20, 30),
    "Horse": (600, 110, 20, 25),
    "Shark": (800, 125, 10, 10),
    "Peacock": (400, 90, 20, 40),
    "Swan": (400, 100, 25, 40),
    "Octopus": (400, 100, 5, 35),
    "Hedgehog": (450, 100, 60, 25),
    "Wolf": (550, 110, 20, 40),
    "Cat": (400, 100, 20, 40),
    "Goat": (500, 110, 20, 25),
    "Elephant": (900, 110, 40, 5),
    "Whale": (1000, 105, 35, 5),
    "Crocodile": (700, 120, 40, 20),
    "Dolphin": (550, 110, 35, 30),
    "Dodo": (200, 50, 50, 25),
    "T_Rex": (850, 150, 80, 25),
    "Sauropod": (1200, 130, 80, 5),
    "Mammoth": (1100, 140, 75, 5),
    "Unicorn": (700, 150, 35, 35),
    "Phoenix": (500, 140, 20, 55),
    "Leviathan": (1000, 130, 75, 10),
    "Dragon": (950, 150, 85, 25),
    "True Phoenix": (1000, 200, 100, 55),
}

spiritMoves = {
    "Bear": ("Scratch", "Bite", "Maul"),
    "Tiger": ("Scratch", "Bite", "Grapple", "Crunch"),
    "Eagle": ("Scratch", "Peck"),
    "Boar": ("Headbutt", "Gore"),
    "Snake": ("Bite", "Crunch"),
    "Gorilla": ("Pound", "Grapple"),
    "Rhino": ("Headbutt", "Gore"),
    "Lion": ("Scratch", "Bite"),
    "Ox": ("Headbutt", "Gore"),
    "Fox": ("Scratch", "Bite"),
    "Horse": ("Headbutt", "Bite"),
    "Dolphin": ("Headbutt", "Bite", "Spout"),
    "Shark": ("Bite", "Crunch", "Maul"),
    "Peacock": ("Scratch", "Peck"),
    "Swan": ("Peck", "Scratch"),
    "Octopus": ("Grapple", "Peck"),
    "Hedgehog": ("Scratch", "Bite"),
    "Wolf": ("Scratch", "Bite"),
    "Cat": ("Scratch", "Bite"),
    "Goat": ("Gore", "Headbutt"),
    "Elephant": ("Pound", "Headbutt", "Gore", "Trample"),
    "Whale": ("Pound", "Crunch", "Spout"),
    "Crocodile": ("Bite", "Crunch", "Maul"),
    "Dodo": ("Peck", "Scratch", "Headbutt"),
    "T_Rex": ("Bite", "Crunch", "Maul"),
    "Sauropod": ("Headbutt", "Bite", "Trample"),
    "Unicorn": ("Headbutt", "Bite", "Gore", "Psychic Crush"),
    "Mammoth": ("Pound", "Headbutt", "Gore", "Trample"),
    "Phoenix": ("Whirlwind", "Peck", "Inferno"),
    "Leviathan": ("Crunch", "Whirlwind", "Spout"),
    "Dragon": ("Scratch", "Bite", "Whirlwind", "Dragon Breath"),
    "True Phoenix": ("Whirlwind", "Inferno", "Psychic Crush"),
}

moveDamage = {
    "Peck": 1,
    "Grapple": 1,
    "Scratch": 1,
    "Pound": 1,
    "Bite": 1.1,
    "Headbutt": 1.1,
    "Gore": 1.2,
    "Crunch": 1.25,
    "Maul": 1.3,
    "Trample": 1.3,
    "Spout": 1.3,
    "Whirlwind": 1.35,
    "Psychic Crush": 1.5,
    "Inferno": 1.5,
    "Dragon Breath": 1.5,
    "Snowball": 1,
    "Sing": 0,
    "Harmony": 0,
    "Developer's Smite": 9999,
}


commonSearchableTalismans = ("Ankh", "Amulet", "Claw", "Bracelet")
rareSearchableTalismans = ("Jade Dragon", "Golden Phoenix", "Silver Unicorn", "Bronze Mammoth", "Onyx Leviathan")
shopTalismans = ("Ankh", "Amulet", "Claw", "Bracelet", "Bamboo Panda", "Amber Leopard", "Granite Ram")

commonTalismans = ("Ankh", "Amulet", "Claw", "Bracelet")
uncommonTalismans = ("Bamboo Panda", "Amber Leopard", "Granite Ram")
rareTalismans = ("Jade Dragon", "Golden Phoenix", "Silver Unicorn", "Bronze Mammoth", "Onyx Leviathan")

tsellPrices = {
    "common": 20,
    "uncommon": 40,
    "rare": 80,
    "easter_egg": 100,
}

MerchantTLists = {
    0: ("Claw", "Jade Dragon", "Golden Phoenix"),
    1: ("Ankh", "Silver Unicorn", "Bronze Mammoth"),
    2: ("Claw", "Onyx Leviathan", "Golden Phoenix"),
    3: ("Amulet", "Silver Unicorn", "Onyx Leviathan"),
    4: ("Ankh", "Bracelet", "Bronze Mammoth"),
    5: ("Amulet", "Claw", "Onyx Leviathan"),
    6: ("Jade Dragon", "Bronze Mammoth", "Onyx Leviathan"),
}

talismanInfo = {
    "None": "",
    "Ankh": "(+10% ALL except EVA)",
    "Amulet": "(+30% HP)",
    "Claw": "(+30% ATK)",
    "Bracelet": "(+15% EVA)",
    "Bamboo Panda": "(+50% HP)",
    "Amber Leopard": "(+50% ATK)",
    "Granite Ram": "(+25% EVA)",
    "Jade Dragon": "(+25% ALL)",
    "Golden Phoenix": "(+30% ATK, EVA)",
    "Silver Unicorn": "(+35% EVA)",
    "Bronze Mammoth": "(+70% HP, -10% EVA)",
    "Onyx Leviathan": "(+60% HP, +10% ATK)",
    "Easter Egg": "(NO BOOSTS)",
    "Incarnation of Epicness": "(TOO EPIC)",
}

talismanIDs = {
    1: "Ankh",
    2: "Amulet",
    3: "Claw",
    4: "Bracelet",
    5: "Bamboo Panda",
    6: "Amber Leopard",
    7: "Granite Ram",
}

talismanPrices = {
    "Ankh": 30,
    "Claw": 40,
    "Amulet": 40,
    "Bracelet": 50,
    "Bamboo Panda": 150,
    "Amber Leopard": 150,
    "Granite Ram": 200,
    "Bronze Mammoth": 300,
    "Jade Dragon": 400,
    "Golden Phoenix": 400,
    "Silver Unicorn": 400,
    "Onyx Leviathan": 400,
}

#stats are: (HP, ATK, DEF, EVA)
talismanBoosts = {
    "None": (1, 1, 1, 1),
    "Ankh": (1.1, 1.1, 1.1, 1),
    "Claw": (1, 1.3, 1, 1),
    "Amulet": (1.3, 1, 1, 1),
    "Bracelet": (1, 1, 1, 1.15),
    "Bamboo Panda": (1.5, 1, 1, 1),
    "Amber Leopard": (1, 1.5, 1, 1),
    "Granite Ram": (1, 1, 1, 1.25),
    "Jade Dragon": (1.25, 1.25, 1.25, 1.25),
    "Golden Phoenix": (1, 1.3, 1, 1.3),
    "Silver Unicorn": (1, 1, 1, 1.35),
    "Bronze Mammoth": (1.7, 1, 1, 0.9),
    "Onyx Leviathan": (1.6, 1.1, 1, 1),
    "Easter Egg": (1, 1, 1, 1),
    "Incarnation of Epicness": (1.5, 1.5, 1.5, 1.5),
}


commonArtifacts = ("Skull", "Spirit Stone", "Moon Rock", "Spirit Urn")
rareArtifacts = ("Ghost Candle", "Spirit Orb", "Rune")
superRareArtifacts = ("Unstable Energy", "Stardust")

artifactLevels = {
    "Skull": (1, 1),
    "Spirit Stone": (1, 2),
    "Moon Rock": (1, 3),
    "Spirit Urn": (2, 3),
    "Ghost Candle": (2, 4),
    "Spirit Orb": (3, 4),
    "Rune": (4, 6),
    "Unstable Energy": (8, 10),
    "Stardust": (9, 10),
}

artifactEmojis = {
    "Skull": ":skull:",
    "Spirit Stone": ":gem:",
    "Moon Rock": ":new_moon:",
    "Spirit Urn": ":urn:",
    "Ghost Candle": ":candle:",
    "Spirit Orb": ":crystal_ball:",
    "Rune": ":om_symbol:",
    "Unstable Energy": ":cyclone:",
    "Stardust": ":sparkles:",
}