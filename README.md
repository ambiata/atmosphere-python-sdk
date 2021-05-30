# atmosphere-python-sdk
Python sdk to create custom code interacting with Atmosphere.

Please look at each individual sub folder to find more information about
the libraries you need.

### Sub Packages
## To get started with activities
[activity](/atmosphere/custom_activity)

## To implement a transformer that we support
[transformer](/atmosphere/transformer)

### Test everything
docker build . -t atmosphere
docker run atmosphere scripts/test.sh
