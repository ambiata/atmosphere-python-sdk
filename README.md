# atmosphere-python-sdk
Python sdk to create custom code interacting with Atmosphere.

Please look at each individual sub folder to find more information about
the libraries you need.

### Sub Packages
- [To get started with activities](/atmosphere/custom_activity)
- [To create a new method](/atmosphere/method)

### Test everything
```shell
docker build . -t atmosphere
docker run atmosphere scripts/test.sh
```
