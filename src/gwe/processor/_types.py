from enum import Enum


class Certainty(str, Enum):
    EXPLICIT = "explicit"
    STRONGLY_IMPLICIT = "strongly_implicit"
    MODERATELY_IMPLICIT = "moderately_implicit"
    WEAKLY_IMPLICIT = "weakly_implicit"
