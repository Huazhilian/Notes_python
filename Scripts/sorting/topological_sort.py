def topological_sort(vertice,edges):
    if len(vertice) > 0:
        for v in vertice:
            if v not in [edges[i][1] for i in range(len(edges))]:
                arr.append(v)
                vertice.remove(v)
                edges = [(i,j) for i,j in edges if i != v and j != v]
                break
        topological_sort(vertice,edges)

if __name__ == "__main__":
    vertice = ['A', 'B', 'C', 'D', 'E']
    edges = [('C', 'B'), ('A', 'E'), ('B', 'D'), ('B', 'A'), ('C', 'A'), ('A', 'D')]
    arr=[]
    topological_sort(vertice, edges)
    print(arr)
        