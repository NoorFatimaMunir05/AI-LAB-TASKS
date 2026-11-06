from math import inf

def minimax(leaves):
    visited=[]
    def visit(start,end,maximizing):
        if end-start==1:
            visited.append(start); return leaves[start]
        mid=(start+end)//2
        a=visit(start,mid,not maximizing)
        b=visit(mid,end,not maximizing)
        return max(a,b) if maximizing else min(a,b)
    return visit(0,len(leaves),True),visited

def alphabeta(leaves):
    visited=[]
    def visit(start,end,maximizing,alpha,beta):
        if end-start==1:
            visited.append(start); return leaves[start]
        mid=(start+end)//2
        value=-inf if maximizing else inf
        for a,b in [(start,mid),(mid,end)]:
            child=visit(a,b,not maximizing,alpha,beta)
            value=max(value,child) if maximizing else min(value,child)
            if maximizing: alpha=max(alpha,value)
            else: beta=min(beta,value)
            if alpha>=beta: break
        return value
    return visit(0,len(leaves),True,-inf,inf),visited

for name,leaves in [("supplied_minimax_padded",[3,5,2,9,0,7,0,0]),("original",[3,5,2,9,3,5,2,9]),("reordered",[9,2,5,3,9,2,5,3]),("all_equal",[4]*8)]:
    a,seen_a=minimax(leaves); b,seen_b=alphabeta(leaves)
    print(name,"leaves",leaves,"minimax",a,"count",len(seen_a),"visited",seen_a,"alpha-beta",b,"count",len(seen_b),"visited",seen_b)
    assert a==b and len(seen_b)<=len(seen_a)
print("MINIMAX HAND TRACE: MAX pairs (3,5)->5, (2,9)->9, (3,5)->5, (2,9)->9; MIN groups 5 and 5; root MAX 5")

print("SUPPLIED TREE: six values [3,5,2,9,0,7], padded with 0 and 0 to a full depth-3 tree")
