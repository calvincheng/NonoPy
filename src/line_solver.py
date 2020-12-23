import numpy as np

"""
(0, 1, 4)
||**|***
01234567

Original: >---#---------#-----#####<
          >#-#---#####-------------<
           012345678901234567890123<
"""

"""
Length:   24
Rule:     1,1,5
Original: >---#---------#-----#####<
Broken:   >---#--         -      # <
           ---X--X-XXXXX  -      # < Slide to furthest legal left
           ---X--X-----------XXXXX-< Slide last block to furthest right uncovered solid
      left>---X--X-----------XXXXX-<
     right>---X-------------X-XXXXX<
      fast>---#--+++++++++-+++####+<

Length:   24
Rule:     1,1,5
Original: >---#-------------#-#####<
Broken:   >---#--         - #    # <
           ---X--X-XXXXX  - #    # < Slide to furthest legal left
           ---X--X-       - #-XXXXX< Slide last block to furthest right uncovered solid legally
           ---X-------------X-XXXXX< Uncovered solid still remaning and block 3 cannot slide further – slide block 2
"""

def get_leftmost(line, rule):
    """
    1. All blocks start on far right
    2. For block 0 to N,
        a. Slide all the way to the left, keeping track of the position of the
           furthest valid position
    3. If uncovered solids remain, then
        a. Slide block N until furthest right solid is covered

    Returns a <Line> array
    """
    res = line[:]
    solids = [1 if c == 1 else 0 for c in line]
    spaces = [1 if c == 0 else 0 for c in line]
    # Start all blocks on the far right
    #
    blocks = [len(line) - 1] * len(rule);
    
    return res

def is_valid_arrangement(line, blocks, rule):
    return (
        no_touching_blocks(line, blocks, rule)
        and no_uncovered_solids(line, blocks, rule)
        and no_covered_gaps(line, blocks, rule)
        and blocks_within_bound(line, blocks, rule)
    )

def no_touching_blocks(line, blocks, rule):
    num_blocks = len(blocks)

    union = set()
    for i in range(num_blocks):
        block_set = set( range( blocks[i], blocks[i] + rule[i] ) )
        if len(union & block_set) != 0:
            # print("Overlap found on block {} at indices {}".format(i, intersection))
            return False
        union |= block_set

    # Check if blocks aren't directly neighbours
    solids_in_a_row = 0
    for i in range(len(line)):
        solids_in_a_row = solids_in_a_row + 1 if i in union else 0
        if solids_in_a_row > max(rule): 
            return False

    return True

def no_uncovered_solids(line, blocks, rule):
    num_blocks = len(blocks)
    solids = set([i for i, c in enumerate(line) if c == 1])
    union = set()
    for i in range(num_blocks):
        union |= set(range(blocks[i], blocks[i] + rule[i]))
    return solids.issubset(union)

def no_covered_gaps(line, blocks, rule):
    num_blocks = len(blocks)
    gaps = set([i for i, c in enumerate(line) if c == 0])
    union = set()
    for i in range(num_blocks):
        union |= set(range(blocks[i], blocks[i] + rule[i]))
    return len(union & gaps) == 0

def blocks_within_bound(line, blocks, rule):
    num_blocks = len(blocks)
    # TODO Can just check the ends of each block instead of creating a set
    union = set()
    for i in range(num_blocks):
        union |= set(range(blocks[i], blocks[i] + rule[i]))
    return max(union) < len(line) and min(union) >= 0

def main():
    string = "---#--         -      # "
    line = [-1] * len(string)
    for i, c in enumerate(string):
        if c == '-': line[i] = 0
        elif c == '#': line[i] = 1
    rule = [1, 1, 5]
    get_leftmost(line, rule)

main()
