from typing import Dict


def choose_template(templates: Dict[str, str], star_rating: int) -> str:
    key = str(star_rating)
    return templates.get(key) or templates.get("fallback", "Thanks for your feedback, {name}!")


def render_template(template: str, reviewer_name: str | None) -> str:
    name = reviewer_name or "there"
    return template.format(name=name)
