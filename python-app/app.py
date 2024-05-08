import re
import json

def parse_questions_from_text(text):
    pattern = re.compile(
        r'QUESTION\s+(\d+)\s+(.*?)(?=\s*QUESTION|\s*$)',  # Capture question ID and text, lookahead for next question or end of text
        re.DOTALL
    )

    questions = []

    for match in pattern.finditer(text):
        question_id = match.group(1).strip()
        question_block = match.group(2).strip()

        # Extract question text up to the options start
        question_text = re.search(r'(.*?)A\.', question_block, re.DOTALL).group(1).strip()
        question_text = re.sub(r'\s+', ' ', question_text)

        # Extract options and normalize them by mapping A, B, C to 1, 2, 3, etc.
        options = re.findall(r'([A-F])\.\s+(.*?)(?=\s+[A-F]\.|\s*Answer:|\s*$)', question_block, re.DOTALL)
        options_dict = {str(index + 1): option[1].strip() for index, option in enumerate(options)}

        # Extract answers and convert A, B, C, etc., to 1, 2, 3, etc.
        # Normalize answer labels to uppercase for consistent processing
        answer_labels = re.search(r'Answer:\s*([A-Fa-f]+)', question_block).group(1).strip().upper()
        correct_answers = [options_dict[str(ord(label) - ord('A') + 1)] for label in answer_labels]

        # Optionally capture explanation and URL
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
            "options": options_dict,
            "correct_answers": [f"options.{str(ord(label) - ord('A') + 1)}" for label in answer_labels],
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

print("JSON file 'pdf-in.json' has been created with the parsed data.")