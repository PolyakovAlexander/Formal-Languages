from collections import defaultdict


class GSS:

    def __init__(self, node):
        # every node is a dict: node -> set((node, label))
        self.nodes = defaultdict(set)
        self.nodes[node] = set()

    def add_node(self, src, dst, label):

        if src in self.nodes:
            self.nodes[src].add((dst, label))
        else:
            self.nodes[src] = {(dst, label)}


class GLL:

    # rfa - grammar, fsm - automaton
    def __init__(self, rfa, fsm, automaton_size):

        self.rfa = rfa
        self.fsm = fsm
        self.automaton_size = automaton_size
        self.gss = None

        # popped gss nodes' set
        self.popped = set()

        # working list of configurations
        self.working_list = set()

        # set of already used nodes
        self.history = set()

        # dict gss.node -> set of input positions where node was popped
        self.popped_info = defaultdict(set)

        # set of result tuples (i, non_term, j)
        self.result = set()

    def add_new_conf(self, conf):
        self.working_list.add(conf)

    def pop_node(self, gss_node, input_pos):

        node_labels = self.gss.nodes[gss_node]
        self.popped_info[gss_node].add(input_pos)

        for node, label in node_labels:
            for automaton_pos in self.popped_info[gss_node]:
                self.add_new_conf(
                    (
                        automaton_pos,
                        label,
                        node
                    )
                )

        self.result.add((gss_node[0], gss_node[1], input_pos))
        self.popped.add(gss_node)

    # add configuration from already popped node
    def back_pop(self, cur_node, popped_node, label):

        for automaton_pos in self.popped_info[popped_node]:
            self.add_new_conf(
                (
                    automaton_pos,
                    label,
                    cur_node
                )
            )

    # case of terminals
    def term_case(self, cur_conf, graph_out_egdes, gram_out_edges):

        automaton_pos, gram_pos, cur_gss_node = cur_conf

        for auto_dst, auto_label in graph_out_egdes:
            for gram_dst, gram_label in gram_out_edges:
                if auto_label == gram_label:
                    self.add_new_conf((
                        auto_dst,
                        gram_dst,
                        cur_gss_node
                    ))

    # case of non-terminal
    def non_term_case(self, cur_conf, gram_out_edges):

        automaton_pos, gram_pos, cur_gss_node = cur_conf

        for gram_dst, gram_label in gram_out_edges:
            for start_pos, start_nonterm in self.rfa.starts.items():
                if gram_label == start_nonterm:
                    new_gss_node = (automaton_pos, gram_label)

                    if new_gss_node in self.popped:
                        self.back_pop(cur_gss_node, new_gss_node, gram_dst)

                    self.add_new_conf((
                            automaton_pos,
                            start_pos,
                            new_gss_node
                        ))

                    self.gss.add_node(new_gss_node, cur_gss_node, gram_dst)

    # case of final non-terminal
    def final_nonterm_case(self, cur_conf):

        automaton_pos, gram_pos, cur_gss_node = cur_conf

        if gram_pos in self.rfa.finals.keys():
            self.pop_node(cur_gss_node, automaton_pos)
            self.popped.add(cur_gss_node)
            self.popped_info[cur_gss_node].add(automaton_pos)

    def next(self, cur_conf):

        automaton_pos, gram_pos, cur_gss_node = cur_conf

        graph_out_edges = self.fsm[automaton_pos]

        gram_out_edges = [(dst, label) for src, dst, label in self.rfa.edges if src == gram_pos]

        self.term_case(cur_conf, graph_out_edges, gram_out_edges)

        self.non_term_case(cur_conf, gram_out_edges)

        self.final_nonterm_case(cur_conf)

    def main(self):

        n = self.automaton_size
        start_states = self.rfa.starts.items()

        for automaton_pos in range(n):
            for start_state, label in start_states:
                self.gss = GSS((automaton_pos, label))
                self.working_list = {(automaton_pos, start_state, (automaton_pos, label))}
                self.history = set()
                self.popped = set()
                self.popped_info = defaultdict(set)

                while self.working_list:
                    cur_conf = self.working_list.pop()
                    if cur_conf in self.history:
                        continue
                    self.history.add(cur_conf)
                    self.next(cur_conf)

        return self.result


