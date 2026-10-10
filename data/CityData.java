package data;

import model.Asset;
import model.TrafficRecord;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public class CityData {

    private static final CityData INSTANCE = new CityData();

    private final Map<Integer, Asset> assets = new LinkedHashMap<>();
    private final Map<Integer, TrafficRecord> roads = new LinkedHashMap<>();
    private int maxNode = 0;

    private CityData() {
        seedSampleAssets();
        seedSampleRoads();
    }

    public static CityData getInstance() {
        return INSTANCE;
    }

    public List<Asset> getAllAssets() {
        return new ArrayList<>(assets.values());
    }

    public void saveAsset(Asset asset) {
        if (asset == null) {
            return;
        }
        assets.put(asset.getAssetId(), asset);
    }

    public List<TrafficRecord> getAllRoads() {
        return new ArrayList<>(roads.values());
    }

    public TrafficRecord getRoad(int roadId) {
        return roads.get(roadId);
    }

    public void saveRoad(TrafficRecord road) {
        if (road == null) {
            return;
        }
        roads.put(road.getRoadId(), road);
        maxNode = Math.max(maxNode, Math.max(road.getSourceNode(), road.getDestNode()));
    }

    public int getMaxNode() {
        if (maxNode == 0 && !roads.isEmpty()) {
            for (TrafficRecord road : roads.values()) {
                maxNode = Math.max(maxNode, Math.max(road.getSourceNode(), road.getDestNode()));
            }
        }
        return maxNode;
    }

    private void seedSampleAssets() {
        saveAsset(new Asset(101, "City Hall", "Downtown", "Government"));
        saveAsset(new Asset(102, "Water Pump", "North District", "Utility"));
        saveAsset(new Asset(103, "Solar Grid", "East Valley", "Energy"));
        saveAsset(new Asset(104, "Traffic Signal", "Central Avenue", "Infrastructure"));
    }

    private void seedSampleRoads() {
        saveRoad(new TrafficRecord(1, 0, 1, 5.0, 200));
        saveRoad(new TrafficRecord(2, 1, 2, 4.0, 120));
        saveRoad(new TrafficRecord(3, 2, 3, 6.5, 350));
        saveRoad(new TrafficRecord(4, 0, 3, 8.0, 180));
        saveRoad(new TrafficRecord(5, 3, 4, 4.5, 450));
        saveRoad(new TrafficRecord(6, 4, 5, 3.5, 90));
        saveRoad(new TrafficRecord(7, 1, 5, 7.0, 260));
        saveRoad(new TrafficRecord(8, 2, 4, 5.5, 310));
    }
}
