import re
import json

def parse_questions_from_text(text):
    # Regex to isolate blocks of text for each question
    block_pattern = re.compile(r'QUESTION\s+(\d+)(.*?)(?=\s*QUESTION|\s*$)', re.DOTALL)
    
    questions = []

    for block_match in block_pattern.finditer(text):
        question_id = block_match.group(1).strip()
        question_block = block_match.group(2).strip()

        # Extract question text by ensuring it stops before the first occurrence of any option "A."
        question_text_match = re.search(r'(.*?)(?=^\s*[A-F]\.)', question_block, re.DOTALL | re.MULTILINE)
        if question_text_match:
            question_text = question_text_match.group(0).strip()
            question_text = re.sub(r'\s+', ' ', question_text)
        else:
            question_text = "Could not properly extract question text."

        # Extract options ensuring each starts with A., B., etc.
        options = {}
        options_matches = re.finditer(r'([A-F])\.\s+(.*?)(?=\s+[A-F]\.|\s*Answer:)', question_block, re.DOTALL)
        for index, match in enumerate(options_matches):
            option_letter = match.group(1)
            option_text = match.group(2).strip()
            options[str(ord(option_letter) - ord('A') + 1)] = option_text
        
        # Extract answers and convert to 1, 2, 3, etc.
        answer_labels = re.search(r'Answer:\s*([A-Fa-f]+)', question_block)
        correct_answers = []
        if answer_labels:
            answer_labels = answer_labels.group(1).strip().upper()
            correct_answers = [f"options.{str(ord(label) - ord('A') + 1)}" for label in answer_labels]
        
        # Extract explanation and URL, if present
        explanation = ''
        source_url = ''
        explanation_match = re.search(r'Explanation:\s*(.*?)\s*(https?://\S+)?$', question_block, re.DOTALL)
        if explanation_match:
            explanation = re.sub(r'\s+', ' ', explanation_match.group(1).strip())
            if explanation_match.group(2):
                source_url = explanation_match.group(2).strip()

        # Assemble the question dictionary
        question_data = {
            "id": question_id,
            "question": question_text,
            "options": options,
            "correct_answers": correct_answers,
            "description": explanation,
            "source_url": source_url
        }

        questions.append(question_data)

    return questions

# Example usage
with open('python-app/pdf-in fixed.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# Parsing questions
parsed_questions = parse_questions_from_text(text)

# JSON output
json_output = json.dumps(parsed_questions, indent=4)

# Writing to a JSON file
with open('pdf-in-fixed.json', 'w', encoding='utf-8') as json_file:
    json_file.write(json_output)

print("JSON file 'pdf-in-fixed.json' has been created with the parsed data.")