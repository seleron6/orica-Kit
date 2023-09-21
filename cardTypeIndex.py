TYPE_VALUE={
    "MONSTER":1,
    "SPELL":2,
    "TRAP":4,
    "NORMAL":16,
    "EFFECT":32,
    "FUSION":64,
    "RITUAL":128,
    "SYNCHRO":8192,
    "XYZ":8388608,
    "PENDULUM":16777216,
    "LINK":67108864,
    "SPECIAL_SUMMON":33554432,
    "FLIP":2097152,
    "TOON":4194304,
    "SPIRIT":512,
    "UNION":1024,
    "GEMINI":2048,
    "TUNER":4096,
    "EQUIP":262144,
    "QUICK_PLAY":65536,
    "FIELD":524288,
    "CONTINUOUS":131072,
    "COUNTER":1048576,
    "TOKEN":16384
}

CHECK_INDEX=[f"-CARD_TYPE_{name}-" for name in TYPE_VALUE.keys()]

MONSTER_CHECK=[
    "-CARD_TYPE_NORMAL-",
    "-CARD_TYPE_EFFECT-",
    "-CARD_TYPE_FUSION-",
    "-CARD_TYPE_RITUAL-",
    "-CARD_TYPE_SYNCHRO-",
    "-CARD_TYPE_XYZ-",
    "-CARD_TYPE_PENDULUM-",
    "-CARD_TYPE_LINK-",
    "-CARD_TYPE_SPECIAL_SUMMON-",
    "-CARD_TYPE_FLIP-",
    "-CARD_TYPE_TOON-",
    "-CARD_TYPE_SPIRIT-",
    "-CARD_TYPE_UNION-",
    "-CARD_TYPE_GEMINI-",
    "-CARD_TYPE_TUNER-",
    "-CARD_TYPE_TOKEN-"
]

SPELL_CHECK=[
    "-CARD_TYPE_RITUAL-",
    "-CARD_TYPE_EQUIP-",
    "-CARD_TYPE_QUICK_PLAY-",
    "-CARD_TYPE_FIELD-",
    "-CARD_TYPE_CONTINUOUS-"
]

TRAP_CHECK=[
    "-CARD_TYPE_CONTINUOUS-",
    "-CARD_TYPE_COUNTER-"
]

LINK_MARKER={
    "_LOWER_LEFT":1,
    "_LOWER":2,
    "_LOWER_RIGHT":4,
    "_LEFT":8,
    "_RIGHT":32,
    "_UPPER_LEFT":64,
    "_UPPER":128,
    "_UPPER_RIGHT":256
}

SCALE=[
    "-SCALE_LEFT-",
    "-SCALE_LEFT_UP-",
    "-SCALE_LEFT_DOWN-",
    "-SCALE_RIGHT-",
    "-SCALE_RIGHT_UP-",
    "-SCALE_RIGHT_DOWN-"
]

ATTRIBUTE_JE={
    "－":"",
    "地":"earth",
    "水":"water",
    "炎":"fire",
    "風":"wind",
    "光":"light",
    "闇":"dark",
    "神":"divine"
}

RACE_JE={
    "戦士":"Warrior",
    "魔法使い":"Spellcaster",
    "天使":"Fairy",
    "悪魔":"Fiend",
    "アンデット":"Zombie",
    "機械":"Machine",
    "水":"Aqua",
    "炎":"Pyro",
    "岩石":"Rock",
    "鳥獣":"Winged Beast",
    "植物":"Plant",
    "昆虫":"Insect",
    "雷":"Thunder",
    "ドラゴン":"Dragon",
    "獣":"Beast",
    "獣戦士":"Beast Warrior",
    "恐竜":"Dinosaur",
    "魚":"Fish",
    "海竜":"Sea Serpent",
    "爬虫類":"Reptile",
    "サイキック":"Psychic",
    "幻神獣":"Divine-Beast",
    "創造神":"Creater",
    "幻竜":"Wyrm",
    "サイバース":"Cyberse",
    "幻想魔":"Illusion"
}

MONSTER_TYPE={
    "SPECIAL_SUMMON":"特殊召喚",
    "FUSION":"融合",
    "RITUAL":"儀式",
    "SYNCHRO":"シンクロ",
    "XYZ":"エクシーズ",
    "PENDULUM":"ペンデュラム",
    "LINK":"リンク",
    "FLIP":"リバース",
    "TOON":"トゥーン",
    "SPIRIT":"スピリット",
    "UNION":"ユニオン",
    "GEMINI":"デュアル",
    "TUNER":"チューナー",
    "NORMAL":"通常",
    "EFFECT":"効果"
}

def calcType(values):
    rtn=0
    for key,val in values.items():
        if key.startswith("-CARD_TYPE") and val:
            ctype=key.replace("-","").replace("CARD_TYPE_","")
            rtn+=TYPE_VALUE[ctype]
    return rtn