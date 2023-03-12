import io
import sys

from click.core       import Command, Context
from click.formatting import HelpFormatter
from rich.console     import Console
from rich.text        import Text
from rich.panel       import Panel

from cryptvault._colors import OriginalColors, WinColors


class HeadlineMixin:
    def get_headline(self, command: str, description: str) -> Text:
        headline_accent_color = OriginalColors.HEADLINE_ACCENT_COLOR
        if sys.platform == "win32":
            headline_accent_color = WinColors.HEADLINE_ACCENT_COLOR
        
        headline = Text()
        headline.append("Usage: ", style = f"bold {headline_accent_color}")
        headline.append(f"cryptvault {command} [OPTIONS]", style = "bold white")
        headline.append("\n\n")
        headline.append(description, style = "bold white")
        headline.append("\n\n") 

        return headline


class OptionMixin:
    def format_option_text(self, flags, descriptions) -> Text:
        # structure: [--][15][2 whitespaces][-2c][5 whitespaces][80], total = 107c
        primary_color         = OriginalColors.PRIMARY_COLOR
        primary_color_shadow  = OriginalColors.PRIMARY_COLOR_SHADOW
        text_color            = OriginalColors.TEXT_COLOR
        if sys.platform == "win32":
            primary_color         = WinColors.PRIMARY_COLOR
            primary_color_shadow  = WinColors.PRIMARY_COLOR_SHADOW
            text_color            = WinColors.TEXT_COLOR

        option_text = Text()
        option_text.append("\n")
        for flag, short_flag, description in zip(flags.keys(), flags.values(), descriptions):
            if len(flag) > 15:
                raise ValueError("Flag should only be max. 15 characters long!")
            if len(short_flag) > 2:
                raise ValueError("The flag abbreviation should be only max. 2 characters long!")
            if len(description) > 80:
                raise ValueError("The description of the flag should be only max. 40 characters long!")
            option_text.append(f'{flag: <17}', style = f"bold {primary_color}")
            if short_flag != "":
                option_text.append(f'{short_flag: <7}', style = f"bold {primary_color_shadow}")
            else:
                option_text.append(f'{" ": <7}')
            option_text.append(f'{description}', style = f"bold {text_color}")
            option_text.append("\n")

        return option_text


class StartCommand(Command, HeadlineMixin, OptionMixin):
    def format_help(self, ctx: Context, formatter: HelpFormatter) -> None:
        string_io = io.StringIO()
        console   = Console(file = string_io, force_terminal = True)

        headline_description = "Starts the CryptVault Server"
        headline = self.get_headline(command = "start", description = headline_description)

        flags = {
            "--host": "-h",
            "--port": "-p",
            "--sslkeyfile": "",
            "--sslcertfile": "",
            "--help": ""
        }

        descriptions = [
            "host on which the server should run",
            "port assigned to the server",
            "ssl keyfile for enabling https",
            "ssl certificate file for enabling https",
            "Shows this message"
        ]

        option_text   = self.format_option_text(flags = flags, descriptions = descriptions)
        options_panel = Panel(option_text, title = "cryptvault start", title_align = "left")

        console.print(headline,
                      options_panel)

        formatter.write(string_io.getvalue())


class VersionCommand(Command, HeadlineMixin, OptionMixin):
    def format_help(self, ctx: Context, formatter: HelpFormatter) -> None:
        string_io = io.StringIO()
        console   = Console(file = string_io, force_terminal = True)

        headline_description = "Prints the current version of the CryptVault library"
        headline = self.get_headline(command = "version", description = headline_description)

        flags = {
            "--help": ""
        }

        descriptions = [
            "Shows this message"
        ]

        option_text   = self.format_option_text(flags = flags, descriptions = descriptions)
        options_panel = Panel(option_text, title = "cryptvault version", title_align = "left")

        console.print(headline,
                      options_panel)

        formatter.write(string_io.getvalue())


class GenerateCommand(Command, HeadlineMixin, OptionMixin):
    def format_help(self, ctx: Context, formatter: HelpFormatter) -> None:
        string_io = io.StringIO()
        console   = Console(file = string_io, force_terminal = True)

        headline_description = "Generates a JSON body template for a post request"
        headline = self.get_headline(command = "generate", description = headline_description)

        flags = {
            "--help": ""
        }

        descriptions = [
            "Shows this message"
        ]

        option_text   = self.format_option_text(flags = flags, descriptions = descriptions)
        options_panel = Panel(option_text, title = "cryptvault generate", title_align = "left")

        console.print(headline,
                      options_panel)

        formatter.write(string_io.getvalue())