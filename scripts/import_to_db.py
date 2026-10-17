    toolbox_fields(id, entry_id, field_name, field_value)

Every column of an HTML table that is not a name, a link column or the
popularity column is stored as one row in ``toolbox_fields`` so that tables
with different columns (tools, languages, .NET versions, syntax reference...)
share one schema.

Credentials are read from environment variables or a ``.env`` file placed next
