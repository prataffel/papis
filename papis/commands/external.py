"""
This module define the entry point for external scripts
to be called by papis.

"""
import os
import re
import logging
from typing import List

import click
import platform

import papis.config
import papis.commands


logger = logging.getLogger("external")


def get_command_help(path: str) -> str:
    """Get help string from external commands."""
    magic_word = papis.config.getstring("scripts-short-help-regex")
    with open(path, "r") as _fd:
        for line in _fd:
            match = re.match(magic_word, line)
            if match:
                return str(match.group(1))
    return "No help message available"


def export_variables() -> None:
    """
    Export environment variables so that external script can access to
    the information
    """
    os.environ["PAPIS_LIB"] = papis.config.get_lib().name
    os.environ["PAPIS_LIB_PATH"] = papis.config.get_lib().path_format()
    os.environ["PAPIS_CONFIG_PATH"] = papis.config.get_config_folder()
    os.environ["PAPIS_CONFIG_FILE"] = papis.config.get_config_file()
    os.environ["PAPIS_SCRIPTS_PATH"] = papis.config.get_scripts_folder()


@click.command(
    context_settings={
        "ignore_unknown_options": True,
        "help_option_names": [],
        }
    )
@click.argument("flags", nargs=-1)
@click.pass_context
def external_cli(ctx: click.core.Context, flags: List[str]) -> None:
    """Actual papis command to call the external command"""
    script = ctx.obj  # type: papis.commands.Script
    path = script.path
    if not path:
        raise Exception("Path for script {} not found".format(script))
    if platform.system() == "Windows":
        # Check for specified script language 
        # (needed for plugins to work under windows)
        exec_word = "#! /usr/bin/env "
        with open(path, 'r') as _fd:
            for line in _fd:
                if line[0:len(exec_word)] == exec_word:
                    cmd_program = line[len(exec_word):-1]
                    if cmd_program == "python3":
                        cmd_program = "python"
                    cmd = [str(cmd_program)] + [path] + list(flags)
    else:
        cmd = [path] + list(flags)
    logger.debug("Calling %s", cmd)
    export_variables()

    import subprocess
    subprocess.call(cmd)
