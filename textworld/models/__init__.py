import random

from pydantic import BaseModel


def populate_with_examples(model: BaseModel) -> dict:
    """Populate fields with example values"""

    result = {}

    for name, field_info in model.model_fields.items():
        if field_info.examples:
            # Populate with example
            result[name] = random.choice(field_info.examples)

    return dict(result)