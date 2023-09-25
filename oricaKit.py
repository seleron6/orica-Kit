import PySimpleGUI as sg
import pyperclip as clip
import cv2
import numpy as np
import os
import sqlite3
import math
import re
import json

import validate as vali
import windowLayout as wl
from setcodeIndex import readSetCodes,createSetcodeTxt,readOricaSetCodes,createOricaSetcodeTxt
import cardTypeIndex as cti
import categoryIndex as ci
import preview as pre

def draw_image_plus(self, img, location=(0,0)):
    if type(img) == np.ndarray:
        img = cv2.imencode('.png', img)[1].tobytes()
    id_ = self.draw_image(data=img, location=location)
    return id_

class main():
    def __init__(self):
        sg.Graph.draw_image_plus = draw_image_plus
        self.createConst()
        self.createVariable()
        self.setting()
        self.createMainWindow()
        self.setValidate()
        self.eventHandler()

    def createConst(self):
        self.UP_EVENT={
            "-ID_UP-":999999999,
            "-ALIAS_UP-":999999999,
            "-SETCODE_UP-":999999999999999,
            "-ATK_UP-":99999,
            "-DEF_UP-":99999,
            "-LEVEL_UP-":13,
            "-SCALE_LEFT_UP-":99,
            "-SCALE_RIGHT_UP-":99
        }
        self.DOWN_EVENT={
            "-ID_DOWN-":0,
            "-ALIAS_DOWN-":0,
            "-SETCODE_DOWN-":0,
            "-ATK_DOWN-":-2,
            "-DEF_DOWN-":-2,
            "-LEVEL_DOWN-":0,
            "-SCALE_LEFT_DOWN-":0,
            "-SCALE_RIGHT_DOWN-":0,
        }
        self.VALIDATE_NUMBER={
            "-ID-":[0,999999999],
            "-ALIAS-":[0,999999999],
            "-SETCODE-":[0,999999999999999],
            "-ATK-":[-2,99999],
            "-DEF-":[-2,99999],
            "-LEVEL-":[0,13],
            "-SCALE_LEFT-":[0,99],
            "-SCALE_RIGHT-":[0,99],
        }
        self.RADIOS={
            "-PRESET_RADIO_MONSTER-":cti.MONSTER_CHECK,
            "-PRESET_RADIO_SPELL-":cti.SPELL_CHECK,
            "-PRESET_RADIO_TRAP-":cti.TRAP_CHECK
        }
        self.DISABLE_STATUS=[
            "-ATK_?-",
            "-ATK-",
            "-ATK_UP-",
            "-ATK_DOWN-",
            "-DEF_?-",
            "-DEF-",
            "-DEF_UP-",
            "-DEF_DOWN-",
            "-LEVEL-",
            "-LEVEL_UP-",
            "-LEVEL_DOWN-",
            "-ATTRIBUTE-",
            "-RACE-",
            "-SCALE_LEFT-",
            "-SCALE_LEFT_UP-",
            "-SCALE_LEFT_DOWN-",
            "-SCALE_RIGHT-",
            "-SCALE_RIGHT_UP-",
            "-SCALE_RIGHT_DOWN-",
            "-LINK_MARKER_LOWER_LEFT-",
            "-LINK_MARKER_LOWER-",
            "-LINK_MARKER_LOWER_RIGHT-",
            "-LINK_MARKER_LEFT-",
            "-LINK_MARKER_RIGHT-",
            "-LINK_MARKER_UPPER_LEFT-",
            "-LINK_MARKER_UPPER-",
            "-LINK_MARKER_UPPER_RIGHT-"
        ]
        self.DISABLE_LINK_STATUS=[
            "-DEF-",
            "-DEF_?-",
            "-DEF_UP-",
            "-DEF_DOWN-",
            "-LEVEL-",
            "-LEVEL_UP-",
            "-LEVEL_DOWN-"
        ]
        self.TRAP_STATUS=[
            "-SCALE_LEFT-",
            "-SCALE_LEFT_UP-",
            "-SCALE_LEFT_DOWN-",
            "-SCALE_RIGHT-",
            "-SCALE_RIGHT_UP-",
            "-SCALE_RIGHT_DOWN-",
            "-LINK_MARKER_LOWER_LEFT-",
            "-LINK_MARKER_LOWER-",
            "-LINK_MARKER_LOWER_RIGHT-",
            "-LINK_MARKER_LEFT-",
            "-LINK_MARKER_RIGHT-",
            "-LINK_MARKER_UPPER_LEFT-",
            "-LINK_MARKER_UPPER-",
            "-LINK_MARKER_UPPER_RIGHT-"
        ]
        self.VALUE_ZERO=[
            "-ID-",
            "-ALIAS-",
            "-SETCODE-",
            "-ATK-",
            "-DEF-",
            "-LEVEL-",
            "-SCALE_RIGHT-",
            "-SCALE_LEFT-"
        ]
        self.VALUE_HIHUN=[
            "-ATTRIBUTE-",
            "-RACE-"
        ]
        self.VALUE_BLANK=[
            "-CARD_NAME-",
            "-CARD_NAME_EN-",
            "-CARD_TEXT-",
            "-CARD_TEXT_P-",
            "-CARD_TEXT_EN-",
            "-CARD_TEXT_EN_P-",
            "-ADJUST_TEXT_JP_HIDDEN-",
            "-ADJUST_PTEXT_JP_HIDDEN-",
            "-ADJUST_TEXT_EN_HIDDEN-",
            "-ADJUST_PTEXT_EN_HIDDEN-"
        ]
        [self.VALUE_BLANK.append(f"-CARD_STR{i}-") for i in range(1,17)]
        self.H2Z_DIGIT = str.maketrans('1234567890', '１２３４５６７８９０')
        self.DATAS=['datas', 'id', 'ot', 'alias', 'setcode', 'type', 'atk', 'def', 'level', 'race', 'attribute', 'category']
        self.VERSION="β-0.2"
        self.ICON="./icon.ico"
        self.DATA_VALIDATE=[
            ["-DATA_DETAIL_ID-",0,999999999],
            ["-DATA_DETAIL_OT-",0,4],
            ["-DATA_DETAIL_ALIAS-",0,999999999],
            ["-DATA_DETAIL_SETCODE-",0,999999999999999],
            ["-DATA_DETAIL_TYPE-",0,999999999],
            ["-DATA_DETAIL_ATK-",0,99999],
            ["-DATA_DETAIL_DEF-",0,99999],
            ["-DATA_DETAIL_LEVEL-",0,999999999],
            ["-DATA_DETAIL_RACE-",0,99999999],
            ["-DATA_DETAIL_ATTRIBUTE-",0,99],
            ["-DATA_DETAIL_CATEGORY-",0,9999999999],
        ]
        self.TEXT_VALIDATE=[
            ["-TEXT_DETAIL_ID-",0,999999999],
            ["-TEXT_DETAIL_NAME-"],
            ["-TEXT_DETAIL_DESC-"],
        ]
        [self.TEXT_VALIDATE.append([f"-TEXT_DETAIL_STR{i}-"]) for i in range (1,17)]

    def createVariable(self):
        self.cardImage=None
        self.cardImageWithoutText=None
        self.tmp_jpText=None
        self.tmp_jpTextP=None
        self.tmp_enText=None
        self.tmp_enTextP=None
        self.textFontType=None
        self.illust=None
        self.bigCanvas=None
        self.canvas_layout,self.canvas=wl.previewWindowLayout()
        self.setcodeWindow=None
        self.adjustWindow=None
        self.imageWindow=None
        self.saveWindow=None
        self.detailDatasWindow=None
        self.detailTextsWindow=None
        self.setcodes=None
        self.oricasetcodes=None
        self.lang="en"
        self.isP=False
        self.bigImage=None
        self.cdbDatas=None
        self.cdbTexts=None
        self.tmpData=None
        self.tmpText=None
        self.layout=[
            [
                sg.TabGroup(
                    [[
                        sg.Tab("datas",wl.mainWindowLayout(),key="-TAB_DATAS-"),
                        sg.Tab("texts",wl.textWindowLayout(),key="-TAB_TEXTS-"),
                        sg.Tab("画像",self.canvas_layout,key="-TAB_PREVIEW-"),
                        sg.Tab("CDB",wl.cdbLayout(),key="-TAB_CDB-")
                    ]],key="-TAB_GROUP-",enable_events=True,tab_background_color="gray"
                )
            ],
            [
                wl.sqlWindowLayout()
            ]
        ]
    
    def reset(self):
        if self.setcodeWindow is not None:
            self.setcodeWindow.close()
        if self.adjustWindow is not None:
            self.adjustWindow.close()
        if self.imageWindow is not None:
            self.imageWindow.close()
        if self.saveWindow is not None:
            self.saveWindow.close()
        if self.detailDatasWindow is not None:
            self.detailDatasWindow.close()
        if self.detailTextsWindow is not None:
            self.detailTextsWindow.close()
        self.mainWindow["-OT-"].update("Custom")
        self.mainWindow["-PRESET_RADIO_FREE-"].update(True)
        [self.mainWindow[n].update(0) for n in self.VALUE_ZERO]
        for n in self.VALUE_HIHUN:
            self.mainWindow[n].update("－")
            self.mainWindow[n].update(background_color="white")
        for cname in cti.TYPE_VALUE.keys():
            self.mainWindow["-CARD_TYPE_"+cname+"-"].update(False)
            self.mainWindow["-CARD_TYPE_"+cname+"-"].update(disabled=False)
        [self.mainWindow[f"-CATEGORY_{n[1]}-"].update(False) for n in ci.CATEGORY]
        for cname in self.DISABLE_STATUS:
            if "LINK_MARKER" in cname:
                self.mainWindow[cname].update(False)
                self.mainWindow[cname].update(disabled=True)
            elif "SCALE" in cname:
                self.mainWindow[cname].update(disabled=True)
            else:
                self.mainWindow[cname].update(disabled=False)
        self.mainWindow.write_event_value("-PARAMETER_SETCODE_SET-",None)
        self.mainWindow.write_event_value("-CARD_TYPE_RESET-",None)
        self.mainWindow.write_event_value("-CATEGORY_RESET-",None)
        [self.mainWindow[n].update("") for n in self.VALUE_BLANK]
        self.mainWindow["-LANGUAGE_EN-"].update(True)
        self.resetVariable()
    
    def resetVariable(self):
        self.cardImage=None
        self.cardImageWithoutText=None
        self.tmp_jpText=None
        self.tmp_jpTextP=None
        self.tmp_enText=None
        self.tmp_enTextP=None
        self.textFontType=None
        self.illust=None
        self.bigCanvas=None
        self.setcodeWindow=None
        self.adjustWindow=None
        self.imageWindow=None
        self.saveWindow=None
        self.detailDatasWindow=None
        self.detailTextsWindow=None
        self.setcodes=None
        self.oricasetcodes=None
        self.lang="en"
        self.isP=False
        self.bigImage=None
        self.tmpData=None
        self.tmpText=None
    
    def setting(self):
        sg.user_settings_filename(filename="config.json",path=".")
        self.startPos=[0,0]
        self.path="./"
        try:
            with open('./config.json') as f:
                d=json.load(f)
                self.startPos=d["-location-"]
                self.path=d["-cdbpath-"]
        except:
            pass
    
    def createMainWindow(self):
        self.mainWindow=sg.Window("オリカ作成キット "+self.VERSION,self.layout,resizable=False,finalize=True,enable_close_attempted_event=True,size=(572,593),location=self.startPos,icon=self.ICON)
        self.mainWindow["-CARD_TEXT-"].Widget.configure(undo=True)
        self.mainWindow["-CARD_TEXT_P-"].Widget.configure(undo=True)
        self.mainWindow["-CARD_TEXT_EN-"].Widget.configure(undo=True)
        self.mainWindow["-CARD_TEXT_EN_P-"].Widget.configure(undo=True)
        self.mainWindow['-CDB_DATAS-'].bind('<Double-Button-1>', '_Double')
        self.mainWindow['-CDB_TEXTS-'].bind('<Double-Button-1>', '_Double')
        self.mainWindow["-CDB_PATH-"].update(self.path)

    def setValidate(self):
        for k,v in self.VALIDATE_NUMBER.items():
            lLimit=v[0]
            uLimit=v[1]
            vcmd = (self.mainWindow.TKroot.register(vali.validateNumber),'%P',lLimit,uLimit)
            self.mainWindow[k].widget.configure(validate='all',validatecommand=vcmd)

    def imread(self,filename, flags=cv2.IMREAD_UNCHANGED, dtype=np.uint8):
        try:
            n = np.fromfile(filename, dtype)
            img = cv2.imdecode(n, flags)
            return img
        except Exception as e:
            #print(e)
            return None
    
    def imwrite(self,filename, img, params=None):
        try:
            ext = os.path.splitext(filename)[1]
            result, n = cv2.imencode(ext, img, params)

            if result:
                with open(filename, mode='w+b') as f:
                    n.tofile(f)
                return True
            else:
                return False
        except Exception as e:
            #print(e)
            return False

    def textDraw(self,baseFrame,text,ctype):
        texts=text.splitlines()
        rtnFrame=baseFrame
        textPosX=90
        widthLimit=995
        if ctype=="st":
            if self.lang=="en":
                fontSize=34
                textInterval=35
                textPosY=1290
            elif self.lang=="jp":
                fontSize=35
                textInterval=38
                textPosY=1310
        else:
            if self.lang=="en":
                if len(texts)<=6:
                    fontSize=35
                    textInterval=37
                    textPosY=1335
                else:
                    fontSize=30
                    textInterval=31
                    textPosY=1340
            else:
                fontSize=35
                textInterval=38
                textPosY=1335
        for i in range(len(texts)):
            if texts[i]!="":
                textImage=pre.createTextImage(texts[i],self.lang,fontSize,widthLimit,ctype)
                rtnFrame=pre.CvOverlayImage.overlay(rtnFrame,textImage,(textPosX,textPosY+textInterval*i))
        return rtnFrame

    def textDrawP(self,baseFrame,text):
        texts=text.splitlines()
        rtnFrame=baseFrame
        textPosX=185
        widthLimit=806
        if self.lang=="en":
            fontSize=35
            textInterval=37
            textPosY=1083
        else:
            fontSize=35
            textInterval=38
            textPosY=1087
        for i in range(len(texts)):
            if texts[i]!="":
                textImage=pre.createTextImage(texts[i],self.lang,fontSize,widthLimit)
                rtnFrame=pre.CvOverlayImage.overlay(rtnFrame,textImage,(textPosX,textPosY+textInterval*i))
        return rtnFrame

    def createSQL(self,radio):
        sql=""
        if radio in ("data","all"):
            id=self.values["-ID-"]
            ot={"OCG":1, "TCG":2, "OCG/TCG":3, "Custom":4}[self.values["-OT-"]]
            alias=self.values["-ALIAS-"]
            setcode=int(self.values["-PARAMETER_SETCODE_HIDDEN-"],16)
            ctype=self.values["-PARAMETER_TYPE_HIDDEN-"]
            atk=self.values["-ATK-"]
            defe=self.values["-DEF-"]
            level=int(self.values["-SCALE_LEFT-"])*16**6+int(self.values["-SCALE_RIGHT-"])*16**4+int(self.values["-LEVEL-"])
            race=wl.RACE_VALUE[self.values["-RACE-"]] if self.values["-RACE-"]!="－" else 0
            attribute=wl.ATTRIBUTE_VALUE[self.values["-ATTRIBUTE-"]] if self.values["-ATTRIBUTE-"]!="－" else 0
            category=self.values["-PARAMETER_CATEGORY_HIDDEN-"]
            sql+="INSERT INTO [datas] ([id],[ot],[alias],[setcode],[type],[atk],[def],[level],[race],[attribute],[category]) values ("
            datas=[id,ot,alias,setcode,ctype,atk,defe,level,race,attribute,category]
            for d in datas:
                sql+="'"+str(d)+"',"
            sql=sql[:-1]+");"
        if radio in ("text","all"):
            if sql!="": sql+="\n"
            sql+="INSERT INTO [texts] ([id],[name],[desc],[str1],[str2],[str3],[str4],[str5],[str6],[str7],[str8],[str9],[str10],[str11],[str12],[str13],[str14],[str15],[str16]) values ("
            datas=[self.values["-ID-"],self.values["-CARD_NAME-"]]
            txt=self.values["-CARD_TEXT-"]
            txtp=self.values["-CARD_TEXT_P-"]
            if self.isP:
                if self.values["-CARD_TYPE_NORMAL-"]:
                    mt="【モンスター情報】"
                else:
                    mt="【モンスター効果】"
                txt=f"【Ｐスケール：青{str(self.values['-SCALE_LEFT-']).translate(self.H2Z_DIGIT)}／赤{str(self.values['-SCALE_RIGHT-']).translate(self.H2Z_DIGIT)}】\n{txtp}\n{mt}\n{txt}"
            datas.append(txt)
            for i in range(1,17):
                datas.append(self.values["-CARD_STR"+str(i)+"-"])
            for d in datas:
                sql+="'"+str(d)+"',"
            sql=sql[:-1]+");"
        return sql
    
    def eventHandler(self):
        while True:
            self.window, self.event, self.values = sg.read_all_windows()
            #print(self.event)
            #print(self.values)
            if self.event in (sg.WIN_CLOSED,sg.WINDOW_CLOSE_ATTEMPTED_EVENT):
                if self.window is self.mainWindow:
                    sg.user_settings_set_entry('-location-', self.window.current_location())
                    sg.user_settings_set_entry('-cdbpath-', self.values["-CDB_PATH-"])
                    break
                elif self.window is self.setcodeWindow:
                    self.setcodeWindow=None
                    self.window.close()
                elif self.window is self.adjustWindow:
                    self.adjustWindow=None
                    self.window.close()
                elif self.window is self.imageWindow:
                    self.imageWindow=None
                    self.window.close()
                elif self.window is self.saveWindow:
                    self.saveWindow=None
                    self.window.close()
                elif self.window is self.detailDatasWindow:
                    self.detailDatasWindow=None
                    self.window.close()
                elif self.window is self.detailTextsWindow:
                    self.detailTextsWindow=None
                    self.window.close()
            elif self.event in self.UP_EVENT:
                limit=self.UP_EVENT[self.event]
                kname=self.event.replace("_UP","")
                if self.values[kname]=="":
                    self.mainWindow[kname].update(0)
                elif int(self.values[kname])<limit:
                    if kname in ("-ATK-","-DEF-") and -1<int(self.values[kname])<99900:
                        plus=100
                    else:
                        plus=1
                    self.mainWindow[kname].update(int(self.values[kname])+plus)
                    if kname in ("-SETCODE-"):
                        self.mainWindow.write_event_value("-PARAMETER_SETCODE_SET-",None)
            elif self.event in self.DOWN_EVENT:
                limit=self.DOWN_EVENT[self.event]
                kname=self.event.replace("_DOWN","")
                if self.values[kname]=="":
                    self.mainWindow[kname].update(0)
                elif int(self.values[kname])>limit:
                    if kname in ("-ATK-","-DEF-") and int(self.values[kname])>99:
                        minus=100
                    else:
                        minus=1
                    self.mainWindow[kname].update(int(self.values[kname])-minus)
                    if kname in ("-SETCODE-"):
                        self.mainWindow.write_event_value("-PARAMETER_SETCODE_SET-",None)
            elif self.event=="setcode":
                if self.setcodeWindow is None:
                    self.setcodes=readSetCodes()
                    self.oricasetcodes=readOricaSetCodes()
                    self.setcodeWindow=sg.Window("",wl.setcodeWindowLayout(),resizable=False,finalize=True,location=(self.mainWindow.current_location()[0]-wl.SETCODE_WIDTH-30,self.mainWindow.current_location()[1]),icon=self.ICON)
                else:
                    self.setcodeWindow.close()
                    self.setcodeWindow=None
            elif self.event in ("-OCG_CATNAME-","-ORICA_CATNAME-"):
                if self.setcodeWindow is not None:
                    e="-OCG_CATNAME-" if self.event=="-OCG_CATNAME-" else "-ORICA_CATNAME-"
                    if self.values[e][0] in self.setcodes:
                        self.setcodeWindow["-OCG_CATID-"].update(self.setcodes[self.values[e][0]])
                        self.setcodeWindow["-OCG_CATID_HIDDEN-"].update(self.setcodes[self.values[e][0]])
                    else:
                        self.setcodeWindow["-ORICA_CATID-"].update(self.oricasetcodes[self.values[e][0]])
                        self.setcodeWindow["-ORICA_CATID_HIDDEN-"].update(self.oricasetcodes[self.values[e][0]])
            elif self.event in ("-OCG_SEARCH-","-ORICA_SEARCH-"):
                if self.setcodeWindow is not None:
                    o=self.event.replace("-","").split("_")[0]
                    search=self.values[self.event]
                    codes=self.setcodes if o=="OCG" else self.oricasetcodes
                    self.setcodeWindow[f"-{o}_CATNAME-"].update(list(filter(lambda n: search in n, codes)))
            elif self.event=="-CREATE_OCG_SETCODE_TXT-":
                if self.setcodeWindow is not None:
                    path=self.values["-CREATE_OCG_SETCODE_TXT-"]
                    createSetcodeTxt(path)
                    self.setcodeWindow.close()
                    self.setcodeWindow=None
                    self.setcodeWindow=sg.Window("",wl.setcodeWindowLayout(),resizable=False,finalize=True,location=(self.mainWindow.current_location()[0]-wl.SETCODE_WIDTH-30,self.mainWindow.current_location()[1]),icon=self.ICON)
                    self.setcodes=readSetCodes()
            elif self.event=="-CREATE_ORICA_SETCODE_TXT-":
                if self.setcodeWindow is not None:
                    path=self.values["-CREATE_ORICA_SETCODE_TXT-"]
                    createOricaSetcodeTxt(path)
                    self.setcodeWindow.close()
                    self.setcodeWindow=None
                    self.setcodeWindow=sg.Window("",wl.setcodeWindowLayout(),resizable=False,finalize=True,location=(self.mainWindow.current_location()[0]-wl.SETCODE_WIDTH-30,self.mainWindow.current_location()[1]),icon=self.ICON)
                    self.oricasetcodes=readOricaSetCodes() 
            elif self.event in ("-ATK_?-","-DEF_?-"):
                ad=self.event.replace("_?","")
                self.mainWindow[ad].update(-2)
            elif self.event in ("-SETCODE-","-PARAMETER_SETCODE_SET-"):
                try:
                    l=int(self.values["-SETCODE-"])
                    sc=hex(l)
                    sch=sc
                    if sc==hex(0):
                        sc="setcode"
                    self.mainWindow["-PARAMETER_SETCODE-"].update(sc)
                    self.mainWindow["-PARAMETER_SETCODE_HIDDEN-"].update(sch)
                except:
                    self.mainWindow["-PARAMETER_SETCODE-"].update("setcode")
                    self.mainWindow["-PARAMETER_SETCODE-"].update(hex(0))
            elif self.event in ("-OCG_CATID_TOP-","-OCG_CATID_CENTER-","-OCG_CATID_UNDER-","-ORICA_CATID_TOP-","-ORICA_CATID_CENTER-","-ORICA_CATID_UNDER-"):
                if self.setcodeWindow is not None:
                    try:
                        tmp=self.event.replace("-","").split("_")
                        o=tmp[0]
                        place=tmp[2]
                        catname=self.values["-"+o+"_CATNAME-"]
                        if len(catname)>0:
                            catname=catname[0]
                        else:
                            raise ValueError("Error")
                        self.setcodeWindow["-CATEGORY_"+place+"-"].update(catname)
                        self.setcodeWindow["-CATEGORY_"+place+"_HIDDEN-"].update(self.values["-"+o+"_CATID_HIDDEN-"])
                    except:
                        pass
            elif self.event in ("-CATID_SET-","-CATID_SET2-"):
                tnum=int(self.values["-CATEGORY_TOP_HIDDEN-"])
                cnum=int(self.values["-CATEGORY_CENTER_HIDDEN-"])
                unum=int(self.values["-CATEGORY_UNDER_HIDDEN-"])
                num=0
                if tnum!=0:
                    num=tnum
                if cnum!=0:
                    if num==0:
                        num=cnum
                    else:
                        num+=cnum*(16**4)
                if unum!=0:
                    if num==0:
                        num=unum
                    elif [cnum,tnum].count(0)==1:
                        num+=unum*(16**4)
                    else:
                        num+=unum*(16**8)
                if num==0:
                    o=self.values["-TAB_SETCODE_GROUP-"].replace("-","").split("_")[2]
                    num=int(self.values["-"+o+"_CATID_HIDDEN-"])
                self.mainWindow["-SETCODE-"].update(num)
                self.mainWindow.write_event_value("-PARAMETER_SETCODE_SET-",None)
            elif self.event in ("-CATID_CLEAR_TOP-","-CATID_CLEAR_CENTER-","-CATID_CLEAR_UNDER-"):
                place=self.event.replace("-","").split("_")[2]
                self.setcodeWindow["-CATEGORY_"+place+"-"].update("")
                self.setcodeWindow["-CATEGORY_"+place+"_HIDDEN-"].update(0)
            elif type(self.event) is str and self.event.startswith("-CARD_TYPE"):
                if self.event in ("-CARD_TYPE_LINK-"):
                    for dis in self.DISABLE_LINK_STATUS:
                        if dis in ("-DEF-","-LEVEL-"): self.mainWindow[dis].update(0)
                        self.mainWindow[f"{dis}"].update(disabled=self.values["-CARD_TYPE_LINK-"])
                    for marker in cti.LINK_MARKER.keys():
                        self.mainWindow[f"-LINK_MARKER{marker}-"].update(disabled=not self.values["-CARD_TYPE_LINK-"])
                        self.mainWindow[f"-LINK_MARKER{marker}-"].update(False)
                elif self.event in ("-CARD_TYPE_PENDULUM-"):
                    self.isP=not self.isP
                    for scale in cti.SCALE:
                        self.mainWindow[f"{scale}"].update(disabled=not self.isP)
                        if not self.isP and "UP" not in scale and "DOWN" not in scale:
                            self.mainWindow[f"{scale}"].update(0)
                typeval=cti.calcType(self.values)
                tvh=typeval
                if typeval==0: typeval="type"
                self.mainWindow["-PARAMETER_TYPE-"].update(typeval)
                self.mainWindow["-PARAMETER_TYPE_HIDDEN-"].update(tvh)
            elif self.event in ("-PARAMETER_SETCODE-","-PARAMETER_TYPE-","-PARAMETER_CATEGORY-"):
                h=self.event[:-1]+"_HIDDEN-"
                clip.copy(self.values[h])
            elif type(self.event) is str and self.event.startswith("-PRESET_RADIO"):
                for category_name in ci.CATEGORY_VALUE.keys():
                     self.mainWindow["-CATEGORY_"+category_name+"-"].update(False)
                for status_name in self.DISABLE_STATUS:
                    if self.event in ("-PRESET_RADIO_FREE-","-PRESET_RADIO_MONSTER-") or (self.event=="-PRESET_RADIO_TRAP-" and status_name not in self.TRAP_STATUS):
                        if self.event=="-PRESET_RADIO_TRAP-" and status_name not in self.TRAP_STATUS:
                            self.mainWindow[status_name].update(disabled=False)
                            if status_name in ("-ATTRIBUTE-","-RACE-"): self.mainWindow[status_name].update(background_color="white")
                        elif (not self.values["-CARD_TYPE_LINK-"] and "LINK_MARKER" in status_name) or (self.values["-CARD_TYPE_LINK-"] and status_name in self.DISABLE_LINK_STATUS) or (not self.isP and "SCALE" in status_name):
                            self.mainWindow[status_name].update(disabled=True)
                        else:
                            self.mainWindow[status_name].update(disabled=False)
                            if status_name in ("-ATTRIBUTE-","-RACE-"): self.mainWindow[status_name].update(background_color="white")
                    else:
                        self.isP=False
                        if status_name in ("-ATTRIBUTE-","-RACE-"):
                            self.mainWindow[status_name].update("－")
                        elif status_name in ("-ATK-","-DEF-","-LEVEL-","-SCALE_RIGHT-","-SCALE_LEFT-"):
                            self.mainWindow[status_name].update(0)
                        elif "LINK_MARKER" in status_name:
                            self.mainWindow[status_name].update(False)
                        self.mainWindow[status_name].update(disabled=True)
                        if status_name in ("-ATTRIBUTE-","-RACE-"): self.mainWindow[status_name].update(background_color="gray")
                for check_name in cti.CHECK_INDEX:
                    if self.event=="-PRESET_RADIO_FREE-":
                        self.mainWindow[check_name].update(disabled=False)
                    elif self.event in self.RADIOS.keys():
                        if check_name=="-CARD_TYPE_"+self.event.replace("-PRESET_RADIO_",""):
                            self.mainWindow[check_name].update(True)
                            self.mainWindow[check_name].update(disabled=True)
                        elif check_name not in self.RADIOS[self.event]:
                            self.mainWindow[check_name].update(False)
                            self.mainWindow[check_name].update(disabled=True)
                        else:
                            self.mainWindow[check_name].update(disabled=False)
                self.mainWindow.write_event_value("-CARD_TYPE_RESET-",None)
                self.mainWindow.write_event_value("-CATEGORY_RESET-",None)
            elif type(self.event) is str and self.event.startswith("-CATEGORY"):
                cval=ci.calcCategory(self.values)
                cvh=cval
                if cval==0:
                    cval="category"
                self.mainWindow["-PARAMETER_CATEGORY-"].update(cval)
                self.mainWindow["-PARAMETER_CATEGORY_HIDDEN-"].update(cvh)
            elif self.event=="-SQL_COPY-":
                if self.values["-SQL_RADIO_DATA-"]:
                    radio="data"
                elif self.values["-SQL_RADIO_TEXT-"]:
                    radio="text"
                else:
                    radio="all"
                sql=self.createSQL(radio)
                clip.copy(sql)
            elif type(self.event) is str and self.event.startswith("-LINK_MARKER"):
                mark=self.event.replace("-","").replace("LINK_MARKER","")
                one=1 if self.values[self.event] else -1
                self.mainWindow["-DEF-"].update(int(self.values["-DEF-"])+cti.LINK_MARKER[mark]*one)
                self.mainWindow["-LEVEL-"].update(int(self.values["-LEVEL-"])+one)
            elif self.event=="-TAB_GROUP-" and self.values["-TAB_GROUP-"]!="-TAB_PREVIEW-":
                if self.adjustWindow is not None:
                    self.adjustWindow.close()
                    self.adjustWindow=None
                if self.imageWindow is not None:
                    self.imageWindow.close()
                    self.imageWindow=None
            elif (self.event=="-TAB_GROUP-" and self.values["-TAB_GROUP-"]=="-TAB_PREVIEW-") or "LANGUAGE" in self.event:
                if self.values["-LANGUAGE_JP-"]:
                    self.lang="jp"
                else:
                    self.lang="en"
                jpText=self.values["-CARD_TEXT-"]
                jpTextP=self.values["-CARD_TEXT_P-"]
                jpChange=self.tmp_jpText!=jpText
                jpPChange=self.tmp_jpTextP!=jpTextP
                enText=self.values["-CARD_TEXT_EN-"]
                enChange=self.tmp_enText!=enText
                enTextP=self.values["-CARD_TEXT_EN_P-"]
                enPChange=self.tmp_enTextP!=enTextP
                if jpChange:
                    self.mainWindow["-ADJUST_TEXT_JP_HIDDEN-"].update(jpText)
                    self.tmp_jpText=jpText
                if jpPChange:
                    self.mainWindow["-ADJUST_PTEXT_JP_HIDDEN-"].update(jpTextP)
                    self.tmp_jpTextP=jpTextP
                if enChange:
                    self.mainWindow["-ADJUST_TEXT_EN_HIDDEN-"].update(enText)
                    self.tmp_enText=enText
                if enPChange:
                    self.mainWindow["-ADJUST_PTEXT_EN_HIDDEN-"].update(enTextP)
                    self.tmp_enTextP=enTextP
                canvasSize=(wl.CANVAS_WIDTH,wl.CANVAS_HEIGHT)
                imgPath=pre.baseImage(self.values,self.lang)
                baseFrame=cv2.imread(imgPath,cv2.IMREAD_UNCHANGED)
                if "unknown" not in imgPath:
                    self.mainWindow["-TEXT_ADJUST-"].update(disabled=False)
                    self.mainWindow["-INSERT_IMAGE-"].update(disabled=False)
                    if self.lang=="jp":
                        name=self.values["-CARD_NAME-"]
                    else:
                        name=self.values["-CARD_NAME_EN-"]
                    if "monster" in imgPath:
                        level=int(self.values["-LEVEL-"])
                        att=self.values["-ATTRIBUTE-"]
                        race=self.values["-RACE-"]
                        atk=self.values["-ATK-"]
                        atkImage=pre.createParamImage(atk if atk!="-2" else "?")
                        atkHeight,atkWidth,atkChannel=atkImage.shape
                        if atkWidth>104:
                            atkImage=cv2.resize(atkImage,(104,atkHeight))
                        atkHeight,atkWidth,atkChannel=atkImage.shape
                        if atk not in ("-2","-1"):
                            baseFrame=pre.CvOverlayImage.overlay(baseFrame,atkImage,(850-atkWidth,1572))
                        elif atk!="-1":
                            baseFrame=pre.CvOverlayImage.overlay(baseFrame,atkImage,(850-atkWidth,1563))
                        if att!="－":
                            attPath=pre.attributePath(att,self.lang)
                            attImage=cv2.imread(attPath,cv2.IMREAD_UNCHANGED)
                            baseFrame=pre.CvOverlayImage.overlay(baseFrame,attImage,(0,0))
                        if race!="－":
                            raceImage=pre.createRaceImage(self.values,self.lang)
                            if self.lang=="jp":
                                baseFrame=pre.CvOverlayImage.overlay(baseFrame,raceImage,(90,1299))
                            else:
                                baseFrame=pre.CvOverlayImage.overlay(baseFrame,raceImage,(90,1290))
                        if "link" in imgPath:
                            markerPaths=pre.linkMarkerPath(self.values)
                            for markerPath in markerPaths:
                                markerImage=cv2.imread(markerPath,cv2.IMREAD_UNCHANGED)
                                baseFrame=pre.CvOverlayImage.overlay(baseFrame,markerImage,(0,0))
                            linkImage=pre.createLinkImage(level)
                            baseFrame=pre.CvOverlayImage.overlay(baseFrame,linkImage,(1047,1573))
                        else:
                            defence=self.values["-DEF-"]
                            if "xyz" in imgPath:
                                rankImage=cv2.imread("./images/level_rank/rank_one.png",cv2.IMREAD_UNCHANGED)
                                rankImage=np.tile(rankImage,(1,level,1))
                                rankHeight,rankWidth,rankChannel=rankImage.shape
                                if level<13:
                                    rankImage=cv2.copyMakeBorder(rankImage, 210, 1720-210-rankHeight, 121, 1180-121-rankWidth, cv2.BORDER_CONSTANT, value=(0,0,0))
                                else:
                                    rankImage=cv2.copyMakeBorder(rankImage, 210, 1720-210-rankHeight, 84, 1180-84-rankWidth, cv2.BORDER_CONSTANT, value=(0,0,0))
                                baseFrame=pre.CvOverlayImage.overlay(baseFrame,rankImage,(0,0))
                            else:
                                levelImage=cv2.imread("./images/level_rank/level_one.png",cv2.IMREAD_UNCHANGED)
                                levelImage=np.tile(levelImage,(1,level,1))
                                levelHeight,levelWidth,levelChannel=levelImage.shape
                                if level<13:
                                    levelImage=cv2.copyMakeBorder(levelImage, 210, 1720-210-levelHeight, 1180-121-levelWidth, 121, cv2.BORDER_CONSTANT, value=(0,0,0))
                                else:
                                    levelImage=cv2.copyMakeBorder(levelImage, 210, 1720-210-levelHeight, 1180-84-levelWidth, 84, cv2.BORDER_CONSTANT, value=(0,0,0))
                                baseFrame=pre.CvOverlayImage.overlay(baseFrame,levelImage,(0,0))
                            defImage=pre.createParamImage(defence if defence!="-2" else "?")
                            defHeight,defWidth,defChannel=defImage.shape
                            if defWidth>104:
                                defImage=cv2.resize(defImage,(104,defHeight))
                            defHeight,defWidth,defChannel=defImage.shape
                            if defence not in ("-2","-1"):
                                baseFrame=pre.CvOverlayImage.overlay(baseFrame,defImage,(1084-defWidth,1572))
                            elif defence!="-1":
                                baseFrame=pre.CvOverlayImage.overlay(baseFrame,defImage,(1084-defWidth,1563))
                        if "pendulum" in imgPath:
                            scalePosY=1173
                            leftScale=self.values["-SCALE_LEFT-"]
                            leftScaleImage=pre.createScaleImage(leftScale)
                            leftScaleWidth=leftScaleImage.shape[1]
                            baseFrame=pre.CvOverlayImage.overlay(baseFrame,leftScaleImage,(120-int(leftScaleWidth/2),scalePosY))
                            rightScale=self.values["-SCALE_RIGHT-"]
                            rightScaleImage=pre.createScaleImage(rightScale)
                            rightScaleWidth=rightScaleImage.shape[1]
                            baseFrame=pre.CvOverlayImage.overlay(baseFrame,rightScaleImage,(1060-int(rightScaleWidth/2),scalePosY))
                    if name!="":
                        textImage=pre.createNameImage(name,self.values,self.lang)
                        if self.lang=="jp":
                            baseFrame=pre.CvOverlayImage.overlay(baseFrame,textImage,(105,85))
                        else:
                            baseFrame=pre.CvOverlayImage.overlay(baseFrame,textImage,(85,75))
                    if self.illust is not None:
                        illustHeight,illustWidth,_=self.illust.shape
                        illustImage=self.illust
                        if self.isP:
                            if illustHeight!=1028 or illustWidth!=1028:
                                illustImage=cv2.resize(self.illust,(1028,1028))
                            illustImage=cv2.copyMakeBorder(illustImage, 307, 385, 77, 77, cv2.BORDER_CONSTANT, value=(0,0,0))
                        else:
                            if illustHeight!=904 or illustWidth!=904:
                                illustImage=cv2.resize(illustImage,(904,904))
                            illustImage=cv2.copyMakeBorder(illustImage, 311, 505, 138, 138, cv2.BORDER_CONSTANT, value=(0,0,0))
                        baseFrame=pre.CvOverlayImage.overlay(illustImage,baseFrame,(0,0))
                    self.cardImageWithoutText=baseFrame
                    if self.values["-CARD_TYPE_NORMAL-"]:
                        self.textFontType="normal"
                    elif self.values["-CARD_TYPE_SPELL-"] or self.values["-CARD_TYPE_TRAP-"]:
                        self.textFontType="st"
                    else:
                        self.textFontType=None
                    if self.lang=="jp":
                        text=jpText if jpChange else self.values["-ADJUST_TEXT_JP_HIDDEN-"]
                        textP=jpTextP if jpPChange else self.values["-ADJUST_PTEXT_JP_HIDDEN-"]
                    else:
                        text=enText if enChange else self.values["-ADJUST_TEXT_EN_HIDDEN-"]
                        textP=enTextP if enPChange else self.values["-ADJUST_PTEXT_EN_HIDDEN-"]
                    baseFrame=self.textDraw(baseFrame,text,self.textFontType)
                    if self.isP:
                        baseFrame=self.textDrawP(baseFrame,textP)
                else:
                    self.mainWindow["-TEXT_ADJUST-"].update(disabled=True)
                    self.mainWindow["-INSERT_IMAGE-"].update(disabled=True)
                    self.cardImageWithoutText=baseFrame
                self.cardImage=baseFrame
                baseFrame = cv2.resize(baseFrame, canvasSize)
                self.canvas.erase()
                self.canvas.draw_image_plus(baseFrame)
                if self.bigCanvas is not None:
                    if self.bigImage is None:
                        self.bigImage=cv2.resize(self.cardImage,(590,860))
                    else:
                        bigImageHeight,bigImageWidth,_=self.bigImage.shape
                        self.bigImage=cv2.resize(self.cardImage,(bigImageWidth,bigImageHeight))
                    self.bigCanvas.draw_image_plus(self.bigImage)
                if "LANGUAGE" in self.event and self.adjustWindow is not None:
                    self.adjustWindow.close()
                    self.adjustWindow=None
                    self.mainWindow.write_event_value("-TEXT_ADJUST-",None)
            elif self.event=="-IMAGE_SAVE-":
                if self.saveWindow is None:
                    self.saveWindow=sg.Window("保存",wl.saveWindowLayout(),resizable=False,finalize=True,location=(int(self.mainWindow.current_location()[0]+wl.WIDTH/3),int(self.mainWindow.current_location()[1]+wl.HEIGHT/2)),icon=self.ICON)
                    self.saveWindow["-SAVE_NAME-"].update(self.values["-ID-"])
                    vcmd = (self.saveWindow.TKroot.register(vali.validateNumber),'%P',0,1180)
                    self.saveWindow["-SAVE_WIDTH-"].widget.configure(validate='all',validatecommand=vcmd)
                    vcmd = (self.saveWindow.TKroot.register(vali.validateNumber),'%P',0,1720)
                    self.saveWindow["-SAVE_HEIGHT-"].widget.configure(validate='all',validatecommand=vcmd)
                else:
                    self.saveWindow.close()
                    self.saveWindow=None
            elif self.event=="-TEXT_ADJUST-":
                if self.adjustWindow is None:
                    self.adjustWindow=sg.Window("",wl.adjustWindowLayout(self.lang),resizable=False,finalize=True,location=(self.mainWindow.current_location()[0]+wl.WIDTH+40,self.mainWindow.current_location()[1]),size=(wl.ADJUST_WIDTH,wl.ADJUST_HEIGHT),icon=self.ICON)
                    self.adjustWindow["-ADJUST_TEXT_"+self.lang.upper()+"-"].update(self.values["-ADJUST_TEXT_"+self.lang.upper()+"_HIDDEN-"])
                    self.adjustWindow["-ADJUST_PTEXT_"+self.lang.upper()+"-"].update(self.values["-ADJUST_PTEXT_"+self.lang.upper()+"_HIDDEN-"])
                    self.adjustWindow["-ADJUST_TEXT_"+self.lang.upper()+"-"].Widget.configure(undo=True)
                    self.adjustWindow["-ADJUST_PTEXT_"+self.lang.upper()+"-"].Widget.configure(undo=True)
                    if self.isP:
                        self.adjustWindow["-TAB_ADJUST_TEXT_"+self.lang.upper()+"_P-"].update(disabled=False)
                    else:
                        self.adjustWindow["-TAB_ADJUST_TEXT_"+self.lang.upper()+"_P-"].update(disabled=True)
                else:
                    self.adjustWindow.close()
                    self.adjustWindow=None
            elif "ADJUST_TEXT_" in self.event or "ADJUST_PTEXT_" in self.event:
                hidden="-ADJUST_TEXT_"+self.lang.upper()+"_HIDDEN-"
                hiddenP="-ADJUST_PTEXT_"+self.lang.upper()+"_HIDDEN-"
                text=self.values["-ADJUST_TEXT_"+self.lang.upper()+"-"]
                textP=self.values["-ADJUST_PTEXT_"+self.lang.upper()+"-"]
                self.mainWindow[hidden].update(text)
                self.mainWindow[hiddenP].update(textP)
                baseFrame=self.textDraw(self.cardImageWithoutText,text,self.textFontType)
                if self.isP:
                    baseFrame=self.textDrawP(baseFrame,textP)
                self.cardImage=baseFrame
                baseFrame = cv2.resize(baseFrame, canvasSize)
                self.canvas.erase()
                self.canvas.draw_image_plus(baseFrame)
                if self.bigCanvas is not None:
                    if self.bigImage is None:
                        self.bigImage=cv2.resize(self.cardImage,(590,860))
                    else:
                        bigImageHeight,bigImageWidth,_=self.bigImage.shape
                        self.bigImage=cv2.resize(self.cardImage,(bigImageWidth,bigImageHeight))
                    self.bigCanvas.draw_image_plus(self.bigImage)
            elif self.event=="-ILLUST_PATH-":
                path=self.values["-ILLUST_PATH-"]
                self.illust=self.imread(path)
                self.mainWindow.write_event_value("-TAB_GROUP-","-TAB_PREVIEW-")
            elif self.event=="-IMAGE_WINDOW-":
                if self.imageWindow is None:
                    bigCanvasLayout,self.bigCanvas=wl.imageWindowLayout()
                    self.imageWindow=sg.Window("拡大画像",bigCanvasLayout,resizable=False,finalize=True,location=(self.mainWindow.current_location()[0]+wl.WIDTH+40,self.mainWindow.current_location()[1]),return_keyboard_events=True,icon=self.ICON)
                    if self.bigImage is None:
                        self.bigImage=cv2.resize(self.cardImage,(590,860))
                    else:
                        bigImageHeight,bigImageWidth,_=self.bigImage.shape
                        self.bigImage=cv2.resize(self.cardImage,(bigImageWidth,bigImageHeight))
                    self.bigCanvas.draw_image_plus(self.bigImage)
                else:
                    self.imageWindow.close()
                    self.imageWindow=None
            elif self.saveWindow is not None and (self.event=="-SAVE_WIDTH-" or self.event=="-SET_ASPECT-"):
                try:
                    if self.values["-SET_ASPECT-"]:
                        val=int(1720*int(self.values["-SAVE_WIDTH-"])/1180) if int(1720*int(self.values["-SAVE_WIDTH-"])/1180)<=1720 else 1720
                        self.saveWindow["-SAVE_HEIGHT-"].update(val)
                except:
                    pass
            elif self.event=="-SAVE_HEIGHT-" and self.saveWindow is not None:
                try:
                    if self.values["-SET_ASPECT-"]:
                        val=int(1180*int(self.values["-SAVE_HEIGHT-"])/1720) if int(1180*int(self.values["-SAVE_HEIGHT-"])/1720)<=1180 else 1180
                        if val==0: val=1
                        self.saveWindow["-SAVE_WIDTH-"].update(val)
                except:
                    pass
            elif self.event=="-SAVE_IMAGE-" and self.saveWindow is not None:
                try:
                    path=self.values["-SAVE_FOLDER-"]
                    name=self.values["-SAVE_NAME-"]
                    ext=self.values["-SAVE_EXTENSION-"]
                    path=path+"/"+name+"."+ext
                    size=(int(self.values["-SAVE_WIDTH-"]),int(self.values["-SAVE_HEIGHT-"]))
                    saveImage=cv2.resize(self.cardImage,size)
                    if self.imwrite(path, saveImage):
                        sg.popup('保存しました',location=(int(self.saveWindow.current_location()[0]+80),int(self.saveWindow.current_location()[1]+80)),icon=self.ICON)
                    else:
                        raise SystemError()
                except:
                    sg.popup('保存失敗。保存先・ファイル名・画像サイズに問題がある可能性があります',location=(int(self.saveWindow.current_location()[0]),int(self.saveWindow.current_location()[1])),icon=self.ICON)
            elif self.event=="-RESET-":
                self.reset()
            elif type(self.event) is tuple and self.event[0]=="-CDB_DATAS-" and self.event[2][0] is not None and self.event[2][0]!=-1:
                index=self.values["-CDB_DATAS-"][0]
                i=index
                if index>=len(self.cdbTexts): i=len(self.cdbTexts)-1
                texts=self.cdbTexts[i]
                if self.cdbDatas[index][0]!=texts[0]:
                    i=0
                    while i<len(self.cdbTexts):
                        texts=self.cdbTexts[i]
                        if self.cdbDatas[index][0]==texts[0]: break
                        i+=1
                if i<len(self.cdbTexts):
                    self.mainWindow["-CDB_TEXTS-"].update(select_rows=[i])
                    self.mainWindow["-CDB_TEXTS-"].set_vscroll_position(i/len(self.cdbTexts))
                else:
                    sg.popup('選択されたdatasに対応するtextsが存在しません。',location=(int(self.mainWindow.current_location()[0]+wl.WIDTH/3),int(self.mainWindow.current_location()[1]+wl.HEIGHT/2)),icon=self.ICON)
                    self.mainWindow["-CDB_TEXTS-"].update(select_rows=[])
            elif type(self.event) is tuple and self.event[0]=="-CDB_TEXTS-" and self.event[2][0] is not None and self.event[2][0]!=-1:
                index=self.values["-CDB_TEXTS-"][0]
                i=index
                if index>=len(self.cdbDatas): i=len(self.cdbDatas)-1
                datas=self.cdbDatas[i]
                if self.cdbTexts[index][0]!=datas[0]:
                    i=0
                    while i<len(self.cdbDatas):
                        datas=self.cdbDatas[i]
                        if self.cdbTexts[index][0]==datas[0]: break
                        i+=1
                if i<len(self.cdbDatas):
                    self.mainWindow["-CDB_DATAS-"].update(select_rows=[i])
                    self.mainWindow["-CDB_DATAS-"].set_vscroll_position(i/len(self.cdbDatas))
                else:
                    sg.popup('選択されたtextsに対応するdatasが存在しません。',location=(int(self.mainWindow.current_location()[0]+wl.WIDTH/3),int(self.mainWindow.current_location()[1]+wl.HEIGHT/2)),icon=self.ICON)
                    self.mainWindow["-CDB_DATAS-"].update(select_rows=[])
            elif self.event=="-CDB_DATAS-_Double" and len(self.values["-CDB_DATAS-"])==1:
                if self.detailDatasWindow is not None:
                    self.detailDatasWindow.close()
                self.tmpData=[]
                index=self.values["-CDB_DATAS-"][0]
                i=0
                self.detailDatasWindow=sg.Window("",wl.datasLayout(),resizable=False,finalize=True,location=(int(self.mainWindow.current_location()[0]-wl.WIDTH/3),int(self.mainWindow.current_location()[1]+wl.HEIGHT/2)),icon=self.ICON)
                self.detailDatasWindow["-CDB_PATH-"].update(self.values["-CDB_PATH-"])
                for d in self.DATA_VALIDATE:
                    self.detailDatasWindow[d[0]].update(self.cdbDatas[index][i])
                    self.tmpData.append(self.cdbDatas[index][i])
                    vcmd = (self.detailDatasWindow.TKroot.register(vali.validateNumber),'%P',d[1],d[2])
                    self.detailDatasWindow[d[0]].widget.configure(validate='all',validatecommand=vcmd)
                    i+=1
            elif self.event=="-DATA_UPDATE-" and self.detailDatasWindow is not None:
                sql="UPDATE datas SET "
                whe="WHERE "
                i=0
                ch=[]
                for d in self.DATA_VALIDATE:
                    com=d[0].replace("-","").split("_")[2].lower()
                    ch.append(self.values[d[0]])
                    if com=="id":
                        sql+=f"{com} = {self.values[d[0]]}"
                        whe+=f"{com} = {self.tmpData[i]}"
                    else:
                        sql+=f", {com} = {self.values[d[0]]}"
                        whe+=f" AND {com} = {self.tmpData[i]}"
                    i+=1
                sql+=f" {whe}"
                path=self.values["-CDB_PATH-"]
                try:
                    with sqlite3.connect(path) as conn:
                        cur=conn.cursor()
                        cur.execute(sql)
                        cur.close()
                        sg.popup('変更しました。',location=(int(self.mainWindow.current_location()[0]+wl.WIDTH/3),int(self.mainWindow.current_location()[1]+wl.HEIGHT/2)),icon=self.ICON)
                        self.tmpData=ch
                        self.mainWindow.write_event_value("-READ_CDB-",None)
                except Exception as e:
                    #print(e)
                    sg.popup('変更失敗。cdbが移動しているかデータに誤りがある可能性があります。',location=(int(self.mainWindow.current_location()[0]+wl.WIDTH/3),int(self.mainWindow.current_location()[1]+wl.HEIGHT/2)),icon=self.ICON)
            elif self.event=="-CDB_TEXTS-_Double" and len(self.values["-CDB_TEXTS-"])==1:
                if self.detailTextsWindow is not None:
                    self.detailTextsWindow.close()
                self.tmpText=[]
                index=self.values["-CDB_TEXTS-"][0]
                i=0
                self.detailTextsWindow=sg.Window("",wl.textsLayout(),resizable=False,finalize=True,location=(int(self.mainWindow.current_location()[0]-wl.WIDTH),int(self.mainWindow.current_location()[1]+wl.HEIGHT/2)),icon=self.ICON)
                self.detailTextsWindow["-CDB_PATH-"].update(self.values["-CDB_PATH-"])
                self.detailTextsWindow["-TEXT_DETAIL_DESC-"].Widget.configure(undo=True)
                for d in self.TEXT_VALIDATE:
                    self.detailTextsWindow[d[0]].update(self.cdbTexts[index][i])
                    self.tmpText.append(self.cdbTexts[index][i])
                    if len(d)==3:
                        vcmd = (self.detailTextsWindow.TKroot.register(vali.validateNumber),'%P',d[1],d[2])
                        self.detailTextsWindow[d[0]].widget.configure(validate='all',validatecommand=vcmd)
                    i+=1
            elif self.event=="-TEXT_UPDATE-" and self.detailTextsWindow is not None:
                sql="UPDATE texts SET "
                whe="WHERE "
                i=0
                ch=[]
                path=self.values["-CDB_PATH-"]
                for d in self.TEXT_VALIDATE:
                    com=d[0].replace("-","").split("_")[2].lower()
                    ch.append(self.values[d[0]])
                    if com=="id":
                        sql+=f"{com} = {self.values[d[0]]}"
                        whe+=f"{com} = {self.tmpText[i]}"
                    else:
                        sql+=f", {com} = '{self.values[d[0]]}'"
                        whe+=f" AND {com} = '{self.tmpText[i]}'"
                    i+=1
                sql+=f" {whe}"
                try:
                    with sqlite3.connect(path) as conn:
                        cur=conn.cursor()
                        cur.execute(sql)
                        cur.close()
                        sg.popup('変更しました。',location=(int(self.mainWindow.current_location()[0]+wl.WIDTH/3),int(self.mainWindow.current_location()[1]+wl.HEIGHT/2)),icon=self.ICON)
                        self.tmpText=ch
                        self.mainWindow.write_event_value("-READ_CDB-",None)
                except Exception as e:
                    print(e)
                    sg.popup('変更失敗。cdbが移動しているかデータに誤りがある可能性があります。',location=(int(self.mainWindow.current_location()[0]+wl.WIDTH/3),int(self.mainWindow.current_location()[1]+wl.HEIGHT/2)),icon=self.ICON)
            elif self.event=="-DELETE_CDB-":
                if self.values["-TAB_CDB_GROUP-"]=="-TAB_CDB_DATAS-":
                    db=self.cdbDatas
                    val=self.values["-CDB_DATAS-"]
                else:
                    db=self.cdbTexts
                    val=self.values["-CDB_TEXTS-"]
                if db is None:
                    sg.popup('cdbを読み込んでください。',location=(int(self.mainWindow.current_location()[0]+wl.WIDTH/3),int(self.mainWindow.current_location()[1]+wl.HEIGHT/2)),icon=self.ICON)
                elif len(val)==0:
                    sg.popup('読み込むレコードを選択してください。',location=(int(self.mainWindow.current_location()[0]+wl.WIDTH/3),int(self.mainWindow.current_location()[1]+wl.HEIGHT/2)),icon=self.ICON)
                else:
                    yesno=sg.popup_yes_no('本当に削除しますか？',location=(int(self.mainWindow.current_location()[0]+wl.WIDTH/3),int(self.mainWindow.current_location()[1]+wl.HEIGHT/2)),icon=self.ICON)
                    if yesno=="Yes":
                        path=self.values["-CDB_PATH-"]
                        try:
                            with sqlite3.connect(path) as conn:
                                if db==self.cdbDatas:
                                    datas=self.cdbDatas[val[0]]
                                    sql=f"DELETE FROM datas WHERE id = {datas[0]} AND ot = {datas[1]} AND alias = {datas[2]} AND setcode = {datas[3]} AND type = {datas[4]} AND atk = {datas[5]} AND def = {datas[6]} AND level = {datas[7]} AND race = {datas[8]} AND attribute = {datas[9]} AND category = {datas[10]};"
                                elif db==self.cdbTexts:
                                    texts=self.cdbTexts[val[0]]
                                    sql=f"DELETE FROM texts WHERE id = {texts[0]} AND name = '{texts[1]}' AND desc = '{texts[2]}'"
                                    for i in range(1,17):
                                        sql+=f" AND str{i} = '{texts[i+2]}'"
                                cur=conn.cursor()
                                cur.execute(sql)
                                cur.close()
                                sg.popup('削除しました。',location=(int(self.mainWindow.current_location()[0]+wl.WIDTH/3),int(self.mainWindow.current_location()[1]+wl.HEIGHT/2)),icon=self.ICON)
                                self.mainWindow.write_event_value("-READ_CDB-",None)
                        except Exception as e:
                            #print(e)
                            sg.popup('削除できませんでした。cdbのパスが間違っているか既に削除されている可能性があります。',location=(int(self.mainWindow.current_location()[0]+wl.WIDTH/3),int(self.mainWindow.current_location()[1]+wl.HEIGHT/2)),icon=self.ICON)
            elif self.event=="-READ_CDB-":
                path=self.values["-CDB_PATH-"]
                try:
                    with sqlite3.connect(path) as conn:
                        cur=conn.cursor()
                        cur.execute('SELECT * FROM datas')
                        self.cdbDatas=cur.fetchall()
                        self.mainWindow["-CDB_DATAS-"].update(self.cdbDatas)
                        cur.execute('SELECT * FROM texts')
                        self.cdbTexts=cur.fetchall()
                        self.mainWindow["-CDB_TEXTS-"].update(self.cdbTexts)
                        cur.close()
                except Exception as e:
                    #print(e)
                    sg.popup('読み込み失敗。cdbのパスを再確認してください。',location=(int(self.mainWindow.current_location()[0]+wl.WIDTH/3),int(self.mainWindow.current_location()[1]+wl.HEIGHT/2)),icon=self.ICON)
            elif self.event=="-LOAD_CDB-":
                if self.cdbDatas is None:
                    sg.popup('cdbを読み込んでください。',location=(int(self.mainWindow.current_location()[0]+wl.WIDTH/3),int(self.mainWindow.current_location()[1]+wl.HEIGHT/2)),icon=self.ICON)
                elif len(self.values["-CDB_DATAS-"])==0 or len(self.values["-CDB_TEXTS-"])==0:
                    sg.popup('datas,textsともに存在するレコードを選択してください。',location=(int(self.mainWindow.current_location()[0]+wl.WIDTH/3),int(self.mainWindow.current_location()[1]+wl.HEIGHT/2)),icon=self.ICON)
                else:
                    self.reset()
                    pen=False
                    lin=False
                    datas=self.cdbDatas[self.values["-CDB_DATAS-"][0]]
                    self.mainWindow["-ID-"].update(datas[0])
                    self.mainWindow["-OT-"].update(["OCG","TCG","OCG/TCG","Custom"][datas[1]-1])
                    self.mainWindow["-ALIAS-"].update(datas[2])
                    self.mainWindow["-SETCODE-"].update(datas[3])
                    tybin=format(datas[4],"b")[::-1]
                    numType={v: k for k, v in cti.TYPE_VALUE.items()}
                    for i in range(len(tybin)):
                        b=tybin[i]
                        if b=="1":
                            n=2**i
                            if n in numType.keys():
                                self.mainWindow[f"-CARD_TYPE_{numType[n]}-"].update(True)
                                if f"-CARD_TYPE_{numType[n]}-"=="-CARD_TYPE_PENDULUM-":
                                    pen=True
                                    self.isP=True
                                    for scale in cti.SCALE:
                                        self.mainWindow[f"{scale}"].update(disabled=False)
                                if f"-CARD_TYPE_{numType[n]}-"=="-CARD_TYPE_LINK-":
                                    lin=True
                                    for dis in self.DISABLE_LINK_STATUS:
                                        self.mainWindow[f"{dis}"].update(disabled=True)
                                    for marker in cti.LINK_MARKER.keys():
                                        self.mainWindow[f"-LINK_MARKER{marker}-"].update(disabled=False)
                    self.mainWindow["-ATK-"].update(datas[5])
                    if lin:
                        defbin=format(datas[6],"b")[::-1]
                        numMarker={v: k for k, v in cti.LINK_MARKER.items()}
                        for i in range(len(defbin)):
                            b=defbin[i]
                            if b=="1":
                                n=2**i
                                if n in numMarker.keys():
                                    self.mainWindow[f"-LINK_MARKER{numMarker[n]}-"].update(True)
                    self.mainWindow["-DEF-"].update(datas[6])
                    if pen:
                        levelHex=format(datas[7],"x")
                        level=int(levelHex[-4:],16)
                        rightScale=int(levelHex[-6:-4],16)
                        leftScale=int(levelHex[:-6],16)
                        self.mainWindow["-LEVEL-"].update(level)
                        self.mainWindow["-SCALE_RIGHT-"].update(rightScale)
                        self.mainWindow["-SCALE_LEFT-"].update(leftScale)
                    else:
                        self.mainWindow["-LEVEL-"].update(datas[7])
                    self.mainWindow["-RACE-"].update(wl.RACE[int(math.log2(datas[8]))+1 if datas[8]!=0 else 0])
                    self.mainWindow["-ATTRIBUTE-"].update(wl.ATTRIBUTE[int(math.log2(datas[9]))+1 if datas[9]!=0 else 0])
                    catbin=format(datas[10],"b")[::-1]
                    numCat={v: k for k, v in ci.CATEGORY_VALUE.items()}
                    for i in range(len(catbin)):
                        b=catbin[i]
                        if b=="1":
                            n=2**i
                            if n in numCat.keys():
                                self.mainWindow[f"-CATEGORY_{numCat[n]}-"].update(True)
                    texts=self.cdbTexts[self.values["-CDB_TEXTS-"][0]]
                    self.mainWindow["-CARD_NAME-"].update(texts[1])
                    t=texts[2]
                    if pen and re.search("【Ｐスケール：青.*】",t,flags=0) and re.search("【モンスター.*】",t,flags=0):
                        try:
                            t=re.split('【モンスター.*】', re.split('【Ｐスケール：青.*】', t)[1].strip())
                            pt=t[0].strip()
                            mt=t[1].strip()
                            self.mainWindow["-CARD_TEXT-"].update(mt)
                            self.mainWindow["-CARD_TEXT_P-"].update(pt)
                        except:
                            self.mainWindow["-CARD_TEXT-"].update(texts[2])
                    else:
                        self.mainWindow["-CARD_TEXT-"].update(texts[2])
                    for i in range(3,19):
                        self.mainWindow[f"-CARD_STR{i-2}-"].update(texts[i])
                    sg.popup('レコードから反映しました。',location=(int(self.mainWindow.current_location()[0]+wl.WIDTH/3),int(self.mainWindow.current_location()[1]+wl.HEIGHT/2)),icon=self.ICON)
            elif self.event=="-WRITE_CDB-":
                path=self.values["-CDB_PATH-"]
                try:
                    with sqlite3.connect(path) as conn:
                        cur=conn.cursor()
                        sql=self.createSQL("data")
                        cur.execute(sql)
                        sql=self.createSQL("text")
                        cur.execute(sql)
                        cur.close()
                        sg.popup('追加しました。',location=(int(self.mainWindow.current_location()[0]+wl.WIDTH/3),int(self.mainWindow.current_location()[1]+wl.HEIGHT/2)),icon=self.ICON)
                        self.mainWindow.write_event_value("-READ_CDB-",None)
                except Exception as e:
                    #print(e)
                    sg.popup('書き込み失敗。cdbのパスが誤っているか既に同様のレコードが存在している可能性があります。',location=(int(self.mainWindow.current_location()[0]+wl.WIDTH/3),int(self.mainWindow.current_location()[1]+wl.HEIGHT/2)),icon=self.ICON)
        self.mainWindow.close()

if __name__=="__main__":
    main()