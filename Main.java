import data.CityData;

import module1.AssetManager;

import module2.TrafficManager;

import module3.Graph;
import module3.BFS;
import module3.DFS;

import module4.Dijkstra;
import module4.FloydWarshall;

import module6.ActivitySelection;
import module6.FractionalKnapsack;
import module6.Knapsack01;

import java.util.Scanner;

public class Main {

    private static Scanner sc;

    // ---------- Safe input helpers (never crash on bad input) ----------

    private static int readInt(String prompt) {
        while (true) {
            System.out.print(prompt);
            String line = sc.nextLine().trim();
            try {
                return Integer.parseInt(line);
            } catch (NumberFormatException e) {
                System.out.println("Invalid input - please enter a whole number.");
            }
        }
    }

    private static double readDouble(String prompt) {
        while (true) {
            System.out.print(prompt);
            String line = sc.nextLine().trim();
            try {
                return Double.parseDouble(line);
            } catch (NumberFormatException e) {
                System.out.println("Invalid input - please enter a number.");
            }
        }
    }

    private static String readText(String prompt) {
        while (true) {
            System.out.print(prompt);
            String line = sc.nextLine().trim();
            if (!line.isEmpty()) {
                return line;
            }
            System.out.println("This field cannot be empty.");
        }
    }

    private static boolean hasRoads() {
        if (CityData.getInstance().getAllRoads().isEmpty()) {
            System.out.println("\nNo roads in the network. Add roads first (option 4).");
            return false;
        }
        return true;
    }

    public static void main(String[] args) {

        try (Scanner scanner = new Scanner(System.in)) {

            sc = scanner;

            AssetManager assetManager = new AssetManager();
            TrafficManager trafficManager = new TrafficManager();

            while (true) {

                System.out.println("\n=================================================");
                System.out.println("      URBANAI SMART CITY OPTIMIZATION PLATFORM");
                System.out.println("=================================================");

                System.out.println("\n  Trees & Asset Management");
                System.out.println("1. Add Asset");
                System.out.println("2. Search Asset");
                System.out.println("3. Display Assets");

                System.out.println("\n  Road Network Management");
                System.out.println("4. Add Road (Insert into Graph)");
                System.out.println("5. Check Traffic Density");
                System.out.println("6. Cumulative Traffic Statistics");
                System.out.println("7. Display Road Network");

                System.out.println("\n  Graph Algorithms");
                System.out.println("8. BFS — Shortest Path (Fewest Roads)");
                System.out.println("9. DFS — Connectivity Check");

                System.out.println("\n  Shortest Path Optimization");
                System.out.println("10. Dijkstra — Traffic-Aware Shortest Path");
                System.out.println("11. Floyd-Warshall — All-Pairs Distance Matrix");

                System.out.println("\n  Greedy & Dynamic Programming");
                System.out.println("12. Schedule Maintenance Tasks (Activity Selection)");
                System.out.println("13. Allocate City Resources (Fractional Knapsack)");
                System.out.println("14. Select Projects Within Budget (0/1 Knapsack)");

                System.out.println("\n0. Exit");

                int choice = readInt("\nEnter Choice : ");

                switch (choice) {

                    // ========== MODULE 1: ASSET MANAGEMENT ==========
                    case 1: {
                        int assetId = readInt("Enter Asset ID : ");
                        String assetName = readText("Enter Asset Name : ");
                        String location = readText("Enter Location : ");
                        String type = readText("Enter Asset Type : ");

                        assetManager.addAsset(assetId, assetName, location, type);
                        break;
                    }

                    case 2: {
                        int searchId = readInt("Enter Asset ID : ");
                        assetManager.searchAsset(searchId);
                        break;
                    }

                    case 3:
                        assetManager.displayAssets();
                        break;

                    // ========== MODULE 2: ROAD NETWORK ==========
                    case 4: {
                        int roadId = readInt("Enter Road ID (1-" + TrafficManager.MAX_ROAD_ID + ") : ");
                        int sourceNode = readInt("Enter Source Node : ");
                        int destNode = readInt("Enter Destination Node : ");
                        double distanceKm = readDouble("Enter Distance (km) : ");
                        int vehicleCount = readInt("Enter Vehicle Count : ");

                        trafficManager.insertTrafficRecord(
                                roadId, sourceNode, destNode, distanceKm, vehicleCount);
                        break;
                    }

                    case 5: {
                        int densityRoad = readInt("Enter Road ID : ");
                        trafficManager.calculateTrafficDensity(densityRoad);
                        break;
                    }

                    case 6: {
                        int startRoad = readInt("Enter Start Road ID : ");
                        int endRoad = readInt("Enter End Road ID : ");
                        trafficManager.getCumulativeTrafficStatistics(startRoad, endRoad);
                        break;
                    }

                    case 7:
                        trafficManager.displayRecords();
                        break;

                    // ========== MODULE 3: GRAPH ALGORITHMS ==========
                    case 8: {
                        if (!hasRoads()) break;
                        Graph graph = Graph.buildFromRoads();

                        int bfsStart = readInt("Enter Start Node : ");
                        int bfsEnd = readInt("Enter Destination Node : ");

                        new BFS().findShortestPath(graph, bfsStart, bfsEnd);
                        break;
                    }

                    case 9: {
                        if (!hasRoads()) break;
                        Graph dfsGraph = Graph.buildFromRoads();

                        int dfsStart = readInt("Enter Start Node : ");

                        new DFS().traverse(dfsGraph, dfsStart);
                        break;
                    }

                    // ========== MODULE 4: SHORTEST PATH ==========
                    case 10: {
                        if (!hasRoads()) break;

                        int dijStart = readInt("Enter Start Node : ");
                        int dijEnd = readInt("Enter Destination Node : ");

                        new Dijkstra().findEmergencyRoute(dijStart, dijEnd);
                        break;
                    }

                    case 11:
                        new FloydWarshall().generateCityDistanceMatrix();
                        break;

                    // ========== MODULE 6: GREEDY & DP ==========
                    case 12:
                        new ActivitySelection().scheduleMaintenanceTasks();
                        break;

                    case 13:
                        new FractionalKnapsack().allocateResources();
                        break;

                    case 14:
                        new Knapsack01().selectProjects();
                        break;

                    case 0:
                        System.out.println("\nThank You For Using UrbanAI");
                        return;

                    default:
                        System.out.println("\nInvalid Choice");
                }
            }

        } catch (java.util.NoSuchElementException e) {
            // Input stream closed (Ctrl+D / end of piped input)
            System.out.println("\nInput closed. Exiting UrbanAI.");
        }
    }
}
