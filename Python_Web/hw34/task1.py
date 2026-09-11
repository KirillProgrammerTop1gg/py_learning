from pydantic import BaseModel, EmailStr, field_validator


class User(BaseModel):
    username: str
    email: EmailStr

    @field_validator("username")
    @classmethod
    def no_spaces(cls, v: str) -> str:
        if " " in v:
            raise ValueError("Username не повинен містити пробілів")
        return v


test_cases = [
    {
        "email": "testing@test.fun",
    },
    {
        "username": "Kirill Prog",
        "email": "test@a.fun",
    },
    {
        "username": "BlackHole",
        "email": "test@a",
    },
    {
        "username": "TestUser",
        "email": "test@ a.fun",
    },
    {
        "username": "TestUser",
        "email": "test_email@test.fun",
    },
]

for idx, test_case in enumerate(test_cases):
    print(f"Testing {idx+1} case:")
    try:
        user = User(**test_case)
    except Exception as e:
        print(f"Error: {e.errors()[0]['msg']}")
    else:
        print(f"User created successfully: {user}")
