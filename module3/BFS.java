package module3;

import java.util.*;

public class BFS {

    public void findShortestPath(Graph graph, int start, int end) {

        int vertices = graph.getVertices();

        if (start < 0 || start >= vertices || end < 0 || end >= vertices) {
            System.out.println("\nInvalid node! Valid range: 0 to " + (vertices - 1));
            return;
        }

        boolean[] visited = new boolean[vertices];
        int[] parent = new int[vertices];
        int[] level = new int[vertices];
        Arrays.fill(parent, -1);
        Arrays.fill(level, -1);

        Queue<Integer> queue = new LinkedList<>();
        visited[start] = true;
        level[start] = 0;
        queue.add(start);

        System.out.println("\n=========== BFS SHORTEST PATH (Unweighted) ===========");
        System.out.println("Exploring nodes level by level (Queue):");
        System.out.println("  Level 0: " + start);

        // Track levels for display
        int currentLevel = 0;
        StringBuilder levelNodes = new StringBuilder("  Level ");

        boolean found = false;

        while (!queue.isEmpty()) {
            int current = queue.poll();

            if (current == end) { found = true; }

            for (int neighbor : graph.getAdjList()[current]) {
                if (!visited[neighbor]) {
                    visited[neighbor] = true;
                    parent[neighbor] = current;
                    level[neighbor] = level[current] + 1;
                    queue.add(neighbor);

                    // Print level information
                    if (level[neighbor] > currentLevel) {
                        currentLevel = level[neighbor];
                        if (levelNodes.length() > 10) {
                            System.out.println(levelNodes + "]");
                        }
                        levelNodes = new StringBuilder("  Level " + currentLevel + ": [");
                    } else {
                        levelNodes.append(", ");
                    }
                    levelNodes.append(neighbor);
                }
            }
        }
        if (levelNodes.length() > 10) {
            System.out.println(levelNodes + "]");
        }

        System.out.println();

        if (found) {
            LinkedList<Integer> path = new LinkedList<>();
            int cur = end;
            while (cur != -1) { path.addFirst(cur); cur = parent[cur]; }

            System.out.print("  Shortest path by fewest roads:\n    ");
            for (int i = 0; i < path.size(); i++) {
                System.out.print(path.get(i));
                if (i < path.size() - 1) System.out.print(" → ");
            }
            System.out.println("\n\n  Number of road segments: " + (path.size() - 1));
            System.out.println("  Type: UNWEIGHTED graph (all roads equal)");
            System.out.println("  Logic: First time BFS reaches a node = shortest path in hops.");
        } else {
            System.out.println("  No path exists from Node " + start + " to Node " + end + "!");
            System.out.println("  These zones are NOT connected — city needs new roads!");
        }
        System.out.println("====================================================");
    }

    public void traverse(Graph graph, int start) {

        int vertices = graph.getVertices();

        if (start < 0 || start >= vertices) {
            System.out.println("\nInvalid start node!");
            return;
        }

        boolean[] visited = new boolean[vertices];
        Queue<Integer> queue = new LinkedList<>();
        visited[start] = true;
        queue.add(start);

        System.out.println("\nBFS Traversal from Node " + start + ":");
        while (!queue.isEmpty()) {
            int current = queue.poll();
            System.out.print(current + " ");
            for (int neighbor : graph.getAdjList()[current]) {
                if (!visited[neighbor]) {
                    visited[neighbor] = true;
                    queue.add(neighbor);
                }
            }
        }
        System.out.println();

        int visitedCount = 0;
        for (boolean v : visited) if (v) visitedCount++;

        if (visitedCount == vertices) {
            System.out.println("  City FULLY CONNECTED \u2014 all " + vertices + " zones reachable from Node " + start + ".");
        } else {
            System.out.print("  WARNING: Only " + visitedCount + "/" + vertices + " zones reachable. Unreachable: ");
            for (int i = 0; i < vertices; i++) {
                if (!visited[i]) System.out.print("Node " + i + "  ");
            }
            System.out.println();
        }
    }
}
