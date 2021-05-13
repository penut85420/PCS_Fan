import os
import time
import random
import threading
from tracking.riots import get_pros_match
from tracking.utils import load, short_team_fn
from twitchio.ext import commands
from twitchio.ext.commands.errors import CommandNotFound

class PCS_Fan(commands.Bot):
    def __init__(self):
        super().__init__(
            irc_token=os.getenv('TMI_TOKEN'),
            client_id=os.getenv('CLIENT_ID'),
            nick='PCS_Fan',
            prefix='!',
            initial_channels=['PCS_Fan', 'penut85420']
        )
        self.reset_poll()
        self.poll_name = ''
        self.match_enable = True

    def reset_poll(self):
        self.poll = {
            'all': {'users': set(), 'num': 0},
            'yes': {'users': set(), 'num': 0},
            'no': {'users': set(), 'num': 0},
        }

    def chk_poll(self, msg):
        if '+1' in msg:
            return 1
        if '0' in msg:
            return -1
        if '-1' in msg:
            return -1
        return 0

    async def event_ready(self):
        print(f'Ready | {self.nick}')
        return await super().event_ready()

    async def event_message(self, msg):
        name = msg.author.name
        print(f'{name}: {msg.content}')

        chk_poll_result = self.chk_poll(msg.content)

        if name not in self.poll['all']['users'] and chk_poll_result:
            self.poll['all']['num'] += 1
            self.poll['all']['users'].add(name)
            if chk_poll_result > 0:
                self.poll['yes']['num'] += 1
                self.poll['yes']['users'].add(name)
            elif chk_poll_result < 0:
                self.poll['no']['num'] += 1
                self.poll['no']['users'].add(name)

        if self.is_psg(msg.content):
            await msg.channel.send(f'@{msg.author.name} 右下角有寫選手名單喔 SeemsGood')
        elif msg.author.name != self.nick.lower() and self.is_hello(msg.content):
            emotes = ['BloodTrail', 'SeemsGood', 'VoHiYo', 'HeyGuys']
            await msg.channel.send(f'@{msg.author.name} 安安 {random.choice(emotes)}')

        if msg.content.startswith('！'):
            msg.content = msg.content.replace('！', '!')

        await self.handle_commands(msg)

    def is_psg(self, msg):
        sents = [
            '這場誰是PSG的啊',
            '這場有誰',
            '哪邊是PSG的'
        ]

        return self.sent_include(sents, msg)

    def is_hello(self, msg):
        sents = ['安安']

        return self.sent_include(sents, msg)

    def sent_include(self, sents, msg):
        msg = msg.lower()
        for sent in sents:
            if sent.lower() in msg:
                return True
        return False

    async def event_command_error(self, _, error):
        if isinstance(error, CommandNotFound):
            pass
        else:
            print(f'[Error] {str(error)}')

    def wrap_bot(self, sent, emote='MrDestructoid'):
        return f'{emote} {sent} {emote}'

    @commands.command(name='match')
    async def cmd_match(self, ctx):
        if not self.match_enable:
            return

        self.match_enable = False

        def tmp_disable():
            time.sleep(10)
            self.match_enable = True

        t_disable = threading.Thread(target=tmp_disable)
        t_disable.start()

        _, *name = ctx.message.content.split(' ')

        server = 'euw1'
        org_name = ' '.join(name)

        if name[0].startswith('-'):
            server = name[0][1:]
            org_name = ' '.join(name[1:])

        name = org_name.lower()

        print(server, name, org_name)

        if name.strip() == '':
            await ctx.send(self.wrap_bot('請輸入 !match [選手名稱]'))
            return

        if len(name) > 17:
            await ctx.send(
                self.wrap_bot(f'@{ctx.author.name} 你有想過機器人的感受嗎')
            )
            return

        status, name, code, team_side = get_pros_match(name, server)

        if not status:
            if code == 1:
                await ctx.send(self.wrap_bot(f'找不到 {org_name} 這個選手'))
            elif code == 2:
                await ctx.send(
                    self.wrap_bot(f'目前沒有 {name} 的積分對戰可以觀戰')
                )
        else:
            _join = lambda x: ' & '.join(x)
            blue = _join(team_side[100]) if team_side[100] else ''
            red = _join(team_side[200]) if team_side[200] else ''

            if blue and red:
                blue = f'[藍] {blue}'
                red = f'[紅] {red}'

            show_info = f'{blue} {red}'.strip()
            await ctx.send(
                self.wrap_bot(f'目前 {name} 的對戰資訊如下：{show_info}')
            )

    @commands.command(name='like')
    async def cmd_like(self, ctx):
        _, *name = ctx.message.content.split(' ')
        name = ' '.join(name)
        if len(name) > 20:
            await ctx.send(
                self.wrap_bot(f'@{ctx.author.name} 7414 啦')
            )
            return
        self.reset_poll()
        self.poll_name = name
        await ctx.send(self.wrap_bot(f'超喜歡 {name} 的 +1'))

    @commands.command(name='poll')
    async def cmd_poll(self, ctx):
        print(self.poll)
        if self.poll['yes']['num'] > self.poll['no']['num']:
            n, t = self.poll['yes']['num'], self.poll['all']['num']
            user = random.choice(list(self.poll['yes']['users']))
            msg = (
                f'大家都喜歡 {self.poll_name} ({n/t*100:.2f}%) BloodTrail '
                f'其中 @{user} 是 {self.poll_name} 的頭號粉絲 BloodTrail'
            )
        else:
            n, t = self.poll['no']['num'], self.poll['all']['num']
            user = random.choice(list(self.poll['no']['users']))
            msg = (
                f'大家都不喜歡 {self.poll_name} ({n/t*100:.2f}%) BibleThump '
                f'其中 @{user} 是 {self.poll_name} 的頭號黑粉 BibleThump'
            )
        await ctx.send(msg)

if __name__ == '__main__':
    PCS_Fan().run()
