CATEGORY=[
    ["魔法罠破壊","SPELL_TRAP_DESTROY"],
    ["モンスター破壊","MONSTER_DESTROY"],
    ["除外","REMOVE"],
    ["墓地へ送る","SEND_GRAVE"],
    ["手札に戻す","SEND_HAND"],
    ["デッキに戻す","SEND_DECK"],
    ["手札破壊","HAND_DESTROY"],
    ["デッキ破壊","DECK_DESTROY"],
    ["ドロー","DRAW"],
    ["サーチ","SEARCH"],
    ["墓地回収","RECOVERY_GRAVE"],
    ["表示形式","POSITION"],
    ["コントロール","CONTROL"],
    ["攻撃力守備力","ATK_DEF"],
    ["戦闘ダメージ","BATTLE_DAMAGE"],
    ["連続攻撃","MULTI_ATTACK"],
    ["攻撃制限","ATTACK_LIMIT"],
    ["直接攻撃","DIRECT_ATTACK"],
    ["特殊召喚","SPECIAL_SUMMON"],
    ["トークン","TOKEN"],
    ["種族関連","RACE"],
    ["属性関連","ATTRIBUTE"],
    ["ライフダメージ","LIFE_DAMAGE"],
    ["ライフ回復","RECOVER_LIFE"],
    ["破壊耐性","INDESTRUCTABLE"],
    ["効果耐性","IMMUNE"],
    ["カウンター","COUNTER"],
    ["ギャンブル","GAMBLE"],
    ["融合関連","FUSION"],
    ["シンクロ関連","SYNCHRO"],
    ["エクシーズ関連","XYZ"],
    ["効果無効","DISABLE"]
]

CATEGORY_VALUE={}
i=0
for data in CATEGORY:
    name=data[1]
    CATEGORY_VALUE[name]=2**i
    i+=1

def calcCategory(values):
    rtn=0
    for key,val in values.items():
        if key.startswith("-CATEGORY_") and val:
            ctype=key.replace("-","").replace("CATEGORY_","")
            rtn+=CATEGORY_VALUE[ctype]
    return rtn