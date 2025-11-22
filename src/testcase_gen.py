#!/usr/bin/env python3
"""
Script to generate test generator code using AI
"""

from pymongo import MongoClient
import os
import random
import sys
import argparse
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv
import requests
import time
from run_cpp import run_file

load_dotenv()

api_key = os.getenv('GENAI_API_KEY')
print(api_key)
client = genai.Client(api_key=api_key)

MONGO_URI = os.getenv('MONGO_URI')
DATABASE_NAME = os.getenv('DATABASE_NAME')
COLLECTION_NAME = "problems"
RULE_CODE = """ "testcases/" + (test_case_index < 10 ? "0" : "") + std::to_string(test_case_index); """

SAMLPLE_GENERATOR_CODE = ""
def read_file(filepath):
    """Read content from file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

def parse_problem(data):
    """Parse problem files"""
    
    data = {
        'statement': data["statement"],
        'input': data["input"],
        'output': data["output"],
        'solution': data['code'],
        'number_of_tests': random.randint(20, 50),
    }
    return data

def generate_with_ai(problem_data):
    """Generate test generator using AI (placeholder - can integrate with OpenAI/Anthropic)"""
    
    # First, check if the problem accepts any valid output
    check_prompt = f"""
Analyze the following competitive programming problem and determine if it accepts multiple valid outputs.

PROBLEM STATEMENT:
{problem_data['statement']}

PROBLEM OUTPUT CONSTRAINTS:
{problem_data['output']}

Does this problem accept ANY valid output (meaning there are multiple correct answers)?
Examples:
- "Output any prime number" - YES (multiple valid outputs)
- "Output any valid coloring" - YES (multiple valid outputs)
- "Output the sum of two numbers" - NO (unique output)
- "Output the maximum value" - NO (unique output)

Respond with ONLY "YES" or "NO".
"""
    
    check_response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=check_prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0)
        ),
    ).text.strip().upper()
    
    if "YES" in check_response:
        print(f"⚠️  Skipping generator: Problem accepts any valid output")
        return None
    
    prompt = f"""
Based on the following competitive programming problem, generate a C++ test generator that creates random test cases.

PROBLEM STATEMENT:
{problem_data['statement']}

PROBLEM INPUT CONSTRAINTS:
{problem_data['input']}

PROBLEM OUTPUT CONSTRAINTS:
{problem_data['output']}

SOLUTION CODE:
{problem_data['solution']}

NUMBER OF TEST CASES TO GENERATE: {problem_data['number_of_tests']}

IMPORTANT - UNDERSTAND THE INPUT FORMAT:
- If the problem input starts with T (number of test cases), then ONE complete test case contains:
  * First line: T (number of sub-problems)
  * Next T lines/blocks: T separate sub-problems to solve
- DO NOT treat each sub-problem as a separate test case
- ONE test case = ONE complete input file with all T sub-problems included

EXAMPLE:
If problem asks to calculate a + b with T test cases:
CORRECT format for ONE test case:
5
1 2
3 4
3 1
2 4
3 5

WRONG format (DO NOT do this):
1 2

Generate a C++ program that:
1. Uses random number generation to create valid test cases
2. Outputs test cases in the EXACT input format specified (including T and all sub-problems)
3. Handles all constraints mentioned in the problem
4. Can generate different types of tests: small, random, edge cases, stress tests
5. Takes command line arguments for test type and seed
6. Creates separate folders for each test case (total {problem_data['number_of_tests']} folders)
7. Each folder contains one COMPLETE test case with 2 files: test.inp and test.out
8. If input format has T at the beginning, generate T sub-problems in EACH test.inp file
9. I want to run the generator program and get a full set of test cases ready to use, I don't want to give generator program any paramters about number of test cases etc.
10. Structure of folder should be:
    - 1 folder root: testcases
    - Inside testcases, will have a lots of folders named 01, 02, ..., 20 (or up to number_of_tests)
    - Inside each folder, will have 2 files: test.inp and test.out
11. Lib to use should be suitable for MACOS
12. Don't use rules like, it will crash on MACOS:
{RULE_CODE}
EXAMPLE ABOUT GENERATOR CODE: 
{SAMLPLE_GENERATOR_CODE}
The generator should be complete and compilable with g++.
Output ONLY the C++ code, no explanations, no markdown code blocks.
"""
    
    generator_template = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    thinking_config=types.ThinkingConfig(thinking_budget=0)
                ),
            ).text
    return generator_template
def save_generator(generator_code, problem_name, output_dir='generators'):
    """Save generated code to file"""
    dir = output_dir+"/"+problem_name
    os.makedirs(dir, exist_ok=True)
    output_file = os.path.join(dir, f'{problem_name}_gen.cpp')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(generator_code)
    
    print(f"✅ Generator saved to: {output_file}")
    return output_file

def main():
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    print("hello")
    SAMLPLE_GENERATOR_CODE = read_file('data/sample_generator_code.txt')
    LIBRARY_CODE = read_file('data/library_code.txt')
    with open('data/problem_solution_data_v1.jsonl', 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            problem_name = data['name']
            print(f"Checking have solution: {data["_id"]} - {problem_name}")
            mongo_doc = collection.find_one({'name': problem_name})
            if mongo_doc:
                # Add _id to data
                isActive = bool(mongo_doc['isActive'])
                if isActive == True:
                    print(f"✅ Problem is active, skipping: {data["_id"]} - {problem_name}")
                    continue

            print(f"Generating test generator for problem: {data["_id"]} - {problem_name}")
            print("--------------------------------------------------")
            # print(data["code"])
            problem_data = parse_problem(data)
            generator_code = generate_with_ai(problem_data)
            if generator_code is None:
                print(f"⏭️  Skipped: {data['_id']} - {problem_name}")
                continue
            print(generator_code)
            save_generator(generator_code=LIBRARY_CODE + "\n" + generator_code, problem_name= data["_id"])
            run_file(data["_id"])
            time.sleep(20)

if __name__ == '__main__':
    main()
