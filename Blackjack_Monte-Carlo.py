import numpy as np
import random

states = []
for i in range(10):
    for j in range(2):
        for k in range(10):
            states.append((i, j, k))

pi = {}
for state in states:
    pi[state] = {
        0 : 0,
        1 : 1
    }

# random policy
for h in range(10):
    for a in range(2):
        for d in range(10):
            r = np.random.random()
            pi[(h, a, d)][1] = r
            pi[(h, a, d)][0] = 1 - r


V = np.zeros((10, 2, 10))
visit_count = np.zeros((10, 2, 10))

def update_values(states, r, V, visit_count):
    for h, a, d in states:
        V[h][a][d] = V[h][a][d] + (1/visit_count[h][a][d])*(r - V[h][a][d]) 


def blackjack_hand_result(V, visit_count):
    #Deck of cards, 4 types of 10
    
    deck=np.array([1,2,3,4,5,6,7,8,9,10,10,10,10])
    
    #Creating a random hand if none is input
    
    player_hand=[random.choice(deck), random.choice(deck)]
        
    dealer_card=random.choice(deck)
    
    # keeps track of all states that the hand has been in during one play
    states_visited = []
    
    player_sum = sum(player_hand)
    
    # an ace that can be used as an 11 i.e. the sum of the cards is less than 12
    usable_ace = 0
    if 1 in player_hand:
        usable_ace = 1
        player_sum += 10
    
    # update states
    if player_sum > 11:
        state = (player_sum-12, usable_ace, dealer_card-1)
        states_visited.append(state)
        visit_count[player_sum-12][usable_ace][dealer_card-1] += 1
        
    # keeps track of dealers hand
    dealer_cards=[dealer_card]
    

    # Seeing if player hit blackjack
    if player_sum == 21:

        #Seeing if casino also hit blackjack, in which case tie

        dealer_cards.append(random.choice(deck))
        if 1 in (dealer_cards) and sum(dealer_cards)==11:
            update_values(states_visited, 0, V, visit_count)
            return 0
        
        update_values(states_visited, 1, V, visit_count)
        return 1
    

    else:
    # Seeing how often it says to 'hit'
        hit = 1
        stay = 0

        while player_sum < 12 or np.random.random() < pi[state][hit]:
            #Adding one card for every hit
            new_card = random.choice(deck)
            player_hand.append(new_card)
            player_sum = sum(player_hand)
            
            usable_ace = 0
            
            if 1 in player_hand and player_sum < 12:
                usable_ace = 1
                player_sum += 10
            
            state = (player_sum-12, usable_ace, dealer_card-1)
            
            #Player loses bet if hand goes above 21
            if player_sum > 21:
                update_values(states_visited, -1, V, visit_count)
                return -1
            
            if player_sum > 11:
                states_visited.append(state)
                visit_count[player_sum-12][usable_ace][dealer_card-1] += 1
            
    while True:
        #Plays out the blackjack hand from dealer's side

        #Give dealer extra card if loop hasn't broken
        dealer_cards.append(random.choice(deck))


        #Keep track of sum of dealer's cards
        dealer_score= sum(dealer_cards)

        #Keep track of soft score if dealer has an ace

        soft_score= dealer_score
        if dealer_score<=11 and 1 in dealer_cards:
            soft_score+=10

        #If dealer gets blackjack you lose even if you have 21
        if len(dealer_cards)==2 and soft_score==21:
            update_values(states_visited, -1, V, visit_count)
            return -1
        
        #Dealer stays on all 17s
        if soft_score>=17:

            #If dealer bust, player wins bet
            if soft_score>21:
                update_values(states_visited, 1, V, visit_count)
                return 1

            #If player has more than dealer, player wins bet
            if player_sum>soft_score:
                update_values(states_visited, 1, V, visit_count)
                return 1

            #Tie means no money changes hands
            if player_sum==soft_score:
                update_values(states_visited, 0, V, visit_count)
                return 0

            #If player has lower, player loses bet
            if player_sum<soft_score:
                update_values(states_visited, -1, V, visit_count)
                return -1


def blackjack_sim(n_hands, V, visit_count):
    for i in range(n_hands):
        blackjack_hand_result(V, visit_count)
     
blackjack_sim(50_000, V, visit_count)
print(V)