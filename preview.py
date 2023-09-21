import cv2
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageChops
import re
from io import BytesIO

import cardTypeIndex as cti
import bfont

def baseImage(values,lang):
    path="./images/others/unknown.png"
    monster,spell,trap=values["-CARD_TYPE_MONSTER-"],values["-CARD_TYPE_SPELL-"],values["-CARD_TYPE_TRAP-"]
    monsters=["NORMAL","EFFECT","FUSION","RITUAL","SYNCHRO","XYZ","LINK","PENDULUM","TOKEN"]
    if [monster,spell,trap].count(True)>1:
        pass
    elif monster:
        normal,effect,fusion,ritual,synchro,xyz,link,pendulum,token=(values[f"-CARD_TYPE_{ctype}-"] for ctype in monsters)
        if [normal,fusion,ritual,synchro,xyz,link].count(True)>1 or [fusion,ritual,synchro,xyz,link,token].count(True)>1 or [normal,effect].count(True)>1 or [pendulum,link].count(True)>1:
            pass
        elif normal:
            if pendulum:
                path="./images/monster/pendulum_normal.png"
            elif token:
                path="./images/monster/token.png"
            else:
                path="./images/monster/normal.png"
        elif fusion:
            if pendulum:
                path="./images/monster/pendulum_fusion.png"
            else:
                path="./images/monster/fusion.png"
        elif ritual:
            if pendulum:
                path="./images/monster/pendulum_ritual.png"
            else:
                path="./images/monster/ritual.png"
        elif synchro:
            if pendulum:
                path="./images/monster/pendulum_synchro.png"
            else:
                path="./images/monster/synchro.png"
        elif xyz:
            if pendulum:
                path="./images/monster/pendulum_xyz.png"
            else:
                path="./images/monster/xyz.png"
        elif link:
            path="./images/monster/link.png"
        elif effect:
            if pendulum:
                path="./images/monster/pendulum_effect.png"
            else:
                path="./images/monster/effect.png"
    elif spell:
        ritual,equip,quick,field,continuous=(values[ctype] for ctype in cti.SPELL_CHECK)
        if [ritual,equip,quick,field,continuous].count(True)>1:
            pass
        elif ritual:
            path="./images/spell/"+lang+"/ritual.png"
        elif equip:
            path="./images/spell/"+lang+"/equip.png"
        elif quick:
            path="./images/spell/"+lang+"/quick.png"
        elif field:
            path="./images/spell/"+lang+"/field.png"
        elif continuous:
            path="./images/spell/"+lang+"/continuous.png"
        else:
            path="./images/spell/"+lang+"/normal.png"
    elif trap:
        continuous,counter=(values[ctype] for ctype in cti.TRAP_CHECK)
        if [continuous,counter].count(True)>1:
            pass
        elif continuous:
            path="./images/trap/"+lang+"/continuous.png"
        elif counter:
            path="./images/trap/"+lang+"/counter.png"
        else:
            path="./images/trap/"+lang+"/normal.png"
    return path

def attributePath(att,lang):
    attE=cti.ATTRIBUTE_JE[att]
    path=""
    if attE!="":
        path="./images/attribute/"+lang+"/"+attE+".png"
    return path

def linkMarkerPath(values):
    paths=[]
    markerName=list(cti.LINK_MARKER.keys())
    markers=[values[f"-LINK_MARKER{onoff}-"] for onoff in markerName]
    for i in range(len(markers)):
        if markers[i]:
            paths.append("./images/monster/marker_on"+markerName[i].lower()+".png")
        else:
            paths.append("./images/monster/marker_off"+markerName[i].lower()+".png")
    return paths

def createNameImage(text,values,lang):
    widthLimit=885
    if values["-CARD_TYPE_XYZ-"] or values["-CARD_TYPE_LINK-"] or values["-CARD_TYPE_SPELL-"] or values["-CARD_TYPE_TRAP-"]:
        textColor=(255,255,255)
    else:
        textColor=(0,0,0)
    if lang=="jp":
        return createNameImageJP(text,textColor,widthLimit)
    else:
        return createNameImageEN(text,textColor,widthLimit)

def createNameImageJP(text,textColor,widthLimit):
    baseFont=bfont.NAME_JP
    baseFontSize=90
    font = ImageFont.truetype(BytesIO(baseFont), baseFontSize)
    atfont=None
    textList=[]
    for i in range(len(text)):
        t=text[i]
        textList.append(t)
    imageList=[]
    textHeight=0
    rtnImage=None
    for t in textList:
        if t!="":
            textHeight=max(textHeight,getTextHeight(t,font))
    for t in textList:
        if t!="":
            if t=="＠":
                if atfont is None:
                    atfont = ImageFont.truetype(BytesIO(baseFont), baseFontSize+17)
                cv_image=createWordImage(t,atfont,baseFontSize+17,textColor,textHeight,"jp")
            else:
                cv_image=createWordImage(t,font,baseFontSize,textColor,textHeight,"jp")
            imageList.append(cv_image)
    for image in imageList:
        if rtnImage is None:
            rtnImage=image
        else:
            rtnImage=cv2.hconcat([rtnImage, image])
    imageHeight,imageWidth,imageChannel=rtnImage.shape
    if imageWidth>widthLimit:
        rtnImage = cv2.resize(rtnImage, (widthLimit,imageHeight))
    return rtnImage

def createNameImageEN(text,textColor,widthLimit):
    baseFont=bfont.NAME_EN
    baseFontSize=130
    font = ImageFont.truetype(BytesIO(baseFont), baseFontSize)
    textHeight=0
    rtnImage=None
    if text!="":
        textHeight=max(textHeight,getTextHeight(text,font))
        rtnImage=createWordImage(text,font,baseFontSize,textColor,textHeight,"en")
    imageHeight,imageWidth,imageChannel=rtnImage.shape
    if imageWidth>widthLimit:
        rtnImage = cv2.resize(rtnImage, (widthLimit,imageHeight))
    return rtnImage

def createLinkImage(link):
    link=str(link)
    baseFont=bfont.LINK_NUM
    baseFontSize=39
    font = ImageFont.truetype(BytesIO(baseFont), baseFontSize)
    linkHeight=getTextHeight(link,font)
    linkImage=createWordImage(link,font,baseFontSize,(0,0,0),linkHeight)
    imageHeight,imageWidth,imageChannel=linkImage.shape
    linkImage=cv2.resize(linkImage,(int(imageWidth*1.3),imageHeight))
    return linkImage

def createParamImage(param):
    baseFont=bfont.PARAMETER
    if param=="?":
        baseFontSize=60
    else:
        baseFontSize=52
    font = ImageFont.truetype(BytesIO(baseFont), baseFontSize)
    paramHeight=getTextHeight(param,font)
    paramImage=createWordImage(param,font,baseFontSize,(0,0,0),paramHeight)
    if param=="?":
        paramHeight,paramWidth,_=paramImage.shape
        paramImage=cv2.resize(paramImage,(int(paramWidth*0.8),paramHeight))
    return paramImage

def createRaceImage(values,lang):
    race=values["-RACE-"]
    typeList=[]
    if lang=="jp":
        baseFont=bfont.RACE_JP
        baseFontSize=34
        font = ImageFont.truetype(BytesIO(baseFont), baseFontSize)
        for i in range(len(race)):
            typeList.append(race[i])
        typeList.append("族")
        for ctype in cti.MONSTER_TYPE.keys():
            if values[f"-CARD_TYPE_{ctype}-"]:
                if len(typeList)>0: typeList.append("／")
                text=cti.MONSTER_TYPE[ctype]
                for i in range(len(text)):
                    typeList.append(text[i])
        return createRaceImageJP(font,typeList,baseFontSize)
    else:
        baseFont=bfont.RACE_EN
        baseFontSize=45
        font = ImageFont.truetype(BytesIO(baseFont), baseFontSize)
        typeList.append(cti.RACE_JE[race])
        for ctype in cti.MONSTER_TYPE.keys():
            if lang=="en" and ctype=="SPECIAL_SUMMON": continue
            if values[f"-CARD_TYPE_{ctype}-"]:
                if len(typeList)>0: typeList.append("/")
                typeList.append(ctype.lower().capitalize())
        return createRaceImageEN(font,typeList,baseFontSize)

def createRaceImageJP(font,typeList,fontSize):
    typeList.insert(0,"【")
    typeList.append("】")
    imageList=[]
    widthLimit=995
    textHeight=0
    rtnImage=None
    for t in typeList:
        if t!="":
            textHeight=max(textHeight,getTextHeight(t,font))
    for t in typeList:
        if t!="":
            cv_image=createWordImage(t,font,fontSize,(0,0,0),textHeight,"jp")
            imageList.append(cv_image)
    for image in imageList:
        if rtnImage is None:
            rtnImage=image
        else:
            rtnImage=cv2.hconcat([rtnImage, image])
    imageHeight,imageWidth,imageChannel=rtnImage.shape
    if imageWidth>widthLimit:
        rtnImage = cv2.resize(rtnImage, (widthLimit,imageHeight))
    return rtnImage

def createRaceImageEN(font,typeList,fontSize):
    typeList.insert(0,"[")
    typeList.append("]")
    imageList=[]
    widthLimit=980
    textHeight=0
    rtnImage=None
    for t in typeList:
        if t!="":
            textHeight=max(textHeight,getTextHeight(t,font))
    for t in typeList:
        if t!="":
            cv_image=createWordImage(t,font,fontSize,(0,0,0),textHeight,"en")
            imageList.append(cv_image)
    for image in imageList:
        if rtnImage is None:
            rtnImage=image
        else:
            rtnImage=cv2.hconcat([rtnImage, image])
    imageHeight,imageWidth,imageChannel=rtnImage.shape
    if imageWidth>widthLimit:
        rtnImage = cv2.resize(rtnImage, (widthLimit,imageHeight))
    return rtnImage

def createTextImage(text,lang,fontSize,widthLimit,ctype=None):
    if lang=="jp":
        return createTextImageJP(text,fontSize,widthLimit)
    else:
        return createTextImageEN(text,fontSize,widthLimit,ctype)

def createTextImageJP(text,fontSize,widthLimit):
    baseFont=bfont.NAME_JP
    font = ImageFont.truetype(BytesIO(baseFont), fontSize)
    atfont=None
    textColor=(0,0,0)
    textList=[]
    for i in range(len(text)):
        t=text[i]
        textList.append(t)
    imageList=[]
    textHeight=0
    rtnImage=None
    for t in textList:
        if t!="":
            textHeight=max(textHeight,getTextHeight(t,font))
    for t in textList:
        if t!="" and not re.match("\t",t,flags=0):
            if t=="＠":
                if atfont is None:
                    atfont = ImageFont.truetype(BytesIO(baseFont), fontSize+10)
                cv_image=createWordImage(t,atfont,fontSize+10,textColor,textHeight,"jp")
            else:
                cv_image=createWordImage(t,font,fontSize,textColor,textHeight,"jp")
            imageList.append(cv_image)
    for image in imageList:
        if rtnImage is None:
            rtnImage=image
        else:
            rtnImage=cv2.hconcat([rtnImage, image])
    imageHeight,imageWidth,imageChannel=rtnImage.shape
    if imageWidth>widthLimit:
        rtnImage = cv2.resize(rtnImage, (widthLimit,imageHeight))
    return rtnImage

def createTextImageEN(text,fontSize,widthLimit,ctype):
    if ctype=="normal":
        baseFont=bfont.NORMAL_TEXT_EN
    else:
        baseFont=bfont.TEXT_EN
    font = ImageFont.truetype(BytesIO(baseFont), fontSize)
    textColor=(0,0,0)
    textHeight=0
    rtnImage=None
    if text!="":
        textHeight=max(textHeight,getTextHeight(text,font))
        rtnImage=createWordImage(text,font,fontSize,textColor,textHeight,"en")
    imageHeight,imageWidth,imageChannel=rtnImage.shape
    if imageWidth>widthLimit:
        rtnImage = cv2.resize(rtnImage, (widthLimit,imageHeight))
    return rtnImage

def createScaleImage(text):
    baseFont=bfont.SCALE
    fontSize=85
    font = ImageFont.truetype(BytesIO(baseFont), fontSize)
    textColor=(0,0,0)
    rtnImage=None
    textHeight=0
    if text!="":
        textHeight=max(textHeight,getTextHeight(text,font))
        rtnImage=createWordImage(text,font,fontSize,textColor,textHeight)
    return rtnImage

def getTextHeight(text,font):
    a,b,textWidth, textHeight = font.getbbox(text)
    return textHeight

def createWordImage(text,font,fontSize,textColor,height,lang=None):
    a,b,textWidth, textHeight = font.getbbox(text)
    canvasSize=(textWidth, height)
    img  = Image.new('RGBA', canvasSize, (255-textColor[0],255-textColor[1],255-textColor[2],0))
    draw = ImageDraw.Draw(img)
    textTopLeft = (0,0)
    if lang=="jp" and text=="＠":
        textTopLeft = (0,-(fontSize/107*10))
    draw.text(textTopLeft, text, fill=textColor, font=font)
    cv_image = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGBA2BGRA)
    if lang=="en":
        if text in ("["):
            cv_image=cv2.copyMakeBorder(cv_image, 0, 0, 0, 4, cv2.BORDER_CONSTANT, value=(0,0,0))
        elif text in ("/"):
            cv_image=cv2.copyMakeBorder(cv_image, 0, 0, 5, 5, cv2.BORDER_CONSTANT, value=(0,0,0))
        elif text in ("]"):
            cv_image=cv2.copyMakeBorder(cv_image, 0, 0, 4, 0, cv2.BORDER_CONSTANT, value=(0,0,0))
    elif lang=="jp" and not re.match("\s",text,flags=0):
        threshold=255
        left_margin = 0
        img_data=img.load()
        while left_margin < img.width:
            column = [img_data[left_margin, y] for y in range(img.height)]
            if textColor[0]==0:
                if any(sum(pixel) < threshold * 3 for pixel in column):
                    break
            else:
                if any(sum(pixel) > threshold * 3 for pixel in column):
                    break
            left_margin += 1
        right_margin = img.width - 1
        while right_margin >= 0:
            column = [img_data[right_margin, y] for y in range(img.height)]
            if textColor[0]==0:
                if any(sum(pixel) < threshold * 3 for pixel in column):
                    break
            else:
                if any(sum(pixel) > threshold * 3 for pixel in column):
                    break
            right_margin -= 1
        img = img.crop((left_margin, 0, right_margin + 1, img.height))
        cv_image = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGBA2BGRA)
        pad2=0
        if text in ("ヴ"):
            pad=0
        elif text in ("グ"):
            pad=int(fontSize/18)
        elif text in ("＠","。","、"):
            pad=int(fontSize/6)
        elif re.match("[ぁ-んァ-ヶｱ-ﾝﾞﾟ]",text,flags=0) or text in ("ー","＝","【"):
            pad=int(fontSize/4.5)
        elif text in ["・","："]:
            pad=int(fontSize/3)
            pad2=int(fontSize/6)
        else:
            pad=int(fontSize/9)
        imageHeight,imageWidth,imageChannel=cv_image.shape
        if text=="＠":
            cv_image = cv2.resize(cv_image, (int(imageWidth*0.85),imageHeight))
        cv_image=cv2.copyMakeBorder(cv_image, 0, 0, pad2, pad, cv2.BORDER_CONSTANT, value=(0,0,0))
    return cv_image

class CvOverlayImage(object):
    """
    [summary]
      OpenCV形式の画像に指定画像を重ねる
    """

    def __init__(self):
        pass

    @classmethod
    def overlay(
            cls,
            cv_background_image,
            cv_overlay_image,
            point,
    ):
        """
        [summary]
          OpenCV形式の画像に指定画像を重ねる
        Parameters
        ----------
        cv_background_image : [OpenCV Image]
        cv_overlay_image : [OpenCV Image]
        point : [(x, y)]
        Returns : [OpenCV Image]
        """
        overlay_height, overlay_width = cv_overlay_image.shape[:2]

        # OpenCV形式の画像をPIL形式に変換(α値含む)
        # 背景画像
        cv_rgb_bg_image = cv2.cvtColor(cv_background_image, cv2.COLOR_BGR2RGBA)
        pil_rgb_bg_image = Image.fromarray(cv_rgb_bg_image)
        pil_rgba_bg_image = pil_rgb_bg_image.convert('RGBA')
        # オーバーレイ画像
        cv_rgb_ol_image = cv2.cvtColor(cv_overlay_image, cv2.COLOR_BGRA2RGBA)
        pil_rgb_ol_image = Image.fromarray(cv_rgb_ol_image)
        pil_rgba_ol_image = pil_rgb_ol_image.convert('RGBA')

        # composite()は同サイズ画像同士が必須のため、合成用画像を用意
        pil_rgba_bg_temp = Image.new('RGBA', pil_rgba_bg_image.size,
                                     (255, 255, 255, 0))
        # 座標を指定し重ね合わせる
        pil_rgba_bg_temp.paste(pil_rgba_ol_image, point, pil_rgba_ol_image)
        result_image = \
            Image.alpha_composite(pil_rgba_bg_image, pil_rgba_bg_temp)

        # OpenCV形式画像へ変換
        cv_bgr_result_image = cv2.cvtColor(
            np.asarray(result_image), cv2.COLOR_RGBA2BGRA)

        return cv_bgr_result_image