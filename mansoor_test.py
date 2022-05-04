
import sqlite3

import pytest

from refactored_code import Appointments


def setUpPatient(username, password, pin):
    con = sqlite3.connect('shms.db')
    cursor = con.cursor()
    sql = "SELECT * FROM pat_signup_info where pat_username=? AND pat_password=?"
    cursor.execute(sql, (username, password))

    row = cursor.fetchone()

    if row == None:
        cur = con.cursor()
        cur.execute("INSERT INTO pat_signup_info VALUES (:pat_username, :pat_password,:pat_sp,NULL,NULL,NULL,NULL,NULL,NULL,NULL)", {
            'pat_username': username,
            'pat_password': password,
            'pat_sp': pin})
        con.close()


@pytest.mark.parametrize("pat_un, values", [
    ("admin", {
        'val1': 'PatientX',
        'val2': '26',
        'val3': 'Male',
        'val4': 'NYC',
        'val5': '1/06/2022',
        'val6': '7875483120'
    })
])
def test_add_appointment(pat_un, values):
    setUpPatient('admin', 'password', 1234)
    # Set Values for the remaining rows
    appointment = Appointments.__new__(Appointments)
    appointment.val1 = values.get('val1')
    appointment.val2 = values.get('val2')
    appointment.val3 = values.get('val3')
    appointment.val4 = values.get('val4')
    appointment.val5 = values.get('val5')
    appointment.val6 = values.get('val6')
    appointment.add_appointment_to_db(pat_un)

    con = sqlite3.connect('shms.db')
    cursor = con.cursor()
    sql = 'SELECT * FROM appointments WHERE pat_username = ?'
    row = cursor.execute(sql, (pat_un,)).fetchone()
    con.close()
    # Assert if row exists
    assert row != None


@pytest.mark.parametrize("pat_un", [
    ("admin")
])
def test_check_appointment(pat_un):
    con = sqlite3.connect('shms.db')
    cursor = con.cursor()
    sql = 'SELECT * FROM appointments WHERE pat_username = ?'
    row = cursor.execute(sql, (pat_un,)).fetchone()
    assert row[7] == 'CONFIRMED'


@pytest.mark.parametrize("pat_un,new_time", [
    ("admin", "17/8/2022"
     )])
def test_update_appointment(pat_un, new_time):
    appointment = Appointments.__new__(Appointments)
    appointment.update_appointment_db(new_time, pat_un)
    # Verify if Record is updated
    con = sqlite3.connect('shms.db')
    cursor = con.cursor()
    sql = 'SELECT * FROM appointments WHERE pat_username = ? AND scheduled_time = ?'
    row = cursor.execute(sql, (pat_un, new_time)).fetchone()
    con.close()
    assert row != None


@pytest.mark.parametrize("pat_un", [
    ("admin")
])
def test_cancel_appointment(pat_un):
    appointment = Appointments.__new__(Appointments)
    appointment.cancel_appointent_from_db(pat_un)

    # Verify if record is deleted From db.
    con = sqlite3.connect('shms.db')
    cursor = con.cursor()
    sql = 'SELECT * FROM appointments WHERE pat_username = ?'
    row = cursor.execute(sql, (pat_un,)).fetchone()
    con.close()
    assert row is None
