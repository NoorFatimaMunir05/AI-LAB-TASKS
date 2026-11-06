from collections import deque
from heapq import heappush, heappop

graph = {"A":["B","C"], "B":["D","E"], "C":["F"], "D":[], "E":["G"], "F":[], "G":[]}

def bfs(g, start, goal):
    queue = deque([(start,[start])]); seen={start}; trace=[]
    while queue:
        node,path=queue.popleft(); trace.append((node,list(path),[x[0] for x in queue]))
        if node==goal: return path,trace
        for nxt in g.get(node,[]):
            if nxt not in seen:
                seen.add(nxt); queue.append((nxt,path+[nxt]))
    return None,trace

def dfs(g,start,goal):
    stack=[(start,[start])]; seen=set(); trace=[]
    while stack:
        node,path=stack.pop()
        if node in seen: continue
        seen.add(node)
        if node==goal:
            trace.append((node,path,[x[0] for x in stack])); return path,trace
        for nxt in reversed(g.get(node,[])):
            if nxt not in seen: stack.append((nxt,path+[nxt]))
        trace.append((node,path,[x[0] for x in stack]))
    return None,trace

def dls(g,start,goal,limit):
    def visit(node,path,depth):
        if node==goal: return "FOUND",path
        children=[x for x in g.get(node,[]) if x not in path]
        if depth==limit: return ("CUTOFF",None) if children else ("FAILURE",None)
        cutoff=False
        for nxt in children:
            status,result=visit(nxt,path+[nxt],depth+1)
            if status=="FOUND": return status,result
            if status=="CUTOFF": cutoff=True
        return ("CUTOFF",None) if cutoff else ("FAILURE",None)
    return visit(start,[start],0)

def iddfs(g,start,goal,max_depth):
    attempts=[]
    for depth in range(max_depth+1):
        status,path=dls(g,start,goal,depth); attempts.append((depth,status))
        if status=="FOUND": return status,path,attempts
        if status=="FAILURE": return status,None,attempts
    return "CUTOFF",None,attempts

def ucs(g,start,goal):
    pq=[(0,start,[start])]; best={start:0}; trace=[]
    while pq:
        cost,node,path=heappop(pq)
        if cost!=best[node]: continue
        trace.append(node)
        if node==goal: return cost,path,trace
        for nxt,weight in g.get(node,[]):
            new=cost+weight
            if new<best.get(nxt,float('inf')):
                best[nxt]=new; heappush(pq,(new,nxt,path+[nxt]))
    return None,None,trace

weighted={"A":[("B",1),("C",6)],"B":[("D",2),("E",1)],"C":[("F",2),("G",6)],"D":[],"E":[("G",1)],"F":[],"G":[]}
print("BFS",bfs(graph,"A","G"))
print("DFS",dfs(graph,"A","G"))
for limit in range(1,5):
    print("DLS",limit,dls(graph,"A","G",limit))
    print("IDDFS",limit,iddfs(graph,"A","G",limit))
print("WEIGHTED EDGES",weighted)
weighted_plain={node:[x for x,_ in edges] for node,edges in weighted.items()}
print("WEIGHTED BFS",bfs(weighted_plain,"A","G"))
print("UCS",ucs(weighted,"A","G"))
print("EDGE start=goal",bfs(graph,"A","A"))
print("EDGE unreachable",dls(graph,"A","Z",4))
cycle={**graph,"F":["A"]}
print("EDGE cycle",bfs(cycle,"A","G"))
