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
                    "by Tim Berners-Lee in 1991. The latest version is HTML5."
                ),
            },
            {
                "section_id": "s2",
                "title": "Core Tags",
                "content": (
                    "The <h1> to <h6> tags define headings. <p> defines "
                    "a paragraph. <a> creates a hyperlink using the href attribute. "
                    "<img> embeds an image using the src attribute. "
                    "<div> is a block-level container. <span> is an inline container. "
                    "<ul> creates an unordered list, <ol> creates an ordered list, "
                    "and <li> is a list item. <br> inserts a line break. "
                    "<strong> makes text bold. <em> makes text italic. "
                    "<table> creates a table with <tr> for rows, <th> for headers, "
                    "and <td> for data cells."
                ),
            },
            {
                "section_id": "s3",
                "title": "Document Structure and Forms",
                "content": (
                    "Every HTML document begins with <!DOCTYPE html>. "
                    "The <html> element is the root. <head> contains "
                    "metadata like <title> and <meta charset='UTF-8'>. "
                    "<body> contains visible content. "
                    "The <link> tag links external stylesheets. "
                    "The <script> tag embeds or references JavaScript. "
                    "Forms use <form>, <input>, <textarea>, <select>, "
                    "and <button>. The action attribute on <form> specifies "
                    "where to send form data. The method attribute can be GET or POST. "
                    "Semantic tags include <header>, <nav>, <main>, <article>, "
                    "<section>, <aside>, and <footer>."
                ),
            },
        ],
        "quiz_pool": [
            {
                "question_id": "q1",
                "question": "What does HTML stand for?",
                "options": ["HyperText Markup Language", "High Tech Modern Language",
                            "Hyper Transfer Markup Language", "Home Tool Markup Language"],
                "correct_options": [0], "type": "single", "key_section": "s1",
                "wrong_feedback": "Review section 'What is HTML?' for the full name.",
            },
            {
                "question_id": "q2",
                "question": "Which tag creates a hyperlink?",
                "options": ["<img>", "<p>", "<a>", "<h1>"],
                "correct_options": [2], "type": "single", "key_section": "s2",
                "wrong_feedback": "Review 'Core Tags' for the hyperlink tag.",
            },
            {
                "question_id": "q3",
                "question": "Who invented HTML?",
                "options": ["Brendan Eich", "Tim Berners-Lee", "Guido van Rossum", "James Gosling"],
                "correct_options": [1], "type": "single", "key_section": "s1",
                "wrong_feedback": "Review 'What is HTML?' for the inventor.",
            },
            {
                "question_id": "q4",
                "question": "Which tag defines a paragraph?",
                "options": ["<h1>", "<div>", "<p>", "<a>"],
                "correct_options": [2], "type": "single", "key_section": "s2",
                "wrong_feedback": "Review 'Core Tags' — <p> defines a paragraph.",
            },
            {
                "question_id": "q5",
                "question": "What does <!DOCTYPE html> declare?",
                "options": ["A comment", "The document type as HTML5", "A JavaScript function", "A CSS rule"],
                "correct_options": [1], "type": "single", "key_section": "s3",
                "wrong_feedback": "Review 'Document Structure' for the DOCTYPE role.",
            },
            {
                "question_id": "q6",
                "question": "Which tag embeds an image?",
                "options": ["<a>", "<img>", "<div>", "<span>"],
                "correct_options": [1], "type": "single", "key_section": "s2",
                "wrong_feedback": "Review 'Core Tags' for the image tag.",
            },
            {
                "question_id": "q7",
                "question": "Which tags are used for lists in HTML? (Select ALL)",
                "options": ["<ul>", "<ol>", "<li>", "<div>"],
                "correct_options": [0, 1, 2], "type": "multi", "key_section": "s2",
                "wrong_feedback": "Review 'Core Tags' for list-related tags.",
            },
            {
                "question_id": "q8",
                "question": "Where is metadata placed in an HTML document?",
                "options": ["<body>", "<head>", "<footer>", "<main>"],
                "correct_options": [1], "type": "single", "key_section": "s3",
                "wrong_feedback": "Review 'Document Structure' for the metadata container.",
            },
            {
                "question_id": "q9",
                "question": "What is the root element of an HTML document?",
                "options": ["<head>", "<body>", "<html>", "<div>"],
                "correct_options": [2], "type": "single", "key_section": "s3",
                "wrong_feedback": "Review 'Document Structure' for the root element.",
            },
            {
                "question_id": "q10",
                "question": "Which tag links an external CSS stylesheet?",
                "options": ["<script>", "<style>", "<link>", "<meta>"],
                "correct_options": [2], "type": "single", "key_section": "s3",
                "wrong_feedback": "Review 'Document Structure' for the <link> tag.",
            },
            {
                "question_id": "q11",
                "question": "What is the latest version of HTML?",
                "options": ["HTML4", "XHTML", "HTML5", "HTML3"],
                "correct_options": [2], "type": "single", "key_section": "s1",
                "wrong_feedback": "Review 'What is HTML?' for the latest version.",
            },
            {
                "question_id": "q12",
                "question": "Which attribute specifies the URL for a hyperlink?",
                "options": ["src", "href", "action", "link"],
                "correct_options": [1], "type": "single", "key_section": "s2",
                "wrong_feedback": "Review 'Core Tags' — <a> uses the href attribute.",
            },
            {
                "question_id": "q13",
                "question": "Which tag makes text bold?",
                "options": ["<em>", "<strong>", "<b>", "<span>"],
                "correct_options": [1], "type": "single", "key_section": "s2",
                "wrong_feedback": "Review 'Core Tags' for bold text.",
            },
            {
                "question_id": "q14",
                "question": "Which are semantic HTML5 elements? (Select ALL)",
                "options": ["<header>", "<div>", "<article>", "<footer>"],
                "correct_options": [0, 2, 3], "type": "multi", "key_section": "s3",
                "wrong_feedback": "Review 'Document Structure' for semantic tags.",
            },
            {
                "question_id": "q15",
                "question": "What attribute on <form> specifies where to send data?",
                "options": ["method", "action", "target", "enctype"],
                "correct_options": [1], "type": "single", "key_section": "s3",
                "wrong_feedback": "Review 'Document Structure' — the action attribute.",
            },
            {
                "question_id": "q16",
                "question": "Which tag creates a table row?",
                "options": ["<td>", "<th>", "<tr>", "<table>"],
                "correct_options": [2], "type": "single", "key_section": "s2",
                "wrong_feedback": "Review 'Core Tags' — <tr> creates table rows.",
            },
            {
                "question_id": "q17",
                "question": "What is <div> used for?",
                "options": ["Creating hyperlinks", "Embedding images",
                            "Block-level container", "Inline text styling"],
                "correct_options": [2], "type": "single", "key_section": "s2",
                "wrong_feedback": "Review 'Core Tags' — <div> is a block-level container.",
            },
            {
                "question_id": "q18",
                "question": "Which tag inserts a line break?",
                "options": ["<hr>", "<br>", "<lb>", "<break>"],
                "correct_options": [1], "type": "single", "key_section": "s2",
                "wrong_feedback": "Review 'Core Tags' — <br> inserts line breaks.",
            },
            {
                "question_id": "q19",
                "question": "Which form elements accept user input? (Select ALL)",
                "options": ["<input>", "<textarea>", "<select>", "<div>"],
                "correct_options": [0, 1, 2], "type": "multi", "key_section": "s3",
                "wrong_feedback": "Review 'Document Structure' for form elements.",
            },
            {
                "question_id": "q20",
                "question": "In what year was HTML invented?",
                "options": ["1989", "1991", "1995", "2000"],
                "correct_options": [1], "type": "single", "key_section": "s1",
                "wrong_feedback": "Review 'What is HTML?' — HTML was created in 1991.",
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
        "instruction": "Study Python data type materials, then attempt the quiz.",
        "study_materials": [
            {
                "section_id": "s1",
                "title": "Numeric Types",
                "content": (
                    "Python has int for whole numbers (x = 5) and float "
                    "for decimals (y = 3.14). Convert with int() and float(). "
                    "Python also has complex numbers: z = 2 + 3j. "
                    "The bool type is a subclass of int: True is 1, False is 0. "
                    "Division with / always returns float. Floor division // returns int. "
                    "The modulo operator % returns the remainder."
                ),
            },
            {
                "section_id": "s2",
                "title": "Text Type",
                "content": (
                    "Strings (str) represent text. Defined with quotes: "
                    "'hello' or \"world\". Strings are immutable. "
                    "Concatenation uses +. Repetition uses *. "
                    "len() returns the string length. "
                    "f-strings like f'{name}' allow inline expressions. "
                    "Common methods: .upper(), .lower(), .strip(), .split(), "
                    ".replace(), .find(), .startswith(), .endswith(). "
                    "Slicing: s[1:4] returns characters at index 1, 2, 3."
                ),
            },
            {
                "section_id": "s3",
                "title": "Collections",
                "content": (
                    "A list is ordered and mutable: [1, 2, 3]. Methods: "
                    ".append(), .extend(), .pop(), .sort(), .reverse(). "
                    "A tuple is ordered but immutable: (1, 2, 3). "
                    "A dict maps keys to values: {'a': 1}. Methods: "
                    ".keys(), .values(), .items(), .get(). "
                    "A set holds unique unordered items: {1, 2, 3}. "
                    "Set operations: union |, intersection &, difference -. "
                    "A frozenset is an immutable version of a set. "
                    "List comprehension: [x**2 for x in range(5)]."
                ),
            },
        ],
        "quiz_pool": [
            {
                "question_id": "q1",
                "question": "What type is 3.14 in Python?",
                "options": ["int", "str", "float", "list"],
                "correct_options": [2], "type": "single", "key_section": "s1",
                "wrong_feedback": "Review 'Numeric Types' for decimal number types.",
            },
            {
                "question_id": "q2",
                "question": "Which collection type is ordered but immutable?",
                "options": ["list", "dict", "set", "tuple"],
                "correct_options": [3], "type": "single", "key_section": "s3",
                "wrong_feedback": "Review 'Collections' for the immutable ordered type.",
            },
            {
                "question_id": "q3",
                "question": "What does len('hello') return?",
                "options": ["4", "5", "6", "Error"],
                "correct_options": [1], "type": "single", "key_section": "s2",
                "wrong_feedback": "Review 'Text Type' — len() returns character count.",
            },
            {
                "question_id": "q4",
                "question": "Which type is a subclass of int?",
                "options": ["float", "str", "bool", "complex"],
                "correct_options": [2], "type": "single", "key_section": "s1",
                "wrong_feedback": "Review 'Numeric Types' — bool is a subclass of int.",
            },
            {
                "question_id": "q5",
                "question": "How do you write an f-string?",
                "options": ["f'{expr}'", "str(expr)", "'%s' % expr", "format(expr)"],
                "correct_options": [0], "type": "single", "key_section": "s2",
                "wrong_feedback": "Review 'Text Type' for f-string syntax.",
            },
            {
                "question_id": "q6",
                "question": "Which collection holds unique unordered items?",
                "options": ["list", "tuple", "set", "dict"],
                "correct_options": [2], "type": "single", "key_section": "s3",
                "wrong_feedback": "Review 'Collections' for unique unordered items.",
            },
            {
                "question_id": "q7",
                "question": "Which are valid Python number types? (Select ALL)",
                "options": ["int", "float", "complex", "char"],
                "correct_options": [0, 1, 2], "type": "multi", "key_section": "s1",
                "wrong_feedback": "Review 'Numeric Types' for built-in number types.",
            },
            {
                "question_id": "q8",
                "question": "Are Python strings mutable?",
                "options": ["Yes", "No", "Only single characters", "Depends on length"],
                "correct_options": [1], "type": "single", "key_section": "s2",
                "wrong_feedback": "Review 'Text Type' — strings are immutable.",
            },
            {
                "question_id": "q9",
                "question": "What is a frozenset?",
                "options": ["A mutable set", "An immutable version of a set",
                            "A sorted list", "A type of dictionary"],
                "correct_options": [1], "type": "single", "key_section": "s3",
                "wrong_feedback": "Review 'Collections' for frozenset.",
            },
            {
                "question_id": "q10",
                "question": "What operator concatenates strings?",
                "options": ["&", "+", ".", "++"],
                "correct_options": [1], "type": "single", "key_section": "s2",
                "wrong_feedback": "Review 'Text Type' — + concatenates strings.",
            },
            {
                "question_id": "q11",
                "question": "What does // do in Python?",
                "options": ["Regular division", "Floor division", "Modulo", "Power"],
                "correct_options": [1], "type": "single", "key_section": "s1",
                "wrong_feedback": "Review 'Numeric Types' — // is floor division.",
            },
            {
                "question_id": "q12",
                "question": "What does 'hello'[1:4] return?",
                "options": ["'hel'", "'ell'", "'ello'", "'hell'"],
                "correct_options": [1], "type": "single", "key_section": "s2",
                "wrong_feedback": "Review 'Text Type' — slicing s[1:4] returns index 1,2,3.",
            },
            {
                "question_id": "q13",
                "question": "Which list method adds an element to the end?",
                "options": [".insert()", ".append()", ".extend()", ".add()"],
                "correct_options": [1], "type": "single", "key_section": "s3",
                "wrong_feedback": "Review 'Collections' — .append() adds to the end.",
            },
            {
                "question_id": "q14",
                "question": "Which dict method safely gets a value with a default?",
                "options": [".find()", ".get()", ".fetch()", ".value()"],
                "correct_options": [1], "type": "single", "key_section": "s3",
                "wrong_feedback": "Review 'Collections' — .get() with default value.",
            },
            {
                "question_id": "q15",
                "question": "What is the set intersection operator?",
                "options": ["|", "&", "-", "^"],
                "correct_options": [1], "type": "single", "key_section": "s3",
                "wrong_feedback": "Review 'Collections' — & is set intersection.",
            },
            {
                "question_id": "q16",
                "question": "What does .strip() do on a string?",
                "options": ["Removes vowels", "Removes whitespace from both ends",
                            "Reverses the string", "Converts to uppercase"],
                "correct_options": [1], "type": "single", "key_section": "s2",
                "wrong_feedback": "Review 'Text Type' — .strip() removes whitespace.",
            },
            {
                "question_id": "q17",
                "question": "What does % operator return for numbers?",
                "options": ["Quotient", "Remainder", "Product", "Power"],
                "correct_options": [1], "type": "single", "key_section": "s1",
                "wrong_feedback": "Review 'Numeric Types' — % returns the remainder.",
            },
            {
                "question_id": "q18",
                "question": "Which are mutable Python collections? (Select ALL)",
                "options": ["list", "tuple", "dict", "set"],
                "correct_options": [0, 2, 3], "type": "multi", "key_section": "s3",
                "wrong_feedback": "Review 'Collections' — tuples and frozensets are immutable.",
            },
            {
                "question_id": "q19",
                "question": "What does [x**2 for x in range(3)] produce?",
                "options": ["[1, 4, 9]", "[0, 1, 4]", "[0, 2, 4]", "[1, 2, 3]"],
                "correct_options": [1], "type": "single", "key_section": "s3",
                "wrong_feedback": "Review 'Collections' — range(3) gives 0,1,2.",
            },
            {
                "question_id": "q20",
                "question": "What does / always return in Python 3?",
                "options": ["int", "float", "str", "bool"],
                "correct_options": [1], "type": "single", "key_section": "s1",
                "wrong_feedback": "Review 'Numeric Types' — / always returns float.",
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
                "title": "Element and Group Selectors",
                "content": (
                    "Element selectors target HTML tags: 'p { color: red; }'. "
                    "Universal selector '*' matches everything and has 0 specificity. "
                    "Grouping: 'h1, h2, h3 { margin: 0; }' applies to all listed. "
                    "Attribute selectors: [type='text'] targets inputs with type text. "
                    "[href^='https'] matches hrefs starting with https. "
                    "[class~='warning'] matches elements with 'warning' in class list."
                ),
            },
            {
                "section_id": "s2",
                "title": "Class and ID Selectors",
                "content": (
                    "Class selectors use a dot: '.warning { color: orange; }'. "
                    "ID selectors use a hash: '#main { width: 100%; }'. "
                    "IDs must be unique per page. Classes can be reused freely. "
                    "Chaining classes: '.btn.primary' matches elements with both. "
                    "You can combine: 'div.highlight' targets <div> with class highlight."
                ),
            },
            {
                "section_id": "s3",
                "title": "Combinators and Pseudo-classes",
                "content": (
                    "Descendant 'div p' selects all <p> inside <div>. "
                    "Child 'div > p' selects only direct children. "
                    "Adjacent sibling 'h1 + p' selects <p> right after <h1>. "
                    "General sibling 'h1 ~ p' selects all <p> siblings after <h1>. "
                    "Pseudo-classes: :hover, :focus, :first-child, :last-child, "
                    ":nth-child(n), :not(selector). "
                    "Pseudo-elements: ::before, ::after, ::first-line, ::first-letter."
                ),
            },
            {
                "section_id": "s4",
                "title": "Specificity and Cascade",
                "content": (
                    "Inline styles = 1000. ID selectors = 100. "
                    "Class/pseudo-class/attribute selectors = 10. Element/pseudo-element = 1. "
                    "Universal selector * = 0. "
                    "!important overrides all normal specificity. "
                    "When specificity is equal, the last rule wins (cascade order). "
                    "Inherited properties have no specificity — they're overridden by any rule."
                ),
            },
        ],
        "quiz_pool": [
            {
                "question_id": "q1",
                "question": "Which selector targets an element by unique identifier?",
                "options": [".classname", "#idname", "tagname", "*"],
                "correct_options": [1], "type": "single", "key_section": "s2",
                "wrong_feedback": "Review 'Class and ID Selectors' for unique IDs.",
            },
            {
                "question_id": "q2",
                "question": "What does 'div > p' target?",
                "options": ["All <p> on page", "All <p> inside any <div>",
                            "Only direct <p> children of <div>", "<p> next to <div>"],
                "correct_options": [2], "type": "single", "key_section": "s3",
                "wrong_feedback": "Review 'Combinators' for the child combinator.",
            },
            {
                "question_id": "q3",
                "question": "Which have HIGHER specificity than class selectors? (Select ALL)",
                "options": ["Element selectors", "ID selectors", "Inline styles", "Universal selector (*)"],
                "correct_options": [1, 2], "type": "multi", "key_section": "s4",
                "wrong_feedback": "Review 'Specificity Rules' and compare values.",
            },
            {
                "question_id": "q4",
                "question": "What does the universal selector * match?",
                "options": ["Only <div>", "All elements", "Only classes", "Nothing"],
                "correct_options": [1], "type": "single", "key_section": "s1",
                "wrong_feedback": "Review 'Element Selectors' for universal selector.",
            },
            {
                "question_id": "q5",
                "question": "What specificity value does :hover have?",
                "options": ["0", "1", "10", "100"],
                "correct_options": [2], "type": "single", "key_section": "s4",
                "wrong_feedback": "Review 'Specificity' — pseudo-classes are class-level (10).",
            },
            {
                "question_id": "q6",
                "question": "What does 'h1 + p' select?",
                "options": ["All <p> inside <h1>", "The <p> immediately after <h1>",
                            "All <p> with class h1", "<h1> and <p> together"],
                "correct_options": [1], "type": "single", "key_section": "s3",
                "wrong_feedback": "Review 'Combinators' for adjacent sibling.",
            },
            {
                "question_id": "q7",
                "question": "Can you reuse an ID on multiple elements?",
                "options": ["Yes, always", "No, IDs must be unique", "Only in forms", "Only in divs"],
                "correct_options": [1], "type": "single", "key_section": "s2",
                "wrong_feedback": "Review 'Class and ID Selectors' — IDs are unique.",
            },
            {
                "question_id": "q8",
                "question": "Which are valid CSS combinators? (Select ALL)",
                "options": ["Descendant (space)", "Child (>)", "Adjacent sibling (+)", "Equality (==)"],
                "correct_options": [0, 1, 2], "type": "multi", "key_section": "s3",
                "wrong_feedback": "Review 'Combinators' for valid CSS combinators.",
            },
            {
                "question_id": "q9",
                "question": "What specificity does an inline style have?",
                "options": ["1", "10", "100", "1000"],
                "correct_options": [3], "type": "single", "key_section": "s4",
                "wrong_feedback": "Review 'Specificity' — inline styles = 1000.",
            },
            {
                "question_id": "q10",
                "question": "How do you chain two classes in CSS?",
                "options": [".a .b", ".a.b", ".a + .b", ".a > .b"],
                "correct_options": [1], "type": "single", "key_section": "s2",
                "wrong_feedback": "Review 'Class and ID Selectors' — chaining uses no space.",
            },
            {
                "question_id": "q11",
                "question": "What does [type='text'] select?",
                "options": ["All text nodes", "Elements with type attribute equal to 'text'",
                            "All <text> elements", "Nothing"],
                "correct_options": [1], "type": "single", "key_section": "s1",
                "wrong_feedback": "Review 'Element Selectors' for attribute selectors.",
            },
            {
                "question_id": "q12",
                "question": "What does 'h1 ~ p' select?",
                "options": ["<p> inside <h1>", "Only <p> right after <h1>",
                            "All <p> siblings after <h1>", "<p> before <h1>"],
                "correct_options": [2], "type": "single", "key_section": "s3",
                "wrong_feedback": "Review 'Combinators' for the general sibling combinator.",
            },
            {
                "question_id": "q13",
                "question": "What happens when two rules have equal specificity?",
                "options": ["First one wins", "Last one wins", "Neither applies", "Error"],
                "correct_options": [1], "type": "single", "key_section": "s4",
                "wrong_feedback": "Review 'Specificity' — last rule wins in cascade.",
            },
            {
                "question_id": "q14",
                "question": "Which pseudo-element adds content before an element?",
                "options": ["::after", "::before", "::first-line", ":hover"],
                "correct_options": [1], "type": "single", "key_section": "s3",
                "wrong_feedback": "Review 'Combinators' for pseudo-elements.",
            },
            {
                "question_id": "q15",
                "question": "Which are pseudo-classes? (Select ALL)",
                "options": [":hover", ":focus", "::before", ":first-child"],
                "correct_options": [0, 1, 3], "type": "multi", "key_section": "s3",
                "wrong_feedback": "::before is a pseudo-element, not pseudo-class.",
            },
            {
                "question_id": "q16",
                "question": "What specificity does an element selector have?",
                "options": ["0", "1", "10", "100"],
                "correct_options": [1], "type": "single", "key_section": "s4",
                "wrong_feedback": "Review 'Specificity' — element selectors = 1.",
            },
            {
                "question_id": "q17",
                "question": "What does :not(.active) select?",
                "options": ["Elements with class active", "Elements without class active",
                            "All active elements", "Nothing"],
                "correct_options": [1], "type": "single", "key_section": "s3",
                "wrong_feedback": "Review 'Combinators' — :not() is a negation pseudo-class.",
            },
            {
                "question_id": "q18",
                "question": "What does !important do?",
                "options": ["Adds a comment", "Overrides all normal specificity",
                            "Removes the rule", "Makes text bold"],
                "correct_options": [1], "type": "single", "key_section": "s4",
                "wrong_feedback": "Review 'Specificity' — !important overrides specificity.",
            },
            {
                "question_id": "q19",
                "question": "What does 'div.highlight' target?",
                "options": ["All <div> and all .highlight", "<div> with class highlight",
                            ".highlight inside <div>", "Only <highlight> tags"],
                "correct_options": [1], "type": "single", "key_section": "s2",
                "wrong_feedback": "Review 'Class and ID' — combining tag and class.",
            },
            {
                "question_id": "q20",
                "question": "What does :nth-child(2) select?",
                "options": ["Every second element", "The second child element",
                            "Two elements", "The last child"],
                "correct_options": [1], "type": "single", "key_section": "s3",
                "wrong_feedback": "Review 'Combinators' for :nth-child().",
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
                    "Events are browser-detected actions: clicks, key presses, "
                    "page loads, form submissions, scrolling, resizing. "
                    "JavaScript listens and responds with callback functions. "
                    "Events follow the Observer pattern. "
                    "The event object (e) contains details like target, type, "
                    "clientX, clientY, key, and shiftKey."
                ),
            },
            {
                "section_id": "s2",
                "title": "Event Listeners",
                "content": (
                    "addEventListener('click', handler) attaches a callback. "
                    "removeEventListener() detaches it (must reference same function). "
                    "Multiple listeners can exist on the same element. "
                    "The third parameter controls capture: { capture: true }. "
                    "{ once: true } auto-removes after first trigger. "
                    "{ passive: true } hints the browser for scroll performance."
                ),
            },
            {
                "section_id": "s3",
                "title": "Event Propagation",
                "content": (
                    "Capturing goes top-down (document to target). "
                    "Bubbling goes bottom-up (target to document). "
                    "Default is bubbling. stopPropagation() halts further propagation. "
                    "preventDefault() cancels the default browser action. "
                    "stopImmediatePropagation() stops other listeners on the same element. "
                    "Event delegation: attach one listener to a parent, check e.target."
                ),
            },
            {
                "section_id": "s4",
                "title": "Common Event Types",
                "content": (
                    "click: mouse click. dblclick: double click. contextmenu: right click. "
                    "keydown/keyup: keyboard. keypress is deprecated. "
                    "submit: form submission. change: value changed after blur. "
                    "input: value changed immediately. load: page loaded. "
                    "DOMContentLoaded: DOM ready before images load. "
                    "mouseover/mouseout: mouse entering/leaving (bubbles). "
                    "mouseenter/mouseleave: same but don't bubble. "
                    "focus/blur: element gaining/losing focus (don't bubble). "
                    "focusin/focusout: same but DO bubble. "
                    "scroll: element or page scrolled. resize: window resized."
                ),
            },
        ],
        "quiz_pool": [
            {
                "question_id": "q1",
                "question": "Which method attaches an event handler?",
                "options": ["onClick()", "addEventListener()", "attachEvent()", "bindEvent()"],
                "correct_options": [1], "type": "single", "key_section": "s2",
                "wrong_feedback": "Review 'Event Listeners' for the standard method.",
            },
            {
                "question_id": "q2",
                "question": "In which direction does bubbling propagate?",
                "options": ["Top to bottom", "Left to right", "Bottom to top", "Random"],
                "correct_options": [2], "type": "single", "key_section": "s3",
                "wrong_feedback": "Review 'Event Propagation' for bubbling direction.",
            },
            {
                "question_id": "q3",
                "question": "Which events fire when typing? (Select ALL)",
                "options": ["click", "keydown", "input", "load"],
                "correct_options": [1, 2], "type": "multi", "key_section": "s4",
                "wrong_feedback": "Review 'Common Event Types' for keyboard events.",
            },
            {
                "question_id": "q4",
                "question": "What does preventDefault() do?",
                "options": ["Stops propagation", "Cancels default browser action",
                            "Removes the listener", "Refreshes the page"],
                "correct_options": [1], "type": "single", "key_section": "s3",
                "wrong_feedback": "Review 'Event Propagation' for preventDefault().",
            },
            {
                "question_id": "q5",
                "question": "What pattern do events follow?",
                "options": ["Singleton", "Factory", "Observer", "Strategy"],
                "correct_options": [2], "type": "single", "key_section": "s1",
                "wrong_feedback": "Review 'What are Events?' for the design pattern.",
            },
            {
                "question_id": "q6",
                "question": "Which direction does capturing go?",
                "options": ["Bottom to top", "Top to bottom", "Left to right", "Circular"],
                "correct_options": [1], "type": "single", "key_section": "s3",
                "wrong_feedback": "Review 'Event Propagation' for capturing.",
            },
            {
                "question_id": "q7",
                "question": "How do you remove an event listener?",
                "options": ["deleteEvent()", "removeEventListener()", "detachEvent()", "unbind()"],
                "correct_options": [1], "type": "single", "key_section": "s2",
                "wrong_feedback": "Review 'Event Listeners' for removal.",
            },
            {
                "question_id": "q8",
                "question": "Which are mouse-related events? (Select ALL)",
                "options": ["click", "mouseover", "keydown", "dblclick"],
                "correct_options": [0, 1, 3], "type": "multi", "key_section": "s4",
                "wrong_feedback": "Review 'Common Event Types' for mouse events.",
            },
            {
                "question_id": "q9",
                "question": "Can multiple listeners exist on the same element?",
                "options": ["No", "Yes", "Only with jQuery", "Only in Chrome"],
                "correct_options": [1], "type": "single", "key_section": "s2",
                "wrong_feedback": "Review 'Event Listeners' — multiple are supported.",
            },
            {
                "question_id": "q10",
                "question": "What event fires when an element gains focus?",
                "options": ["click", "hover", "focus", "load"],
                "correct_options": [2], "type": "single", "key_section": "s4",
                "wrong_feedback": "Review 'Common Event Types' for focus.",
            },
            {
                "question_id": "q11",
                "question": "What does { once: true } do?",
                "options": ["Makes listener passive", "Auto-removes after first trigger",
                            "Enables capturing", "Prevents default"],
                "correct_options": [1], "type": "single", "key_section": "s2",
                "wrong_feedback": "Review 'Event Listeners' for the once option.",
            },
            {
                "question_id": "q12",
                "question": "What is event delegation?",
                "options": ["Adding listeners to every child", "Attaching one listener to a parent",
                            "Using inline event attributes", "Removing all listeners"],
                "correct_options": [1], "type": "single", "key_section": "s3",
                "wrong_feedback": "Review 'Event Propagation' for delegation.",
            },
            {
                "question_id": "q13",
                "question": "Which event fires when the DOM is ready (before images)?",
                "options": ["load", "DOMContentLoaded", "ready", "init"],
                "correct_options": [1], "type": "single", "key_section": "s4",
                "wrong_feedback": "Review 'Common Event Types' for DOMContentLoaded.",
            },
            {
                "question_id": "q14",
                "question": "What property on the event object gives the clicked element?",
                "options": ["e.source", "e.target", "e.element", "e.node"],
                "correct_options": [1], "type": "single", "key_section": "s1",
                "wrong_feedback": "Review 'What are Events?' — e.target gives the target.",
            },
            {
                "question_id": "q15",
                "question": "Which right-click event is available?",
                "options": ["rightclick", "contextmenu", "auxclick", "menuclick"],
                "correct_options": [1], "type": "single", "key_section": "s4",
                "wrong_feedback": "Review 'Common Event Types' for right-click.",
            },
            {
                "question_id": "q16",
                "question": "Which focus events bubble? (Select ALL)",
                "options": ["focus", "blur", "focusin", "focusout"],
                "correct_options": [2, 3], "type": "multi", "key_section": "s4",
                "wrong_feedback": "focus/blur don't bubble; focusin/focusout do.",
            },
            {
                "question_id": "q17",
                "question": "What does stopImmediatePropagation() do?",
                "options": ["Stops only bubbling", "Stops further listeners on same element",
                            "Prevents default action", "Removes the element"],
                "correct_options": [1], "type": "single", "key_section": "s3",
                "wrong_feedback": "Review 'Event Propagation' for stopImmediatePropagation.",
            },
            {
                "question_id": "q18",
                "question": "What is the difference between 'change' and 'input' events?",
                "options": ["They are identical", "'change' fires on blur, 'input' fires immediately",
                            "'input' fires on blur, 'change' fires immediately", "Neither exists"],
                "correct_options": [1], "type": "single", "key_section": "s4",
                "wrong_feedback": "Review 'Common Event Types' for change vs input.",
            },
            {
                "question_id": "q19",
                "question": "Is keypress deprecated?",
                "options": ["No", "Yes", "Only in Firefox", "Only for mobile"],
                "correct_options": [1], "type": "single", "key_section": "s4",
                "wrong_feedback": "Review 'Common Event Types' — keypress is deprecated.",
            },
            {
                "question_id": "q20",
                "question": "What does { passive: true } hint?",
                "options": ["Auto-remove listener", "Won't call preventDefault (scroll perf)",
                            "Runs in capture phase", "Delays execution"],
                "correct_options": [1], "type": "single", "key_section": "s2",
                "wrong_feedback": "Review 'Event Listeners' for the passive option.",
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
                    "PATCH partially updates (NOT necessarily idempotent). "
                    "DELETE removes (idempotent). "
                    "HEAD is like GET but returns only headers. "
                    "OPTIONS returns allowed methods for a resource. "
                    "Safe methods don't modify state: GET, HEAD, OPTIONS."
                ),
            },
            {
                "section_id": "s2",
                "title": "Status Codes",
                "content": (
                    "1xx: Informational. 2xx: Success. 3xx: Redirection. "
                    "4xx: Client Error. 5xx: Server Error. "
                    "200 OK. 201 Created. 204 No Content. "
                    "301 Moved Permanently. 304 Not Modified. "
                    "400 Bad Request. 401 Unauthorized (unauthenticated). "
                    "403 Forbidden (authenticated but no permission). "
                    "404 Not Found. 409 Conflict. "
                    "429 Too Many Requests. 500 Internal Server Error. "
                    "502 Bad Gateway. 503 Service Unavailable."
                ),
            },
            {
                "section_id": "s3",
                "title": "Resource Naming and URL Design",
                "content": (
                    "Use nouns not verbs: /users not /getUsers. "
                    "Use plural: /users not /user. "
                    "Nest for relations: /users/123/orders. "
                    "Query params for filtering: /users?active=true. "
                    "Use kebab-case: /user-profiles not /userProfiles. "
                    "Don't use file extensions in URLs. "
                    "Use forward slashes for hierarchy. "
                    "Trailing slashes should be consistent."
                ),
            },
            {
                "section_id": "s4",
                "title": "Authentication and Security",
                "content": (
                    "API Key: simple, in header or query. "
                    "OAuth 2.0: token-based delegated access with scopes. "
                    "JWT: self-contained tokens = header.payload.signature. "
                    "Bearer tokens go in Authorization header: 'Bearer <token>'. "
                    "Basic Auth sends base64-encoded username:password. "
                    "CORS (Cross-Origin Resource Sharing) controls cross-domain access. "
                    "Always validate and sanitize input. "
                    "Use HTTPS everywhere."
                ),
            },
            {
                "section_id": "s5",
                "title": "Best Practices and Patterns",
                "content": (
                    "Version your API: /v1/users or via Accept header. "
                    "Paginate lists: ?page=1&limit=20 or cursor-based. "
                    "Consistent errors: {error: {code, message, details}}. "
                    "Implement rate limiting with 429 responses. "
                    "Use HATEOAS for discoverability (links in responses). "
                    "Support content negotiation via Accept headers. "
                    "Use ETags for caching and conditional requests. "
                    "Implement idempotency keys for safe retries of POST. "
                    "Document with OpenAPI/Swagger."
                ),
            },
        ],
        "quiz_pool": [
            {
                "question_id": "q1",
                "question": "Which HTTP methods are idempotent? (Select ALL)",
                "options": ["GET", "POST", "PUT", "DELETE"],
                "correct_options": [0, 2, 3], "type": "multi", "key_section": "s1",
                "wrong_feedback": "Review 'HTTP Methods' for idempotency.",
            },
            {
                "question_id": "q2",
                "question": "What status code means a new resource was created?",
                "options": ["200 OK", "201 Created", "204 No Content", "400 Bad Request"],
                "correct_options": [1], "type": "single", "key_section": "s2",
                "wrong_feedback": "Review 'Status Codes' for creation responses.",
            },
            {
                "question_id": "q3",
                "question": "Which URL follows REST conventions?",
                "options": ["/getUsers", "/user/list", "/users", "/api/fetchAllUsers"],
                "correct_options": [2], "type": "single", "key_section": "s3",
                "wrong_feedback": "Review 'Resource Naming' for noun-based URLs.",
            },
            {
                "question_id": "q4",
                "question": "Which are valid API auth methods? (Select ALL)",
                "options": ["API Key", "OAuth 2.0", "FTP", "JWT"],
                "correct_options": [0, 1, 3], "type": "multi", "key_section": "s4",
                "wrong_feedback": "Review 'Authentication' — FTP is not auth.",
            },
            {
                "question_id": "q5",
                "question": "What status code indicates rate limiting?",
                "options": ["400", "403", "429", "500"],
                "correct_options": [2], "type": "single", "key_section": "s2",
                "wrong_feedback": "Review 'Status Codes' for rate limiting.",
            },
            {
                "question_id": "q6",
                "question": "What are the three parts of a JWT?",
                "options": ["header.payload.signature", "key.value.hash",
                            "user.role.token", "id.secret.expiry"],
                "correct_options": [0], "type": "single", "key_section": "s4",
                "wrong_feedback": "Review 'Authentication' for JWT structure.",
            },
            {
                "question_id": "q7",
                "question": "Which HTTP method partially updates a resource?",
                "options": ["GET", "PUT", "PATCH", "POST"],
                "correct_options": [2], "type": "single", "key_section": "s1",
                "wrong_feedback": "Review 'HTTP Methods' for partial updates.",
            },
            {
                "question_id": "q8",
                "question": "Which are REST best practices? (Select ALL)",
                "options": ["Version your API", "Use HTTPS", "Use rate limiting", "Use verbs in URLs"],
                "correct_options": [0, 1, 2], "type": "multi", "key_section": "s5",
                "wrong_feedback": "Review 'Best Practices' — no verbs in URLs.",
            },
            {
                "question_id": "q9",
                "question": "What naming convention should REST URLs use?",
                "options": ["camelCase", "PascalCase", "kebab-case", "snake_case"],
                "correct_options": [2], "type": "single", "key_section": "s3",
                "wrong_feedback": "Review 'Resource Naming' for URL conventions.",
            },
            {
                "question_id": "q10",
                "question": "What does 204 mean?",
                "options": ["OK with body", "Created", "No Content (success)", "Not Found"],
                "correct_options": [2], "type": "single", "key_section": "s2",
                "wrong_feedback": "Review 'Status Codes' for 204.",
            },
            {
                "question_id": "q11",
                "question": "What is HATEOAS?",
                "options": ["A hashing algorithm", "Hypermedia links for discoverability",
                            "A database pattern", "An HTTP header"],
                "correct_options": [1], "type": "single", "key_section": "s5",
                "wrong_feedback": "Review 'Best Practices' for HATEOAS.",
            },
            {
                "question_id": "q12",
                "question": "Which method is safe (no side effects)?",
                "options": ["POST", "DELETE", "PUT", "GET"],
                "correct_options": [3], "type": "single", "key_section": "s1",
                "wrong_feedback": "Review 'HTTP Methods' — GET is safe.",
            },
            {
                "question_id": "q13",
                "question": "What is the difference between 401 and 403?",
                "options": ["They are the same", "401=unauthenticated, 403=no permission",
                            "401=not found, 403=server error", "401=redirect, 403=forbidden"],
                "correct_options": [1], "type": "single", "key_section": "s2",
                "wrong_feedback": "Review 'Status Codes' for 401 vs 403.",
            },
            {
                "question_id": "q14",
                "question": "What is CORS?",
                "options": ["A caching mechanism", "Cross-Origin Resource Sharing",
                            "A REST framework", "A status code"],
                "correct_options": [1], "type": "single", "key_section": "s4",
                "wrong_feedback": "Review 'Authentication' for CORS.",
            },
            {
                "question_id": "q15",
                "question": "What is an idempotency key used for?",
                "options": ["Encrypting data", "Safe retries of POST requests",
                            "Rate limiting", "Authentication"],
                "correct_options": [1], "type": "single", "key_section": "s5",
                "wrong_feedback": "Review 'Best Practices' for idempotency keys.",
            },
            {
                "question_id": "q16",
                "question": "Which HTTP method returns only headers?",
                "options": ["GET", "HEAD", "OPTIONS", "TRACE"],
                "correct_options": [1], "type": "single", "key_section": "s1",
                "wrong_feedback": "Review 'HTTP Methods' for HEAD.",
            },
            {
                "question_id": "q17",
                "question": "What are ETags used for?",
                "options": ["Authentication", "Caching and conditional requests",
                            "Rate limiting", "URL routing"],
                "correct_options": [1], "type": "single", "key_section": "s5",
                "wrong_feedback": "Review 'Best Practices' for ETags.",
            },
            {
                "question_id": "q18",
                "question": "Which status codes indicate server errors? (Select ALL)",
                "options": ["404", "500", "502", "503"],
                "correct_options": [1, 2, 3], "type": "multi", "key_section": "s2",
                "wrong_feedback": "404 is client error. 5xx are server errors.",
            },
            {
                "question_id": "q19",
                "question": "How should nested resources be represented?",
                "options": ["/users?orders=123", "/users/123/orders",
                            "/users-orders/123", "/getOrdersForUser/123"],
                "correct_options": [1], "type": "single", "key_section": "s3",
                "wrong_feedback": "Review 'Resource Naming' for nested resources.",
            },
            {
                "question_id": "q20",
                "question": "What documentation standard is recommended for REST APIs?",
                "options": ["JSDoc", "Javadoc", "OpenAPI/Swagger", "WSDL"],
                "correct_options": [2], "type": "single", "key_section": "s5",
                "wrong_feedback": "Review 'Best Practices' for API documentation.",
            },
        ],
        "quiz_count": 4,
        "energy_budget": 18,
        "step_budget": 25,
        "max_attempts": 3,
    },

    # ── MEDIUM #3: Salesforce Admin Basics ────────────────────────────────
    {
        "id": "salesforce_admin",
        "task_type": "course_module",
        "difficulty": "medium",
        "title": "Salesforce Admin Basics",
        "instruction": (
            "This module covers Salesforce platform fundamentals for admins. "
            "Study the materials and answer the quiz. Some questions require "
            "selecting multiple correct answers."
        ),
        "study_materials": [
            {
                "section_id": "s1",
                "title": "Salesforce Platform Overview",
                "content": (
                    "Salesforce is a cloud-based CRM platform. It uses a multi-tenant "
                    "architecture where all customers share the same infrastructure. "
                    "The platform operates on metadata-driven development — you can "
                    "build apps using clicks, not code (declarative). "
                    "AppExchange is the Salesforce marketplace for apps. "
                    "Salesforce editions include Essentials, Professional, Enterprise, "
                    "and Unlimited. Trailhead is Salesforce's free learning platform. "
                    "The three main clouds are Sales Cloud, Service Cloud, and Marketing Cloud."
                ),
            },
            {
                "section_id": "s2",
                "title": "Objects, Fields, and Records",
                "content": (
                    "Standard objects are built-in: Account, Contact, Opportunity, Lead, Case. "
                    "Custom objects are user-created and end with __c (e.g., Invoice__c). "
                    "Fields store data: Text, Number, Date, Picklist, Checkbox, Lookup, "
                    "Master-Detail, Formula, Roll-Up Summary. "
                    "Lookup relationships are loose (child can exist without parent). "
                    "Master-Detail relationships are tight (cascade delete, roll-up summaries). "
                    "Records are individual rows of data in an object. "
                    "Record Types control layouts, picklist values, and business processes. "
                    "Page Layouts control which fields users see on a record page."
                ),
            },
            {
                "section_id": "s3",
                "title": "Security Model",
                "content": (
                    "Organization-level security: Login IP ranges, login hours. "
                    "Object-level security: Profiles and Permission Sets. "
                    "Profiles define baseline permissions — every user has exactly one. "
                    "Permission Sets add extra permissions on top of profiles. "
                    "Field-level security (FLS) controls visibility of individual fields. "
                    "Record-level security uses OWD (Organization-Wide Defaults): "
                    "Private, Public Read Only, Public Read/Write. "
                    "Role Hierarchy grants access up the chain. "
                    "Sharing Rules extend access to specific groups. "
                    "Manual Sharing allows individual record sharing."
                ),
            },
            {
                "section_id": "s4",
                "title": "Automation and Reports",
                "content": (
                    "Flow Builder: most powerful declarative automation tool. "
                    "Types: Screen Flow (user interaction), Record-Triggered Flow "
                    "(before/after save), Scheduled Flow, Platform Event Flow. "
                    "Process Builder is being retired in favor of Flow. "
                    "Workflow Rules are legacy (simple field updates, email alerts). "
                    "Approval Processes route records through approval steps. "
                    "Report Types: Tabular, Summary, Matrix, Joined. "
                    "Dashboards display report data as visual components. "
                    "Report Folders control access. Dashboards have a running user."
                ),
            },
        ],
        "quiz_pool": [
            {
                "question_id": "q1",
                "question": "What development approach does Salesforce emphasize?",
                "options": ["Command-line only", "Declarative (clicks not code)", "Assembly language", "FTP uploads"],
                "correct_options": [1], "type": "single", "key_section": "s1",
                "wrong_feedback": "Review 'Platform Overview' — declarative development.",
            },
            {
                "question_id": "q1",
                "question": "What architecture does Salesforce use?",
                "options": ["Single-tenant", "Multi-tenant", "Peer-to-peer", "Hybrid"],
                "correct_options": [1], "type": "single", "key_section": "s1",
                "wrong_feedback": "Review 'Platform Overview' — multi-tenant architecture.",
            },
            {
                "question_id": "q2",
                "question": "What suffix do custom objects have?",
                "options": ["__r", "__c", "__x", "__s"],
                "correct_options": [1], "type": "single", "key_section": "s2",
                "wrong_feedback": "Review 'Objects' — custom objects end with __c.",
            },
            {
                "question_id": "q3",
                "question": "Which relationship type supports cascade delete?",
                "options": ["Lookup", "Master-Detail", "Many-to-Many", "Self"],
                "correct_options": [1], "type": "single", "key_section": "s2",
                "wrong_feedback": "Review 'Objects' for Master-Detail relationships.",
            },
            {
                "question_id": "q4",
                "question": "How many Profiles can a user have?",
                "options": ["Unlimited", "Up to 5", "Exactly one", "None"],
                "correct_options": [2], "type": "single", "key_section": "s3",
                "wrong_feedback": "Review 'Security' — every user has exactly one profile.",
            },
            {
                "question_id": "q5",
                "question": "What is OWD in Salesforce?",
                "options": ["Object Workflow Definition", "Organization-Wide Defaults",
                            "Online Web Dashboard", "Open Widget Design"],
                "correct_options": [1], "type": "single", "key_section": "s3",
                "wrong_feedback": "Review 'Security' for Organization-Wide Defaults.",
            },
            {
                "question_id": "q6",
                "question": "Which are standard Salesforce objects? (Select ALL)",
                "options": ["Account", "Contact", "Invoice", "Opportunity"],
                "correct_options": [0, 1, 3], "type": "multi", "key_section": "s2",
                "wrong_feedback": "Invoice is custom. Account, Contact, Opportunity are standard.",
            },
            {
                "question_id": "q7",
                "question": "What is the most powerful declarative automation tool?",
                "options": ["Workflow Rules", "Process Builder", "Flow Builder", "Apex Triggers"],
                "correct_options": [2], "type": "single", "key_section": "s4",
                "wrong_feedback": "Review 'Automation' — Flow Builder is most powerful declarative tool.",
            },
            {
                "question_id": "q8",
                "question": "Which report types exist in Salesforce? (Select ALL)",
                "options": ["Tabular", "Summary", "Matrix", "Pivot"],
                "correct_options": [0, 1, 2], "type": "multi", "key_section": "s4",
                "wrong_feedback": "Review 'Reports' — Tabular, Summary, Matrix, Joined.",
            },
            {
                "question_id": "q9",
                "question": "What do Permission Sets do?",
                "options": ["Replace profiles", "Add extra permissions on top of profiles",
                            "Remove permissions", "Manage login hours"],
                "correct_options": [1], "type": "single", "key_section": "s3",
                "wrong_feedback": "Review 'Security' — Permission Sets add extra permissions.",
            },
            {
                "question_id": "q10",
                "question": "What is AppExchange?",
                "options": ["A code editor", "Salesforce marketplace for apps",
                            "A database tool", "An API gateway"],
                "correct_options": [1], "type": "single", "key_section": "s1",
                "wrong_feedback": "Review 'Platform Overview' for AppExchange.",
            },
            {
                "question_id": "q11",
                "question": "What controls which fields a user sees on a record page?",
                "options": ["Profiles", "Page Layouts", "Permission Sets", "Sharing Rules"],
                "correct_options": [1], "type": "single", "key_section": "s2",
                "wrong_feedback": "Review 'Objects' — Page Layouts control field visibility.",
            },
            {
                "question_id": "q12",
                "question": "Which OWD option is most restrictive?",
                "options": ["Public Read/Write", "Public Read Only", "Private", "Controlled by Parent"],
                "correct_options": [2], "type": "single", "key_section": "s3",
                "wrong_feedback": "Review 'Security' — Private is most restrictive.",
            },
            {
                "question_id": "q13",
                "question": "What is being retired in favor of Flow?",
                "options": ["Approval Processes", "Process Builder", "Validation Rules", "Reports"],
                "correct_options": [1], "type": "single", "key_section": "s4",
                "wrong_feedback": "Review 'Automation' — Process Builder is being retired.",
            },
            {
                "question_id": "q14",
                "question": "What field type calculates values from other fields?",
                "options": ["Picklist", "Lookup", "Formula", "Checkbox"],
                "correct_options": [2], "type": "single", "key_section": "s2",
                "wrong_feedback": "Review 'Objects' — Formula fields calculate values.",
            },
            {
                "question_id": "q15",
                "question": "Which Salesforce clouds exist? (Select ALL)",
                "options": ["Sales Cloud", "Service Cloud", "Marketing Cloud", "Weather Cloud"],
                "correct_options": [0, 1, 2], "type": "multi", "key_section": "s1",
                "wrong_feedback": "Review 'Platform Overview' for Salesforce clouds.",
            },
            {
                "question_id": "q16",
                "question": "What does Role Hierarchy do?",
                "options": ["Restricts access down", "Grants access up the chain",
                            "Deletes records", "Creates fields"],
                "correct_options": [1], "type": "single", "key_section": "s3",
                "wrong_feedback": "Review 'Security' — Role Hierarchy grants upward access.",
            },
            {
                "question_id": "q17",
                "question": "What is a Record-Triggered Flow?",
                "options": ["Runs on schedule", "Triggered before/after record save",
                            "Requires user screen", "Sends emails only"],
                "correct_options": [1], "type": "single", "key_section": "s4",
                "wrong_feedback": "Review 'Automation' for Record-Triggered Flows.",
            },
            {
                "question_id": "q18",
                "question": "What field type links two objects?",
                "options": ["Formula", "Text", "Lookup", "Number"],
                "correct_options": [2], "type": "single", "key_section": "s2",
                "wrong_feedback": "Review 'Objects' — Lookup/Master-Detail link objects.",
            },
            {
                "question_id": "q19",
                "question": "What is Salesforce's free learning platform?",
                "options": ["Coursera", "Trailhead", "Udemy", "AppExchange"],
                "correct_options": [1], "type": "single", "key_section": "s1",
                "wrong_feedback": "Review 'Platform Overview' — Trailhead is free learning.",
            },
            {
                "question_id": "q20",
                "question": "What do Dashboards display?",
                "options": ["Raw SOQL data", "Report data as visual components",
                            "Apex debug logs", "User login history"],
                "correct_options": [1], "type": "single", "key_section": "s4",
                "wrong_feedback": "Review 'Reports' — Dashboards visualize report data.",
            },
        ],
        "quiz_count": 3,
        "energy_budget": 15,
        "step_budget": 20,
        "max_attempts": 3,
    },

    # ── HARD #2: Salesforce Apex Development ──────────────────────────────
    {
        "id": "salesforce_apex",
        "task_type": "course_module",
        "difficulty": "hard",
        "title": "Salesforce Apex Development",
        "instruction": (
            "Advanced Salesforce development module covering Apex programming. "
            "Energy is limited — study strategically. Multiple questions "
            "require selecting all correct answers."
        ),
        "study_materials": [
            {
                "section_id": "s1",
                "title": "Apex Fundamentals",
                "content": (
                    "Apex is a strongly-typed, object-oriented language (Java-like). "
                    "Runs on Salesforce servers, not client-side. "
                    "Supports classes, interfaces, enums, triggers, and batch jobs. "
                    "Primitive types: Integer, Long, Double, Decimal, String, Boolean, "
                    "Date, Datetime, Time, Id, Blob. "
                    "Collections: List (ordered, duplicates), Set (unordered, unique), "
                    "Map (key-value pairs). "
                    "All Apex code runs in system mode by default (ignores FLS/CRUD). "
                    "Use 'with sharing' to enforce record-level security."
                ),
            },
            {
                "section_id": "s2",
                "title": "SOQL and SOSL",
                "content": (
                    "SOQL (Salesforce Object Query Language) queries single objects: "
                    "SELECT Id, Name FROM Account WHERE Industry = 'Tech'. "
                    "Supports parent-to-child subqueries: SELECT Id, (SELECT Id FROM Contacts) FROM Account. "
                    "Child-to-parent: SELECT Account.Name FROM Contact. "
                    "Aggregate functions: COUNT(), SUM(), AVG(), MIN(), MAX(). "
                    "SOQL returns max 50,000 records per transaction. "
                    "SOSL (Salesforce Object Search Language) searches across multiple objects: "
                    "FIND 'Acme' IN ALL FIELDS RETURNING Account, Contact. "
                    "SOSL returns max 2,000 records. Use SOSL for text search across objects."
                ),
            },
            {
                "section_id": "s3",
                "title": "Triggers and Trigger Framework",
                "content": (
                    "Triggers execute before/after DML operations: insert, update, delete, undelete. "
                    "Context variables: Trigger.new (new records), Trigger.old (old values), "
                    "Trigger.newMap, Trigger.oldMap, Trigger.isInsert, Trigger.isBefore. "
                    "Best practice: One trigger per object, logic in handler classes. "
                    "NEVER put SOQL or DML inside loops (bulkification). "
                    "Trigger execution order: validation rules, before triggers, system validation, "
                    "after triggers, assignment rules, workflow rules, auto-response rules, "
                    "then commit. Recursive triggers need static variables to prevent infinite loops."
                ),
            },
            {
                "section_id": "s4",
                "title": "Governor Limits",
                "content": (
                    "Salesforce enforces governor limits to protect multi-tenant resources: "
                    "100 SOQL queries per synchronous transaction. "
                    "150 DML statements per transaction. "
                    "50,000 records retrieved by SOQL per transaction. "
                    "10,000 records processed by DML per transaction. "
                    "6 MB heap size for synchronous Apex. 12 MB for async. "
                    "100 callouts per transaction. 120-second timeout for sync. "
                    "10-minute timeout for async (batch). "
                    "Batch Apex processes large data sets: Database.executeBatch(). "
                    "Future methods (@future) run asynchronously for callouts. "
                    "Queueable Apex allows chaining async jobs."
                ),
            },
            {
                "section_id": "s5",
                "title": "Testing in Apex",
                "content": (
                    "75% code coverage required for production deployment. "
                    "Test classes use @isTest annotation. "
                    "Test methods use @isTest or testMethod keyword. "
                    "Use Test.startTest() and Test.stopTest() to reset governor limits. "
                    "Create test data in tests — don't rely on org data by default. "
                    "@TestSetup creates shared test data for all methods in the class. "
                    "System.assert(), System.assertEquals(), System.assertNotEquals(). "
                    "Test both positive and negative scenarios. "
                    "Tests run in their own transaction and are rolled back."
                ),
            },
        ],
        "quiz_pool": [
            {
                "question_id": "q1",
                "question": "What type of language is Apex?",
                "options": ["Weakly-typed scripting", "Strongly-typed object-oriented",
                            "Functional", "Assembly-like"],
                "correct_options": [1], "type": "single", "key_section": "s1",
                "wrong_feedback": "Review 'Apex Fundamentals' — strongly-typed OOP.",
            },
            {
                "question_id": "q2",
                "question": "What is the SOQL record retrieval limit per transaction?",
                "options": ["10,000", "50,000", "100,000", "Unlimited"],
                "correct_options": [1], "type": "single", "key_section": "s4",
                "wrong_feedback": "Review 'Governor Limits' — 50,000 SOQL records.",
            },
            {
                "question_id": "q3",
                "question": "How many SOQL queries are allowed per sync transaction?",
                "options": ["50", "100", "200", "500"],
                "correct_options": [1], "type": "single", "key_section": "s4",
                "wrong_feedback": "Review 'Governor Limits' — 100 SOQL queries sync.",
            },
            {
                "question_id": "q4",
                "question": "What keyword enforces record-level security in Apex?",
                "options": ["with sharing", "without sharing", "private", "secure"],
                "correct_options": [0], "type": "single", "key_section": "s1",
                "wrong_feedback": "Review 'Fundamentals' — 'with sharing' enforces security.",
            },
            {
                "question_id": "q5",
                "question": "Which are Apex collection types? (Select ALL)",
                "options": ["List", "Set", "Map", "Array"],
                "correct_options": [0, 1, 2], "type": "multi", "key_section": "s1",
                "wrong_feedback": "Review 'Fundamentals' — List, Set, Map are Apex collections.",
            },
            {
                "question_id": "q6",
                "question": "What should you NEVER do inside a loop?",
                "options": ["Add to a list", "Put SOQL or DML", "Log messages", "Increment counters"],
                "correct_options": [1], "type": "single", "key_section": "s3",
                "wrong_feedback": "Review 'Triggers' — no SOQL/DML inside loops.",
            },
            {
                "question_id": "q7",
                "question": "What minimum code coverage is needed for deployment?",
                "options": ["50%", "65%", "75%", "90%"],
                "correct_options": [2], "type": "single", "key_section": "s5",
                "wrong_feedback": "Review 'Testing' — 75% coverage required.",
            },
            {
                "question_id": "q8",
                "question": "What does Trigger.new contain?",
                "options": ["Old field values", "New records being processed",
                            "Deleted records", "Query results"],
                "correct_options": [1], "type": "single", "key_section": "s3",
                "wrong_feedback": "Review 'Triggers' — Trigger.new has new records.",
            },
            {
                "question_id": "q9",
                "question": "What is the max SOSL return?",
                "options": ["500", "2,000", "50,000", "Unlimited"],
                "correct_options": [1], "type": "single", "key_section": "s2",
                "wrong_feedback": "Review 'SOQL and SOSL' — SOSL returns max 2,000.",
            },
            {
                "question_id": "q10",
                "question": "What does @TestSetup do?",
                "options": ["Runs the test", "Creates shared test data for all methods",
                            "Deploys to production", "Resets limits"],
                "correct_options": [1], "type": "single", "key_section": "s5",
                "wrong_feedback": "Review 'Testing' for @TestSetup annotation.",
            },
            {
                "question_id": "q11",
                "question": "Which are valid trigger events? (Select ALL)",
                "options": ["before insert", "after update", "before delete", "before query"],
                "correct_options": [0, 1, 2], "type": "multi", "key_section": "s3",
                "wrong_feedback": "Review 'Triggers' — there is no 'before query' event.",
            },
            {
                "question_id": "q12",
                "question": "What aggregate functions does SOQL support? (Select ALL)",
                "options": ["COUNT()", "SUM()", "MEDIAN()", "AVG()"],
                "correct_options": [0, 1, 3], "type": "multi", "key_section": "s2",
                "wrong_feedback": "Review 'SOQL' — MEDIAN is not supported.",
            },
            {
                "question_id": "q13",
                "question": "How many DML statements per transaction?",
                "options": ["50", "100", "150", "200"],
                "correct_options": [2], "type": "single", "key_section": "s4",
                "wrong_feedback": "Review 'Governor Limits' — 150 DML statements.",
            },
            {
                "question_id": "q14",
                "question": "What is the sync Apex heap size limit?",
                "options": ["3 MB", "6 MB", "12 MB", "24 MB"],
                "correct_options": [1], "type": "single", "key_section": "s4",
                "wrong_feedback": "Review 'Governor Limits' — 6 MB sync, 12 MB async.",
            },
            {
                "question_id": "q15",
                "question": "How do you do parent-to-child SOQL?",
                "options": ["JOIN syntax", "Subquery in SELECT", "UNION", "MERGE"],
                "correct_options": [1], "type": "single", "key_section": "s2",
                "wrong_feedback": "Review 'SOQL' — use subqueries for parent-to-child.",
            },
            {
                "question_id": "q16",
                "question": "What processes large data sets asynchronously?",
                "options": ["Triggers", "Batch Apex", "Validation Rules", "Workflows"],
                "correct_options": [1], "type": "single", "key_section": "s4",
                "wrong_feedback": "Review 'Governor Limits' — Batch Apex for large data.",
            },
            {
                "question_id": "q17",
                "question": "What prevents recursive triggers?",
                "options": ["Try-catch blocks", "Static boolean variables",
                            "Validation rules", "Governor limits"],
                "correct_options": [1], "type": "single", "key_section": "s3",
                "wrong_feedback": "Review 'Triggers' — static variables prevent recursion.",
            },
            {
                "question_id": "q18",
                "question": "How does Test.stopTest() help?",
                "options": ["Stops the test", "Executes async code and resets governor limits",
                            "Deletes test data", "Deploys code"],
                "correct_options": [1], "type": "single", "key_section": "s5",
                "wrong_feedback": "Review 'Testing' — stopTest resets limits & runs async.",
            },
            {
                "question_id": "q19",
                "question": "What does System.assertEquals() do?",
                "options": ["Assigns a value", "Verifies two values are equal",
                            "Creates a record", "Runs a query"],
                "correct_options": [1], "type": "single", "key_section": "s5",
                "wrong_feedback": "Review 'Testing' — assertEquals verifies equality.",
            },
            {
                "question_id": "q20",
                "question": "Best practice: how many triggers per object?",
                "options": ["Unlimited", "One", "Two", "None"],
                "correct_options": [1], "type": "single", "key_section": "s3",
                "wrong_feedback": "Review 'Triggers' — one trigger per object best practice.",
            },
        ],
        "quiz_count": 4,
        "energy_budget": 18,
        "step_budget": 25,
        "max_attempts": 3,
    },

    # ── HARD #3: AWS Cloud Fundamentals ───────────────────────────────────
    {
        "id": "aws_cloud",
        "task_type": "course_module",
        "difficulty": "hard",
        "title": "AWS Cloud Fundamentals",
        "instruction": (
            "Advanced module on Amazon Web Services. Energy is limited — "
            "study strategically. Multiple questions require all correct answers."
        ),
        "study_materials": [
            {
                "section_id": "s1",
                "title": "AWS Core Services",
                "content": (
                    "EC2 (Elastic Compute Cloud): virtual servers in the cloud. "
                    "Instance types: General Purpose (t3, m5), Compute Optimized (c5), "
                    "Memory Optimized (r5), Storage Optimized (i3). "
                    "S3 (Simple Storage Service): object storage with 99.999999999% durability. "
                    "S3 storage classes: Standard, Intelligent-Tiering, Glacier, Glacier Deep Archive. "
                    "RDS (Relational Database Service): managed databases — MySQL, PostgreSQL, "
                    "Aurora, SQL Server, Oracle, MariaDB. "
                    "DynamoDB: fully managed NoSQL key-value database. "
                    "Lambda: serverless compute — run code without provisioning servers. "
                    "Pay only for compute time consumed. Max execution: 15 minutes."
                ),
            },
            {
                "section_id": "s2",
                "title": "IAM and Security",
                "content": (
                    "IAM (Identity and Access Management): controls access to AWS resources. "
                    "Users: individual people or services. Groups: collections of users. "
                    "Roles: temporary credentials for services or cross-account access. "
                    "Policies: JSON documents defining permissions (Effect, Action, Resource). "
                    "Root account should have MFA and should NOT be used for daily tasks. "
                    "Principle of Least Privilege: grant only needed permissions. "
                    "KMS (Key Management Service): manages encryption keys. "
                    "CloudTrail: logs all API calls for auditing. "
                    "Security Groups: stateful firewall for EC2 instances (allow rules only). "
                    "NACLs: stateless firewall for subnets (allow AND deny rules)."
                ),
            },
            {
                "section_id": "s3",
                "title": "Networking",
                "content": (
                    "VPC (Virtual Private Cloud): isolated network in AWS. "
                    "Subnets: public (internet accessible) and private (internal only). "
                    "Internet Gateway: connects VPC to the internet. "
                    "NAT Gateway: lets private subnet instances access internet outbound. "
                    "Route Tables: control traffic routing within the VPC. "
                    "Elastic IP: static public IPv4 address. "
                    "CloudFront: global CDN for content delivery. "
                    "Route 53: managed DNS service. Supports A, AAAA, CNAME, MX records. "
                    "ELB (Elastic Load Balancer): distributes traffic. Types: "
                    "Application (HTTP/HTTPS L7), Network (TCP L4), Gateway (L3)."
                ),
            },
            {
                "section_id": "s4",
                "title": "Scaling and Monitoring",
                "content": (
                    "Auto Scaling: automatically adjusts EC2 instance count. "
                    "Scaling policies: Target Tracking, Step Scaling, Simple Scaling. "
                    "CloudWatch: monitoring service for metrics, logs, and alarms. "
                    "CloudWatch can trigger Auto Scaling based on CPU, memory, etc. "
                    "SNS (Simple Notification Service): pub/sub messaging. "
                    "SQS (Simple Queue Service): message queuing for decoupling. "
                    "SQS types: Standard (at-least-once) and FIFO (exactly-once). "
                    "Elastic Beanstalk: PaaS — deploy apps without managing infra. "
                    "CloudFormation: Infrastructure as Code (IaC) using JSON/YAML templates. "
                    "Terraform is a third-party alternative to CloudFormation."
                ),
            },
        ],
        "quiz_pool": [
            {
                "question_id": "q1",
                "question": "What is EC2?",
                "options": ["Object storage", "Virtual servers in the cloud",
                            "DNS service", "Message queue"],
                "correct_options": [1], "type": "single", "key_section": "s1",
                "wrong_feedback": "Review 'Core Services' — EC2 is virtual servers.",
            },
            {
                "question_id": "q2",
                "question": "What S3 durability level?",
                "options": ["99.9%", "99.99%", "99.999999999%", "100%"],
                "correct_options": [2], "type": "single", "key_section": "s1",
                "wrong_feedback": "Review 'Core Services' — S3 is 11 nines durability.",
            },
            {
                "question_id": "q3",
                "question": "What does IAM stand for?",
                "options": ["Internet Access Management", "Identity and Access Management",
                            "Integrated App Manager", "Internal Auth Module"],
                "correct_options": [1], "type": "single", "key_section": "s2",
                "wrong_feedback": "Review 'IAM' — Identity and Access Management.",
            },
            {
                "question_id": "q4",
                "question": "Which are valid S3 storage classes? (Select ALL)",
                "options": ["Standard", "Glacier", "Intelligent-Tiering", "Enterprise"],
                "correct_options": [0, 1, 2], "type": "multi", "key_section": "s1",
                "wrong_feedback": "Review 'Core Services' for S3 storage classes.",
            },
            {
                "question_id": "q5",
                "question": "What is the max Lambda execution time?",
                "options": ["5 minutes", "10 minutes", "15 minutes", "60 minutes"],
                "correct_options": [2], "type": "single", "key_section": "s1",
                "wrong_feedback": "Review 'Core Services' — Lambda max is 15 minutes.",
            },
            {
                "question_id": "q6",
                "question": "Security Groups are stateful or stateless?",
                "options": ["Stateful", "Stateless", "Both", "Neither"],
                "correct_options": [0], "type": "single", "key_section": "s2",
                "wrong_feedback": "Review 'Security' — Security Groups are stateful.",
            },
            {
                "question_id": "q7",
                "question": "What connects a VPC to the internet?",
                "options": ["NAT Gateway", "Internet Gateway", "Route Table", "Security Group"],
                "correct_options": [1], "type": "single", "key_section": "s3",
                "wrong_feedback": "Review 'Networking' — Internet Gateway connects VPC.",
            },
            {
                "question_id": "q8",
                "question": "Which SQS type guarantees exactly-once delivery?",
                "options": ["Standard", "FIFO", "Priority", "Delayed"],
                "correct_options": [1], "type": "single", "key_section": "s4",
                "wrong_feedback": "Review 'Scaling' — FIFO queues are exactly-once.",
            },
            {
                "question_id": "q9",
                "question": "What is CloudFormation?",
                "options": ["Monitoring service", "CDN", "Infrastructure as Code",
                            "Database service"],
                "correct_options": [2], "type": "single", "key_section": "s4",
                "wrong_feedback": "Review 'Scaling' — CloudFormation is IaC.",
            },
            {
                "question_id": "q10",
                "question": "What is the root account best practice?",
                "options": ["Use daily", "Enable MFA, don't use for daily tasks",
                            "Share credentials", "Delete after setup"],
                "correct_options": [1], "type": "single", "key_section": "s2",
                "wrong_feedback": "Review 'Security' — root account needs MFA, minimal use.",
            },
            {
                "question_id": "q11",
                "question": "Which ELB type operates at Layer 7 (HTTP)?",
                "options": ["Network", "Application", "Gateway", "Classic"],
                "correct_options": [1], "type": "single", "key_section": "s3",
                "wrong_feedback": "Review 'Networking' — ALB is Layer 7.",
            },
            {
                "question_id": "q12",
                "question": "What AWS service is managed DNS?",
                "options": ["CloudFront", "Route 53", "VPC", "ELB"],
                "correct_options": [1], "type": "single", "key_section": "s3",
                "wrong_feedback": "Review 'Networking' — Route 53 is DNS.",
            },
            {
                "question_id": "q13",
                "question": "What does DynamoDB provide?",
                "options": ["Relational database", "NoSQL key-value database",
                            "Object storage", "Message queuing"],
                "correct_options": [1], "type": "single", "key_section": "s1",
                "wrong_feedback": "Review 'Core Services' — DynamoDB is NoSQL.",
            },
            {
                "question_id": "q14",
                "question": "Which are valid IAM entities? (Select ALL)",
                "options": ["Users", "Groups", "Roles", "Subnets"],
                "correct_options": [0, 1, 2], "type": "multi", "key_section": "s2",
                "wrong_feedback": "Review 'IAM' — Users, Groups, Roles. Subnets are networking.",
            },
            {
                "question_id": "q15",
                "question": "What lets private subnets access the internet outbound?",
                "options": ["Internet Gateway", "NAT Gateway", "Security Group", "NACL"],
                "correct_options": [1], "type": "single", "key_section": "s3",
                "wrong_feedback": "Review 'Networking' — NAT Gateway for private outbound.",
            },
            {
                "question_id": "q16",
                "question": "What is CloudWatch?",
                "options": ["Storage service", "Monitoring and metrics service",
                            "Database", "Deployment tool"],
                "correct_options": [1], "type": "single", "key_section": "s4",
                "wrong_feedback": "Review 'Scaling' — CloudWatch monitors metrics.",
            },
            {
                "question_id": "q17",
                "question": "NACLs support which rule types? (Select ALL)",
                "options": ["Allow rules", "Deny rules", "Forward rules", "Redirect rules"],
                "correct_options": [0, 1], "type": "multi", "key_section": "s2",
                "wrong_feedback": "Review 'Security' — NACLs have allow AND deny rules.",
            },
            {
                "question_id": "q18",
                "question": "What is Elastic Beanstalk?",
                "options": ["IaC tool", "PaaS for deploying apps",
                            "NoSQL database", "CDN"],
                "correct_options": [1], "type": "single", "key_section": "s4",
                "wrong_feedback": "Review 'Scaling' — Beanstalk is PaaS.",
            },
            {
                "question_id": "q19",
                "question": "What service logs all AWS API calls?",
                "options": ["CloudWatch", "CloudTrail", "CloudFront", "CloudFormation"],
                "correct_options": [1], "type": "single", "key_section": "s2",
                "wrong_feedback": "Review 'Security' — CloudTrail logs API calls.",
            },
            {
                "question_id": "q20",
                "question": "Which databases does RDS support? (Select ALL)",
                "options": ["MySQL", "PostgreSQL", "MongoDB", "Aurora"],
                "correct_options": [0, 1, 3], "type": "multi", "key_section": "s1",
                "wrong_feedback": "Review 'Core Services' — RDS doesn't support MongoDB.",
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
