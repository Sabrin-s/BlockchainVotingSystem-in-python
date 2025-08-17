import mysql.connector

# ------------ Database Connection ------------------ #
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sabrin@cse",
        database="voting_system"
    )


# ------------ Voter Management ------------------ #
def add_voter(name, phone, gender, dob):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if voter already exists
    cursor.execute("""
        SELECT id, voted 
        FROM voters 
        WHERE name=%s AND phone=%s AND dob=%s
    """, (name, phone, dob))
    voter = cursor.fetchone()

    if voter:
        voter_id, voted = voter
        if voted:
            conn.close()
            return voter_id, "Already voted"
        else:
            conn.close()
            return voter_id, "Eligible"
    else:
        # Add new voter
        cursor.execute("""
            INSERT INTO voters (name, phone, gender, dob, voted, voted_candidate) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (name, phone, gender, dob, 0, None))
        conn.commit()
        voter_id = cursor.lastrowid
        conn.close()
        return voter_id, "Eligible"


# ------------ Candidate Management ------------------ #
def add_candidate(name, party):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO candidates (name, party) VALUES (%s, %s)", (name, party))
    conn.commit()
    conn.close()


def delete_candidate(name):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM candidates WHERE name=%s", (name,))
    conn.commit()
    conn.close()


def get_candidates():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name, party FROM candidates")
    candidates = cursor.fetchall()

    conn.close()
    return candidates


# ------------ Voting Management ------------------ #
def vote_for_candidate(voter_id, candidate_name):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if voter has already voted
    cursor.execute("SELECT voted FROM voters WHERE id=%s", (voter_id,))
    has_voted = cursor.fetchone()

    if has_voted and has_voted[0]:
        conn.close()
        return "You have already voted."

    # Get candidate id
    cursor.execute("SELECT id FROM candidates WHERE name=%s", (candidate_name,))
    candidate = cursor.fetchone()

    if not candidate:
        conn.close()
        return "Candidate not found."

    candidate_id = candidate[0]

    # Record vote in votes table
    cursor.execute("INSERT INTO votes (voter_id, candidate_id) VALUES (%s, %s)", (voter_id, candidate_id))

    # Update voter's voted status and voted_candidate
    cursor.execute("""
        UPDATE voters 
        SET voted=1, voted_candidate=%s 
        WHERE id=%s
    """, (candidate_id, voter_id))

    conn.commit()
    conn.close()

    return "Vote recorded"


# ------------ Results Management ------------------ #
def get_voting_results():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT c.name, c.party, COUNT(v.voter_id) AS total_votes
        FROM candidates c
        LEFT JOIN votes v ON c.id = v.candidate_id
        GROUP BY c.id, c.name, c.party
    """)
    results = cursor.fetchall()

    conn.close()
    return results
