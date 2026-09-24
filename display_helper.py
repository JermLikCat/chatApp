class DisplayHelper:
    def __init__(self):
        pass

    def clear_screen(self):
        print("\x1b[2J", end="")

    def go_to_position(self, x: int, y: int):
        print(f"\x1b[{y};{x}H", end="")

    def erase_line(self):
        print("\x1b[2K", end="")

    def clear_rows(self, start, rows):
        """
        Clears a given number of rows. Moves cursor to the beginning of line at the top.
        """
        self.go_to_position(0, start)
        # Clear and move down
        for _ in range(rows):
            self.erase_line()
            print("\x1b[B", end="")
        print(f'\x1b[{rows}F', end="")