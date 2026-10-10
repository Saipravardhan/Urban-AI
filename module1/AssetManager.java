package module1;

import data.CityData;
import model.Asset;

import java.util.List;

public class AssetManager {

    private final AVLTree avlTree;
    private final CityData store;

    public AssetManager() {

        avlTree = new AVLTree();
        store = CityData.getInstance();

        loadSampleAssets();
    }

    private void loadSampleAssets() {

        List<Asset> assets = store.getAllAssets();

        for (Asset asset : assets) {
            avlTree.insert(asset);
        }

        System.out.println("Loaded " + assets.size() + " sample assets into AVL Tree");
    }

    public void addAsset(
            int assetId,
            String assetName,
            String location,
            String assetType) {

        if (avlTree.search(assetId) != null) {
            System.out.println("\nAsset ID " + assetId
                    + " already exists. Use a different ID.");
            return;
        }

        Asset asset = new Asset(assetId, assetName, location, assetType);

        avlTree.insert(asset);
        store.saveAsset(asset);

        System.out.println("\nAsset Added Successfully\n");
    }

    public void searchAsset(int assetId) {

        Asset asset = avlTree.search(assetId);

        if (asset != null) {

            System.out.println("\nAsset Found\n");
            System.out.println(asset);

        } else {

            System.out.println("\nAsset Not Found");
        }
    }

    public void displayAssets() {

        System.out.println("\nInfrastructure Assets (sorted by ID via AVL inorder)\n");

        List<Asset> assets = avlTree.toSortedList();

        if (assets.isEmpty()) {

            System.out.println("No Assets Found");
            return;
        }

        for (Asset asset : assets) {

            System.out.println(asset);
            System.out.println("-------------");
        }
    }
}
