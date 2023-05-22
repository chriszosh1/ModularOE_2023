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
                data_to_return=[],      #Include list of agent time series lists to include
                verbose_choices=False,
                verbose_resource=False,
                verbose_policy=False,
                verbose_payoffs=False,
                verbose_learning=False,
                verbose_init=False,
                verbose_final=True
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
        self.data_to_return = data_to_return
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

    def get_data(self):
        '''Returns a dictionary of long data of specified fields of interest.'''
        data = {}
        for field in self.data_to_return:
            data[field] = []
        for aid, a in self.agents_by_id.items():
            if 'choice' in data:
                choice_list = a.all_choices
                for t in range(len(choice_list)):
                    data['choice'].append({'id': aid, 't': t, 'choice': choice_list[t]})
            if 'game_payoff' in data:
                agp = a.all_game_payoffs
                for t in range(len(agp)):
                    data['game_payoff'].append({'id': aid, 't': t, 'game_payoff': agp[t]})
            if 'fine' in data:
                af = a.all_fines
                for t in range(len(af)):
                    data['fine'].append({'id': aid, 't': t, 'fine': af[t]})
            if 'dollar_payoff' in data:
                dpo = a.dollar_payoffs
                for t in range(len(dpo)):
                    data['dollar_payoff'].append({'id': aid, 't': t, 'dollar_payoff': dpo[t]})
            if 'felicity' in data:
                fel = a.all_felicities
                for t in range(len(fel)):
                    data['felicity'].append({'id': aid, 't': t, 'felicity': fel[t]})
        return data


def run_model(model, steps):
    """Runs the model steps times."""
    for s in range(steps):
        model.step()
    if model.verbose_final:
        print("---Final Choices---")
        for a in model.agents:
            print({a.all_choices[-1]})
    if model.data_to_return:
        return model.get_data()

def run_run_model(
                #Run variables:
                steps, runs,
                #File variables:
                tag = '', #goes before field in filename
                data_to_return=[],
                #Model variables:
                num_agents=2, agent_vars = {}, resource_vars = {}, policy_vars = {},
                verbose_final=False
                ):
    """Runs run_model runs number of times for steps steps each run."""
    if data_to_return:
        files = {}
        for field in data_to_return:
            filename = f'{tag}_{field}.txt'
            files[field] = filename
            f = open(filename,'w')
            f.write(f'run,id,t,{field}\n')
            f.close()
    for r in range(runs):
        model = CPRModel(num_agents = num_agents, agent_vars = agent_vars, resource_vars = resource_vars,
                     policy_vars = policy_vars, data_to_return=data_to_return, verbose_final = verbose_final)
        if verbose_final:
            print(f'---Run {r}---')
        output = run_model(model, steps)
        if data_to_return:
            for field in data_to_return:
                f = open(files[field],'a')
                run_field_data = output[f'{field}']
                for row in run_field_data:
                    f.write(f'{r},{row["id"]},{row["t"]},{row[field]}\n')