# atmospherex-activity-base

Folder containing the base code to implement an activity custom code.

This folder should help create the following required manifests per custom code:

-   a fastapi server with the required endpoints which AtmosphereX will call
-   an artifact usable by the contextual bandit learner.

This project will need to be installed using pip in each custom code repository, allowing to extend the abstract class
containing all the methods to implement.
e.g.:

```python
from atmospherex_activity_base import BaseActivityCustomCode


class MyClass(BaseActivityCustomCode):
    ...
```

The pip command is:

```shell script
pip install git+ssh://git@github.com/ambiata/atmosphere-python-sdk.git@{tag}#subdirectory=atmospherex_activity_base
```

## Fast validation

To validate fastly that the application has well been built without having to run unittest.

To check the server, after  selecting your module you can run:
```shell script
MODULE='abc' CLASS_NAME='Def' python -m atmospherex_activity_base.server
The server started well
```

To check the mocker, after selecting your module, you can run:
```shell script
$ ACTIVITY_INFERENCE_BASE_URL="abc" REQUESTS_PER_SECOND=3 OUTCOMES_TIMEOUT_SECONDS=10 OUTCOMES_RATE=0.5 MODULE='abc' CLASS_NAME='Def' python -m atmospherex_activity_base.mocker.main_mocker test
All good, the mocker could start.
```

If these commands fail, it means that server or the mocker will not be able to start properly.
This command will return at completion.

## Production-ready Dockerfile example

Simple Dockerfile exmaple to run the base activity server
```Dockerfile
FROM python:3.8.5-slim

# install your module ...

ENV MODULE='path.to.the.module'
ENV CLASS_NAME='ClassName'

EXPOSE 8000

CMD ["uvicorn", "--host",  "0.0.0.0", "--port", "8000", "--timeout-keep-alive", "5", "--workers", "4", "atmospherex_activity_base.server:server"]
```
