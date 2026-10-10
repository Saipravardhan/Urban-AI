package module4;

import data.CityData;
import model.TrafficRecord;

import java.util.*;

public class Dijkstra {

    private static final int INF = 99999;

    public void findEmergencyRoute(int startNode, int destNode) {

        System.out.println("\n==============================================");
        System.out.println("   TRAFFIC-AWARE SHORTEST PATH (Dijkstra)");
        System.out.println("==============================================");

        try {
            CityData store = CityData.getInstance();
            List<TrafficRecord> records = store.getAllRoads();

            if (records.isEmpty()) {
                System.out.println("\nNo roads in the network. Add roads first (option 4).");
                return;
            }

            int V = store.getMaxNode() + 1;

            int[][] graph = new int[V][V];

            ArrayList<int[]> roadList = new ArrayList<>();

            for (TrafficRecord r : records) {
                int roadId = r.getRoadId();
                int src = r.getSourceNode();
                int dest = r.getDestNode();
                // distance must stay > 0 because 0 means "no road" in the matrix
                int dist = Math.max(1, (int) Math.round(r.getDistanceKm()));
                int vehicles = r.getVehicleCount();
                graph[src][dest] = dist;
                graph[dest][src] = dist;
                roadList.add(new int[]{roadId, src, dest, dist, vehicles});
            }

            String[] nodeNames = new String[V];
            for (int i = 0; i < V; i++) nodeNames[i] = "Node " + i;
            if (V > 0) nodeNames[0] = "HQ";
            if (V > 1) nodeNames[1] = "Zone A";
            if (V > 2) nodeNames[2] = "Zone B";
            if (V > 3) nodeNames[3] = "Zone C";
            if (V > 4) nodeNames[4] = "Zone D";
            if (V > 5) nodeNames[5] = "Zone E";

            int[][] adjustedGraph = new int[V][V];
            for (int i = 0; i < V; i++)
                for (int j = 0; j < V; j++)
                    adjustedGraph[i][j] = graph[i][j];

            System.out.println("\n[STEP 1] Loaded " + roadList.size() + " roads, " + V + " nodes.");
            System.out.println("\n[STEP 2] Applying traffic penalties:");
            System.out.println("Road\tRoute\t\tBase\tTraffic\tPenalty\tAdjusted");

            for (int[] road : roadList) {
                int roadId = road[0], src = road[1], dest = road[2];
                int baseDist = road[3], vehicles = road[4];

                double penalty = 1.0;
                String density;
                if (vehicles > 1000) { penalty = 2.0; density = "HIGH"; }
                else if (vehicles > 500) { penalty = 1.5; density = "MEDIUM"; }
                else { penalty = 1.0; density = "LOW"; }

                int adjustedDist = (int) Math.round(baseDist * penalty);
                adjustedGraph[src][dest] = adjustedDist;
                adjustedGraph[dest][src] = adjustedDist;

                String marker = (penalty > 1.0) ? " \u26A0" : " \u2713";
                System.out.println(roadId + "\t" + nodeNames[src] + "\u2013" + nodeNames[dest]
                    + "\t" + baseDist + " km\t" + vehicles + " (" + density + ")"
                    + "\t" + penalty + "x\t" + adjustedDist + " km" + marker);
            }

            if (startNode < 0 || startNode >= V || destNode < 0 || destNode >= V) {
                System.out.println("\nInvalid node! Valid range: 0 to " + (V - 1));
                return;
            }

            System.out.println("\n[STEP 3] Computing path from "
                + nodeNames[startNode] + " to " + nodeNames[destNode] + "...");
            System.out.println("  (Priority Queue picks unvisited node with smallest distance)\n");

            int[] dist = new int[V];
            boolean[] visited = new boolean[V];
            int[] parent = new int[V];
            Arrays.fill(dist, INF);
            Arrays.fill(parent, -1);
            dist[startNode] = 0;

            for (int count = 0; count < V - 1; count++) {
                int u = minDistance(dist, visited);
                if (u == -1) break;
                visited[u] = true;

                System.out.println("  Iteration " + (count + 1) + ": Visit "
                    + nodeNames[u] + " (dist=" + dist[u] + " km)"
                    + (u == destNode ? " \u2190 DESTINATION REACHED!" : ""));

                boolean relaxed = false;
                for (int v = 0; v < V; v++) {
                    if (!visited[v] && adjustedGraph[u][v] != 0
                            && dist[u] != INF
                            && dist[u] + adjustedGraph[u][v] < dist[v]) {
                        int oldDist = dist[v];
                        dist[v] = dist[u] + adjustedGraph[u][v];
                        parent[v] = u;
                        System.out.println("    Relax: " + nodeNames[v] + " : "
                            + (oldDist == INF ? "\u221E" : oldDist) + " \u2192 " + dist[v] + " km"
                            + " (via " + nodeNames[u] + ")");
                        relaxed = true;
                    }
                }
                if (!relaxed) System.out.println("    No neighbors to relax.");

                if (u == destNode) break; // early exit if destination reached
            }

            // Show final distances to ALL nodes
            System.out.println("\n  Distances found from " + nodeNames[startNode] + " (search stops once destination is reached):");
            for (int i = 0; i < V; i++) {
                String distStr = (dist[i] == INF) ? "not reached" : dist[i] + " km";
                System.out.println("    " + nodeNames[i] + " (" + i + "): " + distStr);
            }

            // ========= RUN ORIGINAL DIJKSTRA FOR COMPARISON =========
            int[] origDist = new int[V];
            boolean[] origVisited = new boolean[V];
            int[] origParent = new int[V];
            Arrays.fill(origDist, INF);
            Arrays.fill(origParent, -1);
            origDist[startNode] = 0;

            for (int count = 0; count < V - 1; count++) {
                int u = minDistance(origDist, origVisited);
                if (u == -1) break;
                origVisited[u] = true;
                for (int v = 0; v < V; v++) {
                    if (!origVisited[v] && graph[u][v] != 0
                            && origDist[u] != INF
                            && origDist[u] + graph[u][v] < origDist[v]) {
                        origDist[v] = origDist[u] + graph[u][v];
                        origParent[v] = u;
                    }
                }
            }

            System.out.println("\n=============== RESULTS ===============");

            if (dist[destNode] == INF) {
                System.out.println("No path exists from " + nodeNames[startNode]
                    + " to " + nodeNames[destNode] + "!");
            } else {
                System.out.print("  Traffic-Aware Route: ");
                printPath(parent, destNode, nodeNames);
                System.out.println("  Distance (with traffic): " + dist[destNode] + " km\n");

                System.out.print("  Original Route (no traffic): ");
                printPath(origParent, destNode, nodeNames);
                System.out.println("  Distance (no traffic): " + origDist[destNode] + " km");

                int diff = dist[destNode] - origDist[destNode];
                if (diff > 0)
                    System.out.println("\n  Traffic delay: +" + diff + " km (congestion)");
                else if (diff == 0)
                    System.out.println("\n  No delay - traffic did not affect this route.");
            }
            System.out.println("==============================================");


        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
            e.printStackTrace();
        }
    }

    private void printPath(int[] parent, int dest, String[] nodeNames) {
        LinkedList<Integer> path = new LinkedList<>();
        int cur = dest;
        while (cur != -1) { path.addFirst(cur); cur = parent[cur]; }
        for (int i = 0; i < path.size(); i++) {
            System.out.print(nodeNames[path.get(i)] + " (" + path.get(i) + ")");
            if (i < path.size() - 1) System.out.print(" \u2192 ");
        }
        System.out.println();
    }

    private int minDistance(int[] distance, boolean[] visited) {
        int min = INF, index = -1;
        for (int i = 0; i < distance.length; i++) {
            if (!visited[i] && distance[i] < min) {
                min = distance[i]; index = i;
            }
        }
        return index;
    }
}
