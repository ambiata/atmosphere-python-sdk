# Changelog

## v3.0.0

### Breaking change

The `AtmospherexAPI` client init method is now requiring a second attribute `auth_settings` to configure how to generate
the jwt token sent to Atmosphere. If set to None, the client will not add the authorization header in the request.

## v2.0.0

The custom activity `DefaultPredictionResponse` model has been updated: the `logs` object is now a Pydantic model
instead of a `dict`. We can thus specify the expected keys in it.