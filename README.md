# pokeshiri
python slackbot ポケモンの名前でしりとり
python知識ゼロからポケモンの名前でしりとりするslackbotを作ったノウハウのすべて  
https://qiita.com/wagase/items/24eada2db8467119c458



# こんなのです
![pokeshiri1.gif](https://qiita-image-store.s3.amazonaws.com/0/230077/945efd94-22bb-0e12-5c7a-45d6145be9b2.gif)

ソースはgithubで公開してますhttps://github.com/wagase/pokeshiri
よかったら「いいね」してください。

## 環境
OS：windows
言語：python
# 筆者について
趣味でプログラム書いてるにわか。
htmlとcssとjavascriptくらいはかける。
python知識ゼロ
## なぜpython？
話題だから
## なぜslackbot？
開発経験ゼロだから気軽に作れるのがよかった
# 開発環境構築
## 知識ゼロだからまずpythonという言語の仕様を学ぶ
参考にしたサイト
https://www.pythonweb.jp/tutorial/  
斜め読みしながらわからないところはググる
## pythonをwindowsにインストール
https://www.python.org/
Python 3.6.5にしました
Download for windowsからpython-3.6.5.exeを取得して実行
Add Python to PATHチェックする
コンソールでHello pythonくらいはprintできた
## Visual Studio Codeでpythonの設定をする
拡張機能「python」で検索して
・[Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
・[Python for VSCode](https://marketplace.visualstudio.com/items?itemName=tht13.python)
をインストール
pylintがないとかいわれるのでインストール
`pip install pylint`
これでいい感じに開発できるようになった

# slackbotの作り方をググる
参考にしたもの
[Pythonを使ったSlackBotの作成方法](https://qiita.com/kunitaya/items/690028e33ba5c666f3e2)
[PythonのslackbotライブラリでSlackボットを作る](https://qiita.com/sukesuke/items/1ac92251def87357fdf6) 
↑この記事をみながら
`pip3 install slackbot`を実行
slackbotの登録
https://my.slack.com/services/new/bot
にいって書いてある項目を埋めるだけ
API トークンをコピーしておく

# いざ実行
上記の参考サイトを丸パクリして
`python run.py`
をしてみる
Appのところにあるbotがアクティブ表示になった！
リプライすると「何言ってんだこいつ」って返ってくる！！
実行できた！

# あとはゴリゴリプログラミングする
githubで公開中
https://github.com/wagase/pokeshiri
辞書型のあつかいとかわからないところはググる

## ポケモンのデータはこちらからお借りしました
全ポケモンのJSONデータ
https://github.com/kotofurumiya/pokemon_data/blob/master/data/pokemon_data.json
ありがとうございます

## 機能とか
### ポケモンじゃないときは
![image.png](https://qiita-image-store.s3.amazonaws.com/0/230077/82254a21-afb9-6a69-ea19-e23445e409a1.png)

### ンで終わるポケモンはペナルティ
![image.png](https://qiita-image-store.s3.amazonaws.com/0/230077/f09d8944-8643-1897-842d-0432de5eb033.png)
しりとりだから怒られる

### しりとりになってないとペナルティ
![image.png](https://qiita-image-store.s3.amazonaws.com/0/230077/a3e59751-c5dc-b3c7-4dbe-356dcf93db1a.png)
slackのシステム的に１対Nのしりとりを想定してるため多少まちがっても
ゲームオーバーにはならない

### 一度登場したポケモンを言うとペナルティ
![image.png](https://qiita-image-store.s3.amazonaws.com/0/230077/de8d45b3-67c8-a4f7-04a8-0791aa2dd895.png)

### 困ったときはヒントで答えてない一覧をだせる
![image.png](https://qiita-image-store.s3.amazonaws.com/0/230077/a17db2de-7e37-6876-3d30-2f3e81310bec.png)
もちろん一度言うとリストから消える

### 知らないポケモンがでたときに詳細表示機能で教えてもらえる
![image.png](https://qiita-image-store.s3.amazonaws.com/0/230077/e20e0fcc-0b96-5a45-9f15-a71a4800be1e.png)
全ポケモンのJSONデータ作者さんに感謝

### ランキング機能
![image.png](https://qiita-image-store.s3.amazonaws.com/0/230077/5a75113b-28d4-0025-d3e2-81f68082e6f6.png)
登場回数順にランキングを表示。
ル攻めすると勝てるのでルチャブルは受け攻め強い

### リセット機能
![image.png](https://qiita-image-store.s3.amazonaws.com/0/230077/f74b3ff7-b019-aac6-0f60-f37a50c1ffc1.png)
ただのリセット。ゲームリスタートの意味。
リセットするとペナルティと今まで言ったポケモンを忘れる。
リセットしてもランキングは消さない

### ログ表示機能
![image.png](https://qiita-image-store.s3.amazonaws.com/0/230077/72fd7eca-ff36-6040-78d4-3401a9f5434a.png)
今までの記録を教えてくれる

## ソース
ソースはgithubで公開してます
https://github.com/wagase/pokeshiri

```my_mention.py
# -*- coding: utf-8 -*-
from slackbot.bot import respond_to     # @botname: で反応するデコーダ
from slackbot.bot import listen_to      # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ
from libs import my_functions           # 自作関数の読み込み
from libs import log

# 何回呼ばれたかカウントしたい
maincount = 0
resetcount = 0
hintcount = 0
detailcount = 0
rankingcount = 0
nomalcount = 0
errorcount = 0
notpokecount = 0

@respond_to(r'.+')
def mention_func(message):
	global maincount
	global resetcount
	global hintcount
	global detailcount
	global rankingcount
	global nomalcount
	global errorcount
	global notpokecount
	maincount = maincount +1
	req=message.body['text']
	log.logger.info("["+str(maincount)+"] ：総実行回数【"+str(req)+"】：受け取ったメッセージ")
	if req == "リセット" or req == "reset":
		resetcount = resetcount +1
		my_functions.reset()
		message.send("リセットしました")
	elif req == "log" or req == "ログ" or req == "記録" :
		message.send("["+str(maincount)+"] ：総実行回数")
		message.send("["+str(resetcount)+"] ：総リセット回数")
		message.send("["+str(hintcount)+"] ：総ヒント回数")
		message.send("["+str(detailcount)+"] ：総詳細表示回数")
		message.send("["+str(rankingcount)+"] ：総ランキング表示回数")
		message.send("["+str(notpokecount)+"] ：総ポケモンじゃなくね？回数")
		message.send("["+str(nomalcount)+"] ：総しりとり成立回数")
		message.send("["+str(errorcount)+"] ：総しりとり不成立回数")
	elif req == "ランキング" or req == "ranking" :
		rankingcount = rankingcount +1
		message.send(my_functions.remarkRanking())
	elif req[:4] == "ヒント｜" or req[:4] == "ヒント|"  or req[:4] == "hint":
		hintcount = hintcount +1
		log.logger.info("["+str(hintcount)+"] ：ヒント回数")
		hint = my_functions.hint(req[4:5])
		message.send(str(hint))
	elif req[:3] == "詳細｜" or req[:3] == "詳細|" :
		detailcount = detailcount +1
		log.logger.info("["+str(detailcount)+"] ：詳細表示回数")
		if my_functions.checkExistenceAllPoke(req[3:len(req)]) :
			message.send(my_functions.getpokedetail(req[3:len(req)]))
		else:
			message.send("よくわかりませんでした"+req[3:len(req)])
	else:
		if my_functions.checkExistencePoke(req) :
			my_functions.memoryRemark(req)
			IsShiritoriOK = True
			# すでに言ったことがあるかどうか
			if my_functions.checkExistencereq(req) :
				IsShiritoriOK = False
				message.send(my_functions.countreqstock(req))
			# しりとりになってるかどうか
			if not my_functions.checkTruelastword(req) :
				IsShiritoriOK = False
				message.send(my_functions.forgivelastword(req))
			if IsShiritoriOK :
				nomalcount = nomalcount +1
				log.logger.info("["+str(nomalcount)+"] ：しりとり成立回数")
			else :
				errorcount = errorcount +1
				log.logger.info("["+str(errorcount)+"] ：しりとり不成立回数")
			my_functions.reqstockappend(req)
			ret = my_functions.shiritori(req)
			log.logger.info("【"+str(ret)+"】：返答")
		else :
			notpokecount = notpokecount +1
			ret = "ポケモンじゃなくね？"
			log.logger.info("["+str(notpokecount)+"] ：ポケモンじゃなくね？回数")
		message.send(ret)
```

```my_functions.py
# -*- coding: utf-8 -*-
import json
import random
import collections


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
```

```log.py
import logging
logger = logging.getLogger(__name__)
_detail_formatting = '[%(asctime)s] %(module)s.%(funcName)s %(levelname)s -> %(message)s'

logging.basicConfig(
    level=logging.DEBUG,
    format=_detail_formatting, # 出力のformatも変えられる
    filename="./pokeshiri.log", # logファイルのありか
)

```
## ログ出力で参考にしたもの
[Pythonでお手軽にかっこよくlogging](https://qiita.com/koshian2/items/e45d05405faebf770c22)

# あとがき
python知識ゼロからポケモンの名前でしりとりするslackbotを作ったノウハウのすべてでした
pythonは本当に学習コストが少ないと思いました
JSONの読み込みとかリストの並び替えとか辞書の扱い方とかググればすぐにサンプルコードがでてきます。
またググればでてくるポケモンのデータってJSONのすごさにちょっと感動
JSON作者様にこのうえない謝辞をおくります。

以上
ありがとうございました。

よかったら「いいね」してください。
