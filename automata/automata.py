import itertools


class State:
    def __init__(self, id: int, name: str = str(id)):
        self.id = id
        self.name = name

    def __str__(self):
        return self.name


class Transition:
    def __init__(self, src: State = None, dest: State = None, read: str = '', pop: str = '', push: str = ''):
        self.src = src
        self.dest = dest
        self.read = read
        self.push = push
        self.pop = pop

    def __str__(self):
        ret_val = str(self.src) + ', ' + self.read + ', ' + self.pop + ' -> ' + '(' + str(
            self.dest) + ', ' + self.push + ')'
        return ret_val


class Rule:
    def __init__(self):
        self.lhs = ''
        self.rhs = ''

    def __str__(self, format=''):
        if format == 'tex':
            arrow = ' $\\rightarrow$ '
        else:
            arrow = ' -> '
        return self.lhs + arrow + self.rhs

    def get_lhs(self):
        return self.lhs

    def get_rhs(self):
        return self.rhs

        # def __cmp__(self, other):
        #     if self.lhs > other.lhs:
        #         return self


class CFG:
    def __init__(self):
        self.rules = set()

    def __str__(self, format=None):
        if format == 'tex':
            ret_val = '\n'.join(
                [rule.__str__('tex') for rule in sorted(self.rules, key=lambda rule: (rule.get_lhs(), rule.get_rhs()))])
        else:
            ret_val = '\n'.join(
                [str(rule) for rule in sorted(self.rules, key=lambda rule: (rule.get_lhs(), rule.get_rhs()))])
        return ret_val


class PDA:
    def __init__(self):
        self.fa_type = ""
        # TODO: these should be sets...
        self.sigma = list()
        self.gamma = list()
        self.states = list()
        self.state_count = 0
        self.start = None
        self.final = list()
        self.delta = list()

    def __str__(self):
        ret_val = 'type: ' + self.fa_type
        ret_val += '\nsigma: %s' % self.sigma
        if len(self.gamma) > 0:
            ret_val += '\ngamma: %s' % self.gamma
        ret_val += '\nstates: %s' % [str(s) for s in self.states]
        ret_val += '\nstart: ' + str(self.start)
        ret_val += '\nfinal: %s' % [str(s) for s in self.final]
        ret_val += '\ndelta: \n  %s' % '\n  '.join([str(t) for t in self.delta])

        return ret_val

    def add_state(self, id: int = -1, name: str = ''):
        if id == -1:
            id = self.state_count

        if name == '':
            name = 'q' + str(id)

        state = State(id, name)
        self.states.append(state)
        self.state_count += 1
        return state

    def remove_state(self, state: State):
        self.states.remove(state)

    def add_transition(self, src: State = None, dest: State = None, read: str = '', pop: str = '', push: str = ''):
        transition = Transition(src, dest, read, pop, push)
        self.delta.append(transition)

        # TODO: this is easier with sets
        if read != 'ε' and self.sigma.count(read) < 1:
            self.sigma.append(read)
        if pop != 'ε' and self.gamma.count(pop) < 1:
            self.gamma.append(pop)
        if push != 'ε' and self.gamma.count(push) < 1:
            self.gamma.append(push)

        return transition

        # def __init__(self, fa_type: str = "", sigma: list = list(), gamma: list = list(), states: list = list(),

    #                 start: State = None, final: list = list(), delta: list = list()):
    # if type(fa_type) == tuple:
    #     self.fa_type = fa_type[0]
    #     self.sigma = fa_type[1]
    #     self.gamma = fa_type[2]
    #     self.states = fa_type[3]
    #     self.start = fa_type[4]
    #     self.final = fa_type[5]
    #     self.delta = fa_type[6]
    # else:
    #     self.fa_type = fa_type
    #     self.sigma = sigma
    #     self.gamma = gamma
    #     self.states = states
    #     self.start = start
    #     self.final = final
    #     self.delta = delta
    #
    #     self.verify()

    def verify(self):
        assert (self.states.count(self.start) == 1)
        for f in self.final:
            assert (self.states.count(f) == 1)
        for d in self.delta:
            assert self.states.count(d.src) == 1
            assert self.states.count(d.dest) == 1
            # TODO: store alphabets based on transitions
            # assert self.sigma.count(d.read) == 1
            # assert self.gamma.count(d.pop) == 1
            # assert self.gamma.count(d.push) == 1

    def get_state(self, id: int = None, name: str = None):
        if id is not None:
            for s in self.states:
                if s.id == id:
                    ret_state = s
                    break
        elif name is not None:
            for s in self.states:
                if s.name == id:
                    ret_state = s
                    break
        else:
            print('No state specified.')
            raise LookupError

        return ret_state


def union(fa1: State, fa2: State):
    # TODO: rewrite for objects
    fa3 = PDA()
    fa3.gamma = fa1.sigma
    fa3.gamma = fa1.gamma
    fa3.states = list(itertools.product(fa1['states'], fa2['states']))
    new_start = fa3.add_state()

    print("I ain't dun a union, yet!")
    return fa3


def pda_to_cfg(pda: PDA, latex: bool):
    if latex:
        wrap = '$'
        empty = '\epsilon'
        substart = '_{'
        subend = '}'
    else:
        wrap = ''
        empty = 'ε'
        substart = ''
        subend = ''

    # first, add a single final state that clears the stack and remove 'old' final states
    final_state = pda.add_state()
    while len(pda.final) > 0:
        state = pda.final.pop()
        pda.add_transition(state, final_state, 'ε', 'ε', 'ε')
    pda.final.append(final_state)

    for symbol in pda.gamma:
        pda.add_transition(final_state, final_state, 'ε', symbol, 'ε')

    # next, convert transitions to push XOR pop.
    for transition in pda.delta:
        if transition.push == 'ε' and transition.pop == 'ε':
            # no push or pop

            # new intermediate state
            new_state = pda.add_state()

            # push
            pda.add_transition(transition.src, new_state, transition.read, 'ε', '!')

            # pop
            pda.add_transition(new_state, transition.dest, 'ε', '!', 'ε')

            # remove old transition
            pda.delta.remove(transition)

        elif transition.push != 'ε' and transition.pop != 'ε':
            # push and pop

            # new intermediate state
            new_state = pda.add_state()

            # pop
            pda.add_transition(transition.src, new_state, transition.read, transition.pop, 'ε')

            # push
            pda.add_transition(new_state, transition.dest, 'ε', 'ε', transition.push)

            # remove old transition
            pda.delta.remove(transition)

    cfg = CFG()

    # 1: For each state Aq, add rule Aqq -> ε
    cfg1 = CFG()
    for q in pda.states:
        rule = Rule()
        rule.lhs = wrap + 'A' + substart + q.name + q.name + subend + wrap
        rule.rhs = wrap + empty + wrap
        cfg1.rules.add(rule)

    print('type 1 rules:\n' + str(cfg1))

    # 2: For each triplet of states (Ap, Aq, Ar), add rule Apr -> ApqAqr
    cfg2 = CFG()
    for p in pda.states:
        for q in pda.states:
            for r in pda.states:
                rule = Rule()
                rule.lhs = wrap + 'A' + substart + p.name + r.name + subend + wrap
                rule.rhs = wrap + 'A' + substart + p.name + q.name + subend
                rule.rhs += 'A' + substart + q.name + r.name + subend + wrap
                cfg2.rules.add(rule)

    print('type 2 rules:\n' + str(cfg2))

    # 3: For each matching push/pop pair ((p, a, ε -> (r, u)), (s, b, u -> (q, ε)),
    #      Add rule Apq -> a Ars b
    cfg3 = CFG()
    for x in pda.delta:
        if x.push != 'ε':
            for y in pda.delta:
                if x.push == y.pop:
                    rule = Rule()
                    rule.lhs = wrap + 'A' + substart + x.src.name + y.dest.name + subend + wrap
                    rule.rhs = wrap + x.read + 'A' + substart + x.dest.name + y.src.name + subend + y.read + wrap
                    rule.rhs = rule.rhs.replace('ε', '', 2)
                    cfg3.rules.add(rule)

    print('type 3 rules:\n' + str(cfg3))

    cfg.rules = cfg.rules.union(cfg1.rules, cfg2.rules, cfg3.rules)

    return cfg
