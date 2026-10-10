package module2;

public class FenwickTree {

    private int[] tree;
    private int size;

    public FenwickTree(int size) {

        this.size = size;
        tree = new int[size + 1];
    }

    public void update(int index, int value) {

        while(index <= size) {

            tree[index] += value;

            index += index & (-index);
        }
    }

    public int query(int index) {

        int sum = 0;

        while(index > 0) {

            sum += tree[index];

            index -= index & (-index);
        }

        return sum;
    }

    public int rangeQuery(int left, int right) {

        return query(right)
                - query(left - 1);
    }
}
