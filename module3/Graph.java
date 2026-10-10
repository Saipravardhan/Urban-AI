package module3;

import data.CityData;
import model.TrafficRecord;

import java.util.*;

public class Graph {

    private int vertices;
    private LinkedList<Integer>[] adjList;

    @SuppressWarnings("unchecked")
    public Graph(int vertices) {

        this.vertices = vertices;
        adjList = (LinkedList<Integer>[]) new LinkedList<?>[vertices];

        for(int i = 0; i < vertices; i++) {
            adjList[i] = new LinkedList<>();
        }
    }

    public void addEdge(int source, int destination) {
        adjList[source].add(destination);
        adjList[destination].add(source);
    }

    public LinkedList<Integer>[] getAdjList() { return adjList; }
    public int getVertices() { return vertices; }

    /** Builds the road network graph from the in-memory road data. */
    public static Graph buildFromRoads() {

        System.out.println("\nBuilding road network...");

        CityData store = CityData.getInstance();
        List<TrafficRecord> roads = store.getAllRoads();

        Graph graph = new Graph(store.getMaxNode() + 1);

        for (TrafficRecord r : roads) {
            graph.addEdge(r.getSourceNode(), r.getDestNode());
        }

        System.out.println("Road network loaded: " + graph.getVertices()
            + " nodes, " + roads.size() + " roads.");
        return graph;
    }
}
