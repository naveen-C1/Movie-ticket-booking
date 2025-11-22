# Movie-ticket-booking
Majestic Movie System (MMS) is a GUI-based cinema manager that handles movie shows, ticket bookings, snacks, and worker records using Tkinter and MySQL. It allows adding, viewing, and deleting data with an easy-to-use interface.
Majestic Movie System (MMS)
---------------------------------------
A premium Tkinter + MySQL based Movie Ticket Booking System.

DESCRIPTION:
A GUI application to manage movie shows, ticket bookings, snacks, and workers. Features include add, display, and delete operations for shows and bookings.

FEATURES:
1. Add Movie Shows
2. Add Snacks
3. Book Tickets
4. Add Workers
5. Display Shows
6. Display Bookings
7. Display Workers
8. Delete Shows
9. Delete Bookings

TECHNOLOGIES USED:
- Python 3
- Tkinter (GUI)
- MySQL Database
- mysql-connector-python

DATABASE STRUCTURE:
TABLE: MyShow
- moviename
- charge
- showtime
- showdate

TABLE: Snacks
- name
- cost

TABLE: Viewers
- name
- ticket
- payment
- showdata
- phone

TABLE: Worker
- name
- work
- salary

HOW TO RUN:
1. Install dependencies:
   pip install mysql-connector-python
   pip install tk

2. Ensure MySQL is installed and running.

3. Run the Python file:
   python app.py

4. Enter MySQL password when prompted.

FUTURE ENHANCEMENTS:
- Ticket PDF generation
- Movie posters
- Export to Excel
- Admin login system
- EXE packaging support

AUTHOR: Naveen C
Your Name
Majestic Movie System – 2025
