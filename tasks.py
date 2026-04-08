"""Upgraded task bank for web_tutor_env.

Each task is a full course module with:
- study_materials: sections the agent must read to find quiz answers
- quiz: multiple questions per task (single-select and multi-select)
- per-question feedback for wrong answers
- energy and step budgets for resource management
"""

from __future__ import annotations
from copy import deepcopy
from typing import Any, Dict, List


TASK_BANK: List[Dict[str, Any]] = [
    # ── EASY #1: HTML Basics ─────────────────────────────────────────────
    {
        "id": "html_basics",
        "task_type": "course_module",
        "difficulty": "easy",
        "title": "HTML Basics",
        "instruction": (
            "You are taking a web development course. First, study the "
            "materials by reading sections. Then navigate to the quiz "
            "and answer the questions based on what you learned. Manage "
            "your energy carefully."
        ),
        "study_materials": [
            {
                "section_id": "s1",
                "title": "What is HTML?",
                "content": (
                    "HTML stands for HyperText Markup Language. It is "
                    "the standard language for creating web pages and "
                    "web applications. HTML describes the structure of "
                    "a web page using markup elements."
                ),
            },
            {
                "section_id": "s2",
                "title": "Core Tags",
                "content": (
                    "The <h1> to <h6> tags define headings. <p> defines "
                    "a paragraph. <a> creates a hyperlink. <img> embeds "
                    "an image. <div> is a generic container."
                ),
            },
            {
                "section_id": "s3",
                "title": "Document Structure",
                "content": (
                    "Every HTML document begins with <!DOCTYPE html>. "
                    "The <html> element is the root. <head> contains "
                    "metadata like <title>. <body> contains visible content."
                ),
            },
        ],
        "quiz": [
            {
                "question_id": "q1",
                "question": "What does HTML stand for?",
                "options": [
                    "HyperText Markup Language",
                    "High Tech Modern Language",
                    "Hyper Transfer Markup Language",
                    "Home Tool Markup Language",
                ],
                "correct_options": [0],
                "type": "single",
                "key_section": "s1",
                "wrong_feedback": "Review section 'What is HTML?' for the full name.",
            },
            {
                "question_id": "q2",
                "question": "Which tag creates a hyperlink?",
                "options": ["<img>", "<p>", "<a>", "<h1>"],
                "correct_options": [2],
                "type": "single",
                "key_section": "s2",
                "wrong_feedback": "Review 'Core Tags' for the hyperlink tag.",
            },
        ],
        "energy_budget": 12,
        "step_budget": 15,
        "max_attempts": 3,
    },

    # ── EASY #2: Python Data Types ───────────────────────────────────────
    {
        "id": "python_data_types",
        "task_type": "course_module",
        "difficulty": "easy",
        "title": "Python Data Types",
        "instruction": (
            "Study Python data type materials, then attempt the quiz."
        ),
        "study_materials": [
            {
                "section_id": "s1",
                "title": "Numeric Types",
                "content": (
                    "Python has int for whole numbers (x = 5) and float "
                    "for decimals (y = 3.14). Convert with int() and float()."
                ),
            },
            {
                "section_id": "s2",
                "title": "Text Type",
                "content": (
                    "Strings (str) represent text. Defined with quotes: "
                    "'hello' or \"world\". Strings are immutable."
                ),
            },
            {
                "section_id": "s3",
                "title": "Collections",
                "content": (
                    "A list is ordered and mutable: [1, 2, 3]. "
                    "A tuple is ordered but immutable: (1, 2, 3). "
                    "A dict maps keys to values: {'a': 1}. "
                    "A set holds unique unordered items: {1, 2, 3}."
                ),
            },
        ],
        "quiz": [
            {
                "question_id": "q1",
                "question": "What type is 3.14 in Python?",
                "options": ["int", "str", "float", "list"],
                "correct_options": [2],
                "type": "single",
                "key_section": "s1",
                "wrong_feedback": "Review 'Numeric Types' for decimal number types.",
            },
            {
                "question_id": "q2",
                "question": "Which collection type is immutable?",
                "options": ["list", "dict", "set", "tuple"],
                "correct_options": [3],
                "type": "single",
                "key_section": "s3",
                "wrong_feedback": "Review 'Collections' for the immutable type.",
            },
        ],
        "energy_budget": 12,
        "step_budget": 15,
        "max_attempts": 3,
    },

    # ── MEDIUM #1: CSS Selectors ─────────────────────────────────────────
    {
        "id": "css_selectors",
        "task_type": "course_module",
        "difficulty": "medium",
        "title": "CSS Selectors and Specificity",
        "instruction": (
            "This module covers CSS selectors. The quiz includes "
            "multi-select questions where multiple answers are correct."
        ),
        "study_materials": [
            {
                "section_id": "s1",
                "title": "Element Selectors",
                "content": (
                    "Element selectors target HTML tags: 'p { color: red; }' "
                    "targets all <p>. Universal selector '*' matches everything."
                ),
            },
            {
                "section_id": "s2",
                "title": "Class and ID Selectors",
                "content": (
                    "Class selectors use a dot: '.warning { color: orange; }'. "
                    "ID selectors use a hash: '#main { width: 100%; }'. "
                    "IDs must be unique per page."
                ),
            },
            {
                "section_id": "s3",
                "title": "Combinators",
                "content": (
                    "Descendant 'div p' selects all <p> inside <div>. "
                    "Child 'div > p' selects only direct children. "
                    "Adjacent sibling 'h1 + p' selects <p> right after <h1>."
                ),
            },
            {
                "section_id": "s4",
                "title": "Specificity Rules",
                "content": (
                    "Inline styles = 1000. ID selectors = 100. "
                    "Class selectors = 10. Element selectors = 1. "
                    "!important overrides all normal specificity."
                ),
            },
        ],
        "quiz": [
            {
                "question_id": "q1",
                "question": "Which selector targets an element by unique identifier?",
                "options": [".classname", "#idname", "tagname", "*"],
                "correct_options": [1],
                "type": "single",
                "key_section": "s2",
                "wrong_feedback": "Review 'Class and ID Selectors' for unique IDs.",
            },
            {
                "question_id": "q2",
                "question": "What does 'div > p' target?",
                "options": [
                    "All <p> on page",
                    "All <p> inside any <div>",
                    "Only direct <p> children of <div>",
                    "<p> next to <div>",
                ],
                "correct_options": [2],
                "type": "single",
                "key_section": "s3",
                "wrong_feedback": "Review 'Combinators' for the child combinator.",
            },
            {
                "question_id": "q3",
                "question": "Which have HIGHER specificity than class selectors? (Select ALL)",
                "options": [
                    "Element selectors",
                    "ID selectors",
                    "Inline styles",
                    "Universal selector (*)",
                ],
                "correct_options": [1, 2],
                "type": "multi",
                "key_section": "s4",
                "wrong_feedback": "Review 'Specificity Rules' and compare numeric values.",
            },
        ],
        "energy_budget": 15,
        "step_budget": 20,
        "max_attempts": 3,
    },

    # ── MEDIUM #2: JavaScript Events ─────────────────────────────────────
    {
        "id": "js_events",
        "task_type": "course_module",
        "difficulty": "medium",
        "title": "JavaScript Events",
        "instruction": (
            "Learn about JavaScript event handling. Some questions "
            "require selecting multiple correct answers."
        ),
        "study_materials": [
            {
                "section_id": "s1",
                "title": "What are Events?",
                "content": (
                    "Events are browser-detected actions: clicks, key "
                    "presses, page loads, form submissions. JavaScript "
                    "listens and responds with callback functions."
                ),
            },
            {
                "section_id": "s2",
                "title": "Event Listeners",
                "content": (
                    "addEventListener('click', handler) attaches a callback. "
                    "removeEventListener() detaches it. Multiple listeners "
                    "can exist on the same element."
                ),
            },
            {
                "section_id": "s3",
                "title": "Event Propagation",
                "content": (
                    "Capturing goes top-down (document to target). "
                    "Bubbling goes bottom-up (target to document). "
                    "Default is bubbling. stopPropagation() halts it."
                ),
            },
            {
                "section_id": "s4",
                "title": "Common Event Types",
                "content": (
                    "click: mouse click. keydown/keyup: keyboard. "
                    "submit: form submission. load: page loaded. "
                    "input: value changed in input field."
                ),
            },
        ],
        "quiz": [
            {
                "question_id": "q1",
                "question": "Which method attaches an event handler?",
                "options": ["onClick()", "addEventListener()", "attachEvent()", "bindEvent()"],
                "correct_options": [1],
                "type": "single",
                "key_section": "s2",
                "wrong_feedback": "Review 'Event Listeners' for the standard method.",
            },
            {
                "question_id": "q2",
                "question": "In which direction does bubbling propagate?",
                "options": ["Top to bottom", "Left to right", "Bottom to top", "Random"],
                "correct_options": [2],
                "type": "single",
                "key_section": "s3",
                "wrong_feedback": "Review 'Event Propagation' for bubbling direction.",
            },
            {
                "question_id": "q3",
                "question": "Which events fire when typing in an input? (Select ALL)",
                "options": ["click", "keydown", "input", "load"],
                "correct_options": [1, 2],
                "type": "multi",
                "key_section": "s4",
                "wrong_feedback": "Review 'Common Event Types' for keyboard/input events.",
            },
        ],
        "energy_budget": 15,
        "step_budget": 20,
        "max_attempts": 3,
    },

    # ── HARD #1: REST API Design ─────────────────────────────────────────
    {
        "id": "rest_api_design",
        "task_type": "course_module",
        "difficulty": "hard",
        "title": "RESTful API Design",
        "instruction": (
            "Advanced module on REST APIs. Energy is limited so study "
            "strategically. Multiple questions require all correct answers."
        ),
        "study_materials": [
            {
                "section_id": "s1",
                "title": "HTTP Methods",
                "content": (
                    "GET retrieves data (safe, idempotent). "
                    "POST creates resources (NOT idempotent). "
                    "PUT replaces entirely (idempotent). "
                    "PATCH partially updates. "
                    "DELETE removes (idempotent)."
                ),
            },
            {
                "section_id": "s2",
                "title": "Status Codes",
                "content": (
                    "200 OK. 201 Created. 204 No Content. "
                    "400 Bad Request. 401 Unauthorized. "
                    "403 Forbidden. 404 Not Found. 500 Server Error."
                ),
            },
            {
                "section_id": "s3",
                "title": "Resource Naming",
                "content": (
                    "Use nouns not verbs: /users not /getUsers. "
                    "Use plural: /users not /user. "
                    "Nest for relations: /users/123/orders. "
                    "Query params for filtering: /users?active=true."
                ),
            },
            {
                "section_id": "s4",
                "title": "Authentication",
                "content": (
                    "API Key: simple, in header or query. "
                    "OAuth 2.0: token-based delegated access. "
                    "JWT: self-contained tokens with claims. "
                    "Bearer tokens go in Authorization header."
                ),
            },
            {
                "section_id": "s5",
                "title": "Best Practices",
                "content": (
                    "Version your API: /v1/users. "
                    "Paginate lists: ?page=1&limit=20. "
                    "Consistent errors: {error: {code, message}}. "
                    "Always use HTTPS. Implement rate limiting."
                ),
            },
        ],
        "quiz": [
            {
                "question_id": "q1",
                "question": "Which HTTP methods are idempotent? (Select ALL)",
                "options": ["GET", "POST", "PUT", "DELETE"],
                "correct_options": [0, 2, 3],
                "type": "multi",
                "key_section": "s1",
                "wrong_feedback": "Review 'HTTP Methods' for idempotency.",
            },
            {
                "question_id": "q2",
                "question": "What status code means a new resource was created?",
                "options": ["200 OK", "201 Created", "204 No Content", "400 Bad Request"],
                "correct_options": [1],
                "type": "single",
                "key_section": "s2",
                "wrong_feedback": "Review 'Status Codes' for creation responses.",
            },
            {
                "question_id": "q3",
                "question": "Which URL follows REST conventions?",
                "options": ["/getUsers", "/user/list", "/users", "/api/fetchAllUsers"],
                "correct_options": [2],
                "type": "single",
                "key_section": "s3",
                "wrong_feedback": "Review 'Resource Naming' for noun-based URLs.",
            },
            {
                "question_id": "q4",
                "question": "Which are valid API auth methods? (Select ALL)",
                "options": ["API Key", "OAuth 2.0", "FTP", "JWT"],
                "correct_options": [0, 1, 3],
                "type": "multi",
                "key_section": "s4",
                "wrong_feedback": "Review 'Authentication' - FTP is not an auth method.",
            },
        ],
        "energy_budget": 18,
        "step_budget": 25,
        "max_attempts": 3,
    },
]


def get_task_bank() -> List[Dict[str, Any]]:
    """Return a deep copy of the task bank."""
    return deepcopy(TASK_BANK)
