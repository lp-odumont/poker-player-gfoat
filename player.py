
class Player:
    VERSION = "Greatest Folder of all times v0.0.7"

    def betRequest(self, game_state):
        own_card = game_state['players'][game_state['in_action']]["hole_cards"]
        community_cards = game_state['community_cards']
        the_bet_factor=self.compute_bet(own_card,community_cards)
        return (game_state['current_buy_in'] - game_state['players'][game_state['in_action']] ['bet'])*the_bet_factor

      

    def showdown(self, game_state):
        pass

    def strength(self, hand):
        if self.is_four(hand):
            return 64
        if self.is_full_house(hand):
            return 32
        if self.is_straight(hand):
            return 16
        if self.is_three(hand):
            return 8
        if self.is_two_pairs(hand):
            return 3
        if  self.is_pair(hand):
            return 2
        if self.has_kings_aces(hand):
            return 1
        return 0
    
    def compute_bet(self,own_hand,community_hand):
        rel_strength = self.strength(own_hand+community_hand) - self.strength(community_hand)

        if(rel_strength < len(community_hand)):
            return 0
        
                
        return rel_strength-len(community_hand)
        


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

    def is_full_house(self, hand):
        return self.is_two_pairs(hand) and self.is_three(hand)

    def is_straight(self, hand):
        rank_array = [str(i) for i in range(2, 11)] + ['J', 'Q', 'K', 'A']
        ranks = sorted([card['rank'] for card in hand])
        run = 0;
        for i in range(1, len(ranks)):
            if rank_array.index(ranks[i]) - rank_array.index(ranks[i-1]) == 1:
                run += 1
                if run >= 4:
                    return True
            else:
                run = 0
        return False

    def is_flush(self, hand):
        suits = [card['suit'] for card in hand]
        counts = [suits.count(s) for s in set(suits)]
        return any(c >= 5 for c in counts)
        
        