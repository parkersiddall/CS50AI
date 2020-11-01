import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """

        # example: {A, B, C} = 3, we can deduce that A, B, and C are all mines
        if len(self.cells) == self.count:
            return self.cells

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """

        # if the count is 0 then every cell should be safe...
        if self.count == 0:
            return self.cells

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # check to see if said cell is in this particular instance of a Sentence
        if cell in self.cells:

            # remove it and lower the count by 1, as it is known to be a mine
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # check to see if said cell is in this knowledge Sentence
        if cell in self.cells:

            # remove it but leave the count the same, as it is known to not be a mine
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def surrounding_cells(self, cell):
        """
        Creates a list of the cells that surround a given cell.
        """

        # declare list to store cells
        surrounding_cells_list = []

        # loop to go through first point in coordinate
        for i in range(cell[0] - 1, cell[0] + 2):  # creates a range that goes between 1 before and 1 after the cells coordinate.

            # loop through the second point in the coordinate
            for j in range(cell[1] - 1, cell[1] + 2):

                # check to be sure the cell is actuall on the board (not less that 0 or higher than height/width)
                if 0 <= i < self.height and 0 <= j < self.width:

                    # check to be sure that coordinates are not the same as the given cell
                    if (i, j) != cell:

                        # add the coordinate to the surrounding cells list
                        temp_cell = (i, j)
                        surrounding_cells_list.append(temp_cell)
        
        return surrounding_cells_list



    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        # 1) mark the cell as a move that has been made
        self.moves_made.add(cell)

        # 2) mark the cell safe
        self.safes.add(cell)

        # 3) add the new sentence to the AI's knowledge base based on cell value and count

        cells = self.surrounding_cells(cell)  # get a list of the surrounding cells
        real_cells = []  # list to hold the surrounding cells that will remain after removing those based on AI known mines/safes
        real_count = count  # copy the count, it will be adjusted as we 

        for item in cells:  # loop through surrounding cells
            if item in self.mines:
                real_count -= 1
            elif item in self.safes:
                continue
            else:
                real_cells.append(item)

        new_knowledge = Sentence(real_cells, real_count)  # create knew knowledge sentence withe the 'real' cells and count
        self.knowledge.append(new_knowledge)  # add this sentence to the knowledge base

        # 4) mark any additional cells as safe or as mines if it can be concluded based on knowledge base

        for sentence in self.knowledge:  # loop through the sentences in knowledge

            m = sentence.known_mines()  # get list of known mines for sentence
            s = sentence.known_safes()  # get list of known safes for sentence

            temp_mines = []  # create temp lists, otherwise the set is changed during iteration
            temp_safes = []

            if m:  # if there is something, loop through. Check if it has already been marked. If not, add it to the temp list.
                for mine in m:
                    if mine not in self.mines:
                        temp_mines.append(mine)

            if s:
                for safe in s:
                    if safe not in self.safes:
                        temp_safes.append(safe)

            for item in temp_mines:  # go through and mark the safes and mines from temp list
                self.mark_mine(item)
            for item in temp_safes:
                self.mark_safe(item)

        # 5) make inferrals and add them to the knowledge base

        new_inferrals = []

        for sentence in self.knowledge:  # loop through knowledge and see if new inferalls can be made based on new knowledge
            if sentence == new_knowledge:  # ignore the sentence if it is the new knowledge
                break
            elif new_knowledge.cells > sentence.cells:  # see if the new knowledge has more cells than what it is being compared to 
                inferred_cells = new_knowledge.cells - sentence.cells  # rules for inference as outlined in the background
                inferred_count = new_knowledge.count - sentence.count

                new_inferrals.append(Sentence(inferred_cells, inferred_count))  # add the new inferral to the list

        for item in new_inferrals:  # check to see if the inferall is already in the knowledge base. If not, add it. 
            if item not in self.knowledge:
                self.knowledge.append(item)



    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # loop through safe moves. 
        for item in self.safes:

            # If it is not already a move made then it can be played.
            if item not in self.moves_made:
                return item
        
        # if the loop finishes and nothing is returned, there are no known safes
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        # keep repeating this until a possible random move is found.
        while True:

            # get two random ints that are within the height and width range
            rando_1 = random.randint(0, self.height - 1)
            rando_2 = random.randint(0, self.width - 1)

            random_move = (rando_1, rando_2)

            if random_move not in self.moves_made:
                if random_move not in self.mines:
                    return random_move
                else:
                    return None


