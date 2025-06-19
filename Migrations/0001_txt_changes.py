from yoyo import step

steps = [
    step(
        "ALTER TABLE users ALTER COLUMN password_hash TYPE VARCHAR(512);",
        "ALTER TABLE users ALTER COLUMN password_hash TYPE VARCHAR(128);"
    ),
    step(
        "ALTER TABLE posts ALTER COLUMN text TYPE VARCHAR(512);",
        "ALTER TABLE posts ALTER COLUMN text TYPE VARCHAR(256);"
    )
]