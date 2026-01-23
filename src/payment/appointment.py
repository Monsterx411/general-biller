# Appointment scheduling module

from datetime import datetime

class Appointment:
    """Handle appointment scheduling for payments"""
    
    def __init__(self):
        self.appointments = []
    
    def book_appointment(self, biller_name, payment_amount, appointment_date, appointment_time, notes=""):
        """Book an appointment for payment"""
        appointment = {
            "id": len(self.appointments) + 1,
            "biller_name": biller_name,
            "payment_amount": payment_amount,
            "date": appointment_date,
            "time": appointment_time,
            "notes": notes,
            "created_at": datetime.now(),
            "status": "scheduled"
        }
        self.appointments.append(appointment)
        return appointment
    
    def get_appointments(self):
        """Get all appointments"""
        return self.appointments
    
    def cancel_appointment(self, appointment_id):
        """Cancel an appointment"""
        for appointment in self.appointments:
            if appointment["id"] == appointment_id:
                appointment["status"] = "cancelled"
                return True
        return False
