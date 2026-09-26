"""Reference implementation for John Brajer's Causal Reactivation mechanism."""
from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class ReactivationRule:
    variable: str
    operator: str
    threshold: Any

    def matches(self, state: Mapping[str, Any]) -> bool:
        if self.variable not in state:
            return False
        value = state[self.variable]
        if self.operator == "gte":
            return value >= self.threshold
        if self.operator == "lte":
            return value <= self.threshold
        if self.operator == "eq":
            return value == self.threshold
        if self.operator == "changed":
            return value != self.threshold
        raise ValueError(f"Unsupported operator: {self.operator}")


def should_reactivate(rules: list[ReactivationRule], state: Mapping[str, Any]) -> bool:
    return bool(rules) and all(rule.matches(state) for rule in rules)


if __name__ == "__main__":
    rules = [ReactivationRule("budget", "gte", 500)]
    print(should_reactivate(rules, {"budget": 650}))
