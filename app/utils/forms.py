from datetime import datetime
from sqlalchemy import Integer, Float, Boolean, DateTime, Text


def coerce_value(value, col_type):
    if isinstance(col_type, Integer):
        return int(value) if value not in (None, "", "None") else None
    if isinstance(col_type, Float):
        return float(value) if value not in (None, "", "None") else None
    if isinstance(col_type, Boolean):
        return str(value).lower() in ("on", "true", "1", "yes")
    if isinstance(col_type, DateTime):
        if not value:
            return None
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            return datetime.strptime(value, "%Y-%m-%dT%H:%M")
    if isinstance(col_type, Text):
        return value or None
    return value if value != "" else None


def apply_form_to_model(obj, form_data, field_meta, user_id):
    for f in field_meta:
        name = f["name"]
        if name not in form_data:
            continue
        value = form_data.get(name)
        setattr(obj, name, coerce_value(value, obj.__table__.columns[name].type))
    obj.updated_by = user_id