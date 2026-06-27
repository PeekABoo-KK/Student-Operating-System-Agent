class IOValidator:

    @staticmethod
    def validate_student_profile(profile: dict):
        required = ["gpa", "major", "year"]
        for r in required:
            if r not in profile:
                raise ValueError(f"Missing field: {r}")

        if not (0.0 <= profile["gpa"] <= 4.0):
            raise ValueError("Invalid GPA range")

        return True

    @staticmethod
    def sanitize_output(data):
        if isinstance(data, list):
            return [d for d in data if d is not None]
        return data
