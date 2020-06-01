from company_graph.func import PATTERNS
from typing import AnyStr, Tuple

class RuleMatcher:

    RULES = PATTERNS

    @classmethod
    def run(cls, x: str) -> Tuple[AnyStr, bool]:
        for rule in RuleMatcher.RULES:
            result, matched = rule.run(x)
            if matched:
                return result, True
        return x, False

    @classmethod
    def __contains__(cls, item: str) -> bool:
        for rule in RuleMatcher.RULES:
            result, matched = rule.run(x)
            if matched:
                return True
        return False
