import random
 
class BFTNode:
    def __init__(self, nid, faulty=False, f=1):
        self.id=nid; self.faulty=faulty; self.f=f
        self.value=None; self.prepared={}; self.committed={}
 
    def propose(self, v): return v if not self.faulty else random.randint(0,100)
 
    def prepare_phase(self, proposed_values, n):
        counts={}
        for v in proposed_values: counts[v]=counts.get(v,0)+1
        for v,c in counts.items():
            if c >= n-self.f: return v
        return None
 
    def commit_phase(self, prep_value, prepare_msgs, n):
        if prepare_msgs.count(prep_value) >= n-self.f: return prep_value
        return None
 
def simulate_pbft(n_nodes=4, f=1, true_value=42):
    nodes=[BFTNode(i, faulty=(i<f)) for i in range(n_nodes)]
    proposed=[nd.propose(true_value) for nd in nodes]
    print(f"Proposed values: {proposed}")
    prep_results=[nodes[0].prepare_phase(proposed, n_nodes) for _ in nodes]
    valid_prep=[p for p in prep_results if p is not None]
    consensus=nodes[0].commit_phase(true_value, valid_prep, n_nodes)
    print(f"Consensus reached: {consensus}")
    print(f"Correct: {consensus==true_value}")
    return consensus
 
simulate_pbft(n_nodes=4, f=1)
