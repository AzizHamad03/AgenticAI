"""Small helper utilities shared across the core app."""
import json
import os

from jinja2 import Environment, FileSystemLoader


def render_markdown(template_name: str, context: dict, template_dir: str) -> str:
    """Render a Jinja2 markdown template into a string prompt."""
    absolute_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), template_dir))
    env = Environment(loader=FileSystemLoader(absolute_dir))
    template = env.get_template(template_name)
    return template.render(context)


def parse_json_output(raw: str) -> dict:
    """
    Safely parse JSON returned by an LLM.

    Language models sometimes wrap JSON in Markdown code fences
    (```json ... ```). This helper strips those fences before parsing so
    callers always receive a clean Python dict.
    """
    if isinstance(raw, dict):
        return raw

    text = (raw or "").strip()
    if text.startswith("```"):
        # Remove the opening fence (``` or ```json) and the trailing fence.
        text = text.split("```", 2)[1] if text.count("```") >= 2 else text
        if text.lstrip().lower().startswith("json"):
            text = text.lstrip()[4:]
        text = text.strip().strip("`").strip()

    return json.loads(text)