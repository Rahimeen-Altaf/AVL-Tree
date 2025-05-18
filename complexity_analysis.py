def bst_frequency_analysis(n):
    """
    BST Insert frequency count:
    Operations counted:
    1. Memory allocation: 1 operation per node
    2. Root null check: 1 comparison per node
    3. Finding position: comparisons while traversing
    4. Pointer assignments: 2 assignments per node
    """
    # Best case (balanced tree)
    memory_alloc = n      # one new node per insertion
    null_checks = n       # one root check per insertion
    comparisons = 2 * n   # balanced tree: ~2 comparisons per node
    assignments = 2 * n   # two pointer assignments per node
    
    best_case = memory_alloc + null_checks + comparisons + assignments
    
    # Worst case (skewed tree)
    skewed_comparisons = (n * (n + 1)) // 2  # 1+2+3+...+n comparisons
    worst_case = memory_alloc + null_checks + skewed_comparisons + assignments
    
    print("\n=== BST Operation Count ===")
    print(f"Number of nodes (n): {n}")
    print("\nBest Case (Balanced):")
    print(f"F(n) = n + n + 2n + 2n = 6n = {best_case} operations")
    print("Where:")
    print("- n: memory allocations")
    print("- n: null checks")
    print("- 2n: finding position")
    print("- 2n: pointer assignments")
    
    print("\nWorst Case (Skewed):")
    print(f"F(n) = n + n + n(n+1)/2 + 2n = {worst_case} operations")
    print("Where:")
    print("- n: memory allocations")
    print("- n: null checks")
    print(f"- n(n+1)/2 = {skewed_comparisons}: finding position")
    print("- 2n: pointer assignments")
    
    return best_case, worst_case

def avl_frequency_analysis(n):
    """
    AVL Insert frequency count:
    Operations counted:
    1. Memory allocation: 1 operation per node
    2. Root null check: 1 comparison per node
    3. Finding position: 2 comparisons per level
    4. Height updates: 2 operations per node
    5. Balance factor: 1 calculation per node
    6. Rotations: max 2 rotations × 3 operations each
    """
    memory_alloc = n      # one new node per insertion
    null_checks = n       # one root check per insertion
    comparisons = 2 * n   # ~2 comparisons per node (balanced)
    height_ops = 2 * n    # two height calculations per node
    balance_ops = n       # one balance factor calculation per node
    rotation_ops = 6 * n  # worst case: 2 rotations × 3 operations each
    
    total_ops = memory_alloc + null_checks + comparisons + height_ops + balance_ops + rotation_ops
    
    print("\n=== AVL Operation Count ===")
    print(f"Number of nodes (n): {n}")
    print(f"F(n) = n + n + 2n + 2n + n + 6n = 13n = {total_ops} operations")
    print("Where:")
    print("- n: memory allocations")
    print("- n: null checks")
    print("- 2n: finding position")
    print("- 2n: height updates")
    print("- n: balance calculations")
    print("- 6n: rotation operations")
    
    return total_ops

def space_analysis(n):
    """
    Space complexity analysis:
    
    BST Node space:
    1. Data value: 1 unit
    2. Left pointer: 1 unit
    3. Right pointer: 1 unit
    Total per node = 3 units
    
    AVL Node additional space:
    4. Height field: 1 unit
    Total per node = 4 units
    
    Stack space:
    - BST: n units (worst case, skewed tree)
    - AVL: log₂n units (balanced tree)
    """
    # Space for node structure
    bst_node_space = 3 * n  # data + left + right
    avl_node_space = 4 * n  # data + left + right + height
    
    # Additional stack space
    bst_stack_space = n     # worst case: skewed tree
    avl_stack_space = int(1.44 * n)  # log₂n rounded up
    
    bst_total = bst_node_space + bst_stack_space
    avl_total = avl_node_space + avl_stack_space
    
    print("\n=== Space Analysis ===")
    print(f"Number of nodes (n): {n}")
    print("\nBST Space:")
    print(f"F(n) = 3n + n = 4n = {bst_total} units")
    print("Where:")
    print("- 3n: node structure (data + 2 pointers)")
    print("- n: stack space (worst case)")
    
    print("\nAVL Space:")
    print(f"F(n) = 4n + log₂n = {avl_total} units")
    print("Where:")
    print("- 4n: node structure (data + 2 pointers + height)")
    print(f"- log₂n ≈ {avl_stack_space}: stack space (balanced)")
    
    return bst_total, avl_total

def frequency_counts(n):
    """
    Returns total operation counts for BST and AVL
    """
    _, bst_freq = bst_frequency_analysis(n)  # using worst case for BST
    avl_freq = avl_frequency_analysis(n)
    return bst_freq, avl_freq 