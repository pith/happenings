# Happenings

[![Test](https://github.com/pith/happenings/actions/workflows/test.yml/badge.svg)](https://github.com/pith/happenings/actions/workflows/test.yml)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/pith/happenings/blob/main/LICENSE.txt)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?logo=fastapi)](https://fastapi.tiangolo.com)

-----

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Production links

- Prod: https://happenings-production.up.railway.app/
- [docs](https://happenings-production.up.railway.app/docs)

## Local usage

* Create env
```console
hatch env create
```

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
  }' | jq .
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
    "location": { "lat": 47.0971567, "long": -1.2727167 }
  }' | jq .
```

## License

`happenings` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
