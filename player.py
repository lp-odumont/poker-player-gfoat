
class Player:
    VERSION = "Greatest Folder of all times v0.0.4"

    def betRequest(self, game_state):
        own_card = game_state['players'][game_state['in_action']]["hole_cards"]
        community_cards = game_state['community_cards']
        if self.is_garbage(own_card + community_cards):
            return 0
        if self.is_three(own_card + community_cards):
            return game_state['current_buy_in']*8 - game_state['players'][game_state['in_action']] ['bet']
        if self.is_pair(own_card):
            return game_state['current_buy_in']*4 - game_state['players'][game_state['in_action']] ['bet']

        for x in own_card:
            if x['rank'] in ['K','A']:
                return game_state['current_buy_in']*2 - game_state['players'][game_state['in_action']] ['bet']
            
        return game_state['current_buy_in'] - game_state['players'][game_state['in_action']] ['bet']

    def showdown(self, game_state):
        pass

    def is_garbage(self, hand):
        return False

    def is_pair(self, hand):
        ranks = [card['rank'] for card in hand]
        return any(ranks.count(r) >= 2 for r in ranks)

    def is_three(self, hand):
        ranks = [card['rank'] for card in hand]
        return any(ranks.count(r) >= 3 for r in ranks)

    def is_four(self, hand):
        ranks = [card['rank'] for card in hand]
        return any(ranks.count(r) >= 4 for r in ranks)

    def is_two_pairs(self, hand):
        ranks = [card['rank'] for card in hand]
        counts = set(ranks.count(r) for r in ranks)
        return len([c for c in counts if c >= 2]) >= 2
        