import io

from click.core       import Command, Context
from click.formatting import HelpFormatter
from rich.console     import Console
from rich.text        import Text
from rich.panel       import Panel


class OptionMixin:
    def format_option_text(self, flags, descriptions) -> Text:
        # structure: [--][15][2 whitespaces][-2c][5 whitespaces][80], total = 107c
        primary_color        = "rgb(151, 245, 191)"
        primary_color_shadow = "rgb(40, 198, 106)"
        text_color           = "white"

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


class StartCommand(Command, OptionMixin):
    def format_help(self, ctx: Context, formatter: HelpFormatter) -> None:
        string_io = io.StringIO()
        console   = Console(file = string_io, force_terminal = True)

        headline = Text()
        headline.append("Usage: ", style = "bold yellow")
        headline.append("cryptvault start [OPTIONS]", style = "bold white")
        headline.append("\n\n")
        headline.append("Starts the CryptVault Server", style = "bold white")
        headline.append("\n\n")

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
        options_panel = Panel(option_text, title = "cryptvault version", title_align = "left")

        console.print(headline,
                      options_panel)

        formatter.write(string_io.getvalue())


class VersionCommand(Command, OptionMixin):
    def format_help(self, ctx: Context, formatter: HelpFormatter) -> None:
        string_io = io.StringIO()
        console   = Console(file = string_io, force_terminal = True)

        headline = Text()
        headline.append("Usage: ", style = "bold yellow")
        headline.append("cryptvault version [OPTIONS]", style = "bold white")
        headline.append("\n\n")
        headline.append("Prints the current version of the CryptVault library", style = "bold white")
        headline.append("\n\n")

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


class GenerateCommand(Command, OptionMixin):
    def format_help(self, ctx: Context, formatter: HelpFormatter) -> None:
        string_io = io.StringIO()
        console   = Console(file = string_io, force_terminal = True)

        headline = Text()
        headline.append("Usage: ", style = "bold yellow")
        headline.append("cryptvault generate [OPTIONS]", style = "bold white")
        headline.append("\n\n")
        headline.append("Generates a JSON body template for a post request", style = "bold white")
        headline.append("\n\n")

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