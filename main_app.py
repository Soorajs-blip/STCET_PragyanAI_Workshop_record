import sqlite3
import pandas as pd
import streamlit as st

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Student Record Management System",
    page_icon="🎓",
    layout="wide"
)

# -----------------------------
# Database Connection
# -----------------------------
conn = sqlite3.connect("students.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    gender TEXT,
    course TEXT,
    email TEXT,
    phone TEXT
)
""")
conn.commit()

# -----------------------------
# Database Functions
# -----------------------------
def add_student(name, age, gender, course, email, phone):
    cursor.execute(
        """
        INSERT INTO students
        (name, age, gender, course, email, phone)
        VALUES (?,?,?,?,?,?)
        """,
        (name, age, gender, course, email, phone),
    )
    conn.commit()


def view_students():
    cursor.execute("SELECT * FROM students")
    return cursor.fetchall()


def update_student(student_id, name, age, gender, course, email, phone):
    cursor.execute(
        """
        UPDATE students
        SET
            name=?,
            age=?,
            gender=?,
            course=?,
            email=?,
            phone=?
        WHERE id=?
        """,
        (name, age, gender, course, email, phone, student_id),
    )
    conn.commit()


def delete_student(student_id):
    cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
    conn.commit()


# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("Navigation")

menu = [
    "Home",
    "Add Student",
    "View Students",
    "Update Student",
    "Delete Student",
]

choice = st.sidebar.radio("Menu", menu)

# -----------------------------
# Home
# -----------------------------
if choice == "Home":

    st.title("🎓 Student Record Management System")

    st.markdown("---")

    st.write(
        """
        ### Features

        - Add Student
        - View Student Records
        - Update Student
        - Delete Student
        - SQLite Database
        - Deployable on Streamlit Cloud
        """
    )

# -----------------------------
# Add Student
# -----------------------------
elif choice == "Add Student":

    st.header("Add Student")

    with st.form("student_form"):

        name = st.text_input("Student Name")

        age = st.number_input(
            "Age",
            min_value=1,
            max_value=100,
            value=18
        )

        gender = st.selectbox(
            "Gender",
            ["Male", "Female", "Other"]
        )

        course = st.text_input("Course")

        email = st.text_input("Email")

        phone = st.text_input("Phone Number")

        submitted = st.form_submit_button("Add Student")

        if submitted:

            add_student(
                name,
                age,
                gender,
                course,
                email,
                phone,
            )

            st.success("Student Added Successfully")

# -----------------------------
# View Students
# -----------------------------
elif choice == "View Students":

    st.header("Student Records")

    data = view_students()

    if data:

        df = pd.DataFrame(
            data,
            columns=[
                "ID",
                "Name",
                "Age",
                "Gender",
                "Course",
                "Email",
                "Phone",
            ],
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download CSV",
            csv,
            "students.csv",
            "text/csv",
        )

    else:

        st.info("No student records found.")

# -----------------------------
# Update Student
# -----------------------------
elif choice == "Update Student":

    st.header("Update Student")

    data = view_students()

    if data:

        ids = [row[0] for row in data]

        selected = st.selectbox(
            "Select Student ID",
            ids
        )

        student = [x for x in data if x[0] == selected][0]

        name = st.text_input(
            "Name",
            student[1]
        )

        age = st.number_input(
            "Age",
            1,
            100,
            student[2]
        )

        gender = st.selectbox(
            "Gender",
            ["Male", "Female", "Other"],
            index=["Male", "Female", "Other"].index(student[3])
        )

        course = st.text_input(
            "Course",
            student[4]
        )

        email = st.text_input(
            "Email",
            student[5]
        )

        phone = st.text_input(
            "Phone",
            student[6]
        )

        if st.button("Update"):

            update_student(
                selected,
                name,
                age,
                gender,
                course,
                email,
                phone,
            )

            st.success("Student Updated Successfully")

    else:

        st.info("No records available.")

# -----------------------------
# Delete Student
# -----------------------------
elif choice == "Delete Student":

    st.header("Delete Student")

    data = view_students()

    if data:

        ids = [row[0] for row in data]

        selected = st.selectbox(
            "Select Student ID",
            ids
        )

        if st.button("Delete"):

            delete_student(selected)

            st.success("Student Deleted Successfully")

    else:

        st.info("No student records found.")

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.caption("Student Record Management System using Streamlit + SQLite")
