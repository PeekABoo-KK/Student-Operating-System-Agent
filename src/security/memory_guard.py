from src.security.security_rules import security_rules


class MemoryGuard:

    # =========================
    # SCHEMA VALIDATION
    # =========================
    @staticmethod
    def validate_profile_schema(profile: dict) -> dict:
        if not isinstance(profile, dict):
            raise ValueError("Profile must be dict")

        # reject unknown keys (STRICT LOCK)
        for key in profile.keys():
            if key not in security_rules.ALLOWED_SCHEMA_KEYS:
                raise ValueError(f"Forbidden field: {key}")

        return profile

    # =========================
    # PROPOSED UPDATE VALIDATION
    # =========================
    @staticmethod
    def validate_proposed_update(update: dict) -> dict:
        """
        Ensures agents cannot inject malicious memory updates
        """

        if not isinstance(update, dict):
            raise ValueError("Update must be dict")

        if "field" not in update or "new_value" not in update:
            raise ValueError("Invalid update format")

        if update["field"] not in security_rules.ALLOWED_SCHEMA_KEYS:
            raise ValueError("Unauthorized field update")

        return update
