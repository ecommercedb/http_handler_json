#### logging-handler
Subclass of logging.handlers.HTTPHandler, that emits logs as JSON, instead of form-data

##### Installation
```bash
pip install python -m pip install git+https://github.com/ecommercedb/logging-handler.git
```

##### Usage
```python
import logging.handlers
from logging_handler import JsonHttpHandler

logger = logging.getLogger('my_logger')

http_handler = JsonHttpHandler(
    'IP:PORT',
    '/path/to/endpoint',
    method='POST',
    secure=True|False,
)
stream_handler = logging.StreamHandler()

logger.addHandler(stream_handler)
logger.addHandler(http_handler)

logger.setLevel(logging.INFO)
logger.info("Hello, world!")
```

## Development
### Run pre-commit locally
```bash
pre-commit run --show-diff-on-failure --color=always --all-files
```
