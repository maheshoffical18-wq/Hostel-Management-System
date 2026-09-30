from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)


# =========================================================
# DATA
# =========================================================

students = [
    {
        "name": "Maheshwaran S",
        "register": "C4S22184",
        "department": "BCA",
        "year": "3rd Year",
        "room": "18",
        "phone": "7708043539"
    },
    {
        "name": "Arun Kumar",
        "register": "C4S22101",
        "department": "BCA",
        "year": "2nd Year",
        "room": "12",
        "phone": "9876543210"
    },
    {
        "name": "Priya S",
        "register": "C4S22115",
        "department": "BSc CS",
        "year": "3rd Year",
        "room": "21",
        "phone": "9876501234"
    },
    {
        "name": "Karthik R",
        "register": "C4S22120",
        "department": "BCA",
        "year": "1st Year",
        "room": "15",
        "phone": "9123456789"
    },
    {
        "name": "Divya M",
        "register": "C4S22125",
        "department": "BCom",
        "year": "2nd Year",
        "room": "10",
        "phone": "9000001234"
    },
    {
        "name": "Sanjay P",
        "register": "C4S22130",
        "department": "BCA",
        "year": "3rd Year",
        "room": "25",
        "phone": "9888888888"
    }
]


rooms = [
    {"room": "10", "capacity": 4, "occupied": 2},
    {"room": "12", "capacity": 4, "occupied": 3},
    {"room": "15", "capacity": 4, "occupied": 2},
    {"room": "18", "capacity": 4, "occupied": 4},
    {"room": "21", "capacity": 4, "occupied": 3},
    {"room": "25", "capacity": 4, "occupied": 2}
]


fees_collected = 145000
pending_fees = 80000


complaints = [
    {
        "student": "Arun Kumar",
        "issue": "Fan not working",
        "status": "Pending"
    },
    {
        "student": "Priya S",
        "issue": "Water problem",
        "status": "Resolved"
    }
]


visitors = [
    {
        "name": "Parent - Maheshwaran",
        "student": "Maheshwaran S",
        "date": "29-09-2026"
    },
    {
        "name": "Parent - Arun",
        "student": "Arun Kumar",
        "date": "29-09-2026"
    }
]


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/")
def dashboard():

    total_students = len(students)
    total_rooms = len(rooms)

    # FULL ROOM
    # Room is full only when occupied reaches capacity
    full_rooms = sum(
        1
        for r in rooms
        if r["occupied"] >= r["capacity"]
    )

    # AVAILABLE ROOM
    # Room is available if at least one bed is empty
    available_rooms = sum(
        1
        for r in rooms
        if r["occupied"] < r["capacity"]
    )

    # Total bed capacity
    total_capacity = sum(
        r["capacity"]
        for r in rooms
    )

    # Total occupied beds
    total_occupied = sum(
        r["occupied"]
        for r in rooms
    )

    # Overall bed occupancy percentage
    occupancy_percentage = round(
        (total_occupied / total_capacity) * 100
    ) if total_capacity else 0

    # Fee calculation
    total_expected = fees_collected + pending_fees

    collection_rate = round(
        (fees_collected / total_expected) * 100
    ) if total_expected else 0

    return render_template_string(
        HTML,
        page="dashboard",

        total_students=total_students,
        total_rooms=total_rooms,

        full_rooms=full_rooms,
        available_rooms=available_rooms,

        occupancy_percentage=occupancy_percentage,

        total_capacity=total_capacity,
        total_occupied=total_occupied,

        fees_collected=fees_collected,
        pending_fees=pending_fees,

        total_expected=total_expected,
        collection_rate=collection_rate
    )


# =========================================================
# STUDENTS
# =========================================================

@app.route("/students")
def student_page():

    return render_template_string(
        HTML,
        page="students",
        students=students
    )


# =========================================================
# ADD STUDENT
# =========================================================

@app.route("/add-student", methods=["GET", "POST"])
def add_student():

    if request.method == "POST":

        name = request.form.get("name")
        register = request.form.get("register")
        department = request.form.get("department")
        year = request.form.get("year")
        room = request.form.get("room")
        phone = request.form.get("phone")

        if name and register and department and year and room and phone:

            selected_room = None

            for r in rooms:
                if r["room"] == room:
                    selected_room = r
                    break

            if selected_room and selected_room["occupied"] < selected_room["capacity"]:

                students.append({
                    "name": name,
                    "register": register,
                    "department": department,
                    "year": year,
                    "room": room,
                    "phone": phone
                })

                selected_room["occupied"] += 1

                return redirect(url_for("student_page"))

    return render_template_string(
    HTML,
    page="add_student",
    rooms=rooms
)

# =========================================================
# ROOMS
# =========================================================

@app.route("/rooms")
def rooms_page():

    return render_template_string(
        HTML,
        page="rooms",
        rooms=rooms
    )


# =========================================================
# FEES
# =========================================================

@app.route("/fees")
def fees_page():

    total_expected = (
        fees_collected
        + pending_fees
    )

    collection_rate = round(
        (fees_collected / total_expected) * 100
    ) if total_expected else 0

    return render_template_string(
        HTML,
        page="fees",

        fees_collected=fees_collected,
        pending_fees=pending_fees,

        total_expected=total_expected,
        collection_rate=collection_rate
    )


# =========================================================
# COMPLAINTS
# =========================================================

@app.route("/complaints")
def complaints_page():

    return render_template_string(
        HTML,
        page="complaints",
        complaints=complaints
    )


# =========================================================
# VISITORS
# =========================================================

@app.route("/visitors")
def visitors_page():

    return render_template_string(
        HTML,
        page="visitors",
        visitors=visitors
    )


# =========================================================
# HTML
# =========================================================

HTML = """

<!DOCTYPE html>

<html>

<head>

<title>Hostel Management System</title>

<meta name="viewport"
      content="width=device-width, initial-scale=1">

<style>


/* =====================================================
   RESET
===================================================== */

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    font-family: Arial, sans-serif;
}


body {
    background: #f5f7fb;
    color: #1f2937;
}


/* =====================================================
   SIDEBAR
===================================================== */

.sidebar {

    position: fixed;

    left: 0;
    top: 0;

    width: 235px;
    height: 100vh;

    background: #111827;

    color: white;

    padding: 25px 15px;
}


.logo {

    display: flex;

    align-items: center;

    gap: 12px;

    padding: 10px;

    margin-bottom: 30px;
}


.logo-icon {

    width: 42px;
    height: 42px;

    background: #2563eb;

    border-radius: 10px;

    display: flex;

    align-items: center;

    justify-content: center;

    font-size: 23px;
}


.logo h2 {

    font-size: 17px;
}


.logo p {

    font-size: 11px;

    color: #9ca3af;

    margin-top: 3px;
}


.menu a {

    display: flex;

    align-items: center;

    gap: 13px;

    text-decoration: none;

    color: #d1d5db;

    padding: 13px 15px;

    border-radius: 8px;

    margin: 6px 0;

    font-size: 14px;
}


.menu a:hover,
.menu a.active {

    background: #2563eb;

    color: white;
}


.menu-icon {

    width: 20px;

    text-align: center;
}


/* =====================================================
   MAIN
===================================================== */

.main {

    margin-left: 235px;

    padding: 25px 35px;
}


/* =====================================================
   TOP BAR
===================================================== */

.topbar {

    display: flex;

    justify-content: space-between;

    align-items: center;

    margin-bottom: 30px;
}


.topbar h1 {

    font-size: 26px;
}


.top-right {

    display: flex;

    gap: 15px;

    align-items: center;
}


.date {

    background: white;

    padding: 10px 15px;

    border-radius: 8px;

    border: 1px solid #e5e7eb;

    font-size: 13px;
}


.admin {

    font-size: 14px;

    font-weight: bold;
}


/* =====================================================
   HEADING
===================================================== */

.heading {

    margin-bottom: 20px;
}


.heading h2 {

    font-size: 20px;

    margin-bottom: 6px;
}


.heading p {

    color: #6b7280;

    font-size: 13px;
}


/* =====================================================
   CARDS
===================================================== */

.cards {

    display: grid;

    grid-template-columns:
    repeat(3, 1fr);

    gap: 18px;
}


.card {

    background: white;

    border-radius: 14px;

    padding: 22px;

    border: 1px solid #e5e7eb;

    display: flex;

    align-items: center;

    gap: 18px;
}


.card-icon {

    width: 52px;
    height: 52px;

    border-radius: 12px;

    background: #eff6ff;

    display: flex;

    justify-content: center;

    align-items: center;

    font-size: 24px;
}


.card h3 {

    font-size: 25px;

    margin-bottom: 4px;
}


.card p {

    color: #6b7280;

    font-size: 13px;
}


.green {

    color: #059669;
}


.red {

    color: #dc2626;
}


/* =====================================================
   BOX
===================================================== */

.box {

    background: white;

    border-radius: 14px;

    padding: 25px;

    margin-top: 25px;

    border: 1px solid #e5e7eb;
}


.box-header {

    display: flex;

    justify-content: space-between;

    align-items: center;

    margin-bottom: 20px;
}


.box-header h2 {

    font-size: 18px;
}


/* =====================================================
   BUTTON
===================================================== */

.button {

    background: #2563eb;

    color: white;

    padding: 10px 17px;

    border-radius: 7px;

    text-decoration: none;

    border: none;

    cursor: pointer;

    font-size: 13px;
}


.button:hover {

    background: #1d4ed8;
}


/* =====================================================
   OCCUPANCY
===================================================== */

.occupancy {

    display: grid;

    grid-template-columns:
    1fr 1fr;

    gap: 30px;
}


.circle {

    width: 150px;
    height: 150px;

    border-radius: 50%;

    border: 18px solid #2563eb;

    border-right-color: #dbeafe;

    display: flex;

    align-items: center;

    justify-content: center;

    margin: auto;
}


.circle strong {

    font-size: 25px;
}


/* =====================================================
   TABLE
===================================================== */

table {

    width: 100%;

    border-collapse: collapse;
}


th {

    background: #f9fafb;

    text-align: left;

    padding: 13px;

    font-size: 13px;
}


td {

    padding: 13px;

    border-top: 1px solid #eee;

    font-size: 13px;
}


/* =====================================================
   BADGES
===================================================== */

.badge {

    background: #fef3c7;

    color: #92400e;

    padding: 5px 9px;

    border-radius: 15px;

    font-size: 11px;
}


.badge-green {

    background: #d1fae5;

    color: #065f46;

    padding: 5px 9px;

    border-radius: 15px;

    font-size: 11px;
}


.badge-red {

    background: #fee2e2;

    color: #991b1b;

    padding: 5px 9px;

    border-radius: 15px;

    font-size: 11px;
}


/* =====================================================
   FORM
===================================================== */

.form-box {

    max-width: 650px;

    background: white;

    padding: 30px;

    border-radius: 14px;

    border: 1px solid #e5e7eb;
}


.form-group {

    margin-bottom: 18px;
}


.form-group label {

    display: block;

    font-weight: bold;

    font-size: 13px;

    margin-bottom: 7px;
}


.form-group input,
.form-group select {

    width: 100%;

    padding: 12px;

    border: 1px solid #d1d5db;

    border-radius: 7px;

    outline: none;
}


.form-group input:focus,
.form-group select:focus {

    border-color: #2563eb;
}


/* =====================================================
   PROGRESS
===================================================== */

.progress {

    height: 10px;

    background: #e5e7eb;

    border-radius: 10px;

    overflow: hidden;

    margin-top: 20px;
}


.progress-bar {

    height: 100%;

    background: #10b981;

    border-radius: 10px;
}


/* =====================================================
   RESPONSIVE
===================================================== */

@media(max-width: 900px) {

    .sidebar {

        width: 190px;
    }

    .main {

        margin-left: 190px;
    }

    .cards {

        grid-template-columns:
        1fr 1fr;
    }
}


@media(max-width: 650px) {

    .sidebar {

        display: none;
    }

    .main {

        margin-left: 0;

        padding: 15px;
    }

    .cards {

        grid-template-columns:
        1fr;
    }

    .occupancy {

        grid-template-columns:
        1fr;
    }

}


</style>

</head>


<body>


<!-- =====================================================
     SIDEBAR
===================================================== -->

<div class="sidebar">


    <div class="logo">

        <div class="logo-icon">
            🏢
        </div>

        <div>

            <h2>
                Hostel Management
            </h2>

            <p>
                Admin Portal
            </p>

        </div>

    </div>


    <div class="menu">


        <a href="/"
           class="{{ 'active' if page == 'dashboard' else '' }}">

            <span class="menu-icon">
                ▦
            </span>

            Dashboard

        </a>


        <a href="/students"
           class="{{ 'active' if page == 'students' or page == 'add_student' else '' }}">

            <span class="menu-icon">
                👥
            </span>

            Students

        </a>


        <a href="/rooms"
           class="{{ 'active' if page == 'rooms' else '' }}">

            <span class="menu-icon">
                🛏
            </span>

            Rooms & Capacity

        </a>


        <a href="/fees"
           class="{{ 'active' if page == 'fees' else '' }}">

            <span class="menu-icon">
                💳
            </span>

            Fee Payments

        </a>


        <a href="/complaints"
           class="{{ 'active' if page == 'complaints' else '' }}">

            <span class="menu-icon">
                ⓘ
            </span>

            Complaints

        </a>


        <a href="/visitors"
           class="{{ 'active' if page == 'visitors' else '' }}">

            <span class="menu-icon">
                👤
            </span>

            Visitors Log

        </a>


    </div>

</div>


<!-- =====================================================
     MAIN
===================================================== -->

<div class="main">


    <!-- TOP BAR -->

    <div class="topbar">

        <div>

            {% if page == "dashboard" %}

                <h1>
                    Hostel Management System
                </h1>

            {% elif page == "students" %}

                <h1>
                    Student Management
                </h1>

            {% elif page == "add_student" %}

                <h1>
                    Add Student
                </h1>

            {% elif page == "rooms" %}

                <h1>
                    Rooms & Capacity
                </h1>

            {% elif page == "fees" %}

                <h1>
                    Fee Payments
                </h1>

            {% elif page == "complaints" %}

                <h1>
                    Complaints
                </h1>

            {% elif page == "visitors" %}

                <h1>
                    Visitors Log
                </h1>

            {% endif %}

        </div>


        <div class="top-right">

            <div class="date">

                📅 29 Sep 2026

            </div>


            <div class="admin">

                👤 Admin Portal

            </div>

        </div>

    </div>


<!-- =====================================================
     DASHBOARD
===================================================== -->

{% if page == "dashboard" %}


    <div class="heading">

        <h2>
            System Analytics
        </h2>

        <p>
            Real-time occupancy, fee collection & visitor activity
        </p>

    </div>


    <div class="cards">


        <!-- TOTAL STUDENTS -->

        <div class="card">

            <div class="card-icon">
                👥
            </div>

            <div>

                <h3>
                    {{ total_students }}
                </h3>

                <p>
                    Total Students
                </p>

            </div>

        </div>


        <!-- TOTAL ROOMS -->

        <div class="card">

            <div class="card-icon">
                🛏
            </div>

            <div>

                <h3>
                    {{ total_rooms }}
                </h3>

                <p>
                    Total Rooms
                </p>

            </div>

        </div>


        <!-- FULL ROOMS -->

        <div class="card">

            <div class="card-icon">
                ✓
            </div>

            <div>

                <h3>
                    {{ full_rooms }}
                </h3>

                <p>
                    Full Rooms
                </p>

            </div>

        </div>


        <!-- AVAILABLE ROOMS -->

        <div class="card">

            <div class="card-icon">
                🚪
            </div>

            <div>

                <h3>
                    {{ available_rooms }}
                </h3>

                <p>
                    Available Rooms
                </p>

            </div>

        </div>


        <!-- FEES COLLECTED -->

        <div class="card">

            <div class="card-icon">
                ₹
            </div>

            <div>

                <h3 class="green">
                    ₹{{ "{:,.2f}".format(fees_collected) }}
                </h3>

                <p>
                    Total Fees Collected
                </p>

            </div>

        </div>


        <!-- PENDING FEES -->

        <div class="card">

            <div class="card-icon">
                ⚠
            </div>

            <div>

                <h3 class="red">
                    ₹{{ "{:,.2f}".format(pending_fees) }}
                </h3>
                <p>
                    Pending Fees
                </p>

            </div>

        </div>

    </div>


    <!-- =====================================================
         OCCUPANCY + FEE STATUS
    ===================================================== -->

    <div class="occupancy">


        <!-- ROOM OCCUPANCY -->

        <div class="box">

            <div class="box-header">

                <h2>
                    🏢 Room Occupancy Breakdown
                </h2>

                <a
                    class="button"
                    href="/rooms"
                >
                    View Rooms →
                </a>

            </div>


            <div style="
                display:flex;
                align-items:center;
                gap:40px;
            ">


                <div class="circle">

                    <strong>
                        {{ occupancy_percentage }}%
                    </strong>

                </div>


                <div>

                    <p style="margin-bottom:15px;">

                        🔵 Full Rooms:

                        <b>
                            {{ full_rooms }}
                        </b>

                    </p>


                    <p>

                        🟢 Available Rooms:

                        <b>
                            {{ available_rooms }}
                        </b>

                    </p>


                    <p style="
                        margin-top:15px;
                        color:#6b7280;
                    ">

                        Total Capacity:

                        <b>
                            {{ total_capacity }}
                        </b>

                    </p>


                    <p style="
                        margin-top:8px;
                        color:#6b7280;
                    ">

                        Occupied Beds:

                        <b>
                            {{ total_occupied }}
                        </b>

                    </p>

                </div>

            </div>

        </div>


        <!-- FEE COLLECTION -->

        <div class="box">

            <div class="box-header">

                <h2>
                    💰 Fee Collection Status
                </h2>

                <a href="/fees">
                    All Payments →
                </a>

            </div>


            <h1 class="green">
                {{ collection_rate }}%
            </h1>


            <p style="
                margin-top:8px;
                color:#6b7280;
            ">
                Collection Rate
            </p>


            <div class="progress">

                <div
                    class="progress-bar"
                    style="width:{{ collection_rate }}%;">
                </div>

            </div>


            <p style="
                margin-top:20px;
            ">

                Total Expected:

                <b>
                    ₹{{ "{:,.2f}".format(total_expected) }}
                </b>

            </p>


            <p style="
                margin-top:10px;
            ">

                Collected:

                <b class="green">
                    ₹{{ "{:,.2f}".format(fees_collected) }}
                </b>

            </p>


            <p style="
                margin-top:10px;
            ">

                Pending:

                <b class="red">
                    ₹{{ "{:,.2f}".format(pending_fees) }}
                </b>

            </p>

        </div>

    </div>


<!-- =====================================================
     STUDENTS PAGE
===================================================== -->

{% elif page == "students" %}


    <div class="box">

        <div class="box-header">

            <h2>
                Registered Students
            </h2>

            <a
                href="/add-student"
                class="button"
            >
                + Add Student
            </a>

        </div>


        <table>

            <thead>

                <tr>

                    <th>
                        Name
                    </th>

                    <th>
                        Register No
                    </th>

                    <th>
                        Department
                    </th>

                    <th>
                        Year
                    </th>

                    <th>
                        Room
                    </th>

                    <th>
                        Phone
                    </th>

                </tr>

            </thead>


            <tbody>

                {% for student in students %}

                <tr>

                    <td>
                        <b>
                            {{ student.name }}
                        </b>
                    </td>

                    <td>
                        {{ student.register }}
                    </td>

                    <td>
                        {{ student.department }}
                    </td>

                    <td>
                        {{ student.year }}
                    </td>

                    <td>

                        <span class="badge-green">
                            Room {{ student.room }}
                        </span>

                    </td>

                    <td>
                        {{ student.phone }}
                    </td>

                </tr>

                {% endfor %}

            </tbody>

        </table>

    </div>


<!-- =====================================================
     ADD STUDENT PAGE
===================================================== -->

{% elif page == "add_student" %}


    <div class="form-box">

        <div class="heading">

            <h2>
                Add New Student
            </h2>

            <p>
                Enter student details and assign a room.
            </p>

        </div>


        <form
            method="POST"
            action="/add-student"
        >


            <div class="form-group">

                <label>
                    Student Name
                </label>

                <input
                    type="text"
                    name="name"
                    placeholder="Enter student name"
                    required
                >

            </div>


            <div class="form-group">

                <label>
                    Register Number
                </label>

                <input
                    type="text"
                    name="register"
                    placeholder="Enter register number"
                    required
                >

            </div>


            <div class="form-group">

                <label>
                    Department
                </label>

                <select
                    name="department"
                    required
                >

                    <option value="">
                        Select Department
                    </option>

                    <option value="BCA">
                        BCA
                    </option>

                    <option value="BSc CS">
                        BSc CS
                    </option>

                    <option value="BCom">
                        BCom
                    </option>

                    <option value="BA">
                        BA
                    </option>

                    <option value="BSc">
                        BSc
                    </option>

                </select>

            </div>


            <div class="form-group">

                <label>
                    Year
                </label>

                <select
                    name="year"
                    required
                >

                    <option value="">
                        Select Year
                    </option>

                    <option value="1st Year">
                        1st Year
                    </option>

                    <option value="2nd Year">
                        2nd Year
                    </option>

                    <option value="3rd Year">
                        3rd Year
                    </option>

                </select>

            </div>


            <div class="form-group">

                <label>
                    Room
                </label>

                <select
                    name="room"
                    required
                >

                    <option value="">
                        Select Available Room
                    </option>

                    {% for r in rooms %}

                        {% if r.occupied < r.capacity %}

                        <option value="{{ r.room }}">

                            Room {{ r.room }}
                            —
                            {{ r.capacity - r.occupied }}
                            Bed(s) Available

                        </option>

                        {% endif %}

                    {% endfor %}

                </select>

            </div>


            <div class="form-group">

                <label>
                    Phone Number
                </label>

                <input
                    type="tel"
                    name="phone"
                    placeholder="Enter phone number"
                    required
                >

            </div>


            <button
                type="submit"
                class="button"
            >
                Add Student
            </button>


            <a
                href="/students"
                style="
                    margin-left:10px;
                    color:#6b7280;
                    text-decoration:none;
                    font-size:13px;
                "
            >
                Cancel
            </a>


        </form>

    </div>


<!-- =====================================================
     ROOMS PAGE
===================================================== -->

{% elif page == "rooms" %}


    <div class="box">

        <div class="box-header">

            <h2>
                Room Availability
            </h2>

            <span
                style="
                    color:#6b7280;
                    font-size:13px;
                "
            >
                Total Rooms: {{ rooms|length }}
            </span>

        </div>


        <table>

            <thead>

                <tr>

                    <th>
                        Room
                    </th>

                    <th>
                        Capacity
                    </th>

                    <th>
                        Occupied
                    </th>

                    <th>
                        Available Beds
                    </th>

                    <th>
                        Status
                    </th>

                </tr>

            </thead>


            <tbody>

                {% for r in rooms %}

                <tr>

                    <td>

                        <b>
                            Room {{ r.room }}
                        </b>

                    </td>


                    <td>
                        {{ r.capacity }}
                    </td>


                    <td>
                        {{ r.occupied }}
                    </td>


                    <td>

                        <b>
                            {{ r.capacity - r.occupied }}
                        </b>

                    </td>


                    <td>

                        {% if r.occupied >= r.capacity %}

                            <span class="badge-red">
                                Full
                            </span>

                        {% else %}

                            <span class="badge-green">
                                Available
                            </span>

                        {% endif %}

                    </td>

                </tr>

                {% endfor %}

            </tbody>

        </table>

    </div>


<!-- =====================================================
     FEES PAGE
===================================================== -->

{% elif page == "fees" %}


    <div class="cards">


        <div class="card">

            <div class="card-icon">
                ₹
            </div>

            <div>

                <h3 class="green">
                    ₹{{ "{:,.2f}".format(fees_collected) }}
                </h3>

                <p>
                    Fees Collected
                </p>

            </div>

        </div>


        <div class="card">

            <div class="card-icon">
                ⚠
            </div>

            <div>

                <h3 class="red">
                    ₹{{ "{:,.2f}".format(pending_fees) }}
                </h3>

                <p>
                    Pending Fees
                </p>

            </div>

        </div>


        <div class="card">

            <div class="card-icon">
                💰
            </div>

            <div>

                <h3>
                    ₹{{ "{:,.2f}".format(total_expected) }}
                </h3>

                <p>
                    Total Expected
                </p>

            </div>

        </div>

    </div>


    <div class="box">

        <div class="box-header">

            <h2>
                Fee Collection Progress
            </h2>

            <b class="green">
                {{ collection_rate }}%
            </b>

        </div>


        <div class="progress">

            <div
                class="progress-bar"
                style="width:{{ collection_rate }}%;"
            ></div>

        </div>


        <div style="
            display:flex;
            justify-content:space-between;
            margin-top:15px;
            font-size:13px;
        ">

            <span>
                Collected:
                <b class="green">
                    ₹{{ "{:,.2f}".format(fees_collected) }}
                </b>
            </span>

            <span>
                Pending:
                <b class="red">
                    ₹{{ "{:,.2f}".format(pending_fees) }}
                </b>
            </span>

        </div>

    </div>


<!-- =====================================================
     COMPLAINTS PAGE
===================================================== -->

{% elif page == "complaints" %}


    <div class="box">

        <div class="box-header">

            <h2>
                Student Complaints
            </h2>

            <span
                style="
                    color:#6b7280;
                    font-size:13px;
                "
            >
                {{ complaints|length }} Complaints
            </span>

        </div>


        <table>

            <thead>

                <tr>

                    <th>
                        Student
                    </th>

                    <th>
                        Issue
                    </th>

                    <th>
                        Status
                    </th>

                </tr>

            </thead>


            <tbody>

                {% for complaint in complaints %}

                <tr>

                    <td>
                        <b>
                            {{ complaint.student }}
                        </b>
                    </td>


                    <td>
                        {{ complaint.issue }}
                    </td>


                    <td>

                        {% if complaint.status == "Resolved" %}

                            <span class="badge-green">
                                Resolved
                            </span>

                        {% else %}

                            <span class="badge">
                                Pending
                            </span>

                        {% endif %}

                    </td>

                </tr>

                {% endfor %}

            </tbody>

        </table>

    </div>


<!-- =====================================================
     VISITORS PAGE
===================================================== -->

{% elif page == "visitors" %}


    <div class="box">

        <div class="box-header">

            <h2>
                Visitors Log
            </h2>

            <span
                style="
                    color:#6b7280;
                    font-size:13px;
                "
            >
                Recent Visitors
            </span>

        </div>


        <table>

            <thead>

                <tr>

                    <th>
                        Visitor Name
                    </th>

                    <th>
                        Student
                    </th>

                    <th>
                        Date
                    </th>

                </tr>

            </thead>


            <tbody>

                {% for visitor in visitors %}

                <tr>

                    <td>

                        <b>
                            {{ visitor.name }}
                        </b>

                    </td>


                    <td>
                        {{ visitor.student }}
                    </td>


                    <td>

                        <span class="badge-green">
                            {{ visitor.date }}
                        </span>

                    </td>

                </tr>

                {% endfor %}

            </tbody>

        </table>

    </div>


{% endif %}


</div>


</body>

</html>

"""


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )
