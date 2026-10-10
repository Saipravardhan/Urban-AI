package module6;

public class Knapsack01 {

    public void selectProjects() {

        int[] cost = {5, 3, 2, 4};
        int[] value = {10, 6, 4, 8};
        String[] projects = {"Road Expansion", "Bridge Repair", "Park Upgrade", "Drainage Fix"};
        int budget = 5;

        int n = cost.length;

        int[][] dp = new int[n + 1][budget + 1];

        // Build DP table
        for (int i = 1; i <= n; i++) {
            for (int w = 1; w <= budget; w++) {
                if (cost[i - 1] <= w) {
                    dp[i][w] = Math.max(
                        dp[i - 1][w],
                        value[i - 1] + dp[i - 1][w - cost[i - 1]]
                    );
                } else {
                    dp[i][w] = dp[i - 1][w];
                }
            }
        }

        System.out.println("\n0/1 Knapsack — Project Budget Selection");
        System.out.println("Available Projects:");
        System.out.println("Project\t\t\tCost\tValue");
        System.out.println("-------\t\t\t----\t-----");

        for (int i = 0; i < n; i++) {
            System.out.println(projects[i] + "\t\t" + cost[i] + "\t" + value[i]);
        }

        System.out.println("\nTotal Budget: " + budget);

        // Print DP table
        System.out.println("\nDP Table (Projects × Budget):");
        System.out.print("     ");
        for (int w = 0; w <= budget; w++) {
            System.out.print(w + "  ");
        }
        System.out.println();

        for (int i = 0; i <= n; i++) {
            if (i == 0) {
                System.out.print("{}  ");
            } else {
                System.out.print("P" + i + "  ");
            }
            for (int w = 0; w <= budget; w++) {
                System.out.printf("%2d ", dp[i][w]);
            }
            System.out.println();
        }

        // Backtrack to find selected projects
        System.out.println("\nSelected Projects:");
        int remaining = budget;
        int totalVal = 0;

        for (int i = n; i > 0; i--) {
            if (dp[i][remaining] != dp[i - 1][remaining]) {
                System.out.println("  " + projects[i - 1] + " (Cost: " + cost[i - 1] + ", Value: " + value[i - 1] + ")");
                totalVal += value[i - 1];
                remaining -= cost[i - 1];
            }
        }

        System.out.println("\nTotal Value Achieved: " + totalVal);
    }
}
