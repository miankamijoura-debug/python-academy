from flask import Flask, render_template_string, abort, request, session
import webbrowser
from threading import Timer
import secrets
import random

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# ==================================================
# 1. 50 PYTHON CHAPTERS
# ==================================================

CHAPTER_NAMES = [
    "Introduction to Python", "Uses of Python", "Installing Python",
    "Python IDE", "Running Python Programs", "Python Syntax",
    "Python Indentation", "Python Comments", "Variables",
    "Variable Naming Rules", "Python Data Types", "Type Checking",
    "Type Conversion", "User Input", "Print Function",
    "Arithmetic Operators", "Assignment Operators",
    "Comparison Operators", "Logical Operators",
    "Membership Operators", "Identity Operators",
    "Introduction to Strings", "String Indexing", "String Slicing",
    "String Methods", "F-Strings", "Boolean Values", "Lists",
    "List Indexing and Slicing", "List Methods", "Tuples", "Sets",
    "Dictionaries", "Dictionary Methods", "If Statements",
    "If-Else Statements", "Elif Statements", "Nested Conditions",
    "For Loops", "While Loops", "Range Function",
    "Break, Continue and Pass", "Nested Loops", "Functions",
    "Function Parameters and Arguments", "Return Statement",
    "Variable Scope", "Recursion", "Lambda Functions",
    "Exception Handling"
]

# ==================================================
# 2. 15 TOPICS FOR EVERY CHAPTER
# ==================================================

TOPIC_STEPS = [
    "Introduction", "Importance and Uses", "Basic Concepts",
    "Basic Syntax", "First Example", "Understanding the Concept",
    "Working with Values", "Using Variables", "Taking User Input",
    "Displaying Output", "Practical Example", "Common Mistakes",
    "Important Rules", "Real-Life Application", "Practice Exercise"
]

EXAMPLES = [
    ('print("Hello, Python!")', "Hello, Python!"),
    ('name = "Ali"\nprint(name)', "Ali"),
    ('age = 17\nprint(age)', "17"),
    ('number = 10\nprint(number + 5)', "15"),
    ('a = 10\nb = 20\nprint(a + b)', "30"),
    ('name = "Python"\nprint("Welcome to", name)', "Welcome to Python"),
    ('marks = 85\nif marks >= 50:\n    print("Pass")', "Pass"),
    ('for i in range(1, 4):\n    print(i)', "1\n2\n3"),
    ('count = 1\nwhile count <= 3:\n    print(count)\n    count += 1', "1\n2\n3"),
    ('numbers = [10, 20, 30]\nprint(numbers)', "[10, 20, 30]"),
    ('student = {"name": "Ali", "age": 17}\nprint(student["name"])', "Ali"),
    ('colors = ("red", "blue", "green")\nprint(colors[0])', "red"),
    ('def greet():\n    print("Good morning!")\n\ngreet()', "Good morning!"),
    ('try:\n    number = int("abc")\nexcept ValueError:\n    print("Invalid number")', "Invalid number"),
    ('square = lambda x: x * x\nprint(square(5))', "25")
]


def create_topics(chapter_name):
    topics = []

    for i, topic_name in enumerate(TOPIC_STEPS):
        code, output = EXAMPLES[i]

        topics.append({
            "id": i + 1,
            "title": topic_name,
            "explanation": (
                f"This lesson introduces {topic_name.lower()} "
                f"while studying {chapter_name}. "
                "Read the explanation, study the code, "
                "and run the example in Python."
            ),
            "code": code,
            "output": output,
            "exercise": (
                f"Write your own Python program related to "
                f"{chapter_name} and {topic_name.lower()}."
            )
        })

    return topics


CHAPTERS = [
    {
        "id": i + 1,
        "name": name,
        "topics": create_topics(name)
    }
    for i, name in enumerate(CHAPTER_NAMES)
]

# ==================================================
# 3. CHAPTER-SPECIFIC TEST DATA
# Each chapter has six questions based on these facts.
# ==================================================

CHAPTER_QUIZ_FACTS = [
    [
        "Python is a high-level, general-purpose programming language known for readable syntax.",
        "A Python statement can be as simple as: print('Hello, world!')",
        "print('Hello, world!')", "Hello, world!",
        "Python code must always be written in machine code.",
        "Writing scripts, applications, automation tools, and data programs."
    ],
    [
        "Python is used for web development, automation, data analysis, AI, and scripting.",
        "A common automation pattern is: for item in items: process(item)",
        "tasks = ['report', 'backup']\nfor task in tasks:\n    print('Doing', task)",
        "Doing report\nDoing backup",
        "Python can only be used to make websites.",
        "Automating repetitive file or data tasks."
    ],
    [
        "The official Python installer installs the Python interpreter on a computer.",
        "After installation, check the interpreter with: python --version",
        "version = 'Python 3'\nprint(version)", "Python 3",
        "Installing a code editor alone always installs Python itself.",
        "Preparing a computer to run Python programs."
    ],
    [
        "An IDE provides tools such as a code editor, run controls, and debugging features.",
        "In an IDE, create a Python file ending in .py and run it with the Run command.",
        "message = 'Running in an IDE'\nprint(message)", "Running in an IDE",
        "An IDE and the Python programming language are the same thing.",
        "Writing, running, and debugging Python projects in one workspace."
    ],
    [
        "A Python program is commonly saved in a .py file and executed by the Python interpreter.",
        "Run a saved file from a terminal with: python filename.py",
        "print('Program started')", "Program started",
        "A Python file must be renamed to .txt before it can run.",
        "Running a saved script from a terminal or editor."
    ],
    [
        "Python syntax is the set of rules that defines how valid Python statements are written.",
        "A function call uses a name followed by parentheses, such as: print('Hi')",
        "print('Valid syntax')", "Valid syntax",
        "Python ignores every syntax rule as long as the words are understandable.",
        "Writing statements the Python interpreter can parse."
    ],
    [
        "Indentation defines code blocks in Python, commonly after if, for, while, and def.",
        "A block is indented after a colon: if condition:\n    statement",
        "if 5 > 2:\n    print('Yes')", "Yes",
        "Indentation is only decorative and never changes Python code structure.",
        "Grouping statements inside a condition, loop, or function."
    ],
    [
        "A comment is text for readers that Python does not execute as code.",
        "A single-line comment starts with the hash symbol: # comment",
        "# This is a comment\nprint('Hello')", "Hello",
        "Python executes the text after # as a normal statement.",
        "Adding explanations and reminders to source code."
    ],
    [
        "A variable is a named reference used to store or refer to a value.",
        "Assign a value with one equals sign: score = 90",
        "score = 90\nprint(score)", "90",
        "A variable must be declared with a special type keyword before assignment.",
        "Keeping a value such as a score or username for later use."
    ],
    [
        "A valid variable name starts with a letter or underscore and may contain digits after that.",
        "Valid examples include: user_name = 'Ali' and score2 = 10",
        "user_name = 'Ali'\nscore2 = 10\nprint(user_name, score2)", "Ali 10",
        "A variable name can begin with a digit, such as 2score.",
        "Choosing clear names that make a program easier to understand."
    ],
    [
        "Python has built-in types such as int, float, str, bool, list, tuple, set, and dict.",
        "Examples: age = 15; price = 2.5; name = 'Ali'; active = True",
        "age = 15\nprice = 2.5\nprint(type(age).__name__)\nprint(type(price).__name__)",
        "int\nfloat",
        "Every value in Python has to be stored as a string.",
        "Choosing suitable kinds of values for data in a program."
    ],
    [
        "The type() function reports the type of an object.",
        "Use: type(value) or type(value).__name__",
        "value = 12\nprint(type(value).__name__)", "int",
        "type() converts a value into a different type.",
        "Checking what kind of value a variable currently refers to."
    ],
    [
        "Type conversion changes a value from one data type to another when conversion is valid.",
        "Common conversions include int('12'), float('3.5'), and str(25).",
        "age_text = '16'\nage = int(age_text)\nprint(age + 1)", "17",
        "int('hello') is a valid way to convert any text to an integer.",
        "Converting text entered by a user into a number for calculations."
    ],
    [
        "input() reads text entered by the user and returns it as a string.",
        "Use: name = input('Enter your name: ')",
        "name = 'Sara'\nprint('Hello', name)", "Hello Sara",
        "input() automatically returns an integer whenever the user types digits.",
        "Collecting a name or other response from someone using a program."
    ],
    [
        "print() displays values and text in the program output.",
        "Use: print(value); multiple values can be separated with commas.",
        "print('Age:', 16)", "Age: 16",
        "print() is used to receive keyboard input.",
        "Showing results, messages, and instructions to a user."
    ],
    [
        "Arithmetic operators perform calculations such as addition, subtraction, multiplication, and division.",
        "Common operators: +, -, *, /, //, %, and **",
        "print(10 + 3)\nprint(10 % 3)", "13\n1",
        "The % operator performs ordinary division and returns a decimal quotient.",
        "Calculating totals, remainders, averages, and powers."
    ],
    [
        "Assignment operators assign or update a variable's value.",
        "Examples: x = 5; x += 2; x *= 3",
        "score = 5\nscore += 2\nprint(score)", "7",
        "The operator += means compare two values for equality.",
        "Updating a running total or counter."
    ],
    [
        "Comparison operators compare values and produce a Boolean result.",
        "Common operators: ==, !=, >, <, >=, and <=",
        "print(8 > 5)\nprint(8 == 5)", "True\nFalse",
        "A comparison such as 8 > 5 returns the integer 3.",
        "Checking whether a score reaches a pass mark."
    ],
    [
        "Logical operators combine or reverse Boolean conditions.",
        "Python uses: and, or, and not",
        "age = 18\nhas_id = True\nprint(age >= 18 and has_id)", "True",
        "The word and means that either condition may be true.",
        "Checking multiple requirements in a single decision."
    ],
    [
        "Membership operators test whether a value occurs in a sequence or collection.",
        "Use: value in collection and value not in collection",
        "colors = ['red', 'blue']\nprint('red' in colors)", "True",
        "The in operator adds a new item to a list.",
        "Checking whether a username, word, or item is present."
    ],
    [
        "Identity operators test whether two references point to the same object.",
        "Python identity operators are: is and is not",
        "a = None\nprint(a is None)", "True",
        "is always means that two values have equal contents.",
        "Checking identity with singleton values such as None."
    ],
    [
        "A string is an immutable sequence of characters.",
        "Create strings with quotes: name = 'Python' or language = \"Python\"",
        "language = 'Python'\nprint(language)", "Python",
        "A string can be changed in place one character at a time.",
        "Storing names, messages, and other text."
    ],
    [
        "String indexing accesses one character by its position, starting at zero.",
        "Use: text[index]; negative indexes count from the end.",
        "word = 'Python'\nprint(word[0])\nprint(word[-1])", "P\nn",
        "The first character of a string has index 1.",
        "Reading a particular character from a word or code."
    ],
    [
        "String slicing extracts part of a string using start and stop positions.",
        "Use: text[start:stop]; the stop position is excluded.",
        "word = 'Python'\nprint(word[1:4])", "yth",
        "The stop index in a slice is always included.",
        "Extracting a substring such as a first name or file extension."
    ],
    [
        "String methods are built-in operations used to work with text.",
        "Examples: text.upper(), text.lower(), and text.strip()",
        "word = ' python '\nprint(word.strip().upper())", "PYTHON",
        "String methods such as upper() modify the original string in place.",
        "Cleaning or changing the presentation of text."
    ],
    [
        "An f-string inserts expressions or variable values directly into a string.",
        "Start the string with f and place expressions inside braces: f'Hello {name}'",
        "name = 'Ali'\nscore = 90\nprint(f'{name}: {score}')", "Ali: 90",
        "An f-string uses square brackets instead of curly braces for expressions.",
        "Creating readable messages that include changing values."
    ],
    [
        "A Boolean value is either True or False.",
        "Boolean literals are written with capital first letters: True and False",
        "is_ready = True\nprint(is_ready)", "True",
        "Python Boolean literals are written as true and false in lowercase.",
        "Representing yes/no conditions and program states."
    ],
    [
        "A list is an ordered, mutable collection that can contain multiple items.",
        "Create a list with square brackets: numbers = [10, 20, 30]",
        "numbers = [10, 20, 30]\nprint(numbers[1])", "20",
        "A list cannot be changed after it is created.",
        "Keeping an ordered collection such as marks or shopping items."
    ],
    [
        "List indexing gets one item and slicing gets a range of items.",
        "Use numbers[0] for the first item and numbers[1:3] for a slice.",
        "numbers = [10, 20, 30, 40]\nprint(numbers[1:3])", "[20, 30]",
        "A slice numbers[1:3] includes the item at index 3.",
        "Selecting a particular item or a section of a list."
    ],
    [
        "List methods perform operations such as adding, removing, or sorting list items.",
        "Common methods: append(), extend(), insert(), remove(), pop(), and sort()",
        "numbers = [1, 2]\nnumbers.append(3)\nprint(numbers)", "[1, 2, 3]",
        "append() adds an item to the beginning of a list.",
        "Adding or removing entries in a changing collection."
    ],
    [
        "A tuple is an ordered collection that cannot be modified after creation.",
        "Create a tuple with commas: point = (3, 4); a one-item tuple needs a trailing comma.",
        "point = (3, 4)\nprint(point[0])", "3",
        "A tuple supports item reassignment just like a list.",
        "Keeping a fixed group of related values, such as coordinates."
    ],
    [
        "A set is an unordered collection of unique elements.",
        "Create a set with braces: values = {1, 2, 3}; use set() for an empty set.",
        "values = {1, 2, 2, 3}\nprint(len(values))", "3",
        "A set keeps every duplicate item as a separate element.",
        "Removing duplicates or testing membership in a collection."
    ],
    [
        "A dictionary stores key-value pairs and uses keys to look up values.",
        "Create one with braces: student = {'name': 'Ali'}",
        "student = {'name': 'Ali', 'age': 16}\nprint(student['name'])", "Ali",
        "Dictionary values are accessed by numeric position like list indexes.",
        "Storing related information such as a student's name and age."
    ],
    [
        "Dictionary methods access or update dictionary data.",
        "Common methods: get(), keys(), values(), items(), and update()",
        "student = {'name': 'Ali'}\nprint(student.get('name'))", "Ali",
        "get() removes a key from a dictionary.",
        "Safely reading values or iterating through dictionary entries."
    ],
    [
        "An if statement runs an indented block only when its condition is true.",
        "Pattern: if condition:\n    statements",
        "temperature = 30\nif temperature > 25:\n    print('Warm')", "Warm",
        "An if statement does not need a colon at the end of its header.",
        "Running an action only when a condition is met."
    ],
    [
        "An if-else statement chooses between two code paths.",
        "Pattern: if condition:\n    ...\nelse:\n    ...",
        "marks = 40\nif marks >= 50:\n    print('Pass')\nelse:\n    print('Try again')", "Try again",
        "The else block runs when the if condition is true.",
        "Choosing between two outcomes, such as pass or fail."
    ],
    [
        "An elif statement checks another condition when earlier conditions were false.",
        "Use elif between if and optional else blocks.",
        "marks = 75\nif marks >= 80:\n    print('A')\nelif marks >= 50:\n    print('Pass')\nelse:\n    print('Retry')", "Pass",
        "elif must be written before the first if statement.",
        "Selecting one result from several possible conditions."
    ],
    [
        "A nested condition is an if statement placed inside another conditional block.",
        "Indent the inner if block further than the outer if block.",
        "age = 20\nhas_ticket = True\nif age >= 18:\n    if has_ticket:\n        print('Enter')", "Enter",
        "Nested if statements must be placed at the same indentation level as the outer if.",
        "Checking a second requirement only after the first requirement passes."
    ],
    [
        "A for loop repeats a block for each item in an iterable.",
        "Pattern: for item in iterable:\n    statements",
        "for fruit in ['apple', 'mango']:\n    print(fruit)", "apple\nmango",
        "A for loop can only repeat exactly once.",
        "Processing each name, number, or item in a collection."
    ],
    [
        "A while loop repeats as long as its condition remains true.",
        "Pattern: while condition:\n    statements; update the condition to eventually stop.",
        "count = 1\nwhile count <= 3:\n    print(count)\n    count += 1", "1\n2\n3",
        "A while loop always runs a fixed number of times without checking a condition.",
        "Repeating a task until a condition is met."
    ],
    [
        "range() generates a sequence of integers, often used with for loops.",
        "range(stop), range(start, stop), and range(start, stop, step) are common forms.",
        "for number in range(1, 4):\n    print(number)", "1\n2\n3",
        "The stop value in range(1, 4) is included.",
        "Repeating an action a chosen number of times."
    ],
    [
        "break exits the nearest loop, continue skips to its next iteration, and pass does nothing.",
        "Use break, continue, or pass as standalone statements inside a block.",
        "for number in range(1, 5):\n    if number == 3:\n        continue\n    print(number)", "1\n2\n4",
        "continue permanently ends the entire program.",
        "Skipping selected loop items or leaving a placeholder block."
    ],
    [
        "A nested loop is a loop placed inside another loop.",
        "Write an inner for or while loop inside the indented body of an outer loop.",
        "for row in range(2):\n    for col in range(2):\n        print(row, col)", "0 0\n0 1\n1 0\n1 1",
        "A nested loop means two loops must run independently with no nesting.",
        "Working with grids, tables, and combinations of items."
    ],
    [
        "A function is a reusable block of code defined with the def keyword.",
        "Pattern: def function_name():\n    statements",
        "def greet():\n    print('Hello')\ngreet()", "Hello",
        "Defining a function automatically runs its body immediately.",
        "Reusing a task without copying the same code repeatedly."
    ],
    [
        "Parameters are names in a function definition; arguments are values passed when calling it.",
        "Pattern: def greet(name): ... then call greet('Ali')",
        "def greet(name):\n    print('Hello', name)\ngreet('Ali')", "Hello Ali",
        "A parameter is the value supplied in the function call, not the name in the definition.",
        "Passing different data into the same reusable function."
    ],
    [
        "return sends a result back from a function to the code that called it.",
        "Use: return expression inside a function body.",
        "def add(a, b):\n    return a + b\nprint(add(2, 3))", "5",
        "return and print always do exactly the same thing.",
        "Calculating a value in a function so another part of the program can use it."
    ],
    [
        "Variable scope describes where a variable name can be accessed.",
        "A variable created inside a function is local to that function unless declared otherwise.",
        "def show():\n    message = 'local'\n    print(message)\nshow()", "local",
        "A local variable is automatically available everywhere in the program.",
        "Avoiding naming conflicts and understanding local versus global values."
    ],
    [
        "Recursion occurs when a function calls itself, usually with a base case to stop.",
        "A recursive function needs a base case and a step that moves toward it.",
        "def countdown(n):\n    if n == 0:\n        return\n    print(n)\n    countdown(n - 1)\ncountdown(3)", "3\n2\n1",
        "A recursive function should call itself forever without a stopping condition.",
        "Solving problems that can be broken into smaller versions of themselves."
    ],
    [
        "A lambda is a small anonymous function written as a single expression.",
        "Pattern: lambda parameters: expression",
        "square = lambda x: x * x\nprint(square(4))", "16",
        "A lambda function is defined with the def keyword and a block body.",
        "Creating a short function for a simple operation."
    ],
    [
        "Exception handling lets a program respond to runtime errors without crashing unexpectedly.",
        "Use try for risky code and except to handle a matching exception.",
        "try:\n    number = int('abc')\nexcept ValueError:\n    print('Invalid number')", "Invalid number",
        "An except block must always be placed before its try block.",
        "Handling invalid input or other expected runtime errors gracefully."
    ]
]


def create_questions(chapter_name):
    chapter_index = CHAPTER_NAMES.index(chapter_name)

    concept, rule, example, expected, misconception, application = (
        CHAPTER_QUIZ_FACTS[chapter_index]
    )

    question_data = [
        {
            "question": f"Which statement best describes {chapter_name}?",
            "correct": concept,
            "wrong": [
                "It is a feature used only to change the colour of the editor.",
                "It is a command that shuts down the Python interpreter.",
                "It is unrelated to writing or running Python programs."
            ],
            "explanation": concept
        },
        {
            "question": f"Which rule or syntax is associated with {chapter_name}?",
            "correct": rule,
            "wrong": [
                "Python requires every statement to end with two semicolons.",
                "Python uses HTML tags to define all program statements.",
                "Python syntax is written only inside quotation marks."
            ],
            "explanation": rule
        },
        {
            "question": f"What is the output of this {chapter_name} example?\n{example}",
            "correct": expected,
            "wrong": [
                "The program always prints None.",
                "The program always produces a SyntaxError.",
                "The program produces no output in every case."
            ],
            "explanation": f"The example produces: {expected}"
        },
        {
            "question": f"Which option is a correct fact about {chapter_name}?",
            "correct": rule,
            "wrong": [
                "Python code never uses indentation.",
                "Variable names must always contain spaces.",
                "The print function is used to receive keyboard input."
            ],
            "explanation": rule
        },
        {
            "question": f"Which statement is a common misconception about {chapter_name}?",
            "correct": misconception,
            "wrong": [
                "Python programs can use variables to refer to values.",
                "Python code is executed according to its syntax rules.",
                "Clear code examples can help explain a programming concept."
            ],
            "explanation": f"This is incorrect: {misconception}"
        },
        {
            "question": f"Which is a practical application of {chapter_name}?",
            "correct": application,
            "wrong": [
                "Making a computer monitor physically larger.",
                "Changing the electrical power supply of a keyboard.",
                "Replacing the computer's operating system automatically."
            ],
            "explanation": application
        }
    ]

    questions = []

    for item in question_data:
        options = item["wrong"] + [item["correct"]]
        random.shuffle(options)

        questions.append({
            "question": item["question"],
            "options": options,
            "answer": options.index(item["correct"]),
            "explanation": item["explanation"]
        })

    return questions


# ==================================================
# 4. MODERN WEBSITE DESIGN
# ==================================================

STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {
    --page: #080d1b;
    --panel: #111a2e;
    --purple: #8b5cf6;
    --text: #eef2ff;
    --muted: #a6b3c8;
    --line: rgba(255,255,255,.09);
}

* { box-sizing: border-box; }
html { scroll-behavior: smooth; }

body {
    margin: 0;
    min-height: 100vh;
    color: var(--text);
    font-family: 'DM Sans', Arial, sans-serif;
    line-height: 1.7;
    background:
        radial-gradient(ellipse at 8% 0%, rgba(91,33,182,.23), transparent 34%),
        radial-gradient(ellipse at 95% 12%, rgba(14,116,144,.18), transparent 30%),
        var(--page);
}

header {
    position: relative;
    overflow: hidden;
    padding: 48px 20px 38px;
    text-align: center;
    background: linear-gradient(115deg, #17102f, #102744, #17102f);
    border-bottom: 1px solid var(--line);
}

header:before, header:after {
    content: '';
    position: absolute;
    width: 230px;
    height: 230px;
    border-radius: 50%;
    filter: blur(65px);
    opacity: .22;
    pointer-events: none;
}

header:before {
    background: #8b5cf6;
    top: -150px;
    left: 8%;
}

header:after {
    background: #06b6d4;
    right: 8%;
    bottom: -170px;
}

header h1 {
    position: relative;
    z-index: 1;
    margin: 0;
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(32px, 5vw, 49px);
    font-weight: 700;
    letter-spacing: -1.8px;
    background: linear-gradient(90deg, #ddd6fe, #7dd3fc);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}

header p {
    position: relative;
    z-index: 1;
    margin: 9px 0 0;
    color: #c1cce0;
}

nav {
    position: sticky;
    top: 0;
    z-index: 100;
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 10px;
    padding: 13px 16px;
    background: rgba(8,13,27,.88);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-bottom: 1px solid var(--line);
}

nav a {
    color: #cbd5e1;
    text-decoration: none;
    padding: 8px 17px;
    border-radius: 10px;
    font-size: 14px;
    font-weight: 700;
    transition: .2s ease;
}

nav a:hover {
    color: white;
    background: rgba(139,92,246,.2);
}

.container {
    width: min(1180px, 92%);
    margin: 36px auto;
    padding: 0 4px;
    min-height: 62vh;
}

.card {
    position: relative;
    background: linear-gradient(145deg, rgba(23,35,59,.97), rgba(15,23,42,.97));
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: 25px;
    margin-bottom: 20px;
    box-shadow: 0 12px 32px rgba(0,0,0,.2);
    transition: transform .22s ease, border-color .22s ease, box-shadow .22s ease;
}

.card:hover {
    transform: translateY(-3px);
    border-color: rgba(139,92,246,.42);
    box-shadow: 0 16px 38px rgba(0,0,0,.28);
}

.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(245px, 1fr));
    gap: 19px;
}

h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif;
    line-height: 1.3;
}

h2 {
    color: #c4b5fd;
    font-size: clamp(23px, 3vw, 29px);
    margin-top: 0;
}

h3 { color: #e2e8f0; font-size: 19px; }
p { color: var(--muted); }
strong { color: #e2e8f0; }

.btn {
    display: inline-block;
    margin: 6px 4px 4px 0;
    padding: 11px 18px;
    border: 1px solid rgba(255,255,255,.1);
    border-radius: 10px;
    color: white;
    text-decoration: none;
    font-size: 14px;
    font-weight: 700;
    background: linear-gradient(110deg, #7c3aed, #4f46e5);
    cursor: pointer;
    transition: transform .2s ease, filter .2s ease, box-shadow .2s ease;
}

.btn:hover {
    transform: translateY(-2px);
    filter: brightness(1.13);
    box-shadow: 0 8px 22px rgba(124,58,237,.28);
}

.green { background: linear-gradient(110deg, #059669, #0d9488); }
.purple { background: linear-gradient(110deg, #9333ea, #6366f1); }

pre {
    overflow-x: auto;
    white-space: pre-wrap;
    overflow-wrap: anywhere;
    padding: 20px;
    border: 1px solid rgba(56,189,248,.17);
    border-radius: 13px;
    background: #070d19;
    color: #a7f3d0;
    font: 14px/1.8 Consolas, 'Courier New', monospace;
    box-shadow: inset 0 0 24px rgba(0,0,0,.2);
}

.output {
    padding: 16px;
    border-left: 4px solid #10b981;
    border-radius: 10px;
    background: rgba(16,185,129,.09);
    color: #a7f3d0;
}

.output pre {
    margin: 0;
    border: 0;
    background: transparent;
    box-shadow: none;
}

textarea, input[type='text'], input[type='number'], select {
    width: 100%;
    padding: 13px 14px;
    margin: 8px 0;
    border: 1px solid #334155;
    border-radius: 10px;
    outline: none;
    background: #0b1324;
    color: white;
    font: inherit;
}

textarea { min-height: 110px; resize: vertical; }

textarea:focus, input:focus, select:focus {
    border-color: var(--purple);
    box-shadow: 0 0 0 3px rgba(139,92,246,.15);
}

input[type='radio'] {
    accent-color: #8b5cf6;
    width: 17px;
    height: 17px;
    vertical-align: middle;
    margin-right: 8px;
}

label { color: #dbe4f2; cursor: pointer; }

label:has(input[type='radio']) {
    display: block;
    padding: 11px 13px !important;
    margin: 7px 0;
    border: 1px solid var(--line);
    border-radius: 10px;
    background: rgba(255,255,255,.025);
    transition: .2s;
}

label:has(input[type='radio']):hover {
    border-color: rgba(139,92,246,.55);
    background: rgba(139,92,246,.09);
}

button.btn { font-family: inherit; }

.result-label {
    display: inline-block;
    padding: 10px 19px;
    border-radius: 10px;
    color: white;
    font-weight: 800;
    margin: 8px 0;
}

.learn-again { background: #dc2626; }
.good-result { background: #d97706; }
.excellent { background: #059669; }

footer {
    margin-top: 55px;
    padding: 27px 15px;
    text-align: center;
    background: #070c17;
    border-top: 1px solid var(--line);
    color: #cbd5e1;
}

footer p { margin: 5px 0; font-size: 13px; }
::selection { background: #7c3aed; color: white; }

@media (max-width: 650px) {
    header { padding: 34px 14px 28px; }
    nav { gap: 4px; }
    nav a { padding: 8px 11px; font-size: 13px; }
    .container { width: 94%; margin: 23px auto; }
    .card { padding: 19px; border-radius: 15px; }
    .grid { grid-template-columns: 1fr; gap: 13px; }
    h3 { font-size: 17px; }
    .btn { padding: 10px 14px; }
}
</style>
"""

# ==================================================
# 5. COMMON WEBSITE TEMPLATE
# ==================================================

BASE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="theme-color" content="#080d1b">
    <title>Python Academy | Learn Python</title>
    {{ style|safe }}
</head>
<body>

<header>
    <h1>🐍 Python Academy</h1>
    <p>Learn Python step by step • Learn, practise, improve</p>
</header>

<nav>
    <a href="/">⌂ Home</a>
    <a href="/#chapters">▦ Chapters</a>
</nav>

<div class="container">
    {{ content|safe }}
</div>

<footer>
    <strong>🐍 Python Academy</strong>
    <p>Build your programming skills one lesson at a time.</p>
</footer>

</body>
</html>
"""


def page(content):
    return render_template_string(
        BASE,
        content=content,
        style=STYLE
    )


# ==================================================
# 6. HOME PAGE
# ==================================================

@app.route("/")
def home():
    content = """
    <div class="card">
        <h2>Welcome to Python Academy</h2>
        <p>
            Learn Python programming from beginner level.
            This course contains 50 chapters and 750 topics.
        </p>
        <h3>Course Details</h3>
        <p>50 Chapters</p>
        <p>15 Topics in Every Chapter</p>
        <p>750 Topics in Total</p>
        <p>6 Test Questions in Every Chapter</p>
    </div>

    <h2 id="chapters">All Python Chapters</h2>
    <div class="grid">
    """

    for chapter in CHAPTERS:
        content += f"""
        <div class="card">
            <h3>Chapter {chapter['id']}</h3>
            <h3>{chapter['name']}</h3>
            <p>15 Learning Topics</p>

            <a class="btn" href="/chapter/{chapter['id']}">
                Open Chapter
            </a>

            <a class="btn purple" href="/test/{chapter['id']}">
                Take Test
            </a>
        </div>
        """

    content += "</div>"
    return page(content)


# ==================================================
# 7. CHAPTER PAGE
# ==================================================

@app.route("/chapter/<int:chapter_id>")
def chapter_page(chapter_id):
    if chapter_id < 1 or chapter_id > len(CHAPTERS):
        abort(404)

    chapter = CHAPTERS[chapter_id - 1]

    content = f"""
    <div class="card">
        <h2>Chapter {chapter['id']}: {chapter['name']}</h2>
        <p>This chapter contains 15 individual topics.</p>

        <a class="btn purple" href="/test/{chapter_id}">
            Take Chapter Test
        </a>
    </div>

    <h2>Learning Topics</h2>
    <div class="grid">
    """

    for topic in chapter["topics"]:
        content += f"""
        <div class="card">
            <h3>Topic {topic['id']}</h3>
            <h3>{topic['title']}</h3>

            <a class="btn" href="/topic/{chapter_id}/{topic['id']}">
                Start Learning
            </a>
        </div>
        """

    content += """
    </div>
    <a class="btn" href="/">Back to Home</a>
    """

    return page(content)


# ==================================================
# 8. INDIVIDUAL TOPIC PAGE
# ==================================================

@app.route("/topic/<int:chapter_id>/<int:topic_id>")
def topic_page(chapter_id, topic_id):
    if chapter_id < 1 or chapter_id > len(CHAPTERS):
        abort(404)

    chapter = CHAPTERS[chapter_id - 1]

    if topic_id < 1 or topic_id > 15:
        abort(404)

    topic = chapter["topics"][topic_id - 1]

    from markupsafe import escape

    content = f"""
    <div class="card">
        <h2>Chapter {chapter_id}: {escape(chapter['name'])}</h2>
        <h3>Topic {topic_id}: {escape(topic['title'])}</h3>
        <p>{escape(topic['explanation'])}</p>
    </div>

    <div class="card">
        <h2>Python Code Example</h2>
        <pre>{escape(topic['code'])}</pre>

        <h3>Expected Output</h3>
        <div class="output">
            <pre>{escape(topic['output'])}</pre>
        </div>
    </div>

    <div class="card">
        <h2>Practice Exercise</h2>
        <p>{escape(topic['exercise'])}</p>
    </div>

    <a class="btn" href="/chapter/{chapter_id}">
        Back to Topics
    </a>
    """

    if topic_id < 15:
        content += f"""
        <a class="btn green" href="/topic/{chapter_id}/{topic_id + 1}">
            Next Topic →
        </a>
        """
    else:
        content += f"""
        <a class="btn green" href="/test/{chapter_id}">
            Finish Chapter & Take Test
        </a>
        """

    return page(content)


# ==================================================
# 9. CHAPTER TEST WITH AUTOMATIC CHECKING
# ==================================================

@app.route("/test/<int:chapter_id>", methods=["GET", "POST"])
def test_page(chapter_id):
    if chapter_id < 1 or chapter_id > len(CHAPTERS):
        abort(404)

    chapter = CHAPTERS[chapter_id - 1]

    # GET: create the questions and save their exact order.
    if request.method == "GET":
        questions = create_questions(chapter["name"])

        if len(questions) != 6:
            return page("""
            <div class="card">
                <h2>Test setup error</h2>
                <p>This chapter must have exactly six questions.</p>
            </div>
            """)

        session["test_questions"] = questions
        session["test_chapter_id"] = chapter_id

        from markupsafe import escape

        content = f"""
        <div class="card">
            <h2>Chapter {chapter_id} Test</h2>
            <h3>{escape(chapter['name'])}</h3>
            <p>Choose one answer for each of the six questions.</p>
            <p>Each correct answer earns 1 mark.</p>
            <p><strong>Result guide:</strong>
            0–2 = Learn Again, 3–4 = Good, 5–6 = Excellent.</p>
        </div>

        <form method="POST">
        """

        for i, question in enumerate(questions):
            safe_question = escape(question["question"])
            safe_question = str(safe_question).replace("\n", "<br>")

            content += f"""
            <div class="card">
                <h3>Question {i + 1} of 6</h3>
                <p>{safe_question}</p>
            """

            for option_index, option in enumerate(question["options"]):
                content += f"""
                <label>
                    <input
                        type="radio"
                        name="q{i}"
                        value="{option_index}"
                        required
                    >
                    {escape(option)}
                </label>
                """

            content += "</div>"

        content += """
            <button class="btn green" type="submit">
                Check My Test
            </button>
        </form>
        """

        return page(content)

    # POST: use the same questions and options shown on the test page.
    questions = session.get("test_questions")
    saved_chapter_id = session.get("test_chapter_id")

    if not questions or saved_chapter_id != chapter_id:
        session.pop("test_questions", None)
        session.pop("test_chapter_id", None)

        return page(f"""
        <div class="card">
            <h2>Test session expired</h2>
            <p>Please start this chapter's test again.</p>
            <a class="btn" href="/test/{chapter_id}">
                Restart Test
            </a>
        </div>
        """)

    # Check that all six questions have an answer.
    if any(f"q{i}" not in request.form for i in range(len(questions))):
        return page(f"""
        <div class="card">
            <h2>Incomplete Test</h2>
            <p>Please answer all six questions before submitting.</p>
            <a class="btn" href="/test/{chapter_id}">
                Restart Test
            </a>
        </div>
        """)

    score = 0
    review = []

    for i, question in enumerate(questions):
        selected_value = request.form.get(f"q{i}", "")

        try:
            selected_index = int(selected_value)
        except (TypeError, ValueError):
            selected_index = -1

        valid = 0 <= selected_index < len(question["options"])
        is_correct = valid and selected_index == question["answer"]

        if is_correct:
            score += 1

        review.append({
            "number": i + 1,
            "question": question["question"],
            "selected": (
                question["options"][selected_index]
                if valid else "Invalid answer"
            ),
            "correct_answer": question["options"][question["answer"]],
            "is_correct": is_correct,
            "explanation": question["explanation"]
        })

    total = len(questions)
    percentage = round(score / total * 100)

    if score <= 2:
        result_title = "Learn Again"
        result_message = "Review this chapter and practise before trying again."
        result_class = "learn-again"

    elif score <= 4:
        result_title = "Good"
        result_message = "You understand some basics. Review incorrect answers."
        result_class = "good-result"

    else:
        result_title = "Excellent"
        result_message = "You answered almost all questions correctly. Keep practising!"
        result_class = "excellent"

    from markupsafe import escape

    content = f"""
    <div class="card">
        <h2>Chapter {chapter_id}: {escape(chapter['name'])} — Test Result</h2>

        <h1>{score} / {total} correct</h1>
        <h2>{percentage}%</h2>

        <div class="result-label {result_class}">
            {result_title}
        </div>

        <p>{result_message}</p>
        <p>Correct: {score} | Incorrect: {total - score}</p>

        <a class="btn" href="/test/{chapter_id}">
            Try Test Again
        </a>

        <a class="btn green" href="/chapter/{chapter_id}">
            Review Chapter
        </a>

        <a class="btn purple" href="/">
            Home
        </a>
    </div>

    <h2>Answer Review</h2>
    """

    for item in review:
        status = "Correct" if item["is_correct"] else "Incorrect"
        color = "#10b981" if item["is_correct"] else "#ef4444"

        safe_question = escape(item["question"])
        safe_question = str(safe_question).replace("\n", "<br>")

        content += f"""
        <div class="card">
            <h3>Question {item['number']}: {safe_question}</h3>

            <p>
                <strong>Your answer:</strong>
                {escape(item['selected'])}
            </p>

            <p>
                <strong>Correct answer:</strong>
                {escape(item['correct_answer'])}
            </p>

            <p style="color:{color};">
                <strong>Result: {status}</strong>
            </p>

            <p>
                <strong>Explanation:</strong>
                {escape(item['explanation'])}
            </p>
        </div>
        """

    # Clear the test attempt after showing the results.
    session.pop("test_questions", None)
    session.pop("test_chapter_id", None)

    return page(content)


# ==================================================
# 10. START WEBSITE AND OPEN BROWSER AUTOMATICALLY
# ==================================================

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")


if __name__ == "__main__":
    print("Python Academy is starting...")
    print("Total Chapters:", len(CHAPTERS))
    print("Topics Per Chapter:", len(TOPIC_STEPS))
    print("Total Topics:", len(CHAPTERS) * len(TOPIC_STEPS))

    Timer(1, open_browser).start()

    app.run(
        debug=False,
        use_reloader=False
    )