from model import CPRModel, run_model
"""
#Random Agents:
test_random = CPRModel(num_agents=2, 
                  agent_vars= {'name':'RandomAgent', 'selfish': .5}, 
                  resource_vars= {'name':'Investment_Game', 'alpha': 1.5, 'beta': 0, 'max_contribution': 1},
                  policy_vars= {'name':'Investment_fines', 'investment_target': 1, 'tolerance': .2, 'fixed_fine': .1,
                                 'fine_slope': .1, 'infract_coeff': .1, 'infract_x_dist_coeff': .1},
                  verbose_choices = False, verbose_resource = False, verbose_policy = False, verbose_payoffs = False,
                  verbose_learning = False, verbose_init = False, verbose_final = True)
run_model(test_random, 3)
"""

#Hillclimbing Selfish Agents, No Policy:
print("\n\nHillclimbing Selfish Agents, No Policy")
alt_hill = CPRModel(num_agents=10,
                  agent_vars= {'name':'HillclimbingAgent', 'selfish': 0, 'explore_range': .1, 'prob_explore': .25}, 
                  resource_vars= {'name':'Investment_Game', 'alpha': 1.5, 'beta': 0, 'max_contribution': 1},
                  policy_vars= {'name':'No_interventions'},
                  verbose_choices = False, verbose_resource = False, verbose_policy = False, verbose_payoffs = False,
                  verbose_learning = False, verbose_init = False, verbose_final = True)
run_model(alt_hill, 500)


#Hillclimbing Selfish Agents, No Policy:
print("\n\nHillclimbing Selfish Agents, No Policy")
selfish_hill = CPRModel(num_agents=10,
                  agent_vars= {'name':'HillclimbingAgent', 'selfish': 1, 'explore_range': .1, 'prob_explore': .25}, 
                  resource_vars= {'name':'Investment_Game', 'alpha': 1.5, 'beta': 0, 'max_contribution': 1},
                  policy_vars= {'name':'No_interventions'},
                  verbose_choices = False, verbose_resource = False, verbose_policy = False, verbose_payoffs = False,
                  verbose_learning = False, verbose_init = False, verbose_final = True)
run_model(selfish_hill, 500)



#Hillclimbing Selfish Agents, simple fixed policy:
print("\n\nHillclimbing Selfish Agents, simple fixed policy")
selfish_hill_w_policy = CPRModel(num_agents=10, 
                  agent_vars= {'name':'HillclimbingAgent', 'selfish': 1, 'explore_range': .1, 'prob_explore': .25}, 
                  resource_vars= {'name':'Investment_Game', 'alpha': 1.5, 'beta': 0, 'max_contribution': 1},
                  policy_vars= {'name':'Investment_fines', 'investment_target': 1, 'tolerance': .2, 'fixed_fine': .1,
                                 'fine_slope': 1, 'infract_coeff': 0, 'infract_x_dist_coeff': 0},
                  verbose_choices = False, verbose_resource = False, verbose_policy = False, verbose_payoffs = False,
                  verbose_learning = False, verbose_init = False, verbose_final = True)
run_model(selfish_hill_w_policy, 1000)

"""


#Mixed Pop: Hillclimbing and Fixed agent, No Policy:
print("\n\nHillclimbing Altruistic Agents, No Policy")
Selfish_mixed_hill = CPRModel(num_agents=2, 
                  agent_vars= [{'count': 1, 'name':'HillclimbingAgent', 'selfish': 1, 'explore_range': .1},
                               {'count': 1, 'name':'FixedAgent', 'selfish': 0, 'choice': 1}], 
                  resource_vars= {'name':'Investment_Game', 'alpha': 1.5, 'beta': 0, 'max_contribution': 1},
                  policy_vars= {'name':'No_interventions'},
                  verbose_choices = False, verbose_resource = False, verbose_policy = False, verbose_payoffs = False,
                  verbose_learning = False, verbose_init = False, verbose_final = True)
run_model(Selfish_mixed_hill, 50)
"""