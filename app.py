from flask import Flask, render_template, request, redirect, url_for, flash, g
import sqlite3
import os
from datetime import date

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'change-this-secret-before-production')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.environ.get('DATABASE_PATH', os.path.join(BASE_DIR, 'hospital.db'))


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute('PRAGMA foreign_keys = ON')
    return g.db


@app.teardown_appcontext
def close_db(_error=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    with get_db() as db:
        db.executescript('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            phone TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialization TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,
            appointment_date TEXT NOT NULL,
            notes TEXT DEFAULT '',
            FOREIGN KEY(patient_id) REFERENCES patients(id) ON DELETE CASCADE,
            FOREIGN KEY(doctor_id) REFERENCES doctors(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS medical_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            disease TEXT NOT NULL,
            medicine TEXT NOT NULL,
            record_date TEXT NOT NULL,
            FOREIGN KEY(patient_id) REFERENCES patients(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            doctor_fee REAL NOT NULL,
            medicine_fee REAL NOT NULL,
            total REAL NOT NULL,
            bill_date TEXT NOT NULL,
            FOREIGN KEY(patient_id) REFERENCES patients(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 0,
            price REAL NOT NULL DEFAULT 0
        );
        ''')


@app.context_processor
def inject_globals():
    return {'today': date.today().isoformat()}


@app.route('/')
def dashboard():
    with get_db() as db:
        counts = {table: db.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0] for table in
                  ['patients', 'doctors', 'appointments', 'medical_records', 'bills', 'medicines']}
        recent_appointments = db.execute('''SELECT a.id, a.appointment_date, p.name AS patient, d.name AS doctor
            FROM appointments a JOIN patients p ON p.id=a.patient_id JOIN doctors d ON d.id=a.doctor_id
            ORDER BY a.appointment_date DESC, a.id DESC LIMIT 5''').fetchall()
        recent_patients = db.execute('SELECT * FROM patients ORDER BY id DESC LIMIT 5').fetchall()
    return render_template('dashboard.html', counts=counts, recent_appointments=recent_appointments,
                           recent_patients=recent_patients, page='dashboard')


@app.route('/patients', methods=['GET', 'POST'])
def patients():
    with get_db() as db:
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            age_text = request.form.get('age', '').strip()
            phone = request.form.get('phone', '').strip()
            if not name or not age_text.isdigit() or int(age_text) < 0 or not phone:
                flash('Enter a patient name, valid age and phone number.', 'error')
            else:
                db.execute('INSERT INTO patients(name, age, phone) VALUES (?, ?, ?)', (name, int(age_text), phone))
                db.commit()
                flash('Patient registered successfully.', 'success')
                return redirect(url_for('patients'))
        rows = db.execute('SELECT * FROM patients ORDER BY id DESC').fetchall()
    return render_template('patients.html', patients=rows, page='patients')


@app.route('/patients/delete/<int:patient_id>', methods=['POST'])
def delete_patient(patient_id):
    with get_db() as db:
        db.execute('DELETE FROM patients WHERE id=?', (patient_id,))
        db.commit()
    flash('Patient and linked records deleted.', 'success')
    return redirect(url_for('patients'))


@app.route('/doctors', methods=['GET', 'POST'])
def doctors():
    with get_db() as db:
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            specialization = request.form.get('specialization', '').strip()
            if not name or not specialization:
                flash('Enter doctor name and specialization.', 'error')
            else:
                db.execute('INSERT INTO doctors(name, specialization) VALUES (?, ?)', (name, specialization))
                db.commit()
                flash('Doctor added successfully.', 'success')
                return redirect(url_for('doctors'))
        rows = db.execute('SELECT * FROM doctors ORDER BY id DESC').fetchall()
    return render_template('doctors.html', doctors=rows, page='doctors')


@app.route('/doctors/delete/<int:doctor_id>', methods=['POST'])
def delete_doctor(doctor_id):
    with get_db() as db:
        db.execute('DELETE FROM doctors WHERE id=?', (doctor_id,))
        db.commit()
    flash('Doctor and linked appointments deleted.', 'success')
    return redirect(url_for('doctors'))


@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
    with get_db() as db:
        if request.method == 'POST':
            patient_id = request.form.get('patient_id', type=int)
            doctor_id = request.form.get('doctor_id', type=int)
            appointment_date = request.form.get('appointment_date', '').strip()
            notes = request.form.get('notes', '').strip()
            if not patient_id or not doctor_id or not appointment_date:
                flash('Choose a patient, doctor and appointment date.', 'error')
            else:
                db.execute('INSERT INTO appointments(patient_id, doctor_id, appointment_date, notes) VALUES (?, ?, ?, ?)',
                           (patient_id, doctor_id, appointment_date, notes))
                db.commit()
                flash('Appointment booked successfully.', 'success')
                return redirect(url_for('appointments'))
        rows = db.execute('''SELECT a.*, p.name AS patient, d.name AS doctor, d.specialization
            FROM appointments a JOIN patients p ON p.id=a.patient_id JOIN doctors d ON d.id=a.doctor_id
            ORDER BY a.appointment_date DESC, a.id DESC''').fetchall()
        patient_rows = db.execute('SELECT id, name FROM patients ORDER BY name').fetchall()
        doctor_rows = db.execute('SELECT id, name, specialization FROM doctors ORDER BY name').fetchall()
    return render_template('appointments.html', appointments=rows, patients=patient_rows, doctors=doctor_rows, page='appointments')


@app.route('/appointments/delete/<int:appointment_id>', methods=['POST'])
def delete_appointment(appointment_id):
    with get_db() as db:
        db.execute('DELETE FROM appointments WHERE id=?', (appointment_id,))
        db.commit()
    flash('Appointment deleted.', 'success')
    return redirect(url_for('appointments'))


@app.route('/records', methods=['GET', 'POST'])
def records():
    with get_db() as db:
        if request.method == 'POST':
            patient_id = request.form.get('patient_id', type=int)
            disease = request.form.get('disease', '').strip()
            medicine = request.form.get('medicine', '').strip()
            record_date = request.form.get('record_date', '').strip()
            if not patient_id or not disease or not medicine or not record_date:
                flash('Complete all medical record fields.', 'error')
            else:
                db.execute('INSERT INTO medical_records(patient_id, disease, medicine, record_date) VALUES (?, ?, ?, ?)',
                           (patient_id, disease, medicine, record_date))
                db.commit()
                flash('Medical record added successfully.', 'success')
                return redirect(url_for('records'))
        rows = db.execute('''SELECT r.*, p.name AS patient FROM medical_records r
            JOIN patients p ON p.id=r.patient_id ORDER BY r.record_date DESC, r.id DESC''').fetchall()
        patient_rows = db.execute('SELECT id, name FROM patients ORDER BY name').fetchall()
    return render_template('records.html', records=rows, patients=patient_rows, page='records')


@app.route('/records/delete/<int:record_id>', methods=['POST'])
def delete_record(record_id):
    with get_db() as db:
        db.execute('DELETE FROM medical_records WHERE id=?', (record_id,))
        db.commit()
    flash('Medical record deleted.', 'success')
    return redirect(url_for('records'))


@app.route('/billing', methods=['GET', 'POST'])
def billing():
    with get_db() as db:
        if request.method == 'POST':
            patient_id = request.form.get('patient_id', type=int)
            doctor_fee = request.form.get('doctor_fee', type=float)
            medicine_fee = request.form.get('medicine_fee', type=float)
            bill_date = request.form.get('bill_date', '').strip()
            if not patient_id or doctor_fee is None or medicine_fee is None or not bill_date or doctor_fee < 0 or medicine_fee < 0:
                flash('Enter a patient, date and non-negative fees.', 'error')
            else:
                total = round(doctor_fee + medicine_fee, 2)
                db.execute('INSERT INTO bills(patient_id, doctor_fee, medicine_fee, total, bill_date) VALUES (?, ?, ?, ?, ?)',
                           (patient_id, doctor_fee, medicine_fee, total, bill_date))
                db.commit()
                flash(f'Bill generated successfully. Total: ₹{total:.2f}', 'success')
                return redirect(url_for('billing'))
        rows = db.execute('''SELECT b.*, p.name AS patient FROM bills b JOIN patients p ON p.id=b.patient_id
            ORDER BY b.bill_date DESC, b.id DESC''').fetchall()
        patient_rows = db.execute('SELECT id, name FROM patients ORDER BY name').fetchall()
        total_revenue = db.execute('SELECT COALESCE(SUM(total), 0) FROM bills').fetchone()[0]
    return render_template('billing.html', bills=rows, patients=patient_rows, total_revenue=total_revenue, page='billing')


@app.route('/billing/delete/<int:bill_id>', methods=['POST'])
def delete_bill(bill_id):
    with get_db() as db:
        db.execute('DELETE FROM bills WHERE id=?', (bill_id,))
        db.commit()
    flash('Bill deleted.', 'success')
    return redirect(url_for('billing'))


@app.route('/pharmacy', methods=['GET', 'POST'])
def pharmacy():
    with get_db() as db:
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            quantity = request.form.get('quantity', type=int)
            price = request.form.get('price', type=float)
            if not name or quantity is None or price is None or quantity < 0 or price < 0:
                flash('Enter a medicine name and valid non-negative quantity and price.', 'error')
            else:
                existing = db.execute('SELECT id FROM medicines WHERE lower(name)=lower(?)', (name,)).fetchone()
                if existing:
                    db.execute('UPDATE medicines SET quantity=quantity+?, price=? WHERE id=?', (quantity, price, existing['id']))
                    flash('Medicine stock updated.', 'success')
                else:
                    db.execute('INSERT INTO medicines(name, quantity, price) VALUES (?, ?, ?)', (name, quantity, price))
                    flash('Medicine added successfully.', 'success')
                db.commit()
                return redirect(url_for('pharmacy'))
        rows = db.execute('SELECT * FROM medicines ORDER BY name').fetchall()
    return render_template('pharmacy.html', medicines=rows, page='pharmacy')


@app.route('/pharmacy/delete/<int:medicine_id>', methods=['POST'])
def delete_medicine(medicine_id):
    with get_db() as db:
        db.execute('DELETE FROM medicines WHERE id=?', (medicine_id,))
        db.commit()
    flash('Medicine deleted.', 'success')
    return redirect(url_for('pharmacy'))


@app.route('/reports')
def reports():
    with get_db() as db:
        counts = {table: db.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0] for table in
                  ['patients', 'doctors', 'appointments', 'medical_records', 'bills', 'medicines']}
        revenue = db.execute('SELECT COALESCE(SUM(total), 0) FROM bills').fetchone()[0]
        low_stock = db.execute('SELECT * FROM medicines WHERE quantity < 10 ORDER BY quantity ASC').fetchall()
        recent_bills = db.execute('''SELECT b.*, p.name AS patient FROM bills b JOIN patients p ON p.id=b.patient_id
            ORDER BY b.bill_date DESC, b.id DESC LIMIT 10''').fetchall()
    return render_template('reports.html', counts=counts, revenue=revenue, low_stock=low_stock, bills=recent_bills, page='reports')


@app.errorhandler(404)
def not_found(_error):
    return render_template('error.html', code=404, message='The page you requested was not found.'), 404


if __name__ == "__main__":
    with app.app_context():
        init_db()

    app.run(debug=True)
