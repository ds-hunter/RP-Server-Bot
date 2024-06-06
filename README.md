# Demonstration Project
This is now an unused project that I am using as a demonstration of experience using Docker, PostgreSQL, and the discord.py library to program a discord bot for an RP server that allowed them to track and save character data within their discord server. Assistance setting the bot up on a VPS was provided.

[Program entry point](app/main.py)

[Database interactions code](app/database.py)

[Bot commands that modified the database](app/cogs/modify.py)

[Bot commands that requested information from the database](app/cogs/request.py)

[Database schema](database/db-scheme.sql)

### Installation
Download and install [docker](https://www.docker.com/products/docker-desktop/)

### Setup
The first thing you need to do is set up the database information in the [docker compose file](docker-compose.yml).

You should change the POSTGRES_USER, POSTGRES_PASSWORD to something unique.

Next, you will need to modify the [.env](app/.env) file and make sure that
DB_USER and DB_PASS match what you have in the docker-compose. If you change the
POSTGRES_DB name you will also need to change the DB_NAME in the .env. After you
have done this you will need to add your discord bot token to the .env BOT_TOKEN entry.

That is all that should be required for setup!
