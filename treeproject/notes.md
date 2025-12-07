
source: https://benjamincongdon.me/blog/2021/08/17/B-Trees-More-Than-I-Thought-Id-Want-to-Know/

    Constraint: The entire dataset will not fit in memory.
        The effect: Data needs to be laid out such that traversing the structure is possible by loading only a subset of the structure into memory.
    Constraint: The smallest unit of storage that can be read/written to/from a drive is large, compared to in-memory access (usually an entire page vs. a single byte).
        The effect: Try to co-locate data likely to be accessed together as much as possible.
    Constraint: Disk I/O is significantly slower than in-memory lookups.
        The effect: Reduce the # of disk accesses as much as possible.

----------------------------------------------------------------

    B-Trees naturally lend themselves to be laid out in pages: each logical tree node gets a disk page. We can tune the parameters of the tree (primarily, the number of keys per node) so as to fix a node comfortably within a disk page.

    However, B-Trees are dynamic. Tree nodes can change due to any insertion or deletion, and keys must stay in sorted order within nodes. How can we layout data in a sorted order without needing to move a bunch of data around during each mutation operation? The answer: Slotted pages.

    Slotted pages are composed of three components: a header (containing metadata about the page), cells (variable-sized “slots” for data to be stored in), and offset pointers (an array of pointers to those cells).

    The benefit of this layout is that you can store variable sized data, since the cells can be of variable size, and you don’t need to move that data to logically reorder it. Reordering the positions of the pointers in the pointer array is sufficient. This is inexpensive since the pointers are small, and in a well-known position at the beginning of the page. In other words, as long as the offset pointers are ordered in key-sorted order, it doesn’t matter where in the actual page the keys are stored.
    
    ------------------------------------------------------------

    B-Tree lookup Algo
    1. Start at the root node.

    2. Look at the separator keys in the current node, to find the child node which would logically contain the search key you’re looking for.

    3. Recursively traverse the tree using the logic from step 2

    4. If you hit a leaf node containing the key you’re searching for, you’re done. If you discover that a leaf node does not exist for the search key (e.g. there is no leaf for the range you’re seeking), or the leaf node does not contain the desired key, report that the key does not exist, and you’re done.

    details: First: In most implementations when traversing the tree, you perform binary search on the keys within a node . This is why it’s so important that keys are store in sorted order within nodes. Second: Except for the leaf nodes, which actually store data2, the full value of the separator key isn’t important – it’s just acting as a partition between nodes. As long as the separator key accurately represents a partition between the key range each child node is responsible for, it can be any value which holds that partition property. Using one of the actual database keys as the partition key is just a convenient method of picking a partition key.

    optimizations:
    - separator key truncation
    - overflow pages

From: https://www.geeksforgeeks.org/dsa/introduction-of-b-tree-2/#
In a B-Tree of order m, each node can have up to m children and m-1 keys, allowing it to efficiently manage large datasets.
The value of m is decided based on disk block and key sizes.

Properties of a B-Tree

A B Tree of order m can be defined as an m-way search tree which satisfies the following properties:

    1. All leaf nodes of a B tree are at the same level, i.e. they have the same depth (height of the tree).
    2. The keys of each node of a B tree (in case of multiple keys), should be stored in the ascending order.
    3. In a B tree, all non-leaf nodes (except root node) should have at least m/2 children.
    4. All nodes (except root node) should have at least m/2 - 1 keys.
    5. If the root node is a leaf node (only node in the tree), then it will have no children and will have at least one key. If the root node is a non-leaf node, then it will have at least 2 children and at least one key.
    6. A non-leaf node with n-1 key values should have n non NULL children.