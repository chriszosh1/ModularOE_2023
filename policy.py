class Policy():
    """A base class for policies."""
    def __init__(self):
        pass


class No_interventions(Policy):
    """A degenerate policy where nothing is done.
    
    Vars to include:
    -name = No_interventions
    """
    def __init__(self, policy_vars, agent_count):
        self.fine_vector = [0 for aid in range(agent_count)]

    def fines(self, contributions, verbose):
        if verbose:
            print(f"---Policy Info---")
            print(f'Contributions: {contributions}')
            print(f'Fines: {self.fine_vector}')
        return self.fine_vector


class Investment_fines(Policy):
    """A fine associated with number of infractions and size of infraction by individuals.

       Vars to include:
       -name = Investment_fines
       -investment_target           #This should be the i* for social welfare to be maximized.
       -tolerance                   #Fines within this distance of the target will not be fined.
       -fixed_fine                  #This is the fine intercept
       -fine_slope
       -infract_coeff               #A fixed amount you pay for each past infraction you've had.
       -infract_x_dist_coeff        #A coeff for the interaction beteween past infraction count and size of infraction.
    """
    def __init__(self, policy_vars, agent_count):
        self.investment_target = policy_vars["investment_target"]
        self.tolerance = policy_vars["tolerance"]
        self.fixed_fine = policy_vars["fixed_fine"]
        self.dist_coeff = policy_vars["fine_slope"]
        self.infract_coeff = policy_vars["infract_coeff"]
        self.infract_x_dist_coeff = policy_vars["infract_coeff"]
        self.infraction_counts = {aid:0 for aid in range(agent_count)}

    def fines(self, contributions, verbose):
        '''A fine for being at a certain level of investment.'''
        fine_vector = []
        for c_pos in range(len(contributions)):
            dist_from_target = abs(contributions[c_pos] - self.investment_target)
            if dist_from_target > self.tolerance:
                violations = self.infraction_counts[c_pos]
                fine = self.fixed_fine + (self.dist_coeff * dist_from_target) + (self.infract_coeff * violations) + (self.infract_x_dist_coeff * dist_from_target * violations)
                self.infraction_counts[c_pos] += 1
            else:
                fine = 0
            fine_vector.append(fine)
        if verbose:
            print(f"---Policy Info---")
            print(f'Contributions: {contributions}')
            print(f'Investment target {self.investment_target} with tolerance {self.tolerance}')
            print(f'Fines: {fine_vector}')
        return fine_vector


def get_policy(policy_vars, agent_count):
    '''Returns an instance of the policy class you name.'''
    name = policy_vars['name']
    if name == 'Investment_fines':
        return Investment_fines(policy_vars, agent_count)
    elif name == 'No_interventions':
        return No_interventions(policy_vars, agent_count)