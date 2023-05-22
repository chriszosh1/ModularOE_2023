from random import uniform, choice
from copy import copy


class OstAgent():
    """ A base class for agents."""
    def __init__(self, vars, id, model):
        self.type_name = vars['name']
        self.selfish = vars['selfish']
        self.id = id
        self.model = model
        self.all_choices = []
        self.all_game_payoffs = []
        self.all_fines = []
        self.dollar_payoffs = []
        self.all_felicities = []
        
    def process_payoffs(self, a_pos, dollar_payoffs, fine_vector, game_payoffs, verbose):
        '''Stores game payoff and uses self and others game payoff to calculate utility.'''
        own_dpo = dollar_payoffs[a_pos]
        self.all_game_payoffs.append(game_payoffs[a_pos])
        self.all_fines.append(fine_vector[a_pos])
        self.dollar_payoffs.append(own_dpo)
        #Calculating felicity:
        other_dpo = copy(dollar_payoffs)
        del other_dpo[a_pos]
        others_av_dpo = sum(other_dpo)/len(other_dpo)
        felicity = (self.selfish * own_dpo) + ((1-self.selfish) * others_av_dpo)
        self.all_felicities.append(felicity)
        if verbose:
            print(f"---Agent {self.id} Payoffs---")
            print(f"Agent {self.id}'s dollar payoff is {own_dpo}")
            print(f'Agent {self.id} is {self.selfish} selfish.')
            print(f"Agent {self.id}'s felicity is {felicity}")

    def update_memories(self, verbose):
        pass


class FixedAgent(OstAgent):
    """An agent who always chooses the same thing.
    
       Vars to include:
       -name = FixedAgent
       -selfish
       -choice
    """
    def __init__(self, vars, id, model):
        super().__init__(vars, id, model)
        self.choice = vars['choice']
    
    def choose(self, action_set, verbose):
        if verbose:
            print(f'Agent {self.id} chooses {self.choice}')
        self.all_choices.append(self.choice)
        return self.choice


class RandomAgent(OstAgent):
    """An agent who decides by flipping coins and spinning wheels.
    
       Vars to include:
       -name = RandomAgent
       -selfish
    """
    def __init__(self, vars, id, model):
        super().__init__(vars, id, model)

    def choose(self, action_set, verbose):
        roll = uniform(action_set[0], action_set[1])
        if verbose:
            print(f'Agent {self.id} chooses {roll}')
        self.all_choices.append(roll)
        return roll
    

class HillclimbingAgent(OstAgent):
    """An agent who decides......
    
       Vars to include:
       -name = HillclimbingAgent
       -selfish
       -explore_range
       -initial_choice (optional):  Randomly chosen ~ Uniform[Min,Max] otherwise
       -prob_explore (optional): Set to 1 by default (always explore)
       -dynamic_explore_coeff (optional): None by default.
            If value given, exploring + choice worse -> self.explore_range = self.explore_range * dynamic_explore_coeff

       -exploration_distr (optional): Uniform[+-explore_range] by default,
            can choose instead: Triangle, TruncNorm
    """
    def __init__(self, vars, id, model):
        super().__init__(vars, id, model)
        self.explore_range = vars['explore_range']
        self.explore = False
        self.alt_choice = None
        if 'initial_choice' in vars:
            self.best_choice = [vars['initial_choice']]
        else:
            self.best_choice = None
        if 'prob_explore' in vars:
            self.prob_explore = vars['prob_explore']
        else:
            self.prob_explore = 1
        if 'dynamic_explore_coeff' in vars:
            self.dynamic_explore_coeff = vars['dynamic_explore_coeff']
        else:
            self.dynamic_explore_coeff = None

    def _decide_explore(self):
        '''Determines if exploring this round.'''
        explore_roll = uniform(0,1)
        return explore_roll <= self.prob_explore

    def _roll_canidate(self, min, max):
        '''Determines what new explored choice will be.'''
        sign = choice([-1,1])
        magnitude = uniform(0,self.explore_range)
        canidate = self.best_choice[0] + (sign)*magnitude
        if canidate > min and canidate < max:
            return canidate
        else:
            return self._roll_canidate(min, max)

    def choose(self, action_set, verbose):
        if self.best_choice:
            if len(self.best_choice) > 1: #Turn 1 on.. chance to explore or use best again..
                self.explore = self._decide_explore()
                if self.explore: #Trying something new
                    self.alt_choice = [self._roll_canidate(action_set[0], action_set[1])] 
                    choice = self.alt_choice[0]
                else: #Sticking with the best tried so far
                    choice = self.best_choice[0]
            else: #Turn 0, need to evaluate your initial choice...
                choice = self.best_choice[0]
            self.all_choices.append(choice)
            if verbose:
                print(f'Agent {self.id} chooses {choice}')
            return choice
        else: #Turn 0 when no seeded choice.. need to grab random using bounds given by action set.
            self.best_choice = [uniform(action_set[0], action_set[1])]
            return self.choose(action_set, verbose)

    def update_memories(self, verbose):
        if self.explore:
            self.alt_choice.append(self.all_felicities[-1])
            if self.best_choice:
                if self.best_choice[1] < self.alt_choice[1]: #New Choice was better
                    if verbose:
                        print(f'New choice for agent {self.id}, {self.alt_choice}, is better than {self.best_choice}.')
                    self.best_choice = copy(self.alt_choice)
                    if self.dynamic_explore_coeff:
                        self.explore_range = max(self.explore_range/self.dynamic_explore_coeff, 1)
                        if verbose:
                            print(f'Agent {self.id} will explore more extremely.')
                elif verbose: #New Choice was as good or worse.
                    print(f'Previous choice for agent {self.id}, {self.best_choice}, is better than {self.alt_choice}.')
                    if self.dynamic_explore_coeff:
                        self.explore_range *= self.dynamic_explore_coeff
                        if verbose:
                            print(f'Agent {self.id} will explore less extremely.')

            else:
                self.best_choice = copy(self.alt_choice)
        else:
            if len(self.best_choice)>1:
                self.best_choice[1] = self.all_felicities[-1] #Updating exploited strats payoff to be the present one
            else:
                self.best_choice.append(self.all_felicities[-1])
            if verbose:
                print(f'Exploited existing choice for agent {self.id}.')


def get_agent(agent_vars, id, model):
    '''Returns an instance of the resource class you name.'''
    name = agent_vars['name']
    if name == 'FixedAgent':
        return FixedAgent(vars = agent_vars, id = id, model = model)
    elif name == 'RandomAgent':
        return RandomAgent(vars = agent_vars, id = id, model = model)
    elif name == 'HillclimbingAgent':
        return HillclimbingAgent(vars = agent_vars, id = id, model = model)