def is_double(own_cards):
    return  own_cards[0]['rank'] == own_cards[1]['rank']

class Player:
    VERSION = "Greatest Folder of all times v0.0.3"

    def betRequest(self, game_state):
        own_card = game_state['players'][game_state['in_action']]["hole_cards"]
        if is_double(own_card):
            return game_state['current_buy_in']*4 - game_state['players'][game_state['in_action']] ['bet']

        for x in own_card:
            if x['rank'] in ['K','A']:
                game_state['current_buy_in']*2 - game_state['players'][game_state['in_action']] ['bet']
            
        return game_state['current_buy_in'] - game_state['players'][game_state['in_action']] ['bet']

    def showdown(self, game_state):
        pass

