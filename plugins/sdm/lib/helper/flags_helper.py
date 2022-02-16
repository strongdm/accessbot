import re


class FlagsHelper:
    @staticmethod
    def remove_flags(arguments: str):
        first_flag_match = re.search(r'--\w', arguments)
        command_end_idx = first_flag_match.start() if first_flag_match else None
        return arguments[0:command_end_idx].strip()

    @staticmethod
    def extract_flags(arguments: str):
        flags = {}
        flag_matches = list(re.finditer(r'--[^ ]+', arguments))
        for idx, match in enumerate(flag_matches):
            flag_name = match.group()[2:]
            next_match = flag_matches[idx + 1] if idx + 1 < len(flag_matches) else None
            flag_value_start_idx = match.end() + 1
            flag_value_end_idx = next_match.start() if next_match else None
            flag_value = arguments[flag_value_start_idx:flag_value_end_idx].strip()
            flags[flag_name] = flag_value
        return flags
