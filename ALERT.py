import requests
import json
import telegram

url = "http://136.243.82.203:8888/v1/chain/get_table_rows"

my_token = ''


def send(msg, chat_id, token):
    bot = telegram.Bot(token=token)
    bot.sendMessage(chat_id=chat_id, text=msg, parse_mode= 'Markdown')


def get_data():

    url = "https://eos.eoscafeblock.com/v1/chain/get_table_rows"

    payload = "{\"code\":\"dcdpcontract\",\
    \"table\":\"tables\",\
    \"scope\":\"dcdpcontract\",\
    \"json\":\"true\",\
    \"limit\":\"1000\", \
    \"lower_bound\":\"""\",}"
    headers = {
     'accept': "application/json",
     'content-type': "application/json"
      }

    response = requests.request("POST", url, data=payload, headers=headers)

    return response


first_list = []
second_list = []


def processing(list1, list2):

    rows = json.loads(get_data().text)['rows']

    if len(rows) != 0:
        players = rows[0]['players']

        list2 = []
    
        for i in range(len(players)):
            list2.append(players[i]['name'])

        if list1 != list2:

            small_blind = rows[0]['small_blind'].rstrip('0 EOS').rstrip('.') if '.' in rows[0]['small_blind'] else rows[0]['small_blind']
            big_blind = str((float(small_blind) * 2))
            buy_in = players[i]['stack'].rstrip('0 EOS').rstrip('.') if '.' in players[i]['stack'] else players[i]['stack']
        
            newlist = list(set(list2).difference(set(list1)))
            list1 = []
            list1 = list2.copy() 
        
            if len(newlist) > 0:
                list_for_message = ""
                for i in range(len(list1)):
                    if list1[i] != "":
                        list_for_message += list1[i] + ", "
                list_for_message = list_for_message.rstrip(", ")

                for i in range(len(newlist)):
                    if newlist[i] != "":
                        message = "*" + str(newlist[i]) + "*" + " в игре!" + "\n\n*Бай-ин:* " + buy_in + " EOS" + "\n*Блайнды:* "  + small_blind + " / " + big_blind + " EOS" + "\n*Игроки:* " + list_for_message + "\n*Осталось мест:* " + str(6 - rows[0]['players_count'])
                        send(message, "@pokerchained_alert", my_token)

    else: list1 = []

    return list1


while True:
    first_list = processing(first_list, second_list)

