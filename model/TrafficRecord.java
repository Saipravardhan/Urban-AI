package model;

public class TrafficRecord {

    private int roadId;
    private int sourceNode;
    private int destNode;
    private double distanceKm;
    private int vehicleCount;

    public TrafficRecord(int roadId, int sourceNode, int destNode,
                         double distanceKm, int vehicleCount) {
        this.roadId = roadId;
        this.sourceNode = sourceNode;
        this.destNode = destNode;
        this.distanceKm = distanceKm;
        this.vehicleCount = vehicleCount;
    }

    public TrafficRecord(int roadId, int vehicleCount) {
        this.roadId = roadId;
        this.sourceNode = -1;
        this.destNode = -1;
        this.distanceKm = 0.0;
        this.vehicleCount = vehicleCount;
    }

    public int getRoadId() { return roadId; }
    public int getSourceNode() { return sourceNode; }
    public int getDestNode() { return destNode; }
    public double getDistanceKm() { return distanceKm; }
    public int getVehicleCount() { return vehicleCount; }

    @Override
    public String toString() {
        return "Road ID: " + roadId +
               "\nRoute: Node " + sourceNode + " → Node " + destNode +
               "\nDistance: " + distanceKm + " km" +
               "\nVehicle Count: " + vehicleCount;
    }
}
