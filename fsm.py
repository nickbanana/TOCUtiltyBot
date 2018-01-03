from transitions.extensions import GraphMachine as Machine

class TocMachine(Machine):
    def __init__(self, **machine_configs):
        self.machine = Machine(
            model = self,
            **machine_configs
        )

    def GoingToBuyQuery(self, update):
        text = update.message.text
        return text == '購物查詢'

    def GoingToWeatherForecast(self, update):
        text = update.message.text
        return text == '天氣查詢'

    def GoingToTinyCodeGame(self, update):
        text = update.message.text
        return text == '終極密碼遊戲'

    def on_enter_BuyQuery(self, update):
        update.message.reply_text("這是購物查詢")
        self.go_back(update)

    def on_exit_BuyQuery(self, update):
        print('Leaving buyq')

    def on_enter_TinyCodeGame(self, update):
        update.message.reply_text("這是終極密碼小遊戲")
        self.go_back(update)

    def on_exit_TinyCodeGame(self, update):
        print('Leaving tinycode')
    
    def on_enter_WeatherForecast(self, update):
        update.message.reply_text("這是天氣查詢")
        self.go_back(update)

    def on_exit_WeatherForecast(self, update):
        print('leave WF')