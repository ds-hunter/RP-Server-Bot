import os
import psycopg2
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

# Load the config from the .env file
HOST = os.getenv('DB_HOST')
DATABASE = os.getenv('DB_NAME')
USER = os.getenv('DB_USER')
PASSWORD = os.getenv('DB_PASS')

# Connect to the database
conn = psycopg2.connect(
    host=HOST,
    database=DATABASE,
    user=USER,
    password=PASSWORD
)

# Create a cursor to perform database operations
cur = conn.cursor()

'''
DB SCHEMA
CREATE TABLE players
(
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    charactername VARCHAR(255) NOT NULL,
    level INTEGER NOT NULL,
    dt INTEGER NOT NULL,
    sp INTEGER NOT NULL,
    ryo INTEGER NOT NULL
);

CREATE TABLE history (
    id SERIAL PRIMARY KEY,
    player_id INTEGER NOT NULL,
    affected_field VARCHAR(255) NOT NULL,
    old_value VARCHAR(255) NOT NULL,
    new_value VARCHAR(255) NOT NULL,
    reason TEXT NOT NULL,
    date DATE NOT NULL
);

SIDENOTE: player name is a discord username#tag
'''

# Search for a player in the database by name
def search_player(name):
    # Get the most similar player name from the database case insensitive 
    # cur.execute(f"SELECT name FROM players WHERE name ILIKE '{name}%' ORDER BY name LIMIT 1") (PRONE TO SQL INJECTION)
    cur.execute(f"SELECT name FROM players WHERE name ILIKE %s ORDER BY name LIMIT 1", (name,))
    player_name = cur.fetchone()
    
    # Check if the player exists
    if not player_name:
        return False
    
    # Fetch all rows where the player name is the same as the one we found
    # cur.execute(f"SELECT * FROM players WHERE name = '{player_name[0]}'") (PRONE TO SQL INJECTION)
    cur.execute(f"SELECT * FROM players WHERE name = %s", (player_name[0],))
    player = cur.fetchall()

    # Return the result
    return player

# Create a character in the database
def create_character(charactername, playername, startinglevel):
    # Check if the player already has a character with the same name
    # cur.execute(f"SELECT * FROM players WHERE name = '{playername}' AND charactername = '{charactername}'")
    cur.execute(f"SELECT * FROM players WHERE name = %s AND charactername = %s", (playername, charactername))
    if cur.fetchone():
        return False

    # Create the character
    # cur.execute(f"INSERT INTO players (name, charactername, level, dt, sp, ryo) VALUES ('{playername}', '{charactername}', {startinglevel}, 0, 0, 0)")
    cur.execute(f"INSERT INTO players (name, charactername, level, dt, sp, ryo) VALUES (%s, %s, %s, 0, 0, 0)", (playername, charactername, startinglevel))
    conn.commit()

    # Return success
    return True

# Delete a character from the database
def delete_character(charactername, playername):
    # Check if the player has a character with the same name
    # cur.execute(f"SELECT * FROM players WHERE name = '{playername}' AND charactername = '{charactername}'")
    cur.execute(f"SELECT * FROM players WHERE name = %s AND charactername = %s", (playername, charactername))
    if not cur.fetchone():
        return False

    # Delete the character
    # cur.execute(f"DELETE FROM players WHERE name = '{playername}' AND charactername = '{charactername}'")
    cur.execute(f"DELETE FROM players WHERE name = %s AND charactername = %s", (playername, charactername))
    conn.commit()

    # Return success
    return True

def update_player_name(oldname, newname):
    # Check if the player exists
    cur.execute(f"SELECT * FROM players WHERE name = %s", (oldname,))
    if not cur.fetchone():
        return False

    # Update the player name
    cur.execute(f"UPDATE players SET name = %s WHERE name = %s", (newname, oldname))
    conn.commit()

    # Return success
    return True

# Add DT to a character
def add_dt(charactername, playername, amount, reason):
    # Check if the player has a character with the same name
    # cur.execute(f"SELECT * FROM players WHERE name = '{playername}' AND charactername = '{charactername}'")
    cur.execute(f"SELECT * FROM players WHERE name = %s AND charactername = %s", (playername, charactername))
    if not cur.fetchone():
        return False
    
    # Get the current DT from the player
    # cur.execute(f"SELECT dt FROM players WHERE name = '{playername}' AND charactername = '{charactername}'")
    cur.execute(f"SELECT dt FROM players WHERE name = %s AND charactername = %s", (playername, charactername))
    current_dt = cur.fetchone()[0]

    # Add the amount to the current DT
    new_dt = int(current_dt) + int(amount)

    # Update the DT in the database
    # cur.execute(f"UPDATE players SET dt = '{new_dt}' WHERE name = '{playername}' AND charactername = '{charactername}'")
    cur.execute(f"UPDATE players SET dt = %s WHERE name = %s AND charactername = %s", (new_dt, playername, charactername))
    conn.commit()

    # Add the change to the history
    # cur.execute(f"INSERT INTO history (player_id, affected_field, old_value, new_value, reason, date) VALUES ((SELECT id FROM players WHERE name = '{playername}' AND charactername = '{charactername}'), 'dt', '{current_dt}', '{new_dt}', '{reason}', CURRENT_DATE)")
    cur.execute(f"INSERT INTO history (player_id, affected_field, old_value, new_value, reason, date) VALUES ((SELECT id FROM players WHERE name = %s AND charactername = %s), 'dt', %s, %s, %s, CURRENT_DATE)", (playername, charactername, current_dt, new_dt, reason))
    conn.commit()

    # Return success
    return True

# Add Sp to a character
def add_sp(charactername, playername, amount, reason):
    # Check if the player has a character with the same name
    # cur.execute(f"SELECT * FROM players WHERE name = '{playername}' AND charactername = '{charactername}'")
    cur.execute(f"SELECT * FROM players WHERE name = %s AND charactername = %s", (playername, charactername))
    if not cur.fetchone():
        return False
    
    # Get the current SP from the player
    # cur.execute(f"SELECT sp FROM players WHERE name = '{playername}' AND charactername = '{charactername}'")
    cur.execute(f"SELECT sp FROM players WHERE name = %s AND charactername = %s", (playername, charactername))
    current_sp = cur.fetchone()[0]

    # Add the amount to the current SP
    new_sp = int(current_sp) + int(amount)

    # Update the SP in the database
    # cur.execute(f"UPDATE players SET sp = '{new_sp}' WHERE name = '{playername}' AND charactername = '{charactername}'")
    cur.execute(f"UPDATE players SET sp = %s WHERE name = %s AND charactername = %s", (new_sp, playername, charactername))
    conn.commit()

    # Add the change to the history
    # cur.execute(f"INSERT INTO history (player_id, affected_field, old_value, new_value, reason, date) VALUES ((SELECT id FROM players WHERE name = '{playername}' AND charactername = '{charactername}'), 'sp', '{current_sp}', '{new_sp}', '{reason}', CURRENT_DATE)")
    cur.execute(f"INSERT INTO history (player_id, affected_field, old_value, new_value, reason, date) VALUES ((SELECT id FROM players WHERE name = %s AND charactername = %s), 'sp', %s, %s, %s, CURRENT_DATE)", (playername, charactername, current_sp, new_sp, reason))
    conn.commit()

    # Return success
    return True

# Add Ryo to a character
def add_ryo(charactername, playername, amount, reason):
    # Check if the player has a character with the same name
    # cur.execute(f"SELECT * FROM players WHERE name = '{playername}' AND charactername = '{charactername}'")
    cur.execute(f"SELECT * FROM players WHERE name = %s AND charactername = %s", (playername, charactername))
    if not cur.fetchone():
        return False
    
    # Get the current Ryo from the player
    # cur.execute(f"SELECT ryo FROM players WHERE name = '{playername}' AND charactername = '{charactername}'")
    cur.execute(f"SELECT ryo FROM players WHERE name = %s AND charactername = %s", (playername, charactername))
    current_ryo = cur.fetchone()[0]

    # Add the amount to the current Ryo
    new_ryo = int(current_ryo) + int(amount)

    # Update the Ryo in the database
    # cur.execute(f"UPDATE players SET ryo = '{new_ryo}' WHERE name = '{playername}' AND charactername = '{charactername}'")
    cur.execute(f"UPDATE players SET ryo = %s WHERE name = %s AND charactername = %s", (new_ryo, playername, charactername))
    conn.commit()

    # Add the change to the history
    # cur.execute(f"INSERT INTO history (player_id, affected_field, old_value, new_value, reason, date) VALUES ((SELECT id FROM players WHERE name = '{playername}' AND charactername = '{charactername}'), 'ryo', '{current_ryo}', '{new_ryo}', '{reason}', CURRENT_DATE)")
    cur.execute(f"INSERT INTO history (player_id, affected_field, old_value, new_value, reason, date) VALUES ((SELECT id FROM players WHERE name = %s AND charactername = %s), 'ryo', %s, %s, %s, CURRENT_DATE)", (playername, charactername, current_ryo, new_ryo, reason))
    conn.commit()

    # Return success
    return True

# Spend DT from a character
def spend_dt(charactername, playername, amount, reason):
    # Check if the player has a character with the same name
    # cur.execute(f"SELECT * FROM players WHERE name = '{playername}' AND charactername = '{charactername}'")
    cur.execute(f"SELECT * FROM players WHERE name = %s AND charactername = %s", (playername, charactername))
    if not cur.fetchone():
        return False
    
    # Get the current DT from the player
    # cur.execute(f"SELECT dt FROM players WHERE name = '{playername}' AND charactername = '{charactername}'")
    cur.execute(f"SELECT dt FROM players WHERE name = %s AND charactername = %s", (playername, charactername))
    current_dt = cur.fetchone()[0]

    # Subtract the amount from the current DT
    new_dt = int(current_dt) - int(amount)

    # Update the DT in the database
    # cur.execute(f"UPDATE players SET dt = '{new_dt}' WHERE name = '{playername}' AND charactername = '{charactername}'")
    cur.execute(f"UPDATE players SET dt = %s WHERE name = %s AND charactername = %s", (new_dt, playername, charactername))
    conn.commit()

    # Add the change to the history
    # cur.execute(f"INSERT INTO history (player_id, affected_field, old_value, new_value, reason, date) VALUES ((SELECT id FROM players WHERE name = '{playername}' AND charactername = '{charactername}'), 'dt', '{current_dt}', '{new_dt}', '{reason}', CURRENT_DATE)")
    cur.execute(f"INSERT INTO history (player_id, affected_field, old_value, new_value, reason, date) VALUES ((SELECT id FROM players WHERE name = %s AND charactername = %s), 'dt', %s, %s, %s, CURRENT_DATE)", (playername, charactername, current_dt, new_dt, reason))
    conn.commit()

    # Return success
    return True

# Spend SP from a character
def spend_sp(charactername, playername, amount, reason):
    # Check if the player has a character with the same name
    # cur.execute(f"SELECT * FROM players WHERE name = '{playername}' AND charactername = '{charactername}'")
    cur.execute(f"SELECT * FROM players WHERE name = %s AND charactername = %s", (playername, charactername))
    if not cur.fetchone():
        return False
    
    # Get the current SP from the player
    # cur.execute(f"SELECT sp FROM players WHERE name = '{playername}' AND charactername = '{charactername}'")
    cur.execute(f"SELECT sp FROM players WHERE name = %s AND charactername = %s", (playername, charactername))
    current_sp = cur.fetchone()[0]

    # Subtract the amount from the current SP
    new_sp = int(current_sp) - int(amount)

    # Update the SP in the database
    # cur.execute(f"UPDATE players SET sp = '{new_sp}' WHERE name = '{playername}' AND charactername = '{charactername}'")
    cur.execute(f"UPDATE players SET sp = %s WHERE name = %s AND charactername = %s", (new_sp, playername, charactername))
    conn.commit()

    # Add the change to the history
    # cur.execute(f"INSERT INTO history (player_id, affected_field, old_value, new_value, reason, date) VALUES ((SELECT id FROM players WHERE name = '{playername}' AND charactername = '{charactername}'), 'sp', '{current_sp}', '{new_sp}', '{reason}', CURRENT_DATE)")
    cur.execute(f"INSERT INTO history (player_id, affected_field, old_value, new_value, reason, date) VALUES ((SELECT id FROM players WHERE name = %s AND charactername = %s), 'sp', %s, %s, %s, CURRENT_DATE)", (playername, charactername, current_sp, new_sp, reason))
    conn.commit()

    # Return success
    return True

# Spend Ryo from a character
def spend_ryo(charactername, playername, amount, reason):
    # Check if the player has a character with the same name
    # cur.execute(f"SELECT * FROM players WHERE name = '{playername}' AND charactername = '{charactername}'")
    cur.execute(f"SELECT * FROM players WHERE name = %s AND charactername = %s", (playername, charactername))
    if not cur.fetchone():
        return False
    
    # Get the current Ryo from the player
    # cur.execute(f"SELECT ryo FROM players WHERE name = '{playername}' AND charactername = '{charactername}'")
    cur.execute(f"SELECT ryo FROM players WHERE name = %s AND charactername = %s", (playername, charactername))
    current_ryo = cur.fetchone()[0]

    # Subtract the amount from the current Ryo
    new_ryo = int(current_ryo) - int(amount)

    # Update the Ryo in the database
    # cur.execute(f"UPDATE players SET ryo = '{new_ryo}' WHERE name = '{playername}' AND charactername = '{charactername}'")
    cur.execute(f"UPDATE players SET ryo = %s WHERE name = %s AND charactername = %s", (new_ryo, playername, charactername))
    conn.commit()

    # Add the change to the history
    # cur.execute(f"INSERT INTO history (player_id, affected_field, old_value, new_value, reason, date) VALUES ((SELECT id FROM players WHERE name = '{playername}' AND charactername = '{charactername}'), 'ryo', '{current_ryo}', '{new_ryo}', '{reason}', CURRENT_DATE)")
    cur.execute(f"INSERT INTO history (player_id, affected_field, old_value, new_value, reason, date) VALUES ((SELECT id FROM players WHERE name = %s AND charactername = %s), 'ryo', %s, %s, %s, CURRENT_DATE)", (playername, charactername, current_ryo, new_ryo, reason))
    conn.commit()

    # Return success
    return True

# Get level of a character
def get_level(charactername, playername):
    # Check if the player has a character with the same name
    # cur.execute(f"SELECT * FROM players WHERE name = '{playername}' AND charactername = '{charactername}'")
    cur.execute(f"SELECT * FROM players WHERE name = %s AND charactername = %s", (playername, charactername))
    if not cur.fetchone():
        return False

    # Get the level of the character
    # cur.execute(f"SELECT level FROM players WHERE name = '{playername}' AND charactername = '{charactername}'")
    cur.execute(f"SELECT level FROM players WHERE name = %s AND charactername = %s", (playername, charactername))
    level = cur.fetchone()[0]

    # Return the level
    return level

# Get SP of a character
def get_sp(charactername, playername):
    # Check if the player has a character with the same name
    # cur.execute(f"SELECT * FROM players WHERE name = '{playername}' AND charactername = '{charactername}'")
    cur.execute(f"SELECT * FROM players WHERE name = %s AND charactername = %s", (playername, charactername))
    if not cur.fetchone():
        return False

    # Get the SP of the character
    # cur.execute(f"SELECT sp FROM players WHERE name = '{playername}' AND charactername = '{charactername}'")
    cur.execute(f"SELECT sp FROM players WHERE name = %s AND charactername = %s", (playername, charactername))
    sp = cur.fetchone()[0]

    # Return the SP
    return sp

# Set SP of a character
def set_sp(charactername, playername, amount, old_amount):
    # Check if the player has a character with the same name
    # cur.execute(f"SELECT * FROM players WHERE name = '{playername}' AND charactername = '{charactername}'")
    cur.execute(f"SELECT * FROM players WHERE name = %s AND charactername = %s", (playername, charactername))
    if not cur.fetchone():
        return False

    # Set the SP of the character
    # cur.execute(f"UPDATE players SET sp = '{amount}' WHERE name = '{playername}' AND charactername = '{charactername}'")
    cur.execute(f"UPDATE players SET sp = %s WHERE name = %s AND charactername = %s", (amount, playername, charactername))
    conn.commit()

    # Add the change to the history
    # cur.execute(f"INSERT INTO history (player_id, affected_field, old_value, new_value, reason, date) VALUES ((SELECT id FROM players WHERE name = '{playername}' AND charactername = '{charactername}'), 'sp', '{current_sp}', '{new_sp}', '{reason}', CURRENT_DATE)")
    cur.execute(f"INSERT INTO history (player_id, affected_field, old_value, new_value, reason, date) VALUES ((SELECT id FROM players WHERE name = %s AND charactername = %s), 'sp', %s, %s, %s, CURRENT_DATE)", (playername, charactername, old_amount, amount, "SYSTEM: LEVEL UP"))
    conn.commit()

    # Return success
    return True

# Set the level of a character
def set_level(charactername, playername, amount):
    # Check if the player has a character with the same name
    # cur.execute(f"SELECT * FROM players WHERE name = '{playername}' AND charactername = '{charactername}'")
    cur.execute(f"SELECT * FROM players WHERE name = %s AND charactername = %s", (playername, charactername))
    if not cur.fetchone():
        return False

    # Set the level of the character
    # cur.execute(f"UPDATE players SET level = '{amount}' WHERE name = '{playername}' AND charactername = '{charactername}'")
    cur.execute(f"UPDATE players SET level = %s WHERE name = %s AND charactername = %s", (amount, playername, charactername))
    conn.commit()

    # Add the change to the history
    # cur.execute(f"INSERT INTO history (player_id, affected_field, old_value, new_value, reason, date) VALUES ((SELECT id FROM players WHERE name = '{playername}' AND charactername = '{charactername}'), 'level', '{current_level}', '{new_level}', '{reason}', CURRENT_DATE)")
    cur.execute(f"INSERT INTO history (player_id, affected_field, old_value, new_value, reason, date) VALUES ((SELECT id FROM players WHERE name = %s AND charactername = %s), 'level', %s, %s, %s, CURRENT_DATE)", (playername, charactername, amount-1, amount, "SYSTEM: LEVEL UP"))
    conn.commit()

    # Return success
    return True

# Show history for a character
def show_history(charactername, playername):
    # Check if the player has a character with the same name
    # cur.execute(f"SELECT * FROM players WHERE name = '{playername}' AND charactername = '{charactername}'")
    cur.execute(f"SELECT * FROM players WHERE name = %s AND charactername = %s", (playername, charactername))
    if not cur.fetchone():
        return False

    # Get the history for the character
    # cur.execute(f"SELECT * FROM history WHERE player_id = (SELECT id FROM players WHERE name = '{playername}' AND charactername = '{charactername}')")
    cur.execute(f"SELECT * FROM history WHERE player_id = (SELECT id FROM players WHERE name = %s AND charactername = %s)", (playername, charactername))
    history = cur.fetchall()

    # Return the history
    return history

### DO NOT EDIT BELOW THIS LINE ###
# Check if the database has any data in it
cur.execute("SELECT * FROM history")
if not cur.fetchone():
    print("Running first time database setup for history...")
    # Do the same for history.csv
    with open('history.csv', 'r') as starter_db:
        line_num = 0
        #id%player_id%affected_field%old_value%new_value%reason%date
        # Ignore id 
        # Read the starter_db.csv file line by line
        for line in starter_db:
            # Skip the first line
            if line_num == 0:
                line_num += 1
                continue

            # Split the line into a list
            line = line.split('%')

            # Remove newlines from each element in the list
            for i in range(len(line)):
                line[i] = line[i].replace('\n', '')

            # Remove double and single quotes from each element in the list
            for i in range(len(line)):
                line[i] = line[i].replace('"', '')
                line[i] = line[i].replace("'", '')

            # Convert each element to the correct type
            line[1] = int(line[1])
            line[2] = line[2]
            line[3] = int(line[3])
            line[4] = int(line[4])

            # Store them in variables
            player_id = line[1]
            affected_field = line[2]
            old_value = line[3]
            new_value = line[4]
            reason = line[5]
            date = line[6]

            # Add the player to the database using sql statement
            # cur.execute(f"INSERT INTO history (player_id, affected_field, old_value, new_value, reason, date) VALUES ('{player_id}', '{affected_field}', '{old_value}', '{new_value}', '{reason}', '{date}')")
            cur.execute(f"INSERT INTO history (player_id, affected_field, old_value, new_value, reason, date) VALUES (%s, %s, %s, %s, %s, %s)", (player_id, affected_field, old_value, new_value, reason, date))
            conn.commit()

# Do the same for players.csv
cur.execute("SELECT * FROM players")
if not cur.fetchone():
    # Format id%name%charactername%level%dt%sp%ryo
    print("Running first time database setup for players...")
    with open('players.csv', 'r') as starter_db:
        line_num = 0
        # Ignore id 
        # Read the starter_db.csv file line by line
        for line in starter_db:
            # Skip the first line
            if line_num == 0:
                line_num += 1
                continue

            # Split the line into a list
            line = line.split('%')

            # Remove newlines from each element in the list
            for i in range(len(line)):
                line[i] = line[i].replace('\n', '')

            # Remove double and single quotes from each element in the list
            for i in range(len(line)):
                line[i] = line[i].replace('"', '')
                line[i] = line[i].replace("'", '')

            # Convert each element to the correct type
            line[3] = int(line[3])
            line[4] = int(line[4])
            line[5] = int(line[5])
            line[6] = int(line[6])

            # Store them in variables
            name = line[1]
            charactername = line[2]
            level = line[3]
            dt = line[4]
            sp = line[5]
            ryo = line[6]

            # Add the player to the database using sql statement
            # cur.execute(f"INSERT INTO players (name, charactername, level, dt, sp, ryo) VALUES ('{name}', '{charactername}', '{level}', '{dt}', '{sp}', '{ryo}')")
            cur.execute(f"INSERT INTO players (name, charactername, level, dt, sp, ryo) VALUES (%s, %s, %s, %s, %s, %s)", (name, charactername, level, dt, sp, ryo))
            conn.commit()