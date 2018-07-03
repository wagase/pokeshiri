# -*- coding: utf-8 -*-
import json
import random
import collections
import pprint
import ast


def mid(text,s,e):
	return text[s-1:s+e-1]

def left(text,e):
	return text[:e]

def right(text,s):
	return text[-s:]

# pokemon_data.jsonを読み取ってポケモンの名前だけにする
def getpokenamelist():
	dic = {}
	for key in POKEDATA:
		if not key["no"] in dic.keys() :
			dic[key["no"]]=key["name"]
	return dic

# 辞書{'ア':['アーボ','アーボック'....],'イ':['イシツブテ','イワーク'....].....} の形にするが最後にンがつくものは除外
def makekanalistNotnn():
	kanalist = {}
	for i in range(1,len(KATAKANA)+1):
		kanas = []
		j = 1
		for key in POKENAMELIST:
			if left(POKENAMELIST[key],1) == mid(KATAKANA,i,1) and right(POKENAMELIST[key],1) != "ン" :
				kanas.append(POKENAMELIST[key])
				j = j +1
		kanalist[mid(KATAKANA,i,1)] = kanas
	return kanalist

# 辞書{'ア':['アーボ','アーボック'....],'イ':['イシツブテ','イワーク'....].....} の形にするが「ン」で終わるやつを取得
def makekanalistGetnn():
	kanalist = {}
	for i in range(1,len(KATAKANA)+1):
		kanas = []
		j = 1
		for key in POKENAMELIST:
			if left(POKENAMELIST[key],1) == mid(KATAKANA,i,1) and right(POKENAMELIST[key],1) == "ン" :
				kanas.append(POKENAMELIST[key])
				j = j +1
		kanalist[mid(KATAKANA,i,1)] = kanas
	return kanalist

# makekanalistNotnnのリストから指定した文字で始まるポケモンを適当に選ぶ
def pokechoice(kana):
	val =""
	if len(stock[kana]) == 0 :
		if len(nstock[kana]) != 0 :
			val = random.choice(nstock[kana])
			memoryRemark(val)
			delnstock(kana,val)
		val= val + "・・・もう【"+kana+"】から始まるポケモンは答えられないよ。負けました。リセットしてね"
		if penalty !=0 :
			val= val +" ペナルティ合計は(" +str(penalty) +"回)でした"
	else :
		val = random.choice(stock[kana])
		memorylastword(val)
		reqstockappend(val)
		delstock(kana,val)
		rest = len(stock[kana])
		memoryRemark(val)
		val = val + "・・・【"+kana+"】のこり【"+str(rest)+"】" + "次のことばは【"+getshiri(val)+"】です"
	return val

# そのポケモンがしりとりで存在するかどうか
def checkExistencePoke(req):
	if req in POKENAMELIST.values():
		return True
	else :
		return False

# そのポケモンがそもそも存在するかどうか
def checkExistenceAllPoke(req):
	for key in POKEDATA:
		if req == key["name"] :
			return True
	return False

# しりとりメソッド
def shiritori(req):
	atama = left(req,1)
	shiri = getshiri(req)
	if shiri == "ン":
		global penalty
		penalty = penalty +1
		return "「ン」で終わるやつはだめだよ ペナルティ(" +str(penalty) +"回)"
	else :
		if req in stock[atama]:
			delstock(atama,req)
		return pokechoice(shiri)

# 末尾の文字を調整する
def getshiri(req):
	shiri = right(req,1)
	# ミミッキュ対策
	if shiri in "ァィゥェォッャュョヮヵヶ" :
		shiri = shiri.replace("ァ","ア")
		shiri = shiri.replace("ィ","イ")
		shiri = shiri.replace("ゥ","ウ")
		shiri = shiri.replace("ェ","エ")
		shiri = shiri.replace("ォ","オ")
		shiri = shiri.replace("ッ","ツ")
		shiri = shiri.replace("ャ","ヤ")
		shiri = shiri.replace("ュ","ユ")
		shiri = shiri.replace("ョ","ヨ")
		shiri = shiri.replace("ヮ","ワ")
		shiri = shiri.replace("ヵ","カ")
		shiri = shiri.replace("ヶ","ケ")
	# 長音対策
	if shiri == "ー" :
		shiri = mid(req,len(req)-1,1)
	return shiri

# 一度いったやつはストックから消す
def delstock(kana,val):
	stock[kana].remove(val)

# 一度いったやつはストックから消す
def delnstock(kana,val):
	nstock[kana].remove(val)

# 一度言われたやつを覚える
def reqstockappend(req):
	reqstock.append(req)

# 一度言われたことがあるかどうかしらべる
def checkExistencereq(req):
	if req in reqstock:
		return True
	else:
		return False

# 何回言われてるか調べて返す
def countreqstock(req):
	global penalty
	penalty = penalty +1
	return req + "は【" + str(reqstock.count(req)+1) + "】回目だよ。できれば違うやつ言ってね ペナルティ(" +str(penalty) +"回)"

#　リセット
def reset():
	global stock
	global nstock
	global lastWord
	global reqstock
	global penalty 
	penalty = 0
	lastWord =""
	stock = makekanalistNotnn()
	nstock = makekanalistGetnn()
	reqstock.clear()

# ヒント
def hint(req):
	global penalty
	if req in stock:
		penalty = penalty + 1
		return stock[req]
	else:
		return "カタカナ一文字でお願いします"

# 詳細機能
def getpokedetail(req):
	ret = ""
	for key in POKEDATA:
		if key["name"] == req :
			ret = ret + str(key) + "\n"
	return deteal_formating(ret)

# 詳細の文字列を整列化する
def deteal_formating(moji):
        ret = ast.literal_eval(moji)
        ret = pprint.pformat(ret)
        ret = ret.replace("{","").replace("}","")
        return ret
        
# 最後の文字を覚える
def memorylastword(req):
	global lastWord
	lastWord = getshiri(req)

# しりとりになってるか調べる
def checkTruelastword(req):
	if lastWord != left(req,1) and not lastWord=="":
		return False
	else :
		return True

# しりとりになってないメッセージ
def forgivelastword(req):
	global penalty
	penalty = penalty + 1
	return req + "はしりとりになってないよ。できれば【"+lastWord+"】から始まるやつ言ってほしかったな ペナルティ(" +str(penalty) +"回)"


# 呼ばれたものを記憶
def memoryRemark(req):
	remarkstock.append(req)

# ランキングカウント
def remarkRanking():
	ret =""
	i = 0
	c = collections.Counter(remarkstock)
	for item in c.most_common() :
		i=i+1
		if i > 5 :
			break
		ret = ret + str(item[0]) + "　" + str(item[1]) + "回"+ "\n"
	return ret



# 定数群
KATAKANA = "アイウエオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモヤユヨラリルレロワヲンヴ"
POKEDATA = json.load(open("data/pokemon_data.json","r",encoding="utf-8"))
POKENAMELIST = getpokenamelist()

# 変数群
stock = makekanalistNotnn()
nstock = makekanalistGetnn()
remarkstock=[]
reqstock =[]
lastWord =""
penalty =0
