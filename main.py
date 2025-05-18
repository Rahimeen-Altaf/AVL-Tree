"""
BST vs AVL Tree Analysis Program
This program provides a visual and analytical comparison of Binary Search Trees (BST) and AVL Trees.

Features:
1. Interactive GUI for tree generation
2. Visual comparison of BST and AVL trees
3. Detailed time complexity analysis
4. Space complexity analysis
5. Support for both random and manual input

Author: [Your Name]
Date: [Current Date]
"""

from gui import main

if __name__ == "__main__":
    try:
        main()  # Launch the GUI application
    except Exception as e:
        print(f"An error occurred while starting the application: {str(e)}")
        input("Press Enter to exit...")