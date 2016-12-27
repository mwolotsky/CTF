from Crypto.Random import random as srandom
import argparse
import hashlib

class Graph:
    def __init__(self, n, edges):
        self.edges = edges
        self.n = n

def generate_proof(outstream, graph, color, rounds):
    rnd = srandom
    hash_func = hashlib.sha1
    h = hash_func()

    def emit(s):
        h.update(s)
        outstream.write(s)

    def rand():
        return int(h.hexdigest(), 16)

    def encode_int(num):
        return str(num).rjust(10, '0').encode('ascii') + b'\n'

    def subtree_hash(leafs, i, j):
        if i == j:
            return leafs[i]
        mid = (i + j) // 2
        res = hash_func(subtree_hash(leafs, i, mid) + subtree_hash(leafs, mid + 1, j)).digest()
        return res

    def commit(values):
        ''' Generate a merkle tree over v_i + r_i with randomly chosen r_i. '''
        r = [rnd.getrandbits(128).to_bytes(16, byteorder='big') for v in values]
        values = [v + r for v, r in zip(values, r)]
        leafs = [hash_func(v).digest() for v in values]
        commitment = subtree_hash(leafs, 0, len(leafs)-1)
        return r, commitment

    def reveal(values, randoms, index):
        leafs = [hash_func(v + r).digest() for v, r in zip(values, randoms)]

        emit(values[index])
        emit(randoms[index])

        def dfs(i, j):
            if i == j: return
            mid = (i + j) // 2
            if index <= mid:
                sibling_hash = subtree_hash(leafs, mid + 1, j)
                emit(sibling_hash)
                dfs(i, mid)
            else:
                sibling_hash = subtree_hash(leafs, i, mid)
                emit(sibling_hash)
                dfs(mid+1, j)
        dfs(0, len(leafs)-1)

    emit(encode_int(rounds))

    randoms = []
    colors = []
    for round in range(rounds):
        print('Commitment for round %d' % round)
        perm = list(range(3))
        rnd.shuffle(perm)
        color_perm = [encode_int(perm[color[x]]) for x in range(1, graph.n+1)]
        r, commitment = commit(color_perm)

        randoms.append(r)
        colors.append(color_perm)

        emit(commitment)

    for round, (r, c) in enumerate(zip(randoms, colors)):
        print('Reveal for round %d' % round)
        challenge = rand() % len(graph.edges)
        x, y = graph.edges[challenge]
        assert c[x-1] != c[y-1]
        reveal(c, r, x-1)
        reveal(c, r, y-1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', required=True, dest='graph_file', help='Graph file')
    parser.add_argument('-c', required=True, dest='color_file', help='Color file')
    parser.add_argument('-p', required=True, dest='proof_file', help='Proof output file (WILL BE OVERWRITTEN)')
    parser.add_argument('-r', type=int, dest='rounds', default=300, help='#Rounds')
    args = parser.parse_args()

    n = 0
    edges = []
    with open(args.graph_file) as f:
        for line in f:
            line = line.strip()
            if line.startswith('#') or not line: continue
            if line.startswith('p'):
                n = int(line.split()[2])
            else:
                assert line.startswith('e')
                x, y = map(int, line.split()[1:])
                assert 1 <= x <= n and 1 <= y <= n
                edges.append((x, y))
    graph = Graph(n, edges)

    color = {}
    with open(args.color_file) as f:
        for line in f:
            line = line.strip()
            if line.startswith('#') or not line: continue
            assert line.startswith('c')
            x, c = map(int, line.split()[1:])
            color[x] = c
            assert c in [0,1,2], "Invalid color: %d" % c
    for x in range(1, graph.n+1):
        assert x in color, "Node %d does not have a color" % x

    print('Generating proof...')
    with open(args.proof_file, 'wb') as f:
        generate_proof(f, graph, color, rounds=args.rounds)
