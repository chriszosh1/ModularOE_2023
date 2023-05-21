class Resource():
    """A base-class for resources."""
    def __init__(self):
        pass


class Investment_Game(Resource):
    """This is the investment game
       Ostrom, Gardner, & Walker (1994)
       
       Vars to include:
       -name = Investment_Game
       -alpha
       -beta
       -max_contribution
    """
    def __init__(self, vars):
        self.alpha = vars['alpha']
        self.beta = vars['beta']
        self.min_contribution = 0
        self.max_contribution = vars['max_contribution']
        self.action_set = [self.min_contribution, self.max_contribution]

    def resource_payoffs(self, contributions, verbose):
        """Takes a vector of contributions and returns a
         vector of the players resulting game payoffs."""
        con_total = sum(contributions)
        grown_con_total = (self.alpha*con_total) - self.beta*(con_total**2)
        per_capita_gct = grown_con_total/len(contributions)
        game_payoffs = []
        for c in contributions:
            game_payoffs.append(1 - c + per_capita_gct)
        if verbose:
            print(f"---Resource Info---")
            print(f'Resource contributions: {contributions}')
            print(f'Resource payoff: {grown_con_total}')
            print(f'Resource per capita payoff: {per_capita_gct}')
            print(f'Game_payoffs: {game_payoffs}')
        return game_payoffs
    
    def s_opt(self, player_count):
        """Returns the social optimal for the game."""
        if self.beta == 0:
            if self.alpha <= 1:
                return 0
            else:
                return self.max_contribution
        else:
            thisopt =  (self.alpha - 1) / ( 2 * self.beta * player_count)
            return max(thisopt, 0)

    def i_opt(self, player_count):
        """Returns the individual optimal for the game."""
        if self.beta == 0:
            if self.alpha <= player_count:
                return 0
            else:
                return self.max_contribution
        else:
            thisopt =  (self.alpha - player_count) / ( 2 * self.beta * (player_count ** 2))
            return max( thisopt, 0 )


def get_resource(resource_vars):
    '''Returns an instance of the resource class you name.'''
    name = resource_vars['name']
    if name == 'Investment_Game':
        return Investment_Game(resource_vars)