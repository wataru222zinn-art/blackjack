from random import shuffle

SURFACES = list('🂡🂢🂣🂤🂥🂦🂧🂨🂩🂪🂫🂭🂮' + '🂱🂲🂳🂴🂵🂶🂷🂸🂹🂺🂻🂽🂾' +
                '🃁🃂🃃🃄🃅🃆🃇🃈🃉🃊🃋🃍🃎' + '🃑🃒🃓🃔🃕🃖🃗🃘🃙🃚🃛🃝🃞')
BACK = '🂠'

COLORS = ['MidnightBlue','Crimson','Crimson','MidnightBlue','PaleGoldenRod']
FORMATS = '<span style="font-size: 96px; color: {color};">{surface}</span>'
SUITS = list('SHDC')
SEPARATOR = ' '

def back_cards(separator=SEPARATOR):
    backs = [FORMATS.format(color=COLORS[4],surface=BACK)] * 2
    return SEPARATOR.join(backs)

class Card:
    def __init__(self,num):
        self.num = num  #0~51
        pip = num % 13 #0~12
        suit = int(num/13) #0~3

        self.text = f'{SUITS[suit]}{pip+1}'
        self.unicode = SURFACES[num]
        self.html = FORMATS.format(color=COLORS[suit],surface=SURFACES[num])

        if pip == 0: #A
            self.point = 11
        elif pip >= 9:
            self.point = 10
        else:
            self.point = pip + 1
    
    def __str__(self):
        return self.text
    
    def get_unicode(self):
        return self.unicode
    
    def get_html(self):
        return self.html
    
class Deck:
    def __init__(self):
        self.cards = [Card(i) for i in range(52)]
        shuffle(self.cards)
    
    def __str__(self):
        return str([card.num for card in self.cards])
    
    def draw(self):
        return self.cards.pop(0)

class Player:
    def __init__(self,deck):
        self.deck = deck
        self.score = 0
        self.hand = []
        self.draw();self.draw()
    
    def __str__(self):
        return f'{str([str(c) for c in self.hand])} => {self.score}'
    
    def draw(self):
      self.hand.append(self.deck.draw())
      points = [card.point for card in self.hand]

    # A を 11 として数えた状態で合計
      total = sum(points)

    # A を 11 → 1 に変換する処理（複数枚対応）
      while total > 21 and 11 in points:
        pos = points.index(11)
        points[pos] = 1
        self.hand[pos].point = 1
        total = sum(points)

    # 21 を超えたらバスト
      if total > 21:
        total = None

      self.score = total


    def auto_draw(self,thresh=16):
        while self.score is not None and self.score <= thresh:
            self.draw()
    
    def show_unicode(self,separator=SEPARATOR):
        return separator.join([c.get_unicode() for c in self.hand])
    
    def show_html(self,separator=SEPARATOR):
        return separator.join([c.get_html() for c in self.hand])
    
    def showdown(self,other):
        if other.score is None:
            message = '勝ち'
        elif self.score > other.score:
            message = '勝ち'
        elif self.score < other.score:
            message = '負け'
        else:
            message = '引き分け'
        return message

if __name__ == '__main__':
    deck = Deck()
    player = Player(deck)
    print(player)
    print(player.show_unicode())
    print(player.show_html())

    while True:
        c = input('D=引く,s=勝負> ').lower()

        if c == 'd':
            player.draw()
            print(player)
            if player.score is None:
                break

        else:
            break
    
    dealer = Player(deck)

    if player.score is None:
        print('どぼん')
    else:
        dealer.auto_draw()
        print(dealer)
        print(player.showdown(dealer))            
