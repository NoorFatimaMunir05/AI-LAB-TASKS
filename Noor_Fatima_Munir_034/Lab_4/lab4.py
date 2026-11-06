from heapq import heappush, heappop

graph={"S":[("A",1),("B",4)],"A":[("C",2)],"B":[("G",5)],"C":[("G",3)],"G":[]}
heuristic={"S":5,"A":4,"B":4,"C":2,"G":0}
true_remaining={"S":6,"A":5,"B":5,"C":3,"G":0}

def search(h):
    pq=[(h["S"],0,"S",["S"])]; best={"S":0}; processed=[]; expanded=0; snapshots=[]
    while pq:
        f,g,node,path=heappop(pq)
        if g!=best[node]: continue
        processed.append((node,g,h[node],f))
        if node=="G": return path,g,processed,expanded,snapshots
        expanded+=1
        for nxt,w in graph[node]:
            new=g+w
            if new<best.get(nxt,float("inf")):
                best[nxt]=new; heappush(pq,(new+h[nxt],new,nxt,path+[nxt]))
        snapshots.append((node,sorted([(n,c,fn) for fn,c,n,p in pq])))
    return None,None,processed,expanded,snapshots

def cost(path):
    return sum(next(w for n,w in graph[a] if n==b) for a,b in zip(path,path[1:]))

print("HEURISTIC AUDIT")
for node,edges in graph.items():
    print(node,"admissible",heuristic[node]<=true_remaining[node])
    for nxt,w in edges:
        print(node,nxt,"consistent",heuristic[node]<=w+heuristic[nxt])
for name,h in [("A STAR",heuristic),("UCS",{x:0 for x in heuristic}),("OVERESTIMATE",{**heuristic,"C":10})]:
    path,value,trace,expanded,frontier=search(h)
    print(name,"path",path,"cost",value,"independent",cost(path),"expanded",expanded)
    print("PROCESSED",trace)
    print("FRONTIER",frontier)
