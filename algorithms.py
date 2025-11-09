
"""
Memory allocation algorithms implementation
Team CodeStorm - Memory Management Simulator
"""

def first_fit(blocks, processes):
    """First Fit Algorithm: Allocate process to the first block that fits.
       Returns a list of indexes for each process (or -1)."""
    allocation = [-1] * len(processes)
    blocks_copy = blocks.copy()
    for i, process_size in enumerate(processes):
        for j, block_size in enumerate(blocks_copy):
            if block_size >= process_size:
                allocation[i] = j
                blocks_copy[j] -= process_size
                break
    return allocation

def best_fit(blocks, processes):
    """Best Fit Algorithm: Allocate process to the smallest block that fits."""
    allocation = [-1] * len(processes)
    blocks_copy = blocks.copy()
    for i, process_size in enumerate(processes):
        best_idx = -1
        best_size = float('inf')
        for j, block_size in enumerate(blocks_copy):
            if block_size >= process_size and block_size < best_size:
                best_size = block_size
                best_idx = j
        if best_idx != -1:
            allocation[i] = best_idx
            blocks_copy[best_idx] -= process_size
    return allocation

def worst_fit(blocks, processes):
    """Worst Fit Algorithm: Allocate process to the largest block."""
    allocation = [-1] * len(processes)
    blocks_copy = blocks.copy()
    for i, process_size in enumerate(processes):
        worst_idx = -1
        worst_size = -1
        for j, block_size in enumerate(blocks_copy):
            if block_size >= process_size and block_size > worst_size:
                worst_size = block_size
                worst_idx = j
        if worst_idx != -1:
            allocation[i] = worst_idx
            blocks_copy[worst_idx] -= process_size
    return allocation

def simulate_paging(processes):
    """Simulate paging - always succeeds (simplified)."""
    return [0] * len(processes)

def calculate_fragmentation(blocks):
    """Calculate internal and external fragmentation (simplified)."""
    total_free = sum(blocks)
    largest_free = max(blocks) if blocks else 0
    external_frag = total_free - largest_free
    return {
        'total_free': total_free,
        'largest_free': largest_free,
        'external_fragmentation': external_frag
    }
