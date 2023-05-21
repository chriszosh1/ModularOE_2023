from resources import get_resource
from agent import get_agent
from policy import get_policy

class CPRModel():
    """A model of agents playing a resource game."""
    def __init__(self,
                #Model variables:
                num_agents=2,
                #OstAgent variables:
                agent_vars = {},
                #resource variables
                resource_vars = {},
                #policy variables
                policy_vars = {},
                #output variables
                verbose_choices=False,
                verbose_resource=False,
                verbose_policy=False,
                verbose_payoffs=False,
                verbose_learning=False,
                verbose_init=False,
                verbose_final=True,
                ):
        # Model variables:
        self.num_agents = num_agents
        self.tick = 0
        # Agent variables:
        self.agents = []
        self.agents_by_id = {}
        self.initialize_agents(agent_vars, verbose_init)
        # Resource variables:
        self.resource = get_resource(resource_vars)
        # Policy variables:
        self.policy = get_policy(policy_vars, agent_count = self.num_agents)
        #Output variables:
        self.verbose_payoffs = verbose_payoffs
        self.verbose_resource = verbose_resource
        self.verbose_choices = verbose_choices
        self.verbose_policy = verbose_policy
        self.verbose_learning = verbose_learning
        self.verbose = (self.verbose_choices or self.verbose_resource or self.verbose_policy or self.verbose_payoffs or self.verbose_learning)
        self.verbose_init = verbose_init
        self.verbose_final = verbose_final

    def initialize_agents(self, agent_vars, verbose):
        '''Populates the model with agents'''
        init_aid = 0
        if isinstance(agent_vars, list):
            for i in range(len(agent_vars)):
                avi = agent_vars[i]
                for c in range(avi['count']):
                    new_agent = get_agent(agent_vars = avi, id = init_aid, model = self)
                    if verbose:
                        print(f'Agent {init_aid} is type {new_agent.type_name}')
                    self.agents.append(new_agent)
                    self.agents_by_id[init_aid] = new_agent
                    init_aid += 1
        else:
            for a in range(self.num_agents):
                new_agent = get_agent(agent_vars = agent_vars, id = a, model = self)
                if verbose:
                        print(f'Agent {a} is type {new_agent.type_name}')
                self.agents.append(new_agent)
                self.agents_by_id[a] = new_agent

    def step(self):
        if self.verbose:
            print(f'\nPeriod {self.tick}')
        #Step 1 - Agents take action:
        if self.verbose_choices:
            print(f'---Agent Choices---')
        contributions = []
        actions_avail = self.resource.action_set
        for a in self.agents:
            contributions.append(a.choose(actions_avail, self.verbose_choices))
        #Step 2 - Calculate payoff vector from resource:
        game_payoffs = self.resource.resource_payoffs(contributions, self.verbose_resource)
        #Step 3 - Update payoff to reflect any penalties from policy:
        fine_vector = self.policy.fines(contributions, self.verbose_policy)
        #Step 4 - Players get payoffs and calculate utility:
        dollar_payoffs = [game_payoffs[i] - fine_vector[i] for i in range(len(game_payoffs))]
        for a_pos in range(len(self.agents)):
            self.agents[a_pos].process_payoffs(a_pos, dollar_payoffs, fine_vector, game_payoffs, self.verbose_payoffs)
            self.agents[a_pos].update_memories(self.verbose_learning)
        #Step LAST - Update model variables:
        self.tick += 1

def run_model(model, steps):
    """Runs the model steps times."""
    for s in range(steps):
        model.step()
    if model.verbose_final:
        print("---Final Choices---")
        for a in model.agents:
            print({a.all_choices[-1]})