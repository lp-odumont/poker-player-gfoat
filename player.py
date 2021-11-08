def is_double(own_cards):
    return  own_cards[0]['rank'] == own_cards[1]['rank']

def has_tripple(own_cards,community_cards):
    if not is_double(own_cards):
        return False
    
    for x in community_cards:
        if x['rank'] == own_cards[0]['rank']:
            return True
    return False

class Player:
    VERSION = "Greatest Folder of all times v0.0.4"

    def betRequest(self, game_state):
        own_card = game_state['players'][game_state['in_action']]["hole_cards"]
        community_cards = game_state['community_cards']
        if has_tripple(own_card, community_cards):
            return game_state['current_buy_in']*8 - game_state['players'][game_state['in_action']] ['bet']
        if is_double(own_card):
            return game_state['current_buy_in']*4 - game_state['players'][game_state['in_action']] ['bet']

        for x in own_card:
            if x['rank'] in ['K','A']:
                game_state['current_buy_in']*2 - game_state['players'][game_state['in_action']] ['bet']
            
        return game_state['current_buy_in'] - game_state['players'][game_state['in_action']] ['bet']

    def showdown(self, game_state):
        pass

