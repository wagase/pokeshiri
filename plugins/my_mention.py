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

@listen_to("")
def listen_func(message):
	pass
