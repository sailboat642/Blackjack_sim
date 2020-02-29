import numpy as np
import random
import cProfile

states = []
for i in range(10):
    for j in range(2):
        for k in range(10):
            states.append((i, j, k))

dealer_dist = [
    [13.6,  5.6 , 14.3, 14.6, 13.8, 38.1],
    [34.9, 13.6 , 14.1, 12.8, 12.8, 11.9],
    [38.1, 11.8 , 13.4, 12.6, 12.2, 12.0],
    [39.6, 11.9 , 13.3, 12.1, 11.8, 11.4],
    [42.1, 12.1 , 12.4, 11.0, 11.6, 10.9],
    [43.5, 12.3 , 11.8, 11.0, 11.2, 10.3],
    [26.3, 37.0 , 14.1,  7.9,  7.8,  7.0],
    [25.0, 12.7 , 35.6, 12.8,  7.3,  6.6],
    [22.3, 12.0 , 12.0, 35.6, 11.9,  6.2],
    [21.3, 11.25, 11.5, 11.1, 34.1, 11.3]
]

# cumulative win probability
# sum of all indexes before
for probabilities in dealer_dist:
    for i in range(1, 6):
        probabilities[i] += probabilities[i-1]    

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



def blackjack_probability(s_, s, a, r):
    stay = 0
    hit = 1

    if a == stay:
        '''find Probability of win, loss, tie'''
        if s[0] < 5:
            # probability dealer busts
            if r == 1:
                return (dealer_dist[s[2]][0])/100
            
            elif r == 0:
                return 0

            else:
                return (1 - dealer_dist[s[2]][0]/100)
        
        else:
            index = s[0] - 4      # 17 is 1
            if r == 1:
                # probability of dealer recieving a lower score
                return (dealer_dist[s[2]][index-1]/ 100)
            
            elif r == 0:
                # probability of dealer getting player's score
                return ((dealer_dist[s[2]][index] - dealer_dist[s[2]][index-1])/100)
            
            else:
                # probability of dealer getting a higher score
                return (1-(dealer_dist[s[2]][index]/100))
                
    
    if a == hit:
        '''Find probability s_'''
        
        if s_ == (-1, -1, -1):
            '''find Probability of a bust'''
            if s[1] == 0:
                return (4 + s[0])/13
            else:
                # player cannot bust with an ace
                return 0
            
        if s[2] != s_[2]:
            '''dealer card is not the same'''
            return 0
        
            
        if s_[1] == 0 and s[1] == 1:
            '''player has to use his ace'''
            
            if s_[0] == s[0]:
                '''probability of a 10 value card'''
                return 4/13
            
            if s_[0] > s[0]:
                return 0
            
            return 1/13
        
        if s_[1] == s[1]:
            '''no ace transaction'''
            if s_[0] <= s[0]:
                '''new hand cannot be less than old hand'''
                return 0
        
            return 1/13
        
        return 0


def evaluate_policy(V, theta, pi):
    while True:
        delta = 0
        for s1, s2, s3 in states:
            v = V[s1][s2][s3]
            if abs(v) > 2:
                return
            bellman_update(V, (s1, s2, s3), pi)
            delta = max(delta, abs(v - V[s1][s2][s3]))
        if delta < theta:
            break
    return V


def bellman_update(V, state, pi):
    """Mutate ``V`` according to the Bellman update equation."""
    stay = 0
    hit = 1
    
    hit_value = 0
    probability = [0, 0]
    for s_ in states:
        Vs_ = V[s_[0]][s_[1]][s_[2]]
        hit_value += blackjack_probability(s_, state, hit, 0)*(0 + Vs_)
        probability[0] += blackjack_probability(s_, state, hit, 0)
        
    
    # probability of a bust
    hit_value += blackjack_probability((-1, -1, -1), state, hit, -1)*(-1 + 0)
    probability[0] += blackjack_probability((-1, -1, -1), state, hit, -1)
    
    # value of staying
    stay_value = 0
    for r in [-1, 0, 1]:
        stay_value += blackjack_probability((-1, -1, -1), state, stay, r)*(r + 0)
        probability[1] += blackjack_probability((-1, -1, -1), state, stay, r)
       
    
    hand, ace, dealer = state
    V[hand][ace][dealer] = pi[state][hit]*hit_value + pi[state][stay]*stay_value
    return 


def error(v):
    return (abs(1 - v))


V = np.zeros((10, 2, 10))
cProfile.run("evaluate_policy(V, 0.000001, pi)")
