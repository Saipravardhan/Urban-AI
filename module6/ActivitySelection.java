package module6;

import java.util.*;

public class ActivitySelection {

    public void scheduleMaintenanceTasks() {

        int[] start = {8, 9, 10, 11};
        String[] tasks = {"Road Repair", "Paint Bridge", "Clean Park", "Inspect Drain"};
        int[] finish = {10, 11, 12, 13};

        int n = start.length;

        // Bubble sort by finish time (ascending)
        for (int i = 0; i < n - 1; i++) {
            for (int j = 0; j < n - i - 1; j++) {
                if (finish[j] > finish[j + 1]) {
                    int tempF = finish[j];
                    finish[j] = finish[j + 1];
                    finish[j + 1] = tempF;

                    int tempS = start[j];
                    start[j] = start[j + 1];
                    start[j + 1] = tempS;

                    String tempT = tasks[j];
                    tasks[j] = tasks[j + 1];
                    tasks[j + 1] = tempT;
                }
            }
        }

        System.out.println("\nActivity Selection — Maintenance Task Scheduling");
        System.out.println("Sorted tasks by finish time:");
        System.out.println("Task\t\tStart\tFinish");
        System.out.println("----\t\t-----\t------");

        for (int i = 0; i < n; i++) {
            System.out.println(tasks[i] + "\t" + start[i] + "\t" + finish[i]);
        }

        System.out.println("\nSelected Tasks (non-overlapping):");

        int lastFinish = finish[0];
        System.out.println("  " + tasks[0] + " (" + start[0] + "-" + finish[0] + ")");
        int count = 1;

        for (int i = 1; i < n; i++) {
            if (start[i] >= lastFinish) {
                System.out.println("  " + tasks[i] + " (" + start[i] + "-" + finish[i] + ")");
                lastFinish = finish[i];
                count++;
            }
        }

        System.out.println("\nTotal tasks scheduled: " + count + " / " + n);
    }
}
