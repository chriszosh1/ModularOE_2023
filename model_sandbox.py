from model import CPRModel, run_model, run_run_model
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


#Hillclimbing Altruistic Agents, No Policy:
print("\n\nHillclimbing Altruistic Agents, No Policy")
alt_hill = CPRModel(num_agents=10,
                  agent_vars= {'name':'HillclimbingAgent', 'selfish': 0, 'explore_range': .1, 'prob_explore': .25}, 
                  resource_vars= {'name':'Investment_Game', 'alpha': 1.5, 'beta': 0, 'max_contribution': 1},
                  policy_vars= {'name':'No_interventions'},
                  verbose_choices = False, verbose_resource = False, verbose_policy = False, verbose_payoffs = False,
                  verbose_learning = False, verbose_init = False, verbose_final = True)
run_model(alt_hill, 1000)


#Hillclimbing Selfish Agents, No Policy:
print("\n\nHillclimbing Selfish Agents, No Policy")
selfish_hill = CPRModel(num_agents=10,
                  agent_vars= {'name':'HillclimbingAgent', 'selfish': 1, 'explore_range': .1, 'prob_explore': .25}, 
                  resource_vars= {'name':'Investment_Game', 'alpha': 1.5, 'beta': 0, 'max_contribution': 1},
                  policy_vars= {'name':'No_interventions'},
                  verbose_choices = False, verbose_resource = False, verbose_policy = False, verbose_payoffs = False,
                  verbose_learning = False, verbose_init = False, verbose_final = True)
run_model(selfish_hill, 1000)


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


#Testing data output (as dicts)
print("\n\nHillclimbing Selfish Agents, No Policy")
alt_hill = CPRModel(num_agents=2,
                  agent_vars= {'name':'HillclimbingAgent', 'selfish': 0, 'explore_range': .1, 'prob_explore': .25}, 
                  resource_vars= {'name':'Investment_Game', 'alpha': 1.5, 'beta': 0, 'max_contribution': 1},
                  policy_vars= {'name':'No_interventions'},
                  verbose_choices = False, verbose_resource = False, verbose_policy = False, verbose_payoffs = False,
                  verbose_learning = False, verbose_init = False, verbose_final = True,
                  data_to_return = ['choice', 'game_payoff', 'fine', 'dollar_payoff', 'felicity'])
test = run_model(alt_hill, 3)

for f in alt_hill.data_to_return:
    print(f'\n{f}')
    for i in test[f'{f}']:
        print(i)


#Testing file creation for run_run_model:
run_run_model(steps = 3, runs = 3, tag = 'test', 
              data_to_return=['choice', 'game_payoff', 'fine', 'dollar_payoff', 'felicity'], num_agents=3,
              agent_vars= {'name':'HillclimbingAgent', 'selfish': 0, 'explore_range': .1, 'prob_explore': .25},
              resource_vars= {'name':'Investment_Game', 'alpha': 1.5, 'beta': 0, 'max_contribution': 1},
              policy_vars = {'name':'No_interventions'})
"""

#Testing no file saving for run_run_model, just final output:
run_run_model(steps = 3, runs = 3, tag = 'test', 
              data_to_return=[], num_agents=3,
              agent_vars= {'name':'HillclimbingAgent', 'selfish': 0, 'explore_range': .1, 'prob_explore': .25},
              resource_vars= {'name':'Investment_Game', 'alpha': 1.5, 'beta': 0, 'max_contribution': 1},
              policy_vars = {'name':'No_interventions'},
              verbose_final=True)