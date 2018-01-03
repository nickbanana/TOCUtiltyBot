import sys
from io import BytesIO

import telegram
import requests
from telegram.ext import Updater, CommandHandler
from flask import Flask, request, send_file

from fsm import TocMachine


API_TOKEN = '494050999:AAG2K3npCF38DKLrnEcColHpf8wdskrzRR8'
CWB_TOKEN = 'CWB-3EA4047F-0B3D-4EC3-81BE-FEA95F398D0D'
CWB_URL = 'http://opendata.cwb.gov.tw/opendataapi?dataid=F-C0032-001&authorizationkey=CWB-3EA4047F-0B3D-4EC3-81BE-FEA95F398D0D'

HookURL = 'https://api.telegram.org/bot'+ API_TOKEN + '/setWebhook?url='+ sys.argv[1] +'/webhooks/telegram_vnko2phmnkasjdfkpoh23kojsoagk1243y9'





app = Flask(__name__)
bot = telegram.Bot(token=API_TOKEN)

machine = TocMachine(
    states=[
        'user',
        'BuyQuery',
        'BuyResult',
        'TinyCodeGame',
        'StartSet',
        'EndSet',
        'StartGame',
        'LargerThanTarget',
        'SmallerThanTarget',
        'EqualToTarget',
        'WeatherForecast'
    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'BuyQuery',
            'conditions': 'GoingToBuyQuery'
        },
        {
            'trigger': 'advance',
            'source': 'BuyQuery',
            'dest': 'BuyResult',
            'conditions': 'InputBuyObj'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'TinyCodeGame',
            'conditions': 'GoingToTinyCodeGame'
        },
        {
            'trigger': 'advance',
            'source': 'TinyCodeGame',
            'dest': 'StartSet',
            'conditions': 'GoingToGameSetting'
        },
        {
            'trigger': 'advance',
            'source': 'StartSet',
            'dest': 'EndSet',
            'conditions': 'VerifyStartSet'
        },
        {
            'trigger': 'advance',
            'source': 'EndSet',
            'dest': 'StartGame',
            'conditions': 'VerifyEndSet'
        },
        {
            'trigger': 'advance',
            'source': 'TinyCodeGame',
            'dest': 'StartGame',
            'conditions': 'StartTheGame'
        },
        {
            'trigger': 'advance',
            'source': 'StartGame',
            'dest': 'LargerThanTarget',
            'conditions': 'Large'
        },
        {
            'trigger': 'advance',
            'source': 'StartGame',
            'dest': 'SmallerThanTarget',
            'conditions': 'Small'
        },
        {
            'trigger': 'advance',
            'source': 'StartGame',
            'dest': 'EqualToTarget',
            'conditions': 'Bang'
        },
        {
            'trigger': 'go_back',
            'source': 'StartGame',
            'dest': 'TinyCodeGame',
            'conditions': 'Gotcha'
        },






        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'WeatherForecast',
            'conditions': 'GoingToWeatherForecast'
        },
        {
            'trigger': 'go_back',
            'source' : 'TinyCodeGame',
            'dest': 'user',
            'conditions': 'ReturnToMenu'

        },
        {
            'trigger': 'go_back',
            'source' : 'BuyQuery',
            'dest': 'user',
            'conditions': 'ReturnToMenu'

        },
        {
            'trigger': 'go_back',
            'source' : 'BuyResult',
            'dest': 'BuyQuery'
        },

        {
            'trigger': 'go_back',
            'source' : [
                'LargerThanTarget',
                'SmallerThanTarget',
                'EqualToTarget',
            ],
            'dest': 'StartGame'
        }





    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True,
)
def setHook():
    r = requests.post(HookURL)
    print(r.text)

@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    byte_io = BytesIO()
    machine.graph.draw(byte_io, prog='dot', format='png')
    byte_io.seek(0)
    return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')

@app.route('/webhooks/telegram_vnko2phmnkasjdfkpoh23kojsoagk1243y9', methods=['POST'])
def webhook_handler():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    #text = update.message.text
    #update.message.reply_text(text)
    machine.advance(update)
    return 'ok'



if __name__ == "__main__":
    setHook()
    app.run(host='127.0.0.1', port=8443)
