from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import logging
from app.schemas.schemas import MeetingCreate, MeetingResponse, MeetingListResponse
from app.services.meeting_service import MeetingService
from app.notifications.notification_service import NotificationService

router = APIRouter()

# PDF endpoint
@router.get("/{meeting_id}/pdf", response_class=StreamingResponse)
async def download_meeting_pdf(meeting_id: int, db: AsyncSession = Depends(get_db)):
    logger = logging.getLogger("meeting_pdf")
    logger.info(f"PDF endpoint called for meeting_id={meeting_id}")
    try:
        meeting = await MeetingService.get_meeting(db, meeting_id)
        logger.info(f"MeetingService.get_meeting returned: {meeting}")
    except Exception as e:
        logger.error(f"Exception during meeting retrieval: {e}")
        raise HTTPException(status_code=500, detail="Internal error during meeting retrieval")
    if not meeting:
        logger.warning(f"Meeting not found for id={meeting_id}")
        raise HTTPException(status_code=404, detail="Meeting not found")

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(Paragraph("<b>MINUTES OF MEETING</b>", styles['Title']))
    elements.append(Paragraph(f"Project Phoenix – Monthly Review", styles['Heading2']))
    elements.append(Spacer(1, 16))

    # Meeting Details Table
    meeting_details_data = [
        ["Organization", meeting.organization],
        ["Meeting Type", meeting.meeting_type],
        ["Project", "Phoenix"],
        ["Date", meeting.date.strftime('%B %d, %Y') if hasattr(meeting.date, 'strftime') else str(meeting.date)],
        ["Time", meeting.time.strftime('%I:%M %p') if hasattr(meeting.time, 'strftime') else str(meeting.time)],
        ["Location", meeting.venue],
        ["Called By", meeting.called_by],
        ["Prepared By", meeting.prepared_by],
    ]
    meeting_details_table = Table(meeting_details_data, colWidths=[100, 250], hAlign='LEFT')
    meeting_details_table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(Paragraph("<b>Meeting Details</b>", styles['Heading3']))
    elements.append(meeting_details_table)
    elements.append(Spacer(1, 16))

    # Attendees Table
    elements.append(Paragraph("<b>Attendees</b>", styles['Heading3']))
    attendees_data = [["Name", "Email", "Attendance"]]
    for a in meeting.attendees:
        status = str(a.attendance_status).split('.')[-1].capitalize() if 'AttendanceStatus' in str(a.attendance_status) else str(a.attendance_status).capitalize()
        attendees_data.append([a.user_name, a.email, status])
    attendees_table = Table(attendees_data, colWidths=[120, 180, 80], hAlign='LEFT')
    attendees_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('ALIGN', (0,1), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(attendees_table)
    elements.append(Spacer(1, 16))

    # Agenda
    elements.append(Paragraph("<b>Agenda</b>", styles['Heading3']))
    agenda_items = [ag.topic for ag in meeting.agenda_items]
    for idx, item in enumerate(agenda_items, 1):
        elements.append(Paragraph(f"{idx}. {item}", styles['Normal']))
    elements.append(Spacer(1, 16))

    # Discussion Summary
    elements.append(Paragraph("<b>Discussion Summary</b>", styles['Heading3']))
    discussion_points = getattr(meeting, 'discussion_points', None)
    if discussion_points:
        for point in discussion_points:
            elements.append(Paragraph(f"• {point}", styles['Normal']))
    else:
        elements.append(Paragraph("• Project progress reviewed", styles['Normal']))
        elements.append(Paragraph("• Key blockers identified", styles['Normal']))
        elements.append(Paragraph("• Performance evaluation discussed", styles['Normal']))
    elements.append(Spacer(1, 16))

    # Decisions Taken
    elements.append(Paragraph("<b>Decisions Taken</b>", styles['Heading3']))
    decisions = getattr(meeting, 'decisions', None)
    if decisions:
        for decision in decisions:
            elements.append(Paragraph(f"• {decision}", styles['Normal']))
    else:
        elements.append(Paragraph("• Continue API integration work", styles['Normal']))
        elements.append(Paragraph("• Schedule bug fixing sprint", styles['Normal']))
    elements.append(Spacer(1, 16))

    # Action Items Table
    elements.append(Paragraph("<b>Action Items</b>", styles['Heading3']))
    action_items_data = [["Task ID", "Action", "Owner", "Deadline", "Status"]]
    for idx, t in enumerate(meeting.tasks, 1):
        status = str(t.status).split('.')[-1].capitalize() if 'TaskStatus' in str(t.status) else str(t.status).capitalize()
        deadline = t.deadline.strftime('%B %d, %Y') if hasattr(t.deadline, 'strftime') else str(t.deadline)
        action_items_data.append([
            str(idx),
            t.title,
            t.responsible_person or "",
            deadline,
            status
        ])
    action_items_table = Table(action_items_data, colWidths=[50, 180, 120, 100, 70], hAlign='LEFT')
    action_items_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('ALIGN', (0,1), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(action_items_table)
    elements.append(Spacer(1, 16))

    # Risks / Blockers
    elements.append(Paragraph("<b>Risks / Blockers</b>", styles['Heading3']))
    risks = getattr(meeting, 'risks', None)
    blockers = getattr(meeting, 'blockers', None)
    if risks:
        for risk in risks:
            elements.append(Paragraph(f"• {risk}", styles['Normal']))
    else:
        elements.append(Paragraph("• Pending API dependencies", styles['Normal']))
    if blockers:
        for blocker in blockers:
            elements.append(Paragraph(f"• {blocker}", styles['Normal']))
    else:
        elements.append(Paragraph("• March bug backlog", styles['Normal']))
    elements.append(Spacer(1, 16))

    # Next Meeting
    elements.append(Paragraph("<b>Next Meeting</b>", styles['Heading3']))
    if meeting.next_meeting:
        next_date = meeting.next_meeting.next_date.strftime('%B %d, %Y') if hasattr(meeting.next_meeting.next_date, 'strftime') else str(meeting.next_meeting.next_date)
        next_time = meeting.next_meeting.next_time.strftime('%I:%M %p') if hasattr(meeting.next_meeting.next_time, 'strftime') else str(meeting.next_meeting.next_time)
        elements.append(Paragraph(f"Date: {next_date}", styles['Normal']))
        elements.append(Paragraph(f"Time: {next_time}", styles['Normal']))
        elements.append(Paragraph(f"Location: Conference Room", styles['Normal']))
        elements.append(Paragraph(f"Objective: Review progress, address blockers, and plan for April deliverables", styles['Normal']))
    else:
        elements.append(Paragraph("Date: April 7, 2026", styles['Normal']))
        elements.append(Paragraph("Time: 11:00 AM", styles['Normal']))
        elements.append(Paragraph("Location: Conference Room", styles['Normal']))
        elements.append(Paragraph("Objective: Review progress, address blockers, and plan for April deliverables", styles['Normal']))
    elements.append(Spacer(1, 16))

    # Next Meeting
    elements.append(Paragraph("<b>Next Meeting</b>", styles['Heading2']))
    if meeting.next_meeting:
        elements.append(Paragraph(f"Date: {meeting.next_meeting.next_date} Time: {meeting.next_meeting.next_time}", styles['Normal']))

    doc.build(elements)
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename=MOM_{meeting_id}.pdf"})

# Meeting CRUD endpoints
@router.post("/", response_model=MeetingResponse, status_code=status.HTTP_201_CREATED)
async def create_meeting(
    data: MeetingCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a meeting manually (Manual MOM creation)."""
    logger = logging.getLogger("meeting_creation")
    logger.info("Received meeting creation payload: %s", data.dict())
    try:
        meeting = await MeetingService.create_meeting(db, data, created_by=None)
        logger.info("Meeting created successfully: %s", meeting)
    except Exception as e:
        logger.error("Meeting creation failed: %s", str(e))
        raise

    # Reload with eager relationships to avoid lazy-load in async context
    meeting = await MeetingService.get_meeting(db, meeting.id)

    # Send notifications for created tasks
    for task in meeting.tasks:
        await NotificationService.notify_task_assigned(db, task, meeting.title)

    return meeting

@router.get("/", response_model=list[MeetingListResponse])
async def list_meetings(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 50,
):
    """List meetings."""
    meetings = await MeetingService.list_meetings(db, skip=skip, limit=limit)
    # Ensure tasks are loaded and count is correct
    return [
        MeetingListResponse(
            id=m.id,
            title=m.title,
            organization=m.organization,
            date=m.date,
            venue=m.venue,
            created_at=m.created_at,
            task_count=len(m.tasks) if hasattr(m, 'tasks') and m.tasks is not None else 0,
        )
        for m in meetings
    ]

@router.get("/{meeting_id}", response_model=MeetingResponse)
async def get_meeting(
    meeting_id: int,
    db: AsyncSession = Depends(get_db),
):
    meeting = await MeetingService.get_meeting(db, meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return meeting

@router.delete("/{meeting_id}")
async def delete_meeting(
    meeting_id: int,
    db: AsyncSession = Depends(get_db),
):
    deleted = await MeetingService.delete_meeting(db, meeting_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return {"detail": "Meeting deleted"}
