package module2;

import data.CityData;
import model.TrafficRecord;

import java.util.List;

public class TrafficManager {

    public static final int MAX_ROAD_ID = 100;   // Fenwick Tree size
    public static final int MAX_NODE = 99;       // keeps graph matrices small

    private final FenwickTree fenwick = new FenwickTree(MAX_ROAD_ID);
    private final CityData store = CityData.getInstance();

    public TrafficManager() {
        loadSampleRoads();
    }

    private void loadSampleRoads() {

        List<TrafficRecord> roads = store.getAllRoads();

        for (TrafficRecord record : roads) {
            fenwick.update(record.getRoadId(), record.getVehicleCount());
        }

        System.out.println("Loaded " + roads.size() + " sample roads into Fenwick Tree");
    }

    public void insertTrafficRecord(
            int roadId, int sourceNode, int destNode,
            double distanceKm, int vehicleCount) {

        if (roadId < 1 || roadId > MAX_ROAD_ID) {
            System.out.println("\nRoad ID must be between 1 and " + MAX_ROAD_ID);
            return;
        }
        if (sourceNode < 0 || sourceNode > MAX_NODE
                || destNode < 0 || destNode > MAX_NODE) {
            System.out.println("\nNode numbers must be between 0 and " + MAX_NODE);
            return;
        }
        if (sourceNode == destNode) {
            System.out.println("\nSource and destination nodes must be different");
            return;
        }
        if (distanceKm <= 0) {
            System.out.println("\nDistance must be greater than 0");
            return;
        }
        if (vehicleCount < 0) {
            System.out.println("\nVehicle count cannot be negative");
            return;
        }

        // If the road already exists, update it (and fix the Fenwick Tree by the difference)
        TrafficRecord old = store.getRoad(roadId);
        int delta = vehicleCount - (old == null ? 0 : old.getVehicleCount());

        TrafficRecord record = new TrafficRecord(
                roadId, sourceNode, destNode, distanceKm, vehicleCount);

        store.saveRoad(record);
        fenwick.update(roadId, delta);

        System.out.println(old == null
                ? "\nRoad Added Successfully"
                : "\nRoad " + roadId + " already existed - updated successfully");
    }

    public void calculateTrafficDensity(int roadId) {

        TrafficRecord record = store.getRoad(roadId);

        if (record == null) {
            System.out.println("Road Not Found");
            return;
        }

        int count = record.getVehicleCount();

        System.out.println("\nTraffic Density for Road " + roadId
                + " (Node " + record.getSourceNode()
                + " → Node " + record.getDestNode() + ")");

        System.out.println(densityOf(count) + " (" + count + " vehicles)");
    }

    public void getCumulativeTrafficStatistics(int startRoad, int endRoad) {

        if (startRoad < 1 || endRoad > MAX_ROAD_ID || startRoad > endRoad) {
            System.out.println("\nInvalid range. Use 1 <= start <= end <= " + MAX_ROAD_ID);
            return;
        }

        int totalTraffic = fenwick.rangeQuery(startRoad, endRoad);

        System.out.println("\nTotal Traffic (Roads " + startRoad
                + " to " + endRoad + ") = " + totalTraffic);
    }

    public void displayRecords() {

        List<TrafficRecord> records = store.getAllRoads();

        System.out.println("\nUrbanAI Road Network\n");

        if (records.isEmpty()) {
            System.out.println("No roads in the network.");
            return;
        }

        System.out.println("ID\tSource → Dest\tDistance\tVehicles\tDensity");
        System.out.println("--\t-------------\t--------\t--------\t-------");

        for (TrafficRecord record : records) {

            int count = record.getVehicleCount();

            System.out.println(record.getRoadId()
                    + "\t  " + record.getSourceNode() + "  →  " + record.getDestNode()
                    + "\t  " + record.getDistanceKm() + " km"
                    + "\t\t" + count
                    + "\t\t" + densityOf(count));
        }
    }

    private String densityOf(int count) {
        if (count > 1000) return "HIGH";
        if (count > 500) return "MEDIUM";
        return "LOW";
    }
}
