import re

class ArgumentsHelper:
    def remove_flags(self, arguments: str):
        """
        Remove all flags from the arguments string
        """
        first_flag_match = re.search(r'--\w', arguments)
        command_end_idx = first_flag_match.start() if first_flag_match else None
        return arguments[0:command_end_idx].strip()

    def extract_flags(self, arguments: str, validators: dict = {}):
        flags = {}
        flag_matches = list(re.finditer(r'--[^ ]+', arguments))
        for idx, match in enumerate(flag_matches):
            flag_name = match.group()[2:]
            next_match = flag_matches[idx + 1] if idx + 1 < len(flag_matches) else None
            flag_value_start_idx = match.end() + 1
            flag_value_end_idx = next_match.start() if next_match else None
            flag_value = arguments[flag_value_start_idx:flag_value_end_idx].strip()
            validator = validators.get(flag_name)
            if not validator or validator(flag_value):
                flags[flag_name] = flag_value
        return flags

    def check_required_flags(self, valid_flags: list, required_flags: str, extracted_flags: dict):
        if required_flags is None:
            return
        missing_required_flags = []
        for required_flag in required_flags.split(" "):
            if required_flag in valid_flags and extracted_flags.get(required_flag) is None:
                missing_required_flags.append(required_flag)
        if len(missing_required_flags) > 0:
            raise Exception(f'Missing required flags: {", ".join(missing_required_flags)}.')
