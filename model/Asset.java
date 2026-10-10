package model;

public class Asset {
    private int assetId;
    private String assetName;
    private String location;
    private String assetType;

    public Asset(int assetId, String assetName,
                 String location, String assetType) {
        this.assetId = assetId;
        this.assetName = assetName;
        this.location = location;
        this.assetType = assetType;
    }

    public int getAssetId() {
        return assetId;
    }

    public String getAssetName() {
        return assetName;
    }

    public String getLocation() {
        return location;
    }

    public String getAssetType() {
        return assetType;
    }

    @Override
    public String toString() {
        return "Asset ID: " + assetId +
                "\nAsset Name: " + assetName +
                "\nLocation: " + location +
                "\nType: " + assetType;
    }
}
