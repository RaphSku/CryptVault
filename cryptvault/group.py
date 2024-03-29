import click
import io
import sys

from click.core       import Context
from click.formatting import HelpFormatter
from rich.console     import Console
from rich.text        import Text
from rich.panel       import Panel

from cryptvault._colors import OriginalColors, WinColors


class CustomGroup(click.Group):
    def format_help(self, ctx: Context, formatter: HelpFormatter):
        string_io = io.StringIO()
        console   = Console(file = string_io, force_terminal = True)

        title = r"""
   ___                 _                    _ _   
  / __\ __ _   _ _ __ | |_/\   /\__ _ _   _| | |_ 
 / / | '__| | | | '_ \| __\ \ / / _` | | | | | __|
/ /__| |  | |_| | |_) | |_ \ V / (_| | |_| | | |_ 
\____/_|   \__, | .__/ \__| \_/ \__,_|\__,_|_|\__|
           |___/|_|                                                           
        """

        headline_accent_color = OriginalColors.HEADLINE_ACCENT_COLOR
        primary_color         = OriginalColors.PRIMARY_COLOR
        text_color            = OriginalColors.TEXT_COLOR
        if sys.platform == "win32":
            headline_accent_color = WinColors.HEADLINE_ACCENT_COLOR
            primary_color         = WinColors.PRIMARY_COLOR
            text_color            = WinColors.TEXT_COLOR

        headline = Text()
        headline.append("Usage: ", style = f"bold {headline_accent_color}")
        headline.append("cryptvault COMMAND [OPTIONS]", style = "bold white")

        # structure: [15][2 whitespaces][5 whitespaces][80], total = 102c
        commands  = [
            "version",
            "start",
            "generate"
        ]

        descriptions = [
            "If you forgot with which version you are working, use me.",
            "Start me already. Kick off this CryptVault server.",
            "If you need a JSON template of the body for posting a request, let me know."
        ]

        help_text = Text()
        help_text.append("\n")
        for command, description in zip(commands, descriptions):
            if len(command) > 15:
                raise ValueError("Command should only be max. 15 characters long!")
            if len(description) > 80:
                raise ValueError("The description of the command should be only max. 40 characters long!")
            help_text.append(f'{command: <17}', style = f"bold {primary_color}")
            help_text.append(f'{description}', style = f"bold {text_color}")
            help_text.append("\n")

        help_panel = Panel(help_text, title = "cryptvault commands", title_align = "left")
        tip_text   = Text("Tip: Use cryptvault [COMMAND] --help to see the possible options for a command", style = f"bold {text_color}")

        console.print(title,
                      "\n\n",
                      headline,
                      help_panel,
                      tip_text)

        formatter.write(string_io.getvalue())