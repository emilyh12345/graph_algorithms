# CSCI 220/620
# Summer 2022
# Assignment 6-Graphs and Graph Algorithms
# Emily Haller
import matplotlib.pyplot as plt
import texttable as tt


def read_graph(file_name):
    with open(file_name) as file:
        a = []
        for line in file.readlines():
            s = line.split(" ")
            row = []
            for num in s:
                row.append(int(num))
            a.append(row)
        return a #adjacency matrix


def print_adj_matrix(a):
    print("   ", end="")
    for j in range(len(a)):
        print(str(j) + "  ", end="")
    print()
    for i in range(len(a)):
        row = a[i]
        print(str(i) + ": ", end="")
        for col in row:
            print(str(col) + " ", end=" ")
        print()
    print()


def convert_to_adj_table(a):
    t = []
    for row in a:
        l = [] #list
        for j in range(len(row)):
            if row[j] == 1:
                l.append(j)
        t.append(l)
    return t


def print_adj_table(t):
    for i in range(len(t)):
        l = t[i]
        print(str(i) + ": ", end="")
        for v in l:  #v for vertex
            print(str(v) + " ", end=" ")
        print()
    print()


# from https://www.geeksforgeeks.org/check-star-graph/
def check_star(a):
    global size
    size = len(a)
    vertex_d1 = 0
    vertex_dn_1 = 0
    if size == 1:
        return a[0][0] == 0
    if size == 2:
        return a[0][0] == 0 and a[0][1] == 1 and a[1][0] == 1 and a[1][1] == 0
    for i in range(0, size):
        degree_i = 0
        for j in range(0, size):
            if a[i][j]:
                degree_i = degree_i + 1
        if degree_i == 1:
            vertex_d1 = vertex_d1 + 1
        elif degree_i == size - 1:
            vertex_dn_1 = vertex_dn_1 + 1
    return vertex_d1 == (size - 1) and vertex_dn_1 == 1


def print_graph_info(a):
    is_symmetric = True
    vertices = len(a)
    edges = 0
    headers = ["Vertex", "In-degree", "Out-degree", "Neighbors"]
    data = []
    data.append(headers)
    for i in range(len(a)):
        data_row = []
        data_row.append(i)
        indegree = 0
        for k in range(len(a)):
            if a[k][i] == 1:
                indegree += 1
        data_row.append(indegree)
        row = a[i]
        outdegree = 0
        neighbours = ""
        for j in range(len(row)):
            if row[j] == 1:
                outdegree += 1
                edges += 1
                neighbours += str(j) + " "
        is_symmetric = is_symmetric and indegree == outdegree
        data_row.append(outdegree)
        data_row.append(neighbours)
        data.append(data_row)
    # from https://www.geeksforgeeks.org/texttable-module-in-python/
    tbl = tt.Texttable(100)
    tbl.set_cols_align(["l", "r", "r", "l"])
    tbl.add_rows(data, header=True)
    if is_symmetric:
        edges //= 2
    print(tbl.draw())
    has_euler_circuit = is_symmetric
    for j in range(1, len(data)):
        has_euler_circuit = has_euler_circuit and data[j][2] % 2 == 0 # all even degrees
    print("Vertices:", vertices, "Edges:", edges)
    print("Symmetric:", is_symmetric)
    print("Eulerian Circuit:", has_euler_circuit)
    # check if graph is complete
    is_complete = True
    for n in range(len(a)):
        for m in range(len(a)):
            if n != m and a[n][m] == 0:  #all but diagonal have 1s in complete graph
                is_complete = False
            if n == m and a[n][m] == 1:  #check that the diagonal has no self loops
                is_complete = False
    print("is the graph complete?", is_complete)


def plot_times(dict_sorts, sorts, trials, sizes):
    sort_num = 0
    plt.xticks([j for j in range(len(sizes))], [str(size) for size in sizes]) #create x axis
    for sort_alg in sorts:
        sort_num += 1 #iterate over the sorts
        d = dict_sorts[sort_alg.__name__] #get current dictionary
        x_axis = [j + .05 * sort_num for j in range(len(sizes))]
        y_axis = [d[i] for i in sizes]
        plt. bar(x_axis, y_axis, width=.05, alpha=.75, label=sort_alg.__name__)
    plt.legend()
    plt.title("Runtime of Sorting Algorithms")
    plt.xlabel("Number of Elements")
    plt.ylabel("Time for " + str(trials) + " trials (ms)")
    plt.savefig("Assignment5.png")
    plt.show()


def main():
    files = ["Graph1.txt", "Graph2.txt", "Graph3.txt", "Graph4.txt", "Graph5.txt"]
    for file in files:
        a = read_graph(file)
        t = convert_to_adj_table(a)
        print(file)
        print_adj_matrix(a)
        print_adj_table(t)
        print_graph_info(a)
        print("is it a star?: ", check_star(a))
        print()


if __name__ == "__main__":
    main()