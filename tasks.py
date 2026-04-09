"""Upgraded task bank for web_tutor_env.

Each task is a full course module with:
- study_materials: sections the agent must read to find quiz answers
- quiz_pool: a LARGE pool of questions. Each reset picks a random subset.
- per-question feedback for wrong answers
- energy and step budgets for resource management
"""

from __future__ import annotations
import random
from copy import deepcopy
from typing import Any, Dict, List, Optional


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
                    "a web page using markup elements. HTML was invented "
                    "by Tim Berners-Lee in 1991."
                ),
            },
            {
                "section_id": "s2",
                "title": "Core Tags",
                "content": (
                    "The <h1> to <h6> tags define headings. <p> defines "
                    "a paragraph. <a> creates a hyperlink. <img> embeds "
                    "an image. <div> is a generic container. <span> is "
                    "an inline container. <ul> creates an unordered list "
                    "and <ol> creates an ordered list. <li> is a list item."
                ),
            },
            {
                "section_id": "s3",
                "title": "Document Structure",
                "content": (
                    "Every HTML document begins with <!DOCTYPE html>. "
                    "The <html> element is the root. <head> contains "
                    "metadata like <title> and <meta>. <body> contains visible content. "
                    "The <link> tag is used to link external stylesheets. "
                    "The <script> tag embeds or references JavaScript."
                ),
            },
        ],
        "quiz_pool": [
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
            {
                "question_id": "q3",
                "question": "Who invented HTML?",
                "options": ["Brendan Eich", "Tim Berners-Lee", "Guido van Rossum", "James Gosling"],
                "correct_options": [1],
                "type": "single",
                "key_section": "s1",
                "wrong_feedback": "Review 'What is HTML?' for the inventor.",
            },
            {
                "question_id": "q4",
                "question": "Which tag defines a paragraph?",
                "options": ["<h1>", "<div>", "<p>", "<a>"],
                "correct_options": [2],
                "type": "single",
                "key_section": "s2",
                "wrong_feedback": "Review 'Core Tags' — <p> defines a paragraph.",
            },
            {
                "question_id": "q5",
                "question": "What does <!DOCTYPE html> declare?",
                "options": [
                    "A comment",
                    "The document type as HTML5",
                    "A JavaScript function",
                    "A CSS rule",
                ],
                "correct_options": [1],
                "type": "single",
                "key_section": "s3",
                "wrong_feedback": "Review 'Document Structure' for the DOCTYPE role.",
            },
            {
                "question_id": "q6",
                "question": "Which tag embeds an image?",
                "options": ["<a>", "<img>", "<div>", "<span>"],
                "correct_options": [1],
                "type": "single",
                "key_section": "s2",
                "wrong_feedback": "Review 'Core Tags' for the image tag.",
            },
            {
                "question_id": "q7",
                "question": "Which tags define lists in HTML? (Select ALL)",
                "options": ["<ul>", "<ol>", "<li>", "<div>"],
                "correct_options": [0, 1, 2],
                "type": "multi",
                "key_section": "s2",
                "wrong_feedback": "Review 'Core Tags' for list-related tags.",
            },
            {
                "question_id": "q8",
                "question": "Where is metadata placed in an HTML document?",
                "options": ["<body>", "<head>", "<footer>", "<main>"],
                "correct_options": [1],
                "type": "single",
                "key_section": "s3",
                "wrong_feedback": "Review 'Document Structure' for the metadata container.",
            },
            {
                "question_id": "q9",
                "question": "What is the root element of an HTML document?",
                "options": ["<head>", "<body>", "<html>", "<div>"],
                "correct_options": [2],
                "type": "single",
                "key_section": "s3",
                "wrong_feedback": "Review 'Document Structure' for the root element.",
            },
            {
                "question_id": "q10",
                "question": "Which tag links an external CSS stylesheet?",
                "options": ["<script>", "<style>", "<link>", "<meta>"],
                "correct_options": [2],
                "type": "single",
                "key_section": "s3",
                "wrong_feedback": "Review 'Document Structure' for the <link> tag.",
            },
        ],
        "quiz_count": 3,
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
                    "for decimals (y = 3.14). Convert with int() and float(). "
                    "Python also has complex numbers: z = 2 + 3j. "
                    "The bool type is a subclass of int: True is 1, False is 0."
                ),
            },
            {
                "section_id": "s2",
                "title": "Text Type",
                "content": (
                    "Strings (str) represent text. Defined with quotes: "
                    "'hello' or \"world\". Strings are immutable. "
                    "String concatenation uses +. Repetition uses *. "
                    "The len() function returns the string length. "
                    "f-strings like f'{name}' allow inline expressions."
                ),
            },
            {
                "section_id": "s3",
                "title": "Collections",
                "content": (
                    "A list is ordered and mutable: [1, 2, 3]. "
                    "A tuple is ordered but immutable: (1, 2, 3). "
                    "A dict maps keys to values: {'a': 1}. "
                    "A set holds unique unordered items: {1, 2, 3}. "
                    "A frozenset is an immutable version of a set."
                ),
            },
        ],
        "quiz_pool": [
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
            {
                "question_id": "q3",
                "question": "What does len('hello') return?",
                "options": ["4", "5", "6", "Error"],
                "correct_options": [1],
                "type": "single",
                "key_section": "s2",
                "wrong_feedback": "Review 'Text Type' — len() returns the number of characters.",
            },
            {
                "question_id": "q4",
                "question": "Which type is a subclass of int?",
                "options": ["float", "str", "bool", "complex"],
                "correct_options": [2],
                "type": "single",
                "key_section": "s1",
                "wrong_feedback": "Review 'Numeric Types' — bool is a subclass of int.",
            },
            {
                "question_id": "q5",
                "question": "How do you write an f-string?",
                "options": ["f'{expr}'", "str(expr)", "'%s' % expr", "format(expr)"],
                "correct_options": [0],
                "type": "single",
                "key_section": "s2",
                "wrong_feedback": "Review 'Text Type' for f-string syntax.",
            },
            {
                "question_id": "q6",
                "question": "Which collection holds unique unordered items?",
                "options": ["list", "tuple", "set", "dict"],
                "correct_options": [2],
                "type": "single",
                "key_section": "s3",
                "wrong_feedback": "Review 'Collections' for unique unordered items.",
            },
            {
                "question_id": "q7",
                "question": "Which are valid Python number types? (Select ALL)",
                "options": ["int", "float", "complex", "decimal"],
                "correct_options": [0, 1, 2],
                "type": "multi",
                "key_section": "s1",
                "wrong_feedback": "Review 'Numeric Types' for built-in number types.",
            },
            {
                "question_id": "q8",
                "question": "Are Python strings mutable?",
                "options": ["Yes", "No", "Only single characters", "Depends on length"],
                "correct_options": [1],
                "type": "single",
                "key_section": "s2",
                "wrong_feedback": "Review 'Text Type' — strings are immutable.",
            },
            {
                "question_id": "q9",
                "question": "What is a frozenset?",
                "options": [
                    "A mutable set",
                    "An immutable version of a set",
                    "A sorted list",
                    "A type of dictionary",
                ],
                "correct_options": [1],
                "type": "single",
                "key_section": "s3",
                "wrong_feedback": "Review 'Collections' for frozenset.",
            },
            {
                "question_id": "q10",
                "question": "What operator concatenates strings in Python?",
                "options": ["&", "+", ".", "++"],
                "correct_options": [1],
                "type": "single",
                "key_section": "s2",
                "wrong_feedback": "Review 'Text Type' — + is used for concatenation.",
            },
        ],
        "quiz_count": 3,
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
                    "targets all <p>. Universal selector '*' matches everything. "
                    "Grouping selectors: 'h1, h2, h3 { margin: 0; }' applies to all three."
                ),
            },
            {
                "section_id": "s2",
                "title": "Class and ID Selectors",
                "content": (
                    "Class selectors use a dot: '.warning { color: orange; }'. "
                    "ID selectors use a hash: '#main { width: 100%; }'. "
                    "IDs must be unique per page. Classes can be reused. "
                    "You can chain classes: '.btn.primary' matches elements with both."
                ),
            },
            {
                "section_id": "s3",
                "title": "Combinators",
                "content": (
                    "Descendant 'div p' selects all <p> inside <div>. "
                    "Child 'div > p' selects only direct children. "
                    "Adjacent sibling 'h1 + p' selects <p> right after <h1>. "
                    "General sibling 'h1 ~ p' selects all <p> siblings after <h1>."
                ),
            },
            {
                "section_id": "s4",
                "title": "Specificity Rules",
                "content": (
                    "Inline styles = 1000. ID selectors = 100. "
                    "Class selectors = 10. Element selectors = 1. "
                    "!important overrides all normal specificity. "
                    "Pseudo-classes like :hover count as class-level specificity (10)."
                ),
            },
        ],
        "quiz_pool": [
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
            {
                "question_id": "q4",
                "question": "What does the universal selector * match?",
                "options": ["Only <div> elements", "All elements", "Only classes", "Nothing"],
                "correct_options": [1],
                "type": "single",
                "key_section": "s1",
                "wrong_feedback": "Review 'Element Selectors' for the universal selector.",
            },
            {
                "question_id": "q5",
                "question": "What specificity value does a pseudo-class like :hover have?",
                "options": ["1", "10", "100", "1000"],
                "correct_options": [1],
                "type": "single",
                "key_section": "s4",
                "wrong_feedback": "Review 'Specificity Rules' — pseudo-classes are class-level.",
            },
            {
                "question_id": "q6",
                "question": "What does 'h1 + p' select?",
                "options": [
                    "All <p> inside <h1>",
                    "The <p> immediately after an <h1>",
                    "All <p> with class h1",
                    "<h1> and <p> together",
                ],
                "correct_options": [1],
                "type": "single",
                "key_section": "s3",
                "wrong_feedback": "Review 'Combinators' for the adjacent sibling combinator.",
            },
            {
                "question_id": "q7",
                "question": "Can you reuse an ID on multiple elements?",
                "options": ["Yes, always", "No, IDs must be unique", "Only in forms", "Only in divs"],
                "correct_options": [1],
                "type": "single",
                "key_section": "s2",
                "wrong_feedback": "Review 'Class and ID Selectors' — IDs are unique.",
            },
            {
                "question_id": "q8",
                "question": "Which are valid CSS combinators? (Select ALL)",
                "options": [
                    "Descendant (space)",
                    "Child (>)",
                    "Adjacent sibling (+)",
                    "Equality (==)",
                ],
                "correct_options": [0, 1, 2],
                "type": "multi",
                "key_section": "s3",
                "wrong_feedback": "Review 'Combinators' for valid CSS combinators.",
            },
            {
                "question_id": "q9",
                "question": "What specificity does an inline style have?",
                "options": ["1", "10", "100", "1000"],
                "correct_options": [3],
                "type": "single",
                "key_section": "s4",
                "wrong_feedback": "Review 'Specificity Rules' — inline styles = 1000.",
            },
            {
                "question_id": "q10",
                "question": "How do you chain two classes in CSS?",
                "options": [".a .b", ".a.b", ".a + .b", ".a > .b"],
                "correct_options": [1],
                "type": "single",
                "key_section": "s2",
                "wrong_feedback": "Review 'Class and ID Selectors' — chaining uses no space.",
            },
        ],
        "quiz_count": 3,
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
                    "listens and responds with callback functions. "
                    "Events follow the Observer pattern."
                ),
            },
            {
                "section_id": "s2",
                "title": "Event Listeners",
                "content": (
                    "addEventListener('click', handler) attaches a callback. "
                    "removeEventListener() detaches it. Multiple listeners "
                    "can exist on the same element. The third parameter "
                    "controls capture vs bubble phase: { capture: true }."
                ),
            },
            {
                "section_id": "s3",
                "title": "Event Propagation",
                "content": (
                    "Capturing goes top-down (document to target). "
                    "Bubbling goes bottom-up (target to document). "
                    "Default is bubbling. stopPropagation() halts it. "
                    "preventDefault() cancels the default browser action. "
                    "stopImmediatePropagation() stops other listeners on the same element."
                ),
            },
            {
                "section_id": "s4",
                "title": "Common Event Types",
                "content": (
                    "click: mouse click. dblclick: double click. "
                    "keydown/keyup: keyboard. "
                    "submit: form submission. load: page loaded. "
                    "input: value changed in input field. "
                    "mouseover/mouseout: mouse entering/leaving. "
                    "focus/blur: element gaining/losing focus."
                ),
            },
        ],
        "quiz_pool": [
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
            {
                "question_id": "q4",
                "question": "What does preventDefault() do?",
                "options": [
                    "Stops event propagation",
                    "Cancels the default browser action",
                    "Removes the event listener",
                    "Refreshes the page",
                ],
                "correct_options": [1],
                "type": "single",
                "key_section": "s3",
                "wrong_feedback": "Review 'Event Propagation' for preventDefault().",
            },
            {
                "question_id": "q5",
                "question": "What design pattern do events follow?",
                "options": ["Singleton", "Factory", "Observer", "Strategy"],
                "correct_options": [2],
                "type": "single",
                "key_section": "s1",
                "wrong_feedback": "Review 'What are Events?' for the design pattern.",
            },
            {
                "question_id": "q6",
                "question": "Which direction does capturing go?",
                "options": ["Bottom to top", "Top to bottom", "Left to right", "Circular"],
                "correct_options": [1],
                "type": "single",
                "key_section": "s3",
                "wrong_feedback": "Review 'Event Propagation' for capturing direction.",
            },
            {
                "question_id": "q7",
                "question": "How do you remove an event listener?",
                "options": ["deleteEvent()", "removeEventListener()", "detachEvent()", "unbind()"],
                "correct_options": [1],
                "type": "single",
                "key_section": "s2",
                "wrong_feedback": "Review 'Event Listeners' for listener removal.",
            },
            {
                "question_id": "q8",
                "question": "Which are mouse-related events? (Select ALL)",
                "options": ["click", "mouseover", "keydown", "dblclick"],
                "correct_options": [0, 1, 3],
                "type": "multi",
                "key_section": "s4",
                "wrong_feedback": "Review 'Common Event Types' for mouse events.",
            },
            {
                "question_id": "q9",
                "question": "Can multiple listeners be on the same element?",
                "options": ["No", "Yes", "Only with jQuery", "Only in Chrome"],
                "correct_options": [1],
                "type": "single",
                "key_section": "s2",
                "wrong_feedback": "Review 'Event Listeners' — multiple listeners are supported.",
            },
            {
                "question_id": "q10",
                "question": "What event fires when an element gains focus?",
                "options": ["click", "hover", "focus", "load"],
                "correct_options": [2],
                "type": "single",
                "key_section": "s4",
                "wrong_feedback": "Review 'Common Event Types' for the focus event.",
            },
        ],
        "quiz_count": 3,
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
                    "DELETE removes (idempotent). "
                    "HEAD is like GET but returns only headers."
                ),
            },
            {
                "section_id": "s2",
                "title": "Status Codes",
                "content": (
                    "200 OK. 201 Created. 204 No Content. "
                    "301 Moved Permanently. 304 Not Modified. "
                    "400 Bad Request. 401 Unauthorized. "
                    "403 Forbidden. 404 Not Found. 409 Conflict. "
                    "429 Too Many Requests. 500 Server Error. 503 Service Unavailable."
                ),
            },
            {
                "section_id": "s3",
                "title": "Resource Naming",
                "content": (
                    "Use nouns not verbs: /users not /getUsers. "
                    "Use plural: /users not /user. "
                    "Nest for relations: /users/123/orders. "
                    "Query params for filtering: /users?active=true. "
                    "Use kebab-case: /user-profiles not /userProfiles."
                ),
            },
            {
                "section_id": "s4",
                "title": "Authentication",
                "content": (
                    "API Key: simple, in header or query. "
                    "OAuth 2.0: token-based delegated access. "
                    "JWT: self-contained tokens with claims, made of "
                    "header.payload.signature. "
                    "Bearer tokens go in Authorization header. "
                    "Basic Auth sends base64-encoded username:password."
                ),
            },
            {
                "section_id": "s5",
                "title": "Best Practices",
                "content": (
                    "Version your API: /v1/users. "
                    "Paginate lists: ?page=1&limit=20. "
                    "Consistent errors: {error: {code, message}}. "
                    "Always use HTTPS. Implement rate limiting. "
                    "Use HATEOAS for discoverability. "
                    "Support content negotiation via Accept headers."
                ),
            },
        ],
        "quiz_pool": [
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
            {
                "question_id": "q5",
                "question": "What status code indicates rate limiting?",
                "options": ["400 Bad Request", "403 Forbidden", "429 Too Many Requests", "500 Server Error"],
                "correct_options": [2],
                "type": "single",
                "key_section": "s2",
                "wrong_feedback": "Review 'Status Codes' for rate limiting responses.",
            },
            {
                "question_id": "q6",
                "question": "What are the three parts of a JWT?",
                "options": [
                    "header.payload.signature",
                    "key.value.hash",
                    "user.role.token",
                    "id.secret.expiry",
                ],
                "correct_options": [0],
                "type": "single",
                "key_section": "s4",
                "wrong_feedback": "Review 'Authentication' for JWT structure.",
            },
            {
                "question_id": "q7",
                "question": "Which HTTP method partially updates a resource?",
                "options": ["GET", "PUT", "PATCH", "POST"],
                "correct_options": [2],
                "type": "single",
                "key_section": "s1",
                "wrong_feedback": "Review 'HTTP Methods' for partial updates.",
            },
            {
                "question_id": "q8",
                "question": "Which are REST best practices? (Select ALL)",
                "options": [
                    "Version your API",
                    "Use HTTPS",
                    "Implement rate limiting",
                    "Use verbs in URLs",
                ],
                "correct_options": [0, 1, 2],
                "type": "multi",
                "key_section": "s5",
                "wrong_feedback": "Review 'Best Practices' — URLs should use nouns, not verbs.",
            },
            {
                "question_id": "q9",
                "question": "What naming convention should REST URLs use?",
                "options": ["camelCase", "PascalCase", "kebab-case", "snake_case"],
                "correct_options": [2],
                "type": "single",
                "key_section": "s3",
                "wrong_feedback": "Review 'Resource Naming' for URL conventions.",
            },
            {
                "question_id": "q10",
                "question": "What does status code 204 mean?",
                "options": [
                    "OK with body",
                    "Created",
                    "No Content (success but no body)",
                    "Not Found",
                ],
                "correct_options": [2],
                "type": "single",
                "key_section": "s2",
                "wrong_feedback": "Review 'Status Codes' for 204 No Content.",
            },
            {
                "question_id": "q11",
                "question": "What is HATEOAS?",
                "options": [
                    "A hashing algorithm",
                    "Hypermedia links for API discoverability",
                    "A database pattern",
                    "An HTTP header",
                ],
                "correct_options": [1],
                "type": "single",
                "key_section": "s5",
                "wrong_feedback": "Review 'Best Practices' for HATEOAS.",
            },
            {
                "question_id": "q12",
                "question": "Which method is safe (no side effects)?",
                "options": ["POST", "DELETE", "PUT", "GET"],
                "correct_options": [3],
                "type": "single",
                "key_section": "s1",
                "wrong_feedback": "Review 'HTTP Methods' — GET is safe.",
            },
        ],
        "quiz_count": 4,
        "energy_budget": 18,
        "step_budget": 25,
        "max_attempts": 3,
    },
]


def get_task_bank() -> List[Dict[str, Any]]:
    """Return a deep copy of the task bank."""
    return deepcopy(TASK_BANK)


def select_quiz_questions(
    task: Dict[str, Any],
    rng: Optional[random.Random] = None,
) -> List[Dict[str, Any]]:
    """Randomly select quiz_count questions from the pool for a task.

    Supports both the new 'quiz_pool' format and the legacy 'quiz' format.
    Returns a list of question dicts ready for the environment.
    """
    if rng is None:
        rng = random.Random()

    pool = task.get("quiz_pool", task.get("quiz", []))
    count = task.get("quiz_count", len(pool))
    count = min(count, len(pool))

    selected = rng.sample(pool, count)

    # Re-number question_ids sequentially so they don't collide
    for i, q in enumerate(selected):
        q["question_id"] = f"q{i + 1}"

    return selected
