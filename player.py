
class Player:
    VERSION = "Greatest Folder of all times v0.0.6"

    def betRequest(self, game_state):
        own_card = game_state['players'][game_state['in_action']]["hole_cards"]
        community_cards = game_state['community_cards']
        the_bet_factor=self.compute_bet(own_card,community_cards)
        return (game_state['current_buy_in'] - game_state['players'][game_state['in_action']] ['bet'])*the_bet_factor

      

    def showdown(self, game_state):
        pass

    def strength(self, hand):
        if self.is_four(hand):
            return 5
        if self.is_three(hand):
            return 4
        if self.is_two_pairs(hand):
            return 3
        if  self.is_pair(hand):
            return 2
        if self.has_kings_aces(hand):
            return 1
        return 0
    
    def compute_bet(self,own_hand,community_hand):
        rel_strength = self.strength(own_hand+community_hand) - self.strength(community_hand)
        if(rel_strength == 0):
            return 0
        return 2**rel_strength
        


    def is_garbage(self, own_hand, community_hand):
        return len(community_hand) > 0

    def has_kings_aces(self,hand):
        return any([card['rank'] for card in hand if card['rank'] in ['K','A']])

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
        unique_ranks = set(ranks)
        counts = [ranks.count(r) for r in unique_ranks]
        return len([c for c in counts if c >= 2]) >= 2
        