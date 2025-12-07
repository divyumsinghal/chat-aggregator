from google.adk.agents import LlmAgent, SequentialAgent, LoopAgent
from google.adk.tools.agent_tool import AgentTool
from utils import get_emails, get_slack, get_msteams

summary_agent = LlmAgent(
    name="summary_agent",
    model="gemini-2.5-flash",
    description="Summarizes chats and extracts actionable items.",
    instruction="""You are an expert executive assistant. You will receive a consolidation of unread chats from various sources.
    Your goal is to summarize these chats concisely and extract actionable items (todos, meetings, calendar invites).
    Format the output clearly with "Summary" and "Actionable Items" sections.""",
    tools=[get_emails, get_slack, get_msteams],
    output_key="draft_summary",
)

next_actions_agent = LlmAgent(
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

summary_fact_checker_agent = LlmAgent(
    name="summary_fact_checker_agent",
    model="gemini-2.5-flash",
    description="Verifies the accuracy of a summary against original chat sources.",
    instruction="""You are a strict fact checker. Verify every point in the 'draft_summary' against the 'original_chats'.
    Report any discrepancies, missing context, or hallucinations.
    If everything is correct and fully supported, state "VERIFICATION_PASSED". Otherwise, list the specific errors.""",
    output_key="verification_result",
)

next_actions_fact_checker_agent = LlmAgent(
    name="next_actions_fact_checker_agent",
    model="gemini-2.5-flash",
    description="Verifies the accuracy of a summary against original chat sources.",
    instruction="""You are a strict fact checker. Verify every point in the 'priority_actions' and make sure that they make sense'.
    Report any discrepancies, missing context, or hallucinations.
    If everything is correct and fully supported, state "VERIFICATION_PASSED". Otherwise, list the specific errors.""",
    output_key="verification_result",
)

summarize_and_verify_loop = LoopAgent(
    name="summarize_and_verify_loop",
    sub_agents=[summary_agent, summary_fact_checker_agent],
    max_iterations=3,
)

next_actions_and_verify_loop = LoopAgent(
    name="next_actions_and_verify_loop",
    sub_agents=[next_actions_agent, next_actions_fact_checker_agent],
    max_iterations=3,
)


root_agent = SequentialAgent(
    name="root_agent",
    description="Orchestrates the complete chat consolidation and verification process.",
    sub_agents=[summarize_and_verify_loop, next_actions_and_verify_loop],
)
