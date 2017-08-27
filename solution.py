assignments = []


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    #some initialisation ofr the function when ran standalone
    rows = 'ABCDEFGHI'
    cols = '123456789'
    boxes = cross(rows, cols)
    row_units = [cross(r, cols) for r in rows]
    column_units = [cross(rows, c) for c in cols]
    square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
    unitlist = row_units + column_units + square_units
    units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
    final_dict = {}
    #first look for values composed of 2 numbers
    # if found one just append to dict_alt
    stalled=False
    while not stalled:
        values_old=values
        for unit in unitlist:
            #first find the boxes with a value of length 2
            dict_alt = {}
            for box in unit:
                if len(values[box]) == 2:
                    if not values[box] in dict_alt:
                        dict_alt[values[box]] = [box]
                    else:
                        dict_alt[values[box]].append(box)
            #match the values to the dict
            for key in dict_alt:
                if len(dict_alt[key]) == 2:
                    if not key in final_dict:
                        final_dict[key] = [unit]
                    else:
                        final_dict[key].append(unit)
        #finally just replace the values found by empty string among peers
        for key in final_dict:
            for unit in final_dict[key]:
                for box in unit:
                    if values[box] != key:
                        assign_value(values, box, values[box].replace(key[0], ''))
                        assign_value(values, box, values[box].replace(key[1], ''))
        stalled = values_old == values
    return values


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    values = []
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    assert len(values) == 81
    return dict(zip(boxes, values))

def display(values):
    """
        Display the values as a 2-D grid.
        Input: The sudoku in dictionary form
        Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values=grid_values(grid)
    stalled = False
    display(values)
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values= reduce_puzzle(values)
        values= search(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    display(values)
    return values

def cross_diag(a,b):
    """
        creates strings containing the first letter of a and b then the second one and so on
        Args: a and b two string with the same length
        returns: len(a) strings
    """
    return [a[i]+b[i] for i in range(0,len(a))]
rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
#new block of rules on the diagonal
diag_units =[cross_diag(rows, c) for c in ('123456789', '987654321')]
#adding them to the regular set of blocks
unitlist = row_units + column_units + square_units + diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    before_naked_twins_1 = {"G7": "2345678", "G6": "1236789", "G5": "23456789", "G4": "345678",
        "G3": "1234569", "G2": "12345678", "G1": "23456789", "G9": "24578",
        "G8": "345678", "C9": "124578", "C8": "3456789", "C3": "1234569",
        "C2": "1234568", "C1": "2345689", "C7": "2345678", "C6": "236789",
        "C5": "23456789", "C4": "345678", "E5": "678", "E4": "2", "F1": "1",
        "F2": "24", "F3": "24", "F4": "9", "F5": "37", "F6": "37", "F7": "58",
        "F8": "58", "F9": "6", "B4": "345678", "B5": "23456789", "B6":
        "236789", "B7": "2345678", "B1": "2345689", "B2": "1234568", "B3":
        "1234569", "B8": "3456789", "B9": "124578", "I9": "9", "I8": "345678",
        "I1": "2345678", "I3": "23456", "I2": "2345678", "I5": "2345678",
        "I4": "345678", "I7": "1", "I6": "23678", "A1": "2345689", "A3": "7",
        "A2": "234568", "E9": "3", "A4": "34568", "A7": "234568", "A6":
        "23689", "A9": "2458", "A8": "345689", "E7": "9", "E6": "4", "E1":
        "567", "E3": "56", "E2": "567", "E8": "1", "A5": "1", "H8": "345678",
        "H9": "24578", "H2": "12345678", "H3": "1234569", "H1": "23456789",
        "H6": "1236789", "H7": "2345678", "H4": "345678", "H5": "23456789",
        "D8": "2", "D9": "47", "D6": "5", "D7": "47", "D4": "1", "D5": "36",
        "D2": "9", "D3": "8", "D1": "36"}


    display(grid_values(diag_sudoku_grid))
    display(solve(diag_sudoku_grid))
    display(naked_twins(before_naked_twins_1))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
