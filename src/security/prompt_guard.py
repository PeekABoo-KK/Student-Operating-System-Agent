import re
from src.security.security_rules import security_rules


class PromptGuard:

    @staticmethod
    def is_safe(text: str) -> bool:
        if not isinstance(text, str):
            return False

        lowered = text.lower()

        for bad in security_rules.BLOCKLIST:
            if bad in lowered:
                return False

        patterns = [
            r"system\s*:",
            r"user\s*:",
            r"assistant\s*:",
            r"ignore .* instructions",
            r"###"
        ]

        for p in patterns:
            if re.search(p, lowered):
                return False

        return True
