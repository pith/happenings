# Happenings

[![PyPI - Version](https://img.shields.io/pypi/v/happenings.svg)](https://pypi.org/project/happenings)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/happenings.svg)](https://pypi.org/project/happenings)

-----

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Installation

```console
hatch env create
```

## Usage

* Start the server:
```
hatch run happenings
```

* Signup
```console
curl http://localhost:8000/signup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "JohnDoe44",
    "email": "john.doe@gmail.com",
    "password": "123"
  }' | jq .
```

* login
```console
curl http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "JohnDoe44",
    "password": "123"
  }' | jq
```

* Create an event
```console
curl http://localhost:8000/events \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJKb2huRG9lNDQiLCJleHAiOjE3NDg5MDUxNDMsInR5cGUiOiJhY2Nlc3MifQ.EceWFgI3lZqTrmJIalxa9gQ3yt6rq6WEwe-GL9c3oGI" \
  -d '{
    "name": "Hellfest",
    "start_datetime": "2025-06-19T10:00:00",
    "end_datetime": "2025-06-22T16:00:00",
    "location": { "lat": 47.0971567, "long": -1.2727167}
  }' | jq
```

## License

`happenings` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
