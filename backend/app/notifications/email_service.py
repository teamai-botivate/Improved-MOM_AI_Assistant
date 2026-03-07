"""Email notification service using aiosmtplib."""

import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import aiosmtplib

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class EmailService:

    @staticmethod
    async def send_email(to_email: str, subject: str, body_html: str) -> bool:
        """Send an HTML email via SMTP. Returns True on success."""
        if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
            logger.warning("SMTP credentials not configured – skipping email to %s", to_email)
            return False

        message = MIMEMultipart("alternative")
        message["From"] = settings.EMAIL_FROM
        message["To"] = to_email
        message["Subject"] = subject
        message.attach(MIMEText(body_html, "html"))

        try:
            await aiosmtplib.send(
                message,
                hostname=settings.SMTP_HOST,
                port=settings.SMTP_PORT,
                start_tls=True,
                username=settings.SMTP_USER,
                password=settings.SMTP_PASSWORD,
            )
            logger.info("Email sent to %s: %s", to_email, subject)
            return True
        except Exception as e:
            logger.error("Failed to send email to %s: %s", to_email, e)
            return False

    @staticmethod
    async def send_task_assignment(to_email: str, task_title: str, meeting_title: str, deadline: str | None):
        subject = f"New Task Assigned: {task_title}"
        body = f"""
        <div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;border:1px solid #e0e0e0;padding:24px;background:#fafbfc;">
            <h2 style="color:#2d6cdf;margin-bottom:16px;">New Task Assignment</h2>
            <p style="font-size:16px;">Dear Team Member,</p>
            <p style="font-size:15px;">You have been assigned a new task from the meeting <strong>{meeting_title}</strong>.</p>
            <table style="border-collapse:collapse;width:100%;margin:16px 0;">
                <tr style="background:#f0f4f8;">
                    <td style="padding:10px;font-weight:bold;width:120px;">Task</td>
                    <td style="padding:10px;">{task_title}</td>
                </tr>
                <tr>
                    <td style="padding:10px;font-weight:bold;">Meeting</td>
                    <td style="padding:10px;">{meeting_title}</td>
                </tr>
                <tr>
                    <td style="padding:10px;font-weight:bold;">Deadline</td>
                    <td style="padding:10px;">{deadline or 'Not specified'}</td>
                </tr>
            </table>
            <p style="font-size:15px;">Please log in to the MOM Assistant to view details and update your progress.</p>
            <hr style="margin:24px 0;border:none;border-top:1px solid #e0e0e0;" />
            <p style="font-size:13px;color:#888;">This is an automated email from the MOM AI Assistant. For queries, reply to this email.</p>
        </div>
        """
        await EmailService.send_email(to_email, subject, body)

    @staticmethod
    async def send_deadline_reminder(to_email: str, task_title: str, deadline: str):
        subject = f"Reminder: Task '{task_title}' deadline approaching"
        body = f"""
        <div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;border:1px solid #e0e0e0;padding:24px;background:#fafbfc;">
            <h2 style="color:#e67e22;margin-bottom:16px;">Task Deadline Reminder</h2>
            <p style="font-size:16px;">Dear Team Member,</p>
            <p style="font-size:15px;">Your task <strong>{task_title}</strong> has a deadline on <strong>{deadline}</strong>.</p>
            <p style="font-size:15px;">Please ensure it is completed on time. If you need assistance, contact your manager.</p>
            <hr style="margin:24px 0;border:none;border-top:1px solid #e0e0e0;" />
            <p style="font-size:13px;color:#888;">This is an automated email from the MOM AI Assistant. For queries, reply to this email.</p>
        </div>
        """
        await EmailService.send_email(to_email, subject, body)

    @staticmethod
    async def send_overdue_alert(to_email: str, task_title: str, deadline: str):
        subject = f"OVERDUE: Task '{task_title}'"
        body = f"""
        <div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;border:1px solid #e0e0e0;padding:24px;background:#fff6f6;">
            <h2 style="color:#d32f2f;margin-bottom:16px;">Overdue Task Alert</h2>
            <p style="font-size:16px;">Dear Team Member,</p>
            <p style="font-size:15px;">Your task <strong>{task_title}</strong> was due on <strong>{deadline}</strong> and is now overdue.</p>
            <p style="font-size:15px;">Please update the status or contact your manager immediately to resolve this issue.</p>
            <hr style="margin:24px 0;border:none;border-top:1px solid #e0e0e0;" />
            <p style="font-size:13px;color:#888;">This is an automated email from the MOM AI Assistant. For queries, reply to this email.</p>
        </div>
        """
        await EmailService.send_email(to_email, subject, body)

    @staticmethod
    async def send_absence_warning(to_email: str, user_name: str, absent_count: int):
        subject = f"Attendance Warning: {user_name}"
        body = f"""
        <h2>Attendance Warning</h2>
        <p><strong>{user_name}</strong> has been absent from <strong>{absent_count}</strong> meetings.</p>
        <p>Please review their attendance record.</p>
        """
        await EmailService.send_email(to_email, subject, body)
