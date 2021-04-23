# Changelog

## v2.0.0

The custom activity `DefaultPredictionResponse` model has been updated: the `logs` object is now a Pydantic model
instead of a `dict`. We can thus specify the expected keys in it.