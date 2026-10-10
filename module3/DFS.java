package module3;

import java.util.*;

public class DFS {

    public void traverse(Graph graph, int start) {

        int vertices = graph.getVertices();

        if (start < 0 || start >= vertices) {
            System.out.println("\nInvalid start node!");
            return;
        }

        boolean[] visited = new boolean[vertices];

        System.out.println("\n=========== DFS TRAVERSAL & CONNECTIVITY ===========");
        System.out.print("  DFS order from Node " + start + ": ");

        dfsUtil(graph, start, visited);
        System.out.println();

        int visitedCount = 0;
        for (boolean v : visited) if (v) visitedCount++;

        if (visitedCount == vertices) {
            System.out.println("  City FULLY CONNECTED \u2014 all " + vertices
                + " zones reachable from Node " + start + ".");
        } else {
            System.out.print("  WARNING: Unreachable zones: ");
            for (int i = 0; i < vertices; i++) {
                if (!visited[i]) System.out.print("Node " + i + "  ");
            }
            System.out.println("\n  \u2192 City needs new roads to connect these zones!");
        }
        System.out.println("====================================================");
    }

    public void findAnyPath(Graph graph, int start, int end) {

        int vertices = graph.getVertices();

        if (start < 0 || start >= vertices || end < 0 || end >= vertices) {
            System.out.println("\nInvalid node! Valid range: 0 to " + (vertices - 1));
            return;
        }

        boolean[] visited = new boolean[vertices];
        int[] parent = new int[vertices];
        Arrays.fill(parent, -1);

        System.out.println("\n=========== DFS PATH FINDING (Unweighted) ===========");
        System.out.println("  Note: DFS finds ANY path \u2014 NOT guaranteed to be shortest!");
        System.out.println("  (Use BFS for shortest, DFS for just connectivity)\n");

        boolean found = dfsPathUtil(graph, start, end, visited, parent);

        if (found) {
            LinkedList<Integer> path = new LinkedList<>();
            int cur = end;
            while (cur != -1) { path.addFirst(cur); cur = parent[cur]; }

            System.out.print("  DFS found path:\n    ");
            for (int i = 0; i < path.size(); i++) {
                System.out.print(path.get(i));
                if (i < path.size() - 1) System.out.print(" \u2192 ");
            }
            System.out.println("\n\n  Number of road segments: " + (path.size() - 1));
            System.out.println("  Type: UNWEIGHTED graph (same as BFS)");
            System.out.println("  Key difference: DFS uses STACK (recursion), BFS uses QUEUE");
            System.out.println("  Result: BFS = SHORTEST path, DFS = ANY path");
        } else {
            System.out.println("  No path exists from Node " + start + " to Node " + end + "!");
        }
        System.out.println("====================================================");
    }

    private boolean dfsPathUtil(Graph graph, int current, int end,
                                 boolean[] visited, int[] parent) {
        visited[current] = true;
        System.out.println("  Visiting Node " + current + (current == end ? " \u2190 DESTINATION!" : ""));

        if (current == end) return true;

        for (int neighbor : graph.getAdjList()[current]) {
            if (!visited[neighbor]) {
                parent[neighbor] = current;
                if (dfsPathUtil(graph, neighbor, end, visited, parent)) {
                    return true;
                }
            }
        }
        return false;
    }

    private void dfsUtil(Graph graph, int vertex, boolean[] visited) {
        visited[vertex] = true;
        System.out.print(vertex + " ");
        for (int neighbor : graph.getAdjList()[vertex]) {
            if (!visited[neighbor]) dfsUtil(graph, neighbor, visited);
        }
    }
}
