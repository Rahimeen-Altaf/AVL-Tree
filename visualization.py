import matplotlib.pyplot as plt
from tree_operations import getHeight, getBalance

def getSubtreeHeight(node):
    if not node:
        return 0
    return 1 + max(getSubtreeHeight(node.left), getSubtreeHeight(node.right))

def calculate_tree_width(node):
    """Calculate the width needed for the tree"""
    if not node:
        return 0
    return 1 + calculate_tree_width(node.left) + calculate_tree_width(node.right)

def plot_tree(ax, node, x, y, dx, level=0, node_count=None):
    if node_count is None:
        # Count total nodes to adjust spacing
        def count_nodes(n):
            if not n: return 0
            return 1 + count_nodes(n.left) + count_nodes(n.right)
        node_count = count_nodes(node)
    
    # Adjust spacing based on number of nodes
    if node_count < 10:
        node_size = 12
        text_size = 10
        y_spacing = 40
        dx_factor = 0.8
    elif node_count < 20:
        node_size = 10
        text_size = 8
        y_spacing = 35
        dx_factor = 0.7
    else:
        node_size = 8
        text_size = 6
        y_spacing = 30
        dx_factor = 0.6
    
    if node:
        # Draw node: Light grey circle with black outline, and value inside.
        radius = node_size / 2  # User-set radius, may be very large
        circle = plt.Circle((x, y), radius, fc='lightgrey', ec='black', linewidth=1, zorder=1)
        ax.add_patch(circle)
        
        # Add node value (text on top of the circle)
        ax.text(x, y, str(node.data), ha='center', va='center', fontsize=text_size, zorder=2)
        
        # Add height and balance factor (text with its own background)
        h = getSubtreeHeight(node)
        bf = getBalance(node)
        ax.text(x, y + node_size/2, f"H={h}\nBF={bf}", ha='center', va='bottom', 
                fontsize=text_size-2, bbox=dict(facecolor='lightblue', boxstyle='round,pad=0.3'))
        
        # Calculate new dx for children
        new_dx = dx * dx_factor
        
        # Draw connections and recurse
        if node.left:
            ax.plot([x, x - new_dx], [y, y - y_spacing], color='gray', linewidth=1)
            plot_tree(ax, node.left, x - new_dx, y - y_spacing, new_dx, level + 1, node_count)
        if node.right:
            ax.plot([x, x + new_dx], [y, y - y_spacing], color='gray', linewidth=1)
            plot_tree(ax, node.right, x + new_dx, y - y_spacing, new_dx, level + 1, node_count)

def setup_plot_for_trees(root_bst, root_avl):
    """Setup the plot with proper dimensions based on tree sizes"""
    # Count nodes
    def count_nodes(node):
        if not node: return 0
        return 1 + count_nodes(node.left) + count_nodes(node.right)
    
    node_count = max(count_nodes(root_bst), count_nodes(root_avl))
    
    # Calculate heights
    bst_height = getSubtreeHeight(root_bst)
    avl_height = getSubtreeHeight(root_avl)
    max_height = max(bst_height, avl_height)
    
    # Adjust figure size based on number of nodes and height
    if node_count < 10:
        fig_width = 15
    elif node_count < 20:
        fig_width = 18
    else:
        fig_width = 20
    
    fig_height = max(6, min(12, max_height * 1.5))
    
    # Create figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(fig_width, fig_height))
    # fig.suptitle("BST vs AVL Tree Comparison", fontsize=16, pad=20) # Temporarily comment out to isolate error
    
    # Setup axes
    for ax in (ax1, ax2):
        ax.set_xticks([])
        ax.set_yticks([])
        ax.axis('equal')  # Make sure circles are circular
        ax.set_xlim(-fig_width/2, fig_width/2)
        ax.set_ylim(-fig_height + 2, 2)
    
    ax1.set_title("Binary Search Tree", fontsize=14) # Temporarily remove pad to isolate
    ax2.set_title("AVL Tree", fontsize=14) # Temporarily remove pad to isolate
    
    return fig, ax1, ax2, node_count

def plot_comparison_graph(sizes, bst_freqs, avl_freqs):
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, bst_freqs, label='BST Operations (n² + 4n)', marker='o', color='blue')
    plt.plot(sizes, avl_freqs, label='AVL Operations (13n)', marker='x', color='red')
    plt.xlabel('Number of Nodes (n)')
    plt.ylabel('Number of Operations')
    plt.title('BST vs AVL Operation Count Comparison')
    plt.legend()
    plt.grid(True)
    plt.show()