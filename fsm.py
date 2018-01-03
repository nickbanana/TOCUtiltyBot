from transitions.extensions import GraphMachine 
import random

class TocMachine(GraphMachine):
    
    def __init__(self, **machine_configs):
        self.start = 0
        self.end = 100
        self.target = 0
        self.guess = -1
        self.Got = False
        self.object = ''
        self.url_prefix = "http://ecshweb.pchome.com.tw/search/v3.3/?q="
        self.machine = GraphMachine(
            model=self,
            **machine_configs
        )

    def GoingToBuyQuery(self, update):
        text = update.message.text
        return text == '購物查詢'
    def InputBuyObj(self, update):
        self.object = update.message.text
        return len(self.object) != 0

    def on_enter_BuyResult(self, update):
        update.message.reply_text(self.url_prefix + self.object)
        self.go_back(update)
    def on_exit_BuyResult(self, update):
        update.message.reply_text('現在回到關鍵字輸入，輸入 結束 回到主目錄')

    def GoingToWeatherForecast(self, update):
        text = update.message.text
        return text == '天氣查詢'

    def GoingToTinyCodeGame(self, update):
        text = update.message.text
        return text == '終極密碼遊戲'

    def GoingToGameSetting(self, update):
        text = update.message.text
        return text == '遊戲設定'
    def VerifyStartSet(self, update):
        self.start = int(update.message.text)
        return self.start > -1
    def on_enter_EndSet(self, update):
        update.message.reply_text("輸入終止數字 最大 1000")
    def VerifyEndSet(self, update):
        self.end = int(update.message.text)
        return self.end < 1001
    def GotCha(self, update):
        return self.Got
    def BackToQuery(self, update):
        return True
    def on_enter_BuyQuery(self, update):
        update.message.reply_text("這是購物查詢 請輸入想查詢的物品 輸入 結束 回到主目錄")

    def on_exit_BuyQuery(self, update):
        print('Leaving buyq')

    def on_enter_TinyCodeGame(self, update):
        update.message.reply_text("這是終極密碼小遊戲")
        update.message.reply_text("輸入 遊戲設定 調整範圍")
        update.message.reply_text("輸入 開始遊戲 進入遊戲")
        update.message.reply_text("目前範圍 %s 到 %s", self.start, self.end)
    
    def on_enter_StartSet(self, update):
        update.message.reply_text("這裡會設定數字範圍")
        update.message.reply_text("輸入起始數字 最小 0")
    def StartTheGame(self, update):
        text = update.message.text
        self.TargetNumberGenerate()
        return text == '開始遊戲'

    def on_enter_StartGame(self, update):
        update.message.reply_text("想猜哪個數字")

    def Large(self, update):
        self.guess = int(update.message.text)
        return self.guess > self.target and self.guess < self.end
    def Small(self, update):
        self.guess = int(update.message.text)
        return self.guess < self.target and self.guess > self.start
    def Bang(self, update):
        self.guess = int(update.message.text)
        return self.guess == self.target
    def on_enter_LargerThanTarget(self, update):
        update.message.reply_text("比目標還大")
        self.end = self.guess
        self.go_back(update)
    def on_enter_SmallerThanTarget(self, update):
        update.message.reply_text("比目標還小")
        self.start = self.guess
        self.go_back(update)
    def on_enter_EqualToTarget(self, update):
        update.message.reply_text("中獎")
        update.message.reply_text("結束遊戲")
        self.Got = True
        self.go_back(update)
    def on_enter_user(self, update):
        update.message.reply_text('這是迷你的功能型機器人')
        update.message.reply_text('輸入 天氣查詢 進入 天氣查詢系統')
        update.message.reply_text('輸入 購物查詢 進入 商品查詢系統')
        update.message.reply_text('輸入 終極密碼遊戲 進入 小遊戲')



    
    def ReturnToMenu(self, update):
        text = update.message.text
        return text == '結束'
    

    def on_exit_TinyCodeGame(self, update):
        print('Leaving tinycode')

    def on_enter_WeatherForecast(self, update):
        update.message.reply_text("這是天氣查詢")
        update.message.reply_text("輸入 結束 回到主目錄")

    def on_exit_WeatherForecast(self, update):
        print('leave WF')
    
    def TargetNumberGenerate(self):
        random.seed()
        self.target = random.randint(self.start, self.end-1)

