from transitions.extensions import GraphMachine 
import random

class TocMachine(GraphMachine):
    
    def __init__(self, **machine_configs):
        self.start = 0
        self.end = 100
        self.target = 0
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

    def on_enter_BuyQuery(self, update):
        update.message.reply_text("這是購物查詢 請輸入想查詢的物品 輸入 結束 回到主目錄")

    def on_exit_BuyQuery(self, update):
        print('Leaving buyq')

    def on_enter_TinyCodeGame(self, update):
        update.message.reply_text("這是終極密碼小遊戲")

    def on_enter_SettingGame(self, update):
        update.message.reply_text("這裡會設定數字範圍")
    
    def on_enter_StartSet(self, update):
        update.message.reply_text("輸入起始數字")
    




    def TinyCodeGameStartSet(self, update):
        self.start = int(update.message.text)
    
    def TinyCodeGameEndSet(self, update):
        self.end = int(update.message.text)


    
    def ReturnToMenu(self, update):
        text = update.message.text
        return text == '結束'
    

    def on_exit_TinyCodeGame(self, update):
        print('Leaving tinycode')

    def on_enter_WeatherForecast(self, update):
        update.message.reply_text("這是天氣查詢")
        self.go_back(update)

    def on_exit_WeatherForecast(self, update):
        print('leave WF')
    
    def TargetNumberGenerate(self):
        random.seed()
        self.target = random.randint(self.start, self.end)

