
class Player:
    VERSION = "Greatest Folder of all times v0.0.2"

    def betRequest(self, game_state):
        own_card = game_state['players'][game_state['in_action']]["hole_cards"]
        for x in own_card:
            if x['rank'] in ['K','A']:
                game_state['current_buy_in']*2 - game_state['players'][game_state['in_action']] ['bet']
            
        return game_state['current_buy_in'] - game_state['players'][game_state['in_action']] ['bet']

    def showdown(self, game_state):
        pass

