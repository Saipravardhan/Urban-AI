package module4;

import data.CityData;
import model.TrafficRecord;

import java.util.*;

public class FloydWarshall {

    private static final int INF = 99999;

    public void generateCityDistanceMatrix() {

        System.out.println("\n==============================================");
        System.out.println("   ALL-PAIRS SHORTEST PATH (Floyd-Warshall)");
        System.out.println("==============================================");

        try {
            CityData store = CityData.getInstance();
            List<TrafficRecord> records = store.getAllRoads();

            if (records.isEmpty()) {
                System.out.println("\nNo roads in the network. Add roads first (option 4).");
                return;
            }

            int V = store.getMaxNode() + 1;

            int[][] dist = new int[V][V];
            for (int i = 0; i < V; i++) {
                Arrays.fill(dist[i], INF);
                dist[i][i] = 0;
            }

            for (TrafficRecord r : records) {
                int src = r.getSourceNode();
                int dest = r.getDestNode();
                int d = Math.max(1, (int) Math.round(r.getDistanceKm()));
                if (d < dist[src][dest]) {
                    dist[src][dest] = d;
                    dist[dest][src] = d;
                }
            }

            String[] nodeNames = new String[V];
            for (int i = 0; i < V; i++) nodeNames[i] = "N" + i;
            if (V > 0) nodeNames[0] = "HQ";
            if (V > 1) nodeNames[1] = "A";
            if (V > 2) nodeNames[2] = "B";
            if (V > 3) nodeNames[3] = "C";
            if (V > 4) nodeNames[4] = "D";
            if (V > 5) nodeNames[5] = "E";

            System.out.println("\nInitial matrix (" + V + "\u00D7" + V + "):");
            printMatrix(dist, V, nodeNames, "\u221E");

            System.out.println("\nComputing shortest paths (k = 0 to " + (V-1) + ")...");
            for (int k = 0; k < V; k++)
                for (int i = 0; i < V; i++)
                    for (int j = 0; j < V; j++)
                        if (dist[i][k] + dist[k][j] < dist[i][j])
                            dist[i][j] = dist[i][k] + dist[k][j];

            System.out.println("\n======== FINAL CITY DISTANCE MATRIX ========");
            printMatrix(dist, V, nodeNames, "\u221E");

            System.out.println("\nUseful routes:");
            for (int i = 0; i < V; i++)
                for (int j = i + 1; j < V; j++)
                    if (dist[i][j] != INF)
                        System.out.println("  " + nodeNames[i] + " \u2192 " + nodeNames[j]
                            + " : " + dist[i][j] + " km");

            System.out.println("\n==============================================");

        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
            e.printStackTrace();
        }
    }

    private void printMatrix(int[][] m, int V, String[] labels, String inf) {
        System.out.print("     ");
        for (int j = 0; j < V; j++) System.out.printf("%-5s", labels[j]);
        System.out.println();
        for (int i = 0; i < V; i++) {
            System.out.printf("%-4s ", labels[i]);
            for (int j = 0; j < V; j++)
                System.out.printf("%-5s", m[i][j] == INF ? inf : String.valueOf(m[i][j]));
            System.out.println();
        }
    }
}
