"""Test module for player module."""

import sys
import os
import unittest

sys.path.append(os.path.dirname(__file__))
from player import Player

class PlayerTest(unittest.TestCase):
    """Tests for the player class."""

    def setUp(self):
        """Common setup for all tests."""
        self.player = Player()
        # Example game_state from http://leanpoker.org/player-api
        self.game_state_with_community_cards = {
            "tournament_id":"550d1d68cd7bd10003000003",     # Id of the current tournament
            "game_id":"550da1cb2d909006e90004b1",           # Id of the current sit'n'go game. You can use this to link a
                                                            # sequence of game states together for logging purposes, or to
                                                            # make sure that the same strategy is played for an entire game
            "round":0,                                      # Index of the current round within a sit'n'go
            "bet_index":0,                                  # Index of the betting opportunity within a round
            "small_blind": 10,                              # The small blind in the current round. The big blind is twice the
                                                            #     small blind
            "current_buy_in": 320,                          # The amount of the largest current bet from any one player
            "pot": 400,                                     # The size of the pot (sum of the player bets)
            "minimum_raise": 240,                           # Minimum raise amount. To raise you have to return at least:
                                                            #     current_buy_in - players[in_action][bet] + minimum_raise
            "dealer": 1,                                    # The index of the player on the dealer button in this round
                                                            #     The first player is (dealer+1)%(players.length)
            "orbits": 7,                                    # Number of orbits completed. (The number of times the dealer
                                                            #     button returned to the same player.)
            "in_action": 1,                                 # The index of your player, in the players array
            "players": [                                    # An array of the players. The order stays the same during the
                {                                           #     entire tournament
                    "id": 0,                                # Id of the player (same as the index)
                    "name": "Albert",                       # Name specified in the tournament config
                    "status": "active",                     # Status of the player:
                                                            #   - active: the player can make bets, and win the current pot
                                                            #   - folded: the player folded, and gave up interest in
                                                            #       the current pot. They can return in the next round.
                                                            #   - out: the player lost all chips, and is out of this sit'n'go
                    "version": "Default random player",     # Version identifier returned by the player
                    "stack": 1010,                          # Amount of chips still available for the player. (Not including
                                                            #     the chips the player bet in this round.)
                    "bet": 320                              # The amount of chips the player put into the pot
                },
                {
                    "id": 1,                                # Your own player looks similar, with one extension.
                    "name": "Bob",
                    "status": "active",
                    "version": "Default random player",
                    "stack": 1590,
                    "bet": 80,
                    "hole_cards": [                         # The cards of the player. This is only visible for your own player
                                                            #     except after showdown, when cards revealed are also included.
                        {
                            "rank": "K",                    # Rank of the card. Possible values are numbers 2-10 and J,Q,K,A
                            "suit": "hearts"                # Suit of the card. Possible values are: clubs,spades,hearts,diamonds
                        },
                        {
                            "rank": "K",
                            "suit": "spades"
                        }
                    ]
                },
                {
                    "id": 2,
                    "name": "Chuck",
                    "status": "out",
                    "version": "Default random player",
                    "stack": 0,
                    "bet": 0
                }
            ],
            "community_cards": [                            # Finally the array of community cards.
                {
                    "rank": "4",
                    "suit": "spades"
                },
                {
                    "rank": "A",
                    "suit": "hearts"
                },
                {
                    "rank": "K",
                    "suit": "clubs"
                }
            ]
        }
        self.game_state_without_community_cards = dict(self.game_state_with_community_cards)
        self.game_state_without_community_cards['community_cards'] = []


    def test_version(self):
        """Test the version string."""
        self.assertTrue(isinstance(self.player.VERSION, str), "Version needs to be a string")

    def test_betRequestWithCommunityCards(self):
        """Test the betRequest method."""
        return_value = self.player.betRequest(game_state=self.game_state_without_community_cards)
        print("Returning %d" % return_value)
        self.assertTrue(isinstance(return_value, int), "Not returning an integer.")
        self.assertGreaterEqual(return_value, 0, "No negative return values allowed")

    def test_betRequestWithoutCommunityCards(self):
        """Test the betRequest method."""
        return_value = self.player.betRequest(game_state=self.game_state_without_community_cards)
        print("Returning %d" % return_value)
        self.assertTrue(isinstance(return_value, int), "Not returning an integer.")
        self.assertGreaterEqual(return_value, 0, "No negative return values allowed")

    def test_showdown(self):
        """Test the showdown method."""
        self.player.showdown(game_state=self.game_state_with_community_cards)

    def test_hand_evaluation(self):
        hand1 = [
            {"rank": '3', "suit": 'spades'}, 
            {"rank": 'K', "suit": 'hearts'},
            {"rank": '3', "suit": 'hearts'},
        ]
        
        self.assertTrue(self.player.is_pair(hand1))
        self.assertFalse(self.player.is_three(hand1))
        self.assertFalse(self.player.is_four(hand1))
        self.assertFalse(self.player.is_two_pairs(hand1))
        self.assertTrue(self.player.has_kings_aces(hand1))

        hand2 = [
            {"rank": 'A', "suit": 'spades'},
            {"rank": '5', "suit": 'clubs'}, 
            {"rank": 'K', "suit": 'hearts'},
            {"rank": '5', "suit": 'hearts'},
            {"rank": '5', "suit": 'spades'},
            {"rank": '5', "suit": 'diamonds'},
        ]
        self.assertTrue(self.player.is_pair(hand2))
        self.assertTrue(self.player.is_three(hand2))
        self.assertTrue(self.player.is_four(hand2))
        self.assertFalse(self.player.is_two_pairs(hand2))
        self.assertTrue(self.player.has_kings_aces(hand2))

        hand3 = [
            {"rank": '2', "suit": 'spades'},
            {"rank": '5', "suit": 'clubs'}, 
            {"rank": 'K', "suit": 'hearts'},
            {"rank": '5', "suit": 'hearts'},
            {"rank": '2', "suit": 'hearts'},
        ]
        self.assertTrue(self.player.is_pair(hand3))
        self.assertFalse(self.player.is_three(hand3))
        self.assertFalse(self.player.is_four(hand3))
        self.assertTrue(self.player.is_two_pairs(hand3))
        self.assertFalse(self.player.is_straight(hand3))
        self.assertTrue(self.player.has_kings_aces(hand3))

        hand4 = [
            {"rank": '10', "suit": 'spades'},
            {"rank": 'Q', "suit": 'clubs'}, 
            {"rank": '3', "suit": 'diamonds'},
            {"rank": '10', "suit": 'hearts'},
            {"rank": '10', "suit": 'clubs'},
            {"rank": 'Q', "suit": 'hearts'},
        ]
        self.assertTrue(self.player.is_pair(hand4))
        self.assertTrue(self.player.is_three(hand4))
        self.assertFalse(self.player.is_four(hand4))
        self.assertTrue(self.player.is_two_pairs(hand4))
        self.assertTrue(self.player.is_full_house(hand4))
        self.assertFalse(self.player.is_straight(hand4))
        self.assertFalse(self.player.has_kings_aces(hand4))

        hand5 = [
            {"rank": '2', "suit": 'spades'},
            {"rank": '6', "suit": 'clubs'}, 
            {"rank": '3', "suit": 'diamonds'},
            {"rank": '2', "suit": 'hearts'},
            {"rank": '10', "suit": 'clubs'},
            {"rank": '4', "suit": 'hearts'},
            {"rank": '5', "suit": 'hearts'},
        ]
        self.assertTrue(self.player.is_pair(hand5))
        self.assertFalse(self.player.is_three(hand5))
        self.assertFalse(self.player.is_four(hand5))
        self.assertFalse(self.player.is_two_pairs(hand5))
        self.assertFalse(self.player.is_full_house(hand5))
        self.assertTrue(self.player.is_straight(hand5))

        

if __name__ == "__main__":
    # Automatically executes all test methods (starting with test_) in unittest.TestCase classes
    unittest.main()
