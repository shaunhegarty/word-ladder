#This class is copied verbatim from here: http://www.python-course.eu/graphs_python.php
#Only addition is a get_shortest_path method which uses breadth first search figure out the shortest path
import sys
from collections import deque

class Graph(object):

    def __init__(self, graph_dict=None):
        """ initializes a graph object 
            If no dictionary or None is given, 
            an empty dictionary will be used
        """
        if graph_dict == None:
            graph_dict = {}
        self.__graph_dict = graph_dict

    def vertices(self):
        """ returns the vertices of a graph """
        return list(self.__graph_dict.keys())

    def edges(self):
        """ returns the edges of a graph """
        return self.__generate_edges()

    def add_vertex(self, vertex):
        """ If the vertex "vertex" is not in 
            self.__graph_dict, a key "vertex" with an empty
            list as a value is added to the dictionary. 
            Otherwise nothing has to be done. 
        """
        if vertex not in self.__graph_dict:
            self.__graph_dict[vertex] = []

    def add_edge(self, edge):
        """ assumes that edge is of type set, tuple or list; 
            between two vertices can be multiple edges! 
        """
        edge = set(edge)
        (vertex1, vertex2) = tuple(edge)
        if vertex1 in self.__graph_dict:
            self.__graph_dict[vertex1].append(vertex2)
        else:
            self.__graph_dict[vertex1] = [vertex2]

    def __generate_edges(self):
        """ A static method generating the edges of the 
            graph "graph". Edges are represented as sets 
            with one (a loop back to the vertex) or two 
            vertices 
        """
        edges = []
        for vertex in self.__graph_dict:
            for neighbour in self.__graph_dict[vertex]:
                if {neighbour, vertex} not in edges:
                    edges.append({vertex, neighbour})
        return edges

    def __str__(self):
        res = "vertices: "
        for k in self.__graph_dict:
            res += str(k) + " "
        res += "\nedges: "
        for edge in self.__generate_edges():
            res += str(edge) + " "
        return res

    def get_shortest_path(self, start_vertex, end_vertex):        
        vertex_queue = deque([start_vertex])
        marked = []
        parent_graph = {}
        graph = self.__graph_dict #just the stored graph
        while len(vertex_queue) > 0:
            #pop first vertex off the queue
            current = vertex_queue.popleft()
            #if end condition reached
            if current == end_vertex:
                #build the path from the linked list of parents
                path = [current]
                while parent_graph[current] != start_vertex:
                    current = parent_graph[current]
                    path = [current] + path
                path = [start_vertex] + path
                return path
            
            for node in graph[current]:
                if node not in marked:
                    parent_graph[node] = current
                    marked.append(node)
                    vertex_queue.append(node)

        return None

    def get_shortest_paths(self, start_vertex, end_vertex): 
        vertex_queue = deque([[start_vertex]])
        marked = [] #list of marked vertices

        paths = [] #store all the paths
        graph = self.__graph_dict #just the stored graph

        pathlen = -1

        while len(vertex_queue) > 0:
            #pop first vertex off the queue
            
            current = vertex_queue.popleft()

            #if end condition reached
            if current[0] == end_vertex:
                #build the path list up
                if pathlen == -1:
                    pathlen = len(current)
                    paths += [current]
                elif len(current) < pathlen:
                    pathlen = len(current)
                    paths = [current]
                elif len(current) == pathlen:
                    paths += [current]
            
            for node in graph[current[0]]:
                if node not in marked: 
                    #Don't mark the target vertex or it'll quit after the first valid path                   
                    if node != end_vertex:
                        marked.append(node)
                    vertex_queue.append([node] + current)

        return paths

    def find_path(self, start_vertex, end_vertex, path=None):
        """ find a path from start_vertex to end_vertex 
            in graph """
        #if path is null initialise empty array
        if path == None:
            path = []
        #graph is map of nodes    
        graph = self.__graph_dict
        #add current vertex to path
        path = path + [start_vertex]

        #if end of path reached, return
        if start_vertex == end_vertex:
            return path
        #if vertex invalid, quit
        if start_vertex not in graph:
            return None
        #for each vertex connected to the current vertex
        for vertex in graph[start_vertex]:
            #if vertex not yet visited
            if vertex not in path:
                #recursively follow the path
                extended_path = self.find_path(vertex, 
                                               end_vertex, 
                                               path)
                if extended_path: #if not null?
                    return extended_path
        return None

    def find_all_paths(self, start_vertex, end_vertex, path=[]):
        """ find all paths from start_vertex to 
            end_vertex in graph """
        #graph is map of nodes
        graph = self.__graph_dict
        #add current vertex to path
        path = path + [start_vertex]
        #return path when destination reached
        if start_vertex == end_vertex:
            return [path]
        #return empty if starting vertex invalid
        if start_vertex not in graph:
            return []
        #array of paths
        paths = []

        #for each vertex connected to the current vertex
        count = 0
        totalVerts = len(graph)
        for vertex in graph[start_vertex]:
            print "/r starting with " + vertex
            #go to next vertex if it's not part of the path
            if vertex not in path:
                #recursively follow through until the end is reached
                extended_paths = self.find_all_paths(vertex, 
                                                     end_vertex, 
                                                     path)
                #find each path
                for p in extended_paths: 
                    paths.append(p)
        return paths

