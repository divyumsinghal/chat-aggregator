"""Actionable Insights Agent for chat consolidation pipeline.

This module implements an agent that analyzes chat summaries and extracts
actionable insights including email actions, meeting scheduling needs, and
task reminders for integration with Gmail, Google Calendar, Slack, and Teams.
"""

from google.adk.agents import LlmAgent


root_agent = LlmAgent(
    name="actionable_insights_agent",
    model="gemini-2.5-flash",
    description=(
        "Extracts actionable insights from chat summaries including "
        "email actions, meeting scheduling, and reminders."
    ),
    instruction=(
        "You are an intelligent agent that analyzes the chat summary "
        "stored in {draft_summary} and identifies actionable insights. "
        "Extract the following types of actionable items:\n\n"
        "1. Email actions: Identify when someone needs to send an email. "
        "Extract the recipient email address, subject line, and draft "
        "body content based on context from the conversation.\n\n"
        "2. Meeting actions: Identify when a meeting should be scheduled. "
        "Extract the meeting title, list of participants (with email "
        "addresses if mentioned), proposed time/date, and any agenda "
        "items discussed.\n\n"
        "3. Reminder actions: Identify tasks, follow-ups, or deadlines "
        "mentioned in the conversation. Extract task descriptions and "
        "due dates or deadlines.\n\n"
        "Format your response as a structured JSON object with three "
        "arrays:\n"
        "{\n"
        '  "emails": [\n'
        '    {"to": "recipient@example.com", "subject": "...", '
        '"body": "..."}\n'
        "  ],\n"
        '  "meetings": [\n'
        '    {"title": "...", "participants": ["email1@example.com", '
        '"email2@example.com"], "time": "YYYY-MM-DD HH:MM", '
        '"agenda": "..."}\n'
        "  ],\n"
        '  "reminders": [\n'
        '    {"task": "...", "due_date": "YYYY-MM-DD"}\n'
        "  ]\n"
        "}\n\n"
        "The insights should be actionable and ready for integration with "
        "Gmail, Google Calendar, Slack, and Teams. If no actionable items "
        "are found in a category, return an empty array for that category."
    ),
    output_key="priority_actions",
)
