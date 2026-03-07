from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

mom_data = {
    "title": "Botivate Fake MOM - Project Phoenix",
    "organization": "Botivate Service LLP",
    "meeting_type": "Monthly Review",
    "date": "2026-03-07",
    "time": "11:39:00",
    "venue": "Conference Room",
    "called_by": "Satyendra Tandan",
    "prepared_by": "Pratap",
    "attendees": [
        {"user_name": "Prabhat Kumar Singh", "email": "prabhatkumarsictc7070@gmail.com", "attendance_status": "Present"},
        {"user_name": "Ghanshyam Dewangan", "email": "ghanshyamdewangan1472@gmail.com", "attendance_status": "Present"},
        {"user_name": "Gautam Gupta", "email": "gautamgupta1025@gmail.com", "attendance_status": "Present"},
        {"user_name": "Ashish Kumar Rathour", "email": "rajpootashishd@gmail.com", "attendance_status": "Present"},
        {"user_name": "Nikhil Nishad", "email": "nikhilnishad622@gmail.com", "attendance_status": "Present"},
        {"user_name": "Durgesh Dewangan", "email": "durgeshh.yt@gmail.com", "attendance_status": "Present"},
        {"user_name": "Pratap", "email": "pratap@gmail.com", "attendance_status": "Present"},
    ],
    "agenda_items": [
        {"topic": "Project Phoenix Update", "description": "Review progress and blockers"},
        {"topic": "Employee Performance", "description": "Discuss performance ratings and promotions"},
        {"topic": "Upcoming Deadlines", "description": "Plan for March deliverables"},
    ],
    "discussion_summary": "Discussed project status, employee performance, and upcoming deadlines. Prabhat and Pratap assigned new tasks.",
    "tasks": [
        {"title": "API Integration", "description": "Integrate new endpoints for Project Phoenix", "responsible_person": "Prabhat Kumar Singh", "responsible_email": "prabhatkumarsictc7070@gmail.com", "deadline": "2026-03-25", "status": "Pending"},
        {"title": "Bug Fixing", "description": "Resolve critical bugs reported in March", "responsible_person": "Pratap", "responsible_email": "pratap@gmail.com", "deadline": "2026-03-20", "status": "Pending"},
    ],
    "next_meeting": {"next_date": "2026-04-07", "next_time": "11:00:00"},
}

def generate_mom_pdf(filename):
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph(f"<b>{mom_data['title']}</b>", styles['Title']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"<b>Organization:</b> {mom_data['organization']}", styles['Normal']))
    elements.append(Paragraph(f"<b>Meeting Type:</b> {mom_data['meeting_type']}", styles['Normal']))
    elements.append(Paragraph(f"<b>Date:</b> {mom_data['date']} <b>Time:</b> {mom_data['time']}", styles['Normal']))
    elements.append(Paragraph(f"<b>Venue:</b> {mom_data['venue']}", styles['Normal']))
    elements.append(Paragraph(f"<b>Called By:</b> {mom_data['called_by']} <b>Prepared By:</b> {mom_data['prepared_by']}", styles['Normal']))
    elements.append(Spacer(1, 12))

    # Attendees Table
    elements.append(Paragraph("<b>Attendees</b>", styles['Heading2']))
    attendees_data = [["Name", "Email", "Status"]] + [[a['user_name'], a['email'], a['attendance_status']] for a in mom_data['attendees']]
    attendees_table = Table(attendees_data, hAlign='LEFT')
    attendees_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.black),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
    ]))
    elements.append(attendees_table)
    elements.append(Spacer(1, 12))

    # Agenda Table
    elements.append(Paragraph("<b>Agenda Items</b>", styles['Heading2']))
    agenda_data = [["Topic", "Description"]] + [[a['topic'], a['description']] for a in mom_data['agenda_items']]
    agenda_table = Table(agenda_data, hAlign='LEFT')
    agenda_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
    ]))
    elements.append(agenda_table)
    elements.append(Spacer(1, 12))

    # Discussion Summary
    elements.append(Paragraph("<b>Discussion Summary</b>", styles['Heading2']))
    elements.append(Paragraph(mom_data['discussion_summary'], styles['Normal']))
    elements.append(Spacer(1, 12))

    # Tasks Table
    elements.append(Paragraph("<b>Tasks</b>", styles['Heading2']))
    tasks_data = [["Title", "Description", "Responsible", "Email", "Deadline", "Status"]] + [
        [t['title'], t['description'], t['responsible_person'], t['responsible_email'], t['deadline'], t['status']] for t in mom_data['tasks']
    ]
    tasks_table = Table(tasks_data, hAlign='LEFT')
    tasks_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
    ]))
    elements.append(tasks_table)
    elements.append(Spacer(1, 12))

    # Next Meeting
    elements.append(Paragraph("<b>Next Meeting</b>", styles['Heading2']))
    elements.append(Paragraph(f"Date: {mom_data['next_meeting']['next_date']} Time: {mom_data['next_meeting']['next_time']}", styles['Normal']))

    doc.build(elements)

if __name__ == "__main__":
    generate_mom_pdf("Botivate_Fake_MOM_Project_Phoenix.pdf")
