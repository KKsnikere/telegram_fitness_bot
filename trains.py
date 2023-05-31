import sqlite3

conn = sqlite3.connect('trains.db')

cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS warmups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        gif_path TEXT NOT NULL
    )
""")

warmups = [
    ('1', 'Jumping Jacks', 'Jump legs apart and raise arms overhead, clap hands together, then return to starting position. Repeat.', 'gifs/jumping_jacks.gif'),
    ('2', 'High Knees', 'Jog in place, bringing knees up towards chest with each step. Continue for designated time.', 'gifs/high_knees.gif'),
    ('3', 'Butt Kicks', 'Jog in place, kicking heels up towards butt with each step. Continue for designated time.', 'gifs/butt_kicks.gif'),
    ('4', 'Arm Circles', 'Rotate arms in circles, starting small and gradually increasing size. Repeat in opposite direction.', 'gifs/arm_circles.gif'),
    ('5', 'Hip Circles', 'Rotate hips in circles, starting small and gradually increasing size. Repeat in opposite direction.', 'gifs/hip_circles.gif'),
    ('6', 'Leg Swings', 'Stand on one leg and swing other leg forward and backward, keeping it straight. Repeat with opposite leg.', 'gifs/leg_swings.gif')
]

cursor.executemany('''INSERT INTO warmups
                      (id, name, description, gif_path)
                      VALUES (?, ?, ?, ?)''', warmups)

conn.close()
