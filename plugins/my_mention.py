# -*- coding: utf-8 -*-
from slackbot.bot import respond_to     # @botname: で反応するデコーダ
from slackbot.bot import listen_to      # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ
from libs import my_functions           # 自作関数の読み込み
from libs import log


# 何回呼ばれたかカウントしたい
class Counter:

    def __init__(self, name=None):
        self.name = name
        self.count = 0

    def up(self, addition=''):
        self.count += 1
        log.logger.info("[" + str(self.count) + "] ：" + self.name + addition)


class count:
    main    = Counter("総実行回数")
    reset   = Counter("総リセット回数")
    hint    = Counter("総ヒント回数")
    detail  = Counter("総詳細表示回数")
    ranking = Counter("総ランキング表示回数")
    notpoke = Counter("総ポケモンじゃなくね？回数")
    normal  = Counter("総しりとり成立回数")
    error   = Counter("総しりとり不成立回数")


def reset(message):
    count.reset.up()
    my_functions.reset()
    message.send("リセットしました")


def statistics(message):
    for counter in (count.main, count.reset, count.hint, count.detail,
                    count.ranking, count.notpoke, count.normal, count.error):
        message.send("[" + str(counter.count) + "] ：" + counter.name)


def ranking(message):
    count.ranking.up()
    message.send(my_functions.remarkRanking())


def hint(name, message):
    count.hint.up()
    hint = my_functions.hint(name[:1])
    message.send(str(hint))


def detail(name, message):
    count.detail.up()
    if my_functions.checkExistenceAllPoke(name):
        message.send(my_functions.getpokedetail(name))
    else:
        message.send("よくわかりませんでした" + name)


def shiritori(name, message):
    if my_functions.checkExistencePoke(name):
        my_functions.memoryRemark(name)
        IsShiritoriOK = True
        # すでに言ったことがあるかどうか
        if my_functions.checkExistencereq(name):
            IsShiritoriOK = False
            message.send(my_functions.countreqstock(name))
        # しりとりになってるかどうか
        if not my_functions.checkTruelastword(name):
            IsShiritoriOK = False
            message.send(my_functions.forgivelastword(name))
        if IsShiritoriOK:
            count.normal.up()
        else:
            count.error.up()
        my_functions.reqstockappend(name)
        ret = my_functions.shiritori(name)
        log.logger.info("【" + str(ret) + "】：返答")
    else:
        ret = "ポケモンじゃなくね？"
        count.notpoke.up()
    message.send(ret)


match_functions = {
    ('リセット', 'reset'): reset,
    ("log", "ログ", "記録"): statistics,
    ("ランキング", "ranking"): ranking,
}

starts_functions = {
    ("ヒント｜", "ヒント|", "hint"): hint,
    ("詳細｜", "詳細|"): detail,
}


@respond_to(r'.+')
def mention_func(message):
    req = message.body['text']
    count.main.up("【" + req + "】：受け取ったメッセージ")
    for commands, function in match_functions.items():
        if req in commands:
            function(message)
            return
    for commands, function in starts_functions.items():
        for command in commands:
            if req.startswith(command):
                function(req[len(command):], message)
                return
    shiritori(req, message)

@listen_to("")
def listen_func(message):
	pass
