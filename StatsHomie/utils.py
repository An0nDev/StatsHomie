import time
from typing import List, Optional

def simplify_command (*, message_content: str, prefix: str):
    if not message_content.startswith (prefix):
        return False, None, None
    content_without_prefix = message_content [len (prefix):]
    if content_without_prefix.startswith ('.'):
        command_and_args = content_without_prefix [len ('.'):].split (' ')
        command = command_and_args [0]
        args = command_and_args [1:] if len (command_and_args) > 1 else []
    elif content_without_prefix.startswith (' '):
        command = None
        args = content_without_prefix [len (' '):].split (' ')
    else:
        return True, None, []
    return True, command, args

async def resolve_prefixes_and_exec (*, command_database: dict, command: Optional [str], args: list, execution_target: type):
    if command is None:
        command = command_database ["default"]
    lower_command = command.lower ()
    for command_name, command_info in command_database ["commands"].items ():
        if lower_command == command_name or lower_command in command_info ["aliases"]:
            execution_success = await getattr (execution_target, command_info ["function_name"] if "function_name" in command_info else command_name) (*args)
            return True, execution_success
    return False, False
