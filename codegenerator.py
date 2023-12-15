from flask import Flask, render_template, Blueprint, request

codegenerator_app = Blueprint('/codegenerator',__name__)


# Function to generate code in various languages
def generate_code(user_input, selected_language):
    code = ""

    if selected_language == 'python':
        code = generate_python_code(user_input)
    elif selected_language == 'java':
        code = generate_java_code(user_input)
    elif selected_language == 'php':
        code = generate_php_code(user_input)
    # Add conditions for other languages here
    else:
        code = "# Language not supported yet."

    return code


# Function to generate Python code
def generate_python_code(user_input):
    code = f'''# Python Code
def main():
    user_input = "{user_input}"
    print(user_input)

if __name__ == "__main__":
    main()
'''
    return code


# Function to generate Java code
def generate_java_code(user_input):
    code = f'''// Java Code
public class Main {{
    public static void main(String[] args) {{
        String userInput = "{user_input}";
        System.out.println(userInput);
    }}
}}
'''
    return code


# Function to generate PHP code
def generate_php_code(user_input):
    code = f'''// PHP Code
<?php
$userInput = "{user_input}";
echo $userInput;
?>
'''
    return code


@codegenerator_app.route('/codegenerator')
def index():
    return render_template('codegenerator.html')


@codegenerator_app.route('/codegenerator', methods=['POST'])
def generate_code_handler():
    user_input = request.form['user_input']
    selected_language = request.form['language']
    code = generate_code(user_input, selected_language)
    return render_template('codegenerator.html', user_input=user_input, code=code, selected_language=selected_language)


# Route and function for calculations
@codegenerator_app.route('/calculate', methods=['POST'])
def calculate_handler():
    user_expression = request.form['expression']
    try:
        result = eval(user_expression)
        result_code = f'# Result of Calculation: {result}'
    except Exception as e:
        result_code = f'# Error: {str(e)}'

    return render_template('codegenerator.html', user_expression=user_expression, result_code=result_code)



