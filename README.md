# flask_template

Sample boilerplate flask project

## Frameworks Used

- Cerberus - input validation
- Flask
- Marshmallow - database schema
- PyJWT
- python-dotenv
- SQLAlchemy - database

## Getting the Code

### Cloning the Git Repository

Run the following command to clone the flask_template Git repository

```
git@github.com:ChrisGambrell/flask_template.git
```

or

```
https://github.com/ChrisGambrell/flask_template.git
```

## Installation

Project is installable using `pip`

```
pip install -e .
```

Add the necessary directories to your `PATH`:

```
Tools/Scripts
```

## Running

```
Tools/Scripts/run
```

## Testing

```
Tools/Scripts/test
```

## API Reference

### `GET /hello`

Gets a hello message

Return:

```
hello, world
```

### `GET /secret`

Tests authentication with a greeting

Headers:

```
Authorization: Bearer [token]
```

Return:

```
{
    hello: [name]
}
```

### `POST /auth/login`

Logs in a user

Input:

```
{
    username: <str>,
    password: <str>
}
```

Return:

```
{
    token: <jwt token>
}
```

### `POST /auth/register`

Registers a user

Input:

```
{
    name: <str>,
    username: <str>,
    password: <str>
}
```

Return:

```
{
    id: <int, primary>,
    name: <str>,
    username: <str>,
    password: <str>,
    tasks: <[Task.id]>
}
```

### `GET /tasks/`

Get all tasks for authenticated user

Headers:

```
Authorization: Bearer [token]
```

Return:

```
[
    {
        id: <int, primary>,
        user: <User.id>,
        body: <str>,
        completed: <bool>,
        updated_at: <DateTime>,
        created_at: <DateTime>,
        user_id: <User.id>
    }
]
```

### `POST /tasks/`

Creates and adds a new task to the database

Headers:

```
Authorization: Bearer [token]
```

Input:

```
{
    body: <str>,
    completed: <bool, nullable>
}
```

Return:

```
{
    id: <int, primary>,
    user: <User.id>,
    body: <str>,
    completed: <bool>,
    updated_at: <DateTime>,
    created_at: <DateTime>,
    user_id: <User.id>
}
```

### `GET /tasks/<task_id>`

Gets a task with a certain ID created by the authenticated user

Headers:

```
Authorization: Bearer [token]
```

Return:

```
{
    id: <int, primary>,
    user: <User.id>,
    body: <str>,
    completed: <bool>,
    updated_at: <DateTime>,
    created_at: <DateTime>,
    user_id: <User.id>
}
```

### `PATCH /tasks/<task_id>`

Updates a task with a certain ID created by the authenticated user

Headers:

```
Authorization: Bearer [token]
```

Input:

```
{
    body: <str, nullable>,
    completed: <bool, nullable>
}
```

Return:

```
{
    id: <int, primary>,
    user: <User.id>,
    body: <str>,
    completed: <bool>,
    updated_at: <DateTime>,
    created_at: <DateTime>,
    user_id: <User.id>
}
```

### `DELETE /tasks/<task_id>`

Deletes a task with a certain ID created by the authenticated user

Headers:

```
Authorization: Bearer [token]
```

Return:

```
{}
```

### `GET /user/`

Gets the authenticated user

Headers:

```
Authorization: Bearer [token]
```

Return:

```
{
    id: <int, primary>,
    name: <str>,
    username: <str>,
    password: <str>,
    tasks: <[Task.id]>
}
```

### `PATCH /user/`

Updates the authenticated user

Headers:

```
Authorization: Bearer [token]
```

Input:

```
{
    name: <str, nullable>,
    username: <str, nullable>
}
```

Return:

```
{
    id: <int, primary>,
    name: <str>,
    username: <str>,
    password: <str>,
    tasks: <[Task.id]>
}
```

### `DELETE /user/`

Deletes the authenticated user

Headers:

```
Authorization: Bearer [token]
```

Return:

```
{}
```

### `GET /user/<user_id>`

Gets a user by their ID

Headers:

```
Authorization: Bearer [token]
```

Return:

```
{
    id: <int, primary>,
    name: <str>,
    username: <str>,
    password: <str>,
    tasks: <[Task.id]>
}
```
