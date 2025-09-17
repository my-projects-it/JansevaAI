import streamlit as st
import sqlite3
from hashlib import sha256
from datetime import datetime

# -------------------- DATABASE SETUP --------------------
conn = sqlite3.connect('janseva.db', check_same_thread=False)
c = conn.cursor()

# Users table
c.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT,
            email TEXT)''')

# Problems table
c.execute('''CREATE TABLE IF NOT EXISTS problems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            description TEXT,
            category TEXT,
            status TEXT,
            created_at TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id))''')

# Solutions table
c.execute('''CREATE TABLE IF NOT EXISTS solutions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            problem_id INTEGER,
            user_id INTEGER,
            solution TEXT,
            created_at TEXT,
            FOREIGN KEY(problem_id) REFERENCES problems(id),
            FOREIGN KEY(user_id) REFERENCES users(id))''')
conn.commit()

# -------------------- HELPER FUNCTIONS --------------------
def hash_password(password):
    return sha256(password.encode()).hexdigest()


def verify_user(username, password):
    c.execute('SELECT password FROM users WHERE username=?', (username,))
    data = c.fetchone()
    if data and data[0] == hash_password(password):
        return True
    return False

# -------------------- AUTHENTICATION --------------------
st.title('Janseva App - Citizens Problem Solving Platform')

menu = ['Home', 'Login', 'Signup']
choice = st.sidebar.selectbox('Menu', menu)

if choice == 'Home':
    st.subheader('Welcome to Janseva App')
    st.write('Track problems, submit solutions, get updates, and help your community.')

elif choice == 'Signup':
    st.subheader('Create New Account')
    username = st.text_input('Username')
    email = st.text_input('Email')
    password = st.text_input('Password', type='password')
    role = st.selectbox('Role', ['Citizen','Neta','Adhikari'])

    if st.button('Signup'):
        try:
            c.execute('INSERT INTO users (username, password, role, email) VALUES (?,?,?,?)',
                      (username, hash_password(password), role, email))
            conn.commit()
            st.success('Account created successfully! Please login.')
        except sqlite3.IntegrityError:
            st.error('Username already exists')

elif choice == 'Login':
    st.subheader('Login')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')

    if st.button('Login'):
        if verify_user(username, password):
            st.success(f'Logged in as {username}')
            c.execute('SELECT id, role FROM users WHERE username=?', (username,))
            user_id, role = c.fetchone()

            # -------------------- DASHBOARD --------------------
            st.subheader('Dashboard')
            if role == 'Citizen':
                st.write('Submit a Problem')
                title = st.text_input('Title')
                description = st.text_area('Description')
                category = st.selectbox('Category',['Women & Children','Health','Education','Infrastructure','Other'])
                if st.button('Submit Problem'):
                    c.execute('INSERT INTO problems (user_id, title, description, category, status, created_at) VALUES (?,?,?,?,?,?)',
                              (user_id, title, description, category, 'Pending', datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                    conn.commit()
                    st.success('Problem submitted successfully!')

                st.write('Your Submitted Problems')
                c.execute('SELECT id, title, description, category, status, created_at FROM problems WHERE user_id=?', (user_id,))
                data = c.fetchall()
                for d in data:
                    st.info(f"{d[1]} - {d[4]} ({d[3]})\n{d[2]}\nSubmitted on: {d[5]}")
                    c.execute('SELECT solution, created_at FROM solutions WHERE problem_id=?', (d[0],))
                    solutions = c.fetchall()
                    for s in solutions:
                        st.success(f"Solution: {s[0]}\nAdded on: {s[1]}")

            elif role in ['Neta','Adhikari']:
                st.write('View & Solve Problems')
                c.execute('SELECT p.id, u.username, p.title, p.description, p.category, p.status FROM problems p JOIN users u ON p.user_id=u.id')
                problems = c.fetchall()
                for p_id, uname, title, desc, cat, status in problems:
                    st.info(f"Problem by {uname}: {title} ({status})\nCategory: {cat}\n{desc}")
                    solution = st.text_area(f'Solution for {title}', key=p_id)
                    if st.button(f'Submit Solution {p_id}') and solution:
                        c.execute('INSERT INTO solutions (problem_id, user_id, solution, created_at) VALUES (?,?,?,?)',
                                  (p_id, user_id, solution, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                        c.execute('UPDATE problems SET status=? WHERE id=?', ('Solved', p_id))
                        conn.commit()
                        st.success('Solution submitted and status updated!')

            elif role == 'Admin':
                st.write('Admin Panel: All Users & Problems')
                c.execute('SELECT username, role, email FROM users')
                users = c.fetchall()
                st.write('Users:')
                for u in users:
                    st.write(u)
                c.execute('SELECT p.title, u.username, p.status FROM problems p JOIN users u ON p.user_id=u.id')
                probs = c.fetchall()
                st.write('Problems:')
                for p in probs:
                    st.write(p)
