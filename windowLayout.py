import PySimpleGUI as sg
from setcodeIndex import readSetCodes, readOricaSetCodes
import cardTypeIndex as cti
import cv2
import numpy as np

WIDTH=530
HEIGHT=500
SETCODE_WIDTH=WIDTH/2.8
CANVAS_WIDTH=355
CANVAS_HEIGHT=int(CANVAS_WIDTH*1.458)
ADJUST_WIDTH=WIDTH
ADJUST_HEIGHT=int(HEIGHT*2/3)
BIGCANVAS_WIDTH=590
BIGCANVAS_HEIGHT=860

ATTRIBUTE=[
    "－",
    "地",
    "水",
    "炎",
    "風",
    "光",
    "闇",
    "神"
]
ATTRIBUTE_VALUE={ATTRIBUTE[i+1]:2**i for i in range(len(ATTRIBUTE)-1)}
RACE=[
    "－",
    "戦士",
    "魔法使い",
    "天使",
    "悪魔",
    "アンデット",
    "機械",
    "水",
    "炎",
    "岩石",
    "鳥獣",
    "植物",
    "昆虫",
    "雷",
    "ドラゴン",
    "獣",
    "獣戦士",
    "恐竜",
    "魚",
    "海竜",
    "爬虫類",
    "サイキック",
    "幻神獣",
    "創造神",
    "幻竜",
    "サイバース",
    "幻想魔"
]
RACE_VALUE={RACE[i+1]:2**i for i in range(len(RACE)-1)}

def mainWindowLayout():
    STATUS_WIDTH=WIDTH*5/11
    STATUS_HEIGHT=HEIGHT*11/18-4
    PRESET_WIDTH=WIDTH-STATUS_WIDTH
    CARDTYPE_HEIGHT=STATUS_HEIGHT*12/17
    PRESET_HEIGHT=(STATUS_HEIGHT-CARDTYPE_HEIGHT)/2
    PARAMETER_WIDTH=PRESET_WIDTH
    PARAMETER_HEIGHT=PRESET_HEIGHT
    CARDTYPE_WIDTH=PRESET_WIDTH
    CATEGORY_WIDTH=WIDTH+5
    CATEGORY_HEIGHT=HEIGHT-STATUS_HEIGHT
    STATUS_TEXT_SIZE=(6,1)
    STATUS_INPUT_SIZE=(11,1)
    STATUS_SETCODE_SIZE=(5,1)
    STATUS_TEXT_WITH_BUTTON_SIZE=(3,1)
    PRESET_PAD=(3,0)

    CARD_TYPE=[
        ["モンスター","MONSTER"],
        ["魔法","SPELL"],
        ["罠","TRAP"],
        ["通常","NORMAL"],
        ["効果","EFFECT"],
        ["融合","FUSION"],
        ["儀式","RITUAL"],
        ["シンクロ","SYNCHRO"],
        ["エクシーズ","XYZ"],
        ["ペンデュラム","PENDULUM"],
        ["リンク","LINK"],
        ["特殊召喚","SPECIAL_SUMMON"],
        ["リバース","FLIP"],
        ["トゥーン","TOON"],
        ["スピリット","SPIRIT"],
        ["ユニオン","UNION"],
        ["デュアル","GEMINI"],
        ["チューナー","TUNER"],
        ["装備","EQUIP"],
        ["速攻","QUICK_PLAY"],
        ["フィールド","FIELD"],
        ["永続","CONTINUOUS"],
        ["カウンター","COUNTER"],
        ["トークン","TOKEN"]
    ]

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

    status=sg.Frame("ステータス",
        [
            [
                sg.Text("ot",size=STATUS_TEXT_SIZE),
                sg.Combo(["OCG","TCG","OCG/TCG","Custom"],key="-OT-",readonly=True,default_value="Custom",size=STATUS_INPUT_SIZE)
            ],
            [
                sg.Text("id",size=STATUS_TEXT_SIZE),
                sg.Input(key="-ID-",size=STATUS_INPUT_SIZE,default_text=0),
                sg.Button("↑",key="-ID_UP-",pad=(1,1)),
                sg.Button("↓",key="-ID_DOWN-",pad=(1,1))
            ],
            [
                sg.Text("alias",size=STATUS_TEXT_SIZE),
                sg.Input(key="-ALIAS-",size=STATUS_INPUT_SIZE,default_text=0),
                sg.Button("↑",key="-ALIAS_UP-",pad=(1,1)),
                sg.Button("↓",key="-ALIAS_DOWN-",pad=(1,1))
            ],
            [
                sg.Button("setcode",pad=((0.5,3.5),(1,1))),
                sg.Input(key="-SETCODE-",size=(17,1),default_text=0,pad=((6,5),1),enable_events=True),
                sg.Button("↑",key="-SETCODE_UP-",pad=(1,1)),
                sg.Button("↓",key="-SETCODE_DOWN-",pad=(1,1)),
            ],
            [
                sg.Column([
                    [
                        sg.Text("atk",size=STATUS_TEXT_WITH_BUTTON_SIZE,pad=(0,0)),
                        sg.Button("?",key="-ATK_?-",pad=((6.8,3.5),(1,1))),
                        sg.Input(key="-ATK-",size=STATUS_SETCODE_SIZE,default_text=0,pad=((6,5),1),disabled_readonly_background_color="gray"),
                        sg.Button("↑",key="-ATK_UP-",pad=((0,1),1)),
                        sg.Button("↓",key="-ATK_DOWN-",pad=(1,1)),
                    ],
                    [
                        sg.Text("def",size=STATUS_TEXT_WITH_BUTTON_SIZE,pad=(0,0)),
                        sg.Button("?",key="-DEF_?-",pad=((6.8,3.5),(1,1))),
                        sg.Input(key="-DEF-",size=STATUS_SETCODE_SIZE,default_text=0,pad=((6,5),1),readonly=False,disabled_readonly_background_color="gray"),
                        sg.Button("↑",key="-DEF_UP-",pad=((0,1),1)),
                        sg.Button("↓",key="-DEF_DOWN-",pad=(1,1)),
                    ],
                    [
                        sg.Text("level",size=STATUS_TEXT_SIZE,pad=(0,0)),
                        sg.Input(key="-LEVEL-",size=STATUS_SETCODE_SIZE,default_text=0,pad=((10,5),1),readonly=False,disabled_readonly_background_color="gray"),
                        sg.Button("↑",key="-LEVEL_UP-",pad=((0,1),1)),
                        sg.Button("↓",key="-LEVEL_DOWN-",pad=(1,1))
                    ]
                ]),
                sg.Frame("marker",[
                    [
                        sg.Checkbox("",False,key=f"-LINK_MARKER_UPPER{Ename}-",pad=(0,0),enable_events=True,disabled=True) for Ename in ["_LEFT","","_RIGHT"]
                    ],
                    [
                        sg.Checkbox("",False,key=f"-LINK_MARKER{Ename}-",pad=(0,0),enable_events=True,disabled=True) for Ename in ["_LEFT","","_RIGHT"]
                    ],
                    [
                        sg.Checkbox("",False,key=f"-LINK_MARKER_LOWER{Ename}-",pad=(0,0),enable_events=True,disabled=True) for Ename in ["_LEFT","","_RIGHT"]
                    ]
                ],pad=(0,0))
            ],
            [
                sg.Text("attribute",size=STATUS_TEXT_SIZE),
                sg.Combo(ATTRIBUTE,key="-ATTRIBUTE-",readonly=True,default_value=ATTRIBUTE[0],size=STATUS_INPUT_SIZE)
            ],
            [
                sg.Text("race",size=STATUS_TEXT_SIZE),
                sg.Combo(RACE,key="-RACE-",readonly=True,default_value=ATTRIBUTE[0],size=(11,len(RACE)))
            ],
            [
                sg.Text("scale(l/r)",size=STATUS_TEXT_SIZE),
                sg.Input(key="-SCALE_LEFT-",size=STATUS_SETCODE_SIZE,default_text=0,pad=((6,5),1),disabled_readonly_background_color="gray",disabled=True),
                sg.Button("↑",key="-SCALE_LEFT_UP-",pad=((0,1),1),disabled=True),
                sg.Button("↓",key="-SCALE_LEFT_DOWN-",pad=(1,1),disabled=True),
                sg.Input(key="-SCALE_RIGHT-",size=STATUS_SETCODE_SIZE,default_text=0,disabled_readonly_background_color="gray",disabled=True),
                sg.Button("↑",key="-SCALE_RIGHT_UP-",pad=((0,1),1),disabled=True),
                sg.Button("↓",key="-SCALE_RIGHT_DOWN-",pad=(1,1),disabled=True)
            ],
        ],size=(STATUS_WIDTH,STATUS_HEIGHT),pad=(0,0)
    )
    preset=sg.Frame("プリセット",
        [
            [
                sg.Radio("フリー","PRESET_RADIO",True,key="-PRESET_RADIO_FREE-",pad=PRESET_PAD,enable_events=True),
                sg.Radio("モンスター","PRESET_RADIO",False,key="-PRESET_RADIO_MONSTER-",pad=PRESET_PAD,enable_events=True),
                sg.Radio("魔法","PRESET_RADIO",False,key="-PRESET_RADIO_SPELL-",pad=PRESET_PAD,enable_events=True),
                sg.Radio("罠","PRESET_RADIO",False,key="-PRESET_RADIO_TRAP-",pad=PRESET_PAD,enable_events=True)
            ]
        ],size=(PRESET_WIDTH,PRESET_HEIGHT),pad=(0,0)
    )
    parameter=sg.Frame("",
        [
            [
                sg.Button("setcode",key="-PARAMETER_SETCODE-",size=(14,1),pad=(1,5)),
                sg.Input(hex(0),key="-PARAMETER_SETCODE_HIDDEN-",visible=False,readonly=True),
                sg.Button("type",key="-PARAMETER_TYPE-",size=(8,1),pad=(1,5)),
                sg.Input(0,key="-PARAMETER_TYPE_HIDDEN-",visible=False,readonly=True),
                sg.Button("category",key="-PARAMETER_CATEGORY-",size=(10,1),pad=(1,5)),
                sg.Input(0,key="-PARAMETER_CATEGORY_HIDDEN-",visible=False,readonly=True),
            ]
        ],size=(PARAMETER_WIDTH,PARAMETER_HEIGHT),pad=(0,0)
    )
    CARD_TYPE_CHECK=[sg.Checkbox(name,False,key=f"-CARD_TYPE_{Ename}-",size=(10,1),font=("Rounded Mplus",10),pad=((0,3),(0,4)),enable_events=True) for name,Ename in CARD_TYPE]
    cardType=sg.Frame("カードタイプ",
        [
            [cb for cb in CARD_TYPE_CHECK[i:i+3]] for i in range(0,len(CARD_TYPE_CHECK),3)
        ],size=(CARDTYPE_WIDTH,CARDTYPE_HEIGHT),pad=(0,0)
    )
    CATEGORY_CHECK=[sg.Checkbox(name,False,key=f"-CATEGORY_{Ename}-",size=(12,1),font=("Rounded Mplus",10),pad=((10,18),(0,4)),enable_events=True) for name,Ename in CATEGORY]
    category=sg.Frame("効果カテゴリー",
        [
            [cb for cb in CATEGORY_CHECK[i:i+4]] for i in range(0,len(CATEGORY_CHECK),4)
        ],size=(CATEGORY_WIDTH,CATEGORY_HEIGHT),pad=(0,0),expand_y=True
    )

    preset_cardType=sg.Column([
        [preset],
        [parameter],
        [cardType]
    ])

    layout=[
        [
            status,
            preset_cardType
        ],
        [category]
    ]
    return layout

def setcodeWindowLayout():
    SETCODE=readSetCodes()
    ORICA_SETCODE=readOricaSetCodes()
    NAMES=list(SETCODE.keys())
    ORICA_NAMES=list(ORICA_SETCODE.keys())
    CATNAME_SIZE=(40,23)
    CATEGORY_SIZE=(21,1)
    ocgCategoryName=[
        [
            sg.Text("検索"),
            sg.Input(key="-OCG_SEARCH-",default_text="",expand_x=True,enable_events=True),
        ],
        [
            sg.Listbox(NAMES,size=CATNAME_SIZE,key="-OCG_CATNAME-",enable_events=True,font=("Arial",9))
        ]
    ]
    ocgCategoryID=[
        sg.Text("0",key="-OCG_CATID-",relief=sg.RELIEF_RIDGE, border_width=2,size=(5,1),pad=((5,1),0)),
        sg.Input("0",key="-OCG_CATID_HIDDEN-",visible=False,readonly=True),
        sg.Button("上",key="-OCG_CATID_TOP-",pad=(1,1)),
        sg.Button("中",key="-OCG_CATID_CENTER-",pad=(1,1)),
        sg.Button("下",key="-OCG_CATID_UNDER-",pad=(1,1)),
        sg.Button("反映",key="-CATID_SET-",pad=(1,1))
    ]
    ocgLayout=[
        ocgCategoryName[0],
        ocgCategoryName[1],
        ocgCategoryID,
        [
            sg.Input(key='-CREATE_OCG_SETCODE_TXT-',enable_events=True,visible=False,readonly=True),
            sg.FileBrowse("setcode_ocg.txtを再生成",target='-CREATE_OCG_SETCODE_TXT-',expand_x=True,file_types=(("Conf Files", "*.conf"),))
        ]
    ]
    oricaCategoryName=[
        [
            sg.Text("検索"),
            sg.Input(key="-ORICA_SEARCH-",default_text="",expand_x=True,enable_events=True),
        ],
        [
            sg.Listbox(ORICA_NAMES,size=CATNAME_SIZE,key="-ORICA_CATNAME-",enable_events=True,font=("Arial",9))  
        ]
    ]
    oricaCategoryID=[
        sg.Text("0",key="-ORICA_CATID-",relief=sg.RELIEF_RIDGE, border_width=2,size=(5,1),pad=((5,1),0)),
        sg.Input("0",key="-ORICA_CATID_HIDDEN-",visible=False,readonly=True),
        sg.Button("上",key="-ORICA_CATID_TOP-",pad=(1,1)),
        sg.Button("中",key="-ORICA_CATID_CENTER-",pad=(1,1)),
        sg.Button("下",key="-ORICA_CATID_UNDER-",pad=(1,1)),
        sg.Button("反映",key="-CATID_SET2-",pad=(1,1))
    ]
    oricaLayout=[
        oricaCategoryName[0],
        oricaCategoryName[1],
        oricaCategoryID,
        [
            sg.Input(key='-CREATE_ORICA_SETCODE_TXT-',enable_events=True,visible=False,readonly=True),
            sg.FileBrowse("setcode_orica.txtを再生成",target='-CREATE_ORICA_SETCODE_TXT-',expand_x=True,file_types=(("Conf Files", "*.conf"),))
        ]
    ]
    layout=[
        [
            sg.Frame("",
                [
                    [
                        sg.TabGroup(
                            [[
                                sg.Tab("OCG",ocgLayout,key="-TAB_SETCODE_OCG-"),
                                sg.Tab("オリカ",oricaLayout,key="-TAB_SETCODE_ORICA-")
                            ]],key="-TAB_SETCODE_GROUP-",tab_background_color="gray",pad=(0,(0,10))
                        )
                    ],
                    [
                        sg.Input(key="-CATEGORY_TOP-",size=CATEGORY_SIZE,readonly=True,font=("Arial",9)),
                        sg.Input(0,key="-CATEGORY_TOP_HIDDEN-",readonly=True,visible=False),
                        sg.Button("x",key="-CATID_CLEAR_TOP-",pad=(0,0))
                    ],
                    [
                        sg.Input(key="-CATEGORY_CENTER-",size=CATEGORY_SIZE,readonly=True,font=("Arial",9)),
                        sg.Input(0,key="-CATEGORY_CENTER_HIDDEN-",readonly=True,visible=False),
                        sg.Button("x",key="-CATID_CLEAR_CENTER-",pad=(0,0))
                    ],
                    [
                        sg.Input(key="-CATEGORY_UNDER-",size=CATEGORY_SIZE,readonly=True,font=("Arial",9)),
                        sg.Input(0,key="-CATEGORY_UNDER_HIDDEN-",readonly=True,visible=False),
                        sg.Button("x",key="-CATID_CLEAR_UNDER-",pad=(0,0))
                    ]
                ],size=(SETCODE_WIDTH,HEIGHT+80)
            )
        ]
    ]
    return layout

def textWindowLayout():
    TEXT_WIDTH=WIDTH
    NAME_HEIGHT=HEIGHT/8
    TEXT_HEIGHT=HEIGHT/2
    STR_HEIGHT=HEIGHT-NAME_HEIGHT-TEXT_HEIGHT

    cardName=sg.Frame("",
        [
            [
                sg.Text("カード名",size=(8,1)),
                sg.Input(key="-CARD_NAME-",expand_x=True)
            ],
            [
                sg.Text("英名",size=(8,1)),
                sg.Input(key="-CARD_NAME_EN-",expand_x=True,disabled_readonly_background_color="gray")
            ]
        ],size=(TEXT_WIDTH,NAME_HEIGHT),expand_x=True
    )
    cardText=sg.Frame("",[[sg.TabGroup(
            [[
                sg.Tab("日テキスト",[[sg.Multiline("", disabled=False, key="-CARD_TEXT-",expand_x=True,expand_y=True)]],key="-TAB_TEXT_JP-"),
                sg.Tab("日Ｐテキスト",[[sg.Multiline("", disabled=False, key="-CARD_TEXT_P-",expand_x=True,expand_y=True)]],key="-TAB_TEXT_JP_P-"),
                sg.Tab("英テキスト",[[sg.Multiline("", disabled=False, key="-CARD_TEXT_EN-",expand_x=True,expand_y=True)]],key="-TAB_TEXT_EN-"),
                sg.Tab("英Ｐテキスト",[[sg.Multiline("", disabled=False, key="-CARD_TEXT_EN_P-",expand_x=True,expand_y=True)]],key="-TAB_TEXT_EN_P-")
            ]],key="-TAB_TEXT_GROUP-",expand_x=True,expand_y=True,tab_background_color="gray"
    )]],size=(TEXT_WIDTH,TEXT_HEIGHT),expand_x=True)
    cardStr=sg.Frame("str",
        [[
            sg.Column([
                [sg.Text(str(i).zfill(2)),sg.Input(key="-CARD_STR"+str(i)+"-",expand_x=True,size=(65,1))]for i in range(1,17)
            ],scrollable=True)
        ]],size=(TEXT_WIDTH,STR_HEIGHT),expand_x=True,expand_y=True
    )

    layout=[
        [cardName],
        [cardText],
        [cardStr]
    ]
    return layout

def sqlWindowLayout():
    layout=[
        sg.Column([[
            sg.Radio("datas","SQL_RADIO",True,key="-SQL_RADIO_DATA-",pad=(0,0),enable_events=True),
            sg.Radio("texts","SQL_RADIO",False,key="-SQL_RADIO_TEXT-",pad=(0,0),enable_events=True),
            sg.Radio("両方","SQL_RADIO",False,key="-SQL_RADIO_ALL-",pad=(0,0),enable_events=True),
            sg.Button("コピー",key="-SQL_COPY-",pad=(0,0)),
            sg.Button("リセット",key="-RESET-",pad=(0,0)),
        ]],justification="right")
    ]
    return layout

def previewWindowLayout():
    canvas = sg.Graph(
        (CANVAS_WIDTH, CANVAS_HEIGHT),
        (0, CANVAS_HEIGHT),
        (CANVAS_WIDTH, 0), 
        background_color='#000000',
        pad=(0, 0), 
        key='-CANVAS-', 
    )

    cardsettings=sg.Column([
        [
            sg.Radio("en","LANGUAGE",True,key="-LANGUAGE_EN-",enable_events=True),
        ],
        [
            sg.Radio("jp（ルビ未対応）","LANGUAGE",False,key="-LANGUAGE_JP-",enable_events=True)
        ],
        [
            sg.Button("テキスト調整",key="-TEXT_ADJUST-",pad=(0,0)),
        ],
        [
            sg.Input(key='-ILLUST_PATH-',enable_events=True,visible=False,readonly=True),
            sg.FileBrowse("イラスト挿入",target='-ILLUST_PATH-',key="-INSERT_IMAGE-",pad=(0,0),file_types=(("画像ファイル", "*.png *.jpg *.jpeg *.jpe"),))
        ],
        [
            sg.Button("拡大画像表示",key="-IMAGE_WINDOW-",pad=(0,0)),
        ],
        [
            sg.Button("保存",key="-IMAGE_SAVE-",pad=(0,0)),
        ],
        [
            sg.Multiline("", key="-ADJUST_TEXT_JP_HIDDEN-",visible=False),
            sg.Multiline("", key="-ADJUST_PTEXT_JP_HIDDEN-",visible=False),
            sg.Multiline("", key="-ADJUST_TEXT_EN_HIDDEN-",visible=False),
            sg.Multiline("", key="-ADJUST_PTEXT_EN_HIDDEN-",visible=False)
        ]
    ])

    layout=[
        [
            canvas,
            cardsettings
        ]
    ]
    return layout,canvas

def adjustWindowLayout(lang):
    if lang=="jp":
        jpTextLayout=[[sg.Multiline("", key="-ADJUST_TEXT_JP-",size=(ADJUST_WIDTH,ADJUST_HEIGHT),enable_events=True)]]
        jpPendulumTextLayout=[[sg.Multiline("", key="-ADJUST_PTEXT_JP-",size=(ADJUST_WIDTH,ADJUST_HEIGHT),enable_events=True)]]
        layout=[[
            sg.TabGroup(
                [[
                    sg.Tab("日テキスト",jpTextLayout,key="-TAB_ADJUST_TEXT_JP-"),
                    sg.Tab("日Ｐテキスト",jpPendulumTextLayout,key="-TAB_ADJUST_TEXT_JP_P-")
                ]],key="-TAB_ADJUST_GROUP-",tab_background_color="gray"
            )
        ]]
    else:
        enTextLayout=[[sg.Multiline("", key="-ADJUST_TEXT_EN-",size=(ADJUST_WIDTH,ADJUST_HEIGHT),enable_events=True)]]
        enPendulumTextLayout=[[sg.Multiline("", key="-ADJUST_PTEXT_EN-",size=(ADJUST_WIDTH,ADJUST_HEIGHT),enable_events=True)]]
        layout=[[
            sg.TabGroup(
                [[
                    sg.Tab("英テキスト",enTextLayout,key="-TAB_ADJUST_TEXT_EN-"),
                    sg.Tab("英Ｐテキスト",enPendulumTextLayout,key="-TAB_ADJUST_TEXT_EN_P-")
                ]],key="-TAB_ADJUST_GROUP-",tab_background_color="gray"
            )
        ]]
    return layout

def imageWindowLayout():
    canvas = sg.Graph(
        (BIGCANVAS_WIDTH, BIGCANVAS_HEIGHT),
        (0, BIGCANVAS_HEIGHT),
        (BIGCANVAS_WIDTH, 0), 
        background_color='#000000',
        pad=(0, 0), 
        key='-BIGCANVAS-', 
    )

    layout=[
        [
            canvas
        ],
    ]
    return layout,canvas

def saveWindowLayout():
    layout=[
        [
            sg.Frame("",[
                [
                    sg.Column([
                        [
                            sg.Text("名前",size=(5,1)),
                            sg.Input(key="-SAVE_NAME-",size=(10,1),default_text="")
                        ]
                    ])
                ],
                [
                    sg.Column([
                        [
                            sg.Text("拡張子",size=(5,1)),
                            sg.Combo(["jpg","png"],key="-SAVE_EXTENSION-",readonly=True,default_value="jpg",size=(10,1))
                        ]
                    ])
                ],
                [
                    sg.Column([
                        [
                            sg.Text("幅",size=(5,1)),
                            sg.Input(key="-SAVE_WIDTH-",size=(10,1),default_text=1180,enable_events=True)
                        ],
                        [
                            sg.Text("高さ",size=(5,1)),
                            sg.Input(key="-SAVE_HEIGHT-",size=(10,1),default_text=1720,enable_events=True)
                        ]
                    ]),
                    sg.Checkbox("縦横比を固定",False,key="-SET_ASPECT-",enable_events=True)
                ],
                [
                    sg.Column([
                        [
                            sg.Text("保存先",size=(5,1)),
                            sg.Input(key="-SAVE_FOLDER-",size=(20,1),default_text="./"),
                            sg.FolderBrowse("選択",target="-SAVE_FOLDER-")
                        ]
                    ])
                ],
                [
                    sg.Column([
                        [
                            sg.Button("保存",key="-SAVE_IMAGE-")
                        ]
                    ])
                ]
            ])
        ]
    ]
    return layout

def cdbLayout():
    datasHeader=['id','ot','alias','setcode','type','atk','def','level','race','attribute','category']
    textsHeader=['id','name','desc']
    [textsHeader.append(f"str{i}") for i in range(1,17)]
    datas=[]
    texts=[]
    datasLayout=[
        [
            sg.Table(
                datas,
                key="-CDB_DATAS-",
                headings=datasHeader,
                vertical_scroll_only=False,
                auto_size_columns=False,
                col_widths=[9,2,9,9,7,4,4,8,7,6,9],
                text_color='#000000',
                background_color='#cccccc',
                alternating_row_color='#ffffff',
                size=(100,23),
                enable_click_events=True
            )
        ]
    ]
    textsLayout=[
        [
            sg.Table(
                texts,
                key="-CDB_TEXTS-",
                headings=textsHeader,
                vertical_scroll_only=False,
                auto_size_columns=False,
                col_widths=[9,30,20,9,9,9,4,4,4,4,4,4,4,4,4,4,4,4,4],
                text_color='#000000',
                background_color='#cccccc',
                alternating_row_color='#ffffff',
                size=(100,23),
                enable_click_events=True,
                justification='left'
            )
        ]
    ]
    layout=[
        [
            sg.Frame("",
                [
                    [
                        sg.Text("cdb",size=(5,1)),
                        sg.Input(key="-CDB_PATH-",size=(20,1),default_text=sg.user_settings_get_entry('-cdbpath-', "./"),expand_x=True,readonly=True),
                        sg.FileBrowse("選択",target='-CDB_PATH-',file_types=(("cdb Files", "*.cdb"),),pad=(0,0)),
                        sg.Button("読み込み",key="-READ_CDB-",pad=(0,0))
                    ],
                ],expand_x=True
            )
        ],
        [
            sg.Frame("",[
                [
                    sg.TabGroup(
                        [[
                            sg.Tab("datas",datasLayout,key="-TAB_CDB_DATAS-"),
                            sg.Tab("texts",textsLayout,key="-TAB_CDB_TEXTS-")
                        ]],key="-TAB_CDB_GROUP-",tab_background_color="gray"
                    )
                ],
                [
                    sg.Column([
                        [
                            sg.Button("選択したレコードを削除",key="-DELETE_CDB-",pad=(0,0)),
                            sg.Button("cdbに書き込み",key="-WRITE_CDB-",pad=(0,0)),
                            sg.Button("レコードから読み込み",key="-LOAD_CDB-",pad=(0,0))
                        ]
                    ],justification="right")
                ]
            ])
        ]
    ]
    return layout

def datasLayout():
    layout=[
        [
            sg.Input("",visible=False,readonly=True,key="-CDB_PATH-"),
            sg.Frame("",[
                [
                    sg.Column([
                        [
                            sg.Text("id",justification="center",size=(9,1))
                        ],
                        [
                            sg.Input("",key="-DATA_DETAIL_ID-",size=(10,1),justification="right")
                        ]
                    ]),
                    sg.Column([
                        [
                            sg.Text("ot",size=(2,1),justification="center")
                        ],
                        [
                            sg.Input("",key="-DATA_DETAIL_OT-",size=(2,1),justification="right")
                        ]
                    ]),
                    sg.Column([
                        [
                            sg.Text("alias",size=(9,1),justification="center")
                        ],
                        [
                            sg.Input("",key="-DATA_DETAIL_ALIAS-",size=(10,1),justification="right")
                        ]
                    ]),
                    sg.Column([
                        [
                            sg.Text("setcode",size=(14,1),justification="center")
                        ],
                        [
                            sg.Input("",key="-DATA_DETAIL_SETCODE-",size=(15,1),justification="right")
                        ]
                    ]),
                    sg.Column([
                        [
                            sg.Text("type",size=(9,1),justification="center")
                        ],
                        [
                            sg.Input("",key="-DATA_DETAIL_TYPE-",size=(10,1),justification="right")
                        ]
                    ]),
                    sg.Column([
                        [
                            sg.Text("atk",size=(5,1),justification="center")
                        ],
                        [
                            sg.Input("",key="-DATA_DETAIL_ATK-",size=(6,1),justification="right")
                        ]
                    ]),
                    sg.Column([
                        [
                            sg.Text("def",size=(5,1),justification="center")
                        ],
                        [
                            sg.Input("",key="-DATA_DETAIL_DEF-",size=(6,1),justification="right")
                        ]
                    ]),
                    sg.Column([
                        [
                            sg.Text("level",size=(9,1),justification="center")
                        ],
                        [
                            sg.Input("",key="-DATA_DETAIL_LEVEL-",size=(10,1),justification="right")
                        ]
                    ]),
                    sg.Column([
                        [
                            sg.Text("race",size=(8,1),justification="center")
                        ],
                        [
                            sg.Input("",key="-DATA_DETAIL_RACE-",size=(9,1),justification="right")
                        ]
                    ]),
                    sg.Column([
                        [
                            sg.Text("attribute",size=(7,1),justification="center")
                        ],
                        [
                            sg.Input("",key="-DATA_DETAIL_ATTRIBUTE-",size=(8,1),justification="right")
                        ]
                    ]),
                    sg.Column([
                        [
                            sg.Text("category",size=(9,1),justification="center")
                        ],
                        [
                            sg.Input("",key="-DATA_DETAIL_CATEGORY-",size=(11,1),justification="right")
                        ]
                    ])
                ],
                [
                    sg.Column([
                        [
                            sg.Button("変更を保存",key="-DATA_UPDATE-",pad=(0,0))
                        ]
                    ],justification="right")
                ]
            ])
        ]
    ]
    return layout

def textsLayout():
    layout=[
        [
            sg.Input("",visible=False,readonly=True,key="-CDB_PATH-"),
            sg.Frame("",[
                [
                    sg.Column([
                        [
                            sg.Text("id",justification="center",size=(9,1))
                        ],
                        [
                            sg.Input("",key="-TEXT_DETAIL_ID-",size=(10,1),justification="right")
                        ]
                    ]),
                    sg.Column([
                        [
                            sg.Text("name",justification="center",size=(43,1))
                        ],
                        [
                            sg.Input("",key="-TEXT_DETAIL_NAME-",size=(50,1),justification="left")
                        ]
                    ]),
                    sg.Column([
                        [
                            sg.Text("desc",justification="center",size=(60,1))
                        ],
                        [
                            sg.Multiline("",key="-TEXT_DETAIL_DESC-",size=(80,10),justification="left",font=("Rounded Mplus",10))
                        ]
                    ]),
                    sg.Column([
                        [
                            sg.TabGroup([
                                [sg.Tab(f"str{i}",[[sg.Input("",key=f"-TEXT_DETAIL_STR{i}-",expand_x=True,expand_y=True)]],key="-TAB_TEXT_DETAIL_STR{i}-") for i in range(1,17)]
                            ],key="-TAB_TEXT_DETAIL_STR_GROUP-",tab_background_color="gray")
                        ]
                    ],vertical_alignment="center")
                ],
                [
                    sg.Column([
                        [
                            sg.Button("変更を保存",key="-TEXT_UPDATE-",pad=(0,0))
                        ]
                    ],justification="right")
                ]
            ])
        ]
    ]
    return layout