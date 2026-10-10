package module1;

import model.Asset;

import java.util.ArrayList;
import java.util.List;

public class AVLTree {

    class Node {
        Asset asset;
        Node left;
        Node right;
        int height;

        Node(Asset asset) {
            this.asset = asset;
            height = 1;
        }
    }

    private Node root;

    private int height(Node n) {
        if (n == null)
            return 0;
        return n.height;
    }

    private int getBalance(Node n) {
        if (n == null)
            return 0;

        return height(n.left) - height(n.right);
    }

    private Node rightRotate(Node y) {
        Node x = y.left;
        Node t2 = x.right;

        x.right = y;
        y.left = t2;

        y.height = Math.max(height(y.left),
                height(y.right)) + 1;

        x.height = Math.max(height(x.left),
                height(x.right)) + 1;

        return x;
    }

    private Node leftRotate(Node x) {
        Node y = x.right;
        Node t2 = y.left;

        y.left = x;
        x.right = t2;

        x.height = Math.max(height(x.left),
                height(x.right)) + 1;

        y.height = Math.max(height(y.left),
                height(y.right)) + 1;

        return y;
    }

    public void insert(Asset asset) {
        root = insert(root, asset);
    }

    private Node insert(Node node, Asset asset) {

        if (node == null)
            return new Node(asset);

        if (asset.getAssetId() <
                node.asset.getAssetId()) {
            node.left = insert(node.left, asset);
        } else if (asset.getAssetId() >
                node.asset.getAssetId()) {
            node.right = insert(node.right, asset);
        } else {
            return node;
        }

        node.height = 1 + Math.max(
                height(node.left),
                height(node.right));

        int balance = getBalance(node);

        if (balance > 1 &&
                asset.getAssetId() <
                node.left.asset.getAssetId())
            return rightRotate(node);

        if (balance < -1 &&
                asset.getAssetId() >
                node.right.asset.getAssetId())
            return leftRotate(node);

        if (balance > 1 &&
                asset.getAssetId() >
                node.left.asset.getAssetId()) {

            node.left = leftRotate(node.left);
            return rightRotate(node);
        }

        if (balance < -1 &&
                asset.getAssetId() <
                node.right.asset.getAssetId()) {

            node.right = rightRotate(node.right);
            return leftRotate(node);
        }

        return node;
    }

    public Asset search(int assetId) {

        Node current = root;

        while (current != null) {

            if (assetId ==
                    current.asset.getAssetId()) {
                return current.asset;
            }

            if (assetId <
                    current.asset.getAssetId()) {
                current = current.left;
            } else {
                current = current.right;
            }
        }

        return null;
    }

    public void inorder() {
        inorder(root);
    }

    private void inorder(Node node) {

        if (node != null) {

            inorder(node.left);

            System.out.println(
                    node.asset.getAssetId()
                            + " - "
                            + node.asset.getAssetName());

            inorder(node.right);
        }
    }

    public List<Asset> toSortedList() {
        List<Asset> list = new ArrayList<>();
        collect(root, list);
        return list;
    }

    private void collect(Node node, List<Asset> list) {
        if (node != null) {
            collect(node.left, list);
            list.add(node.asset);
            collect(node.right, list);
        }
    }
}
