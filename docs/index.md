# networking-web

[![Build Status](https://travis-ci.org/kob22/networking-web.svg?branch=master)](https://travis-ci.org/kob22/networking-web)
[![Built with](https://img.shields.io/badge/Built_with-Cookiecutter_Django_Rest-F7B633.svg)](https://github.com/agconti/cookiecutter-django-rest)

Simple app for manage mutual friendship.
# Assumptions
- The service does not have to generate UIDs, they are received from callers of the
service.
- Friendship relationship is mutual, that is: if A is friend of B, then B is also a friend of A
- so I choose to store only one record for relationship, 
- always in first column (first_friend) UID is smaller than in second (second_friend)
- if UID first_friend is bigger than UID second_friend, they are swapped (for user the order doesn't matter)

# Prerequisites

- [Docker](https://docs.docker.com/docker-for-mac/install/)  

# Local Development

Start the dev server for local development:
```bash
docker-compose build
docker-compose up 
```

Run a command inside the docker container:

```bash
docker-compose run --rm web [command]
```

## Add a new friend

**Request**:

`POST` `/api/add_friendship/`

Parameters:

Name       | Type   | Required | Description
-----------|--------|----------|------------
first_friend   | int > 0 | Yes      | first UID
second_friend   | int > 0 | Yes      | second UID
**Example**:

`POST` `http://0.0.0.0:8000/api/add_friendship/`
```json
{
    "first_friend": 55,
    "second_friend": 322
}
```

**Response**:

```json
Content-Type application/json
201 Created

{
    "first_friend": 55,
    "second_friend": 322
}
```

## Remove a new friend

**Request**:

`POST` `/api/remove_friendship/`

Parameters:

Name       | Type   | Required | Description
-----------|--------|----------|------------
first_friend   | int > 0 | Yes      | first UID
second_friend   | int > 0 | Yes      | second UID
**Example**:

`POST` `http://0.0.0.0:8000/api/remove_friendship/`
```json
{
    "first_friend": 55,
    "second_friend": 322
}
```

**Response**:

```json
Content-Type application/json
204 No Content

```

## Retrieving friends list

**Request**:

`GET` `/api/find_friends/:UID/`

Parameters:

Name       | Type   | Required | Description
-----------|--------|----------|------------
UID   | int > 0| Yes      | UID

**Example**:

`GET` `http://127.0.0.1:8000/api/find_friends/55/`

**Response**:

```json
Content-Type application/json
200 OK
[
    19,
    252,
    2
]
```
