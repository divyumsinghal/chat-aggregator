import json
from datetime import datetime
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Google Tasks API scope
SCOPES = ["https://www.googleapis.com/auth/tasks"]
TOKEN_FILE = Path(__file__).parent / "token.json"


def get_emails() -> str:
    """Fetch unread emails from the inbox.

    Returns a formatted string of recent email messages including sender,
    subject, timestamp, and body content.
    """
    data_path = Path(__file__).parent / "mock_data.json"
    with open(data_path) as f:
        data = json.load(f)

    emails = data.get("emails", [])
    if not emails:
        return "No unread emails."

    result = "=== UNREAD EMAILS ===\n\n"
    for email in emails:
        result += f"From: {email['from']}\n"
        result += f"Subject: {email['subject']}\n"
        result += f"Time: {email['timestamp']}\n"
        result += f"Body: {email['body']}\n"
        result += "-" * 40 + "\n\n"

    return result


def get_slack() -> str:
    """Fetch unread Slack messages from all channels.

    Returns a formatted string of recent Slack messages organized by channel,
    including sender, timestamp, and message content.
    """
    data_path = Path(__file__).parent / "mock_data.json"
    with open(data_path) as f:
        data = json.load(f)

    slack_data = data.get("slack", {})
    channels = slack_data.get("channels", [])
    if not channels:
        return "No unread Slack messages."

    result = "=== UNREAD SLACK MESSAGES ===\n\n"
    for channel in channels:
        result += f"Channel: {channel['name']}\n"
        result += "=" * 30 + "\n"
        for msg in channel.get("messages", []):
            result += f"  From: {msg['from']}\n"
            result += f"  Time: {msg['timestamp']}\n"
            result += f"  Message: {msg['text']}\n"
            result += "  " + "-" * 25 + "\n"
        result += "\n"

    return result


def get_msteams() -> str:
    """Fetch unread Microsoft Teams messages from all channels.

    Returns a formatted string of recent Teams messages organized by channel,
    including sender, timestamp, and message content.
    """
    data_path = Path(__file__).parent / "mock_data.json"
    with open(data_path) as f:
        data = json.load(f)

    teams_data = data.get("msteams", {})
    channels = teams_data.get("channels", [])
    if not channels:
        return "No unread Teams messages."

    result = "=== UNREAD MS TEAMS MESSAGES ===\n\n"
    for channel in channels:
        result += f"Channel: {channel['name']}\n"
        result += "=" * 30 + "\n"
        for msg in channel.get("messages", []):
            result += f"  From: {msg['from']}\n"
            result += f"  Time: {msg['timestamp']}\n"
            result += f"  Message: {msg['text']}\n"
            result += "  " + "-" * 25 + "\n"
        result += "\n"

    return result


def _get_tasks_service():
    """Get authenticated Google Tasks service.

    Returns:
        Google Tasks API service object, or None if not authenticated.
    """
    if not TOKEN_FILE.exists():
        return None

    creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    return build("tasks", "v1", credentials=creds)


def create_google_task(title: str, notes: str = "", due_date: str = "") -> str:
    """Create a task in Google Tasks.

    Args:
        title: Task title (required)
        notes: Optional task description/notes
        due_date: Optional due date in YYYY-MM-DD format

    Returns:
        Confirmation message with task details or error message.
    """
    service = _get_tasks_service()
    if not service:
        return (
            "Error: Google Tasks not authenticated. "
            "Run 'python scripts/setup_google_auth.py' first."
        )

    task = {"title": title}

    if notes:
        task["notes"] = notes

    if due_date:
        try:
            dt = datetime.strptime(due_date, "%Y-%m-%d")
            task["due"] = dt.isoformat() + "Z"
        except ValueError:
            return f"Error: Invalid date format '{due_date}'. Use YYYY-MM-DD."

    try:
        result = service.tasks().insert(tasklist="@default", body=task).execute()
        return (
            f"Task created successfully!\n"
            f"  Title: {result.get('title')}\n"
            f"  ID: {result.get('id')}\n"
            f"  Status: {result.get('status')}"
        )
    except Exception as e:
        return f"Error creating task: {str(e)}"
