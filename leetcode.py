import json
import random
import webbrowser
import os
from glob import glob
from configurations import CONFIG
import datetime

# load all the probelms from the JSON files
def load_problems():
    problems = []
    for file in glob("problems/*.json"):
        with open(file, "r") as f:
            data = json.load(f)
            category = data.get("category", "Unknown Category")
            specific_problem = CONFIG.get("specific_problem", [])

            if len(specific_problem) > 0 and category not in specific_problem:
                # skip the category if it is not in the specific problem list
                continue
        
            listOfProblems = data.get("problems", [])
            
            for p in listOfProblems:
                # add the category to the each problem
                p["category"] = category

                # get the solved and neetcode status
                isSolved = p.get("solved", False)
                isNeetcode = p.get("neetcode", False)

                # skip the problem if it is not solved or not neetcode
                if isNeetcode and not CONFIG["include_neetcode"]:
                    continue
                if CONFIG["only_solved"] and not isSolved:
                    continue
                if CONFIG["only_neetcode"] and not isNeetcode:
                    continue

                # add to problems array
                problems.append(p)
    return problems


def get_random_problems(number_of_problems=10): 
    problems = load_problems() # load all the problems
    random.shuffle(problems) # shuffle the problems to get random ones
    number_of_problems = min(number_of_problems, len(problems)) # limit the number of problems to the available ones
    return random.sample(problems, number_of_problems) # randomly select the problems
    

def opening_problem_links(): 
    # get random problems based on the number of problems specified in the config

    number_of_problems = CONFIG["number_of_problems"]
    random_problems = get_random_problems(number_of_problems)


    for problem in random_problems:
        url = problem.get("leetcode_link", "")
        name = problem.get("name", "Unknown Problem")
        difficulty = problem.get("difficulty", "Unknown Difficulty")
        problemCategory = problem.get("category", "Unknown Category")
        if url:
            print(f"{name} ({difficulty}) from {problemCategory}")
            print(f"Opening URL: {url}\n")
            webbrowser.open(url)
        else:
            print(f"No URL found for problem: {name} ({difficulty}) from {problemCategory}\n")

        # update the problem tracking
    update_problem_tracking(random_problems)

def update_problem_tracking(problems: list)-> None:
    tracking_filename = 'problem_tracking.json'

    # load existing data if file exists
    if os.path.exists(tracking_filename):
        with open(tracking_filename, 'r') as f:
            data = json.load(f)
    else:
        data = {}

    
    for problem in problems:
        # extract problem details
        problem_name = problem.get("name", "Unknown Problem")
        category = problem.get("category", "Unknown Category")
        difficulty = problem.get("difficulty", "Unknown Difficulty")
        link = problem.get("leetcode_link", "")

        if not link:
            print(f"No link provided for problem: {problem_name}. Skipping tracking update.")
            continue
        
        # get current time for tracking
        last_done = datetime.datetime.now().strftime("%B %d, %Y at %I:%M %p")
    
        # check if the problem already exists in the tracking data
        if problem_name in data:
            data[problem_name]['times_done'] += 1
            data[problem_name]['last_done'] = last_done
        else:
            # add new problem entry
            data[problem_name] = {
                'category': category,
                'difficulty': difficulty,
                'link': link,
                'times_done': 1,
                'first_done': last_done,
                'last_done': last_done
            }

    # Save back to file
    with open(tracking_filename, 'w') as f:
        json.dump(data, f, indent=2)

# start the process of opening problem links
opening_problem_links()
