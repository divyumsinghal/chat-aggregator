import json
from pathlib import Path


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
