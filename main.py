import os, subprocess, sys, asyncio
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout

# TODO: Use constants for boxses around the string DONE + :> from format string DONE
# TODO: Let message stream be one big multilined string and make it so clicking arrow keys can show different indexes. SORTA DONE

LEFT_BOX_BORDER = "│ "
RIGHT_BOX_BORDER = " │"
HORIZONTAL_BOX_BORDER = "─"
BOTTOM_RIGHT_BOX_BORDER = "┘"
BOTTOM_LEFT_BOX_BORDER = "└"
TOP_RIGHT_BOX_BORDER = "┐"
TOP_LEFT_BOX_BORDER = "┌"

class Message:
    def __init__(self, text: str, user_name: str, is_client: bool):
        self.text = text
        self.user_name = user_name
        self.skibidi = "Rizzler"
        self.is_client = is_client
        self.horizontal_required_whitespace = 4 + len(text)
        self.vertical_required_whitespace = 3

class ChatDisplay:
    def __init__(self, message_list: list[Message], user_name, rows_allocated: int):
        self.message_list = message_list
        self.rows_allocated = rows_allocated
        self.user_name = user_name
    async def display(self, terminal_width, terminal_height, padding: int = 0, message_multiline_margin: int = 20):
        while True:
            self.synced_display(terminal_width, terminal_height, padding, message_multiline_margin)
            await asyncio.sleep(0.5)

    def synced_display(self, terminal_width, terminal_height, padding: int = 0, message_multiline_margin: int = 20):
        # Move to top left
        print('\033[H',end="")
        # Clear and move down
        for _ in range(self.rows_allocated):
            print('\033[2K\033[B', end="")
        print(f'\033[{self.rows_allocated}F', end="")
        rows_taken = 0
        chatString = []
        for i, message in enumerate(self.message_list):
            message_string = f"{message.user_name}: {message.text}"
            message_length = len(message_string)
            max_message_length_per_line = terminal_width - 2 * padding - message_multiline_margin # When the message takes up multiple lines, add a margin on the side
            border_length = max_message_length_per_line if max_message_length_per_line < message_length else message_length
            
            string = self.chunk_string(message_string, max_message_length_per_line)
            if len(string) > 1:
                if message.user_name == self.user_name:
                    string[-1] += " " * (max_message_length_per_line - len(string[-1]))
                else:
                    string[-1] = " " * (max_message_length_per_line - len(string[-1])) + string[-1]
            string = [LEFT_BOX_BORDER + i + RIGHT_BOX_BORDER for i in string]
            components = [TOP_LEFT_BOX_BORDER + HORIZONTAL_BOX_BORDER * (border_length + 2) + TOP_RIGHT_BOX_BORDER] + string + [BOTTOM_LEFT_BOX_BORDER + HORIZONTAL_BOX_BORDER * (border_length + 2) + "┘"]
            for component in components:
                if not message.user_name == self.user_name:
                    chatString.append( (f"{component:>{terminal_width - padding}}") )
                else:
                    chatString.append( (" " * padding + f"{component:<{terminal_width - padding}}") )
            rows_taken += len(components)
        with patch_stdout():
            for i in range((rows_taken - self.rows_allocated - 1 if rows_taken - self.rows_allocated - 1 >= 0 else 0), rows_taken):
                print(chatString[i])
            if rows_taken - self.rows_allocated - 1 < 0: 
                print("\n" * (self.rows_allocated - rows_taken - 2), end="")
            print(" " * padding + HORIZONTAL_BOX_BORDER * (terminal_width - padding*2) + " " * padding)
            print("\n" * (terminal_height - self.rows_allocated), end="")

    def chunk_string(self, string: str, length: int) -> list[str]:
        # Breaks it up into fixed size parts, obtained from https://stackoverflow.com/questions/18854620/whats-the-best-way-to-split-a-string-into-fixed-length-chunks-and-work-with-the

        return [string[0+i:length+i] for i in range(0, len(string), length)]


class ChatInput:
    def __init__(self, message_list, rows_allocated: int, chat_display):
        self.message_list = message_list
        self.rows_allocated = rows_allocated
        self.current_input = ""
        self.session = PromptSession()
        self.chat_display = chat_display

    async def display(self, terminal_width, terminal_height, padding: int = 0):
        """Displays the divider/padding required for input."""
        while True:
            print("\033[H", end="")
            print(f"\033[{str(terminal_height - self.rows_allocated + 1)}B", end="")

            with patch_stdout():
                ## go to where the input divider should be
                text = await self.session.prompt_async(" " * padding + "> ") 
                self.message_list.append(Message(r"{}".format(text), "Jeremy", True))
                self.chat_display.synced_display(terminal_width, terminal_height, padding)


        
    """def display(self, terminal_width, padding: int = 0, default_text = ""):
        ## allocate rows for the input box
        print("\n" * self.rows_allocated, end="")
        print("\x1b[999H" + "\033[2K \033[F" * self.rows_allocated, end="")
        
        ## Print the input box
        print(" " * padding + HORIZONTAL_BOX_BORDER * (terminal_width - padding*2), end="")
        print(" " * padding)
        text = input(" " * padding + "> ") 
        self.message_list.append(Message(r"{}".format(text), "Jeremy", True))"""
        
    

class ChatApplication:
    def __init__(self):
        self.message_list = [
            Message("Hi!", "Jeremy", True),
            Message("What's up! wefliuyhergoihegliuhetsroigubselighbnserlgjbselirgbnelsihbrgkulserbgoeusrgbouesrbouesrbgluershgb", "Xavier", False)
        ]
        self.user_name = "Jeremy"
        self.terminal_size = os.get_terminal_size()
        self.chat_display = ChatDisplay(self.message_list, self.user_name, self.terminal_size[1])
        self.chat_input = ChatInput(self.message_list, 2, self.chat_display)
        self.padding=2
        asyncio.run(self.main())

    async def main(self):
        """Execute the actual program. Uses async to ensure that user can type while receiving messages."""
        print("\x1b[2J")
        print("\x1b[" + str(self.terminal_size[1] - 2 + 1) + "H", end="")
        print("\033[s", end="")
        display_messages_task = asyncio.create_task(self.chat_display.display(self.terminal_size[0], self.terminal_size[1], self.padding))
        await self.chat_input.display(self.terminal_size[0], self.terminal_size[1], self.padding)


    def refresh_chat(self):
        """Display the chat."""
        print("\033c")
        
        self.chat_display.display(self.terminal_size[0], 2)
        self.chat_input.display(self.terminal_size[0], 2)
        self.print_outer_box_overlay()
        
    def print_outer_box_overlay(self):
        """HW"""
        # Go to top left
        print("\x1b[H", end="")
        # Erase line
        print("\x1b[K", end="")
        print(TOP_LEFT_BOX_BORDER + HORIZONTAL_BOX_BORDER * (self.terminal_size[0] - 2) + TOP_RIGHT_BOX_BORDER, end="")
        
        # Go to bottom left
        print("\x1b[999H", end="")
        # Erase line
        print("\x1b[K", end="")
        print(BOTTOM_LEFT_BOX_BORDER + HORIZONTAL_BOX_BORDER * (self.terminal_size[0] - 2) + BOTTOM_RIGHT_BOX_BORDER, end="")

chat_application = ChatApplication()
