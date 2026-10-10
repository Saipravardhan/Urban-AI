package module6;

import java.util.*;

public class FractionalKnapsack {

    public void allocateResources() {

        String[] resources = {"Asphalt", "Paint", "Concrete", "Steel"};
        int[] value = {50, 30, 40, 20};
        int[] weight = {10, 5, 8, 4};
        int capacity = 20;

        int n = resources.length;

        // Calculate value/weight ratio and sort descending
        double[] ratio = new double[n];
        for (int i = 0; i < n; i++) {
            ratio[i] = (double) value[i] / weight[i];
        }

        // Bubble sort by ratio descending
        for (int i = 0; i < n - 1; i++) {
            for (int j = 0; j < n - i - 1; j++) {
                if (ratio[j] < ratio[j + 1]) {
                    double tempR = ratio[j];
                    ratio[j] = ratio[j + 1];
                    ratio[j + 1] = tempR;

                    int tempV = value[j];
                    value[j] = value[j + 1];
                    value[j + 1] = tempV;

                    int tempW = weight[j];
                    weight[j] = weight[j + 1];
                    weight[j + 1] = tempW;

                    String tempS = resources[j];
                    resources[j] = resources[j + 1];
                    resources[j + 1] = tempS;
                }
            }
        }

        System.out.println("\nFractional Knapsack — Resource Allocation");
        System.out.println("Resources sorted by Value/Weight ratio:");
        System.out.println("Resource\tValue\tWeight\tRatio");
        System.out.println("--------\t-----\t------\t-----");

        for (int i = 0; i < n; i++) {
            System.out.printf("%s\t\t%d\t%d\t%.1f\n", resources[i], value[i], weight[i], ratio[i]);
        }

        System.out.println("\nTotal Capacity: " + capacity + " units");
        System.out.println("\nAllocation:");

        double totalValue = 0.0;
        int remainingCap = capacity;

        for (int i = 0; i < n; i++) {
            if (weight[i] <= remainingCap) {
                // Take full item
                System.out.println("  " + resources[i] + ": " + weight[i] + " units (full) — Value: " + value[i]);
                totalValue += value[i];
                remainingCap -= weight[i];
            } else {
                // Take fraction
                double fraction = (double) remainingCap / weight[i];
                double partialValue = value[i] * fraction;
                System.out.printf("  %s: %d units (fraction: %.2f%%) — Value: %.1f\n",
                    resources[i], remainingCap, fraction * 100, partialValue);
                totalValue += partialValue;
                remainingCap = 0;
                break;
            }
        }

        System.out.printf("\nTotal Resource Utility Achieved: %.1f\n", totalValue);
    }
}
