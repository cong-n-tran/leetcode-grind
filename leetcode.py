import json
import random
from glob import glob
import webbrowser

# all the categories of problems
CATEGORIES = [
    "Arrays & Hashing", 
    "Two Pointers",
    "Sliding Window",
    "Stack",
    "Binary Search",
    "Linked List",
    "Trees",
    "Binary Search",
    "Heap & Priority Queue",
    "Graphs",
    "Backtracking",
    "1-D Dynamic Programming", 
    "2-D Dynamic Programming", 
    "Greedy",
    "Bit Manipulation",
    "Math & Geometry",
    "Tries",
]

# specific configurations 
CONFIG = {
    "only_solved": True, 
    "only_neetcode": True, 
    "specific_problem": [], 
    "number_of_problems": 10,
}

# load all the probelms from the JSON files
def load_problems():
    problems = []
    for file in glob("problems/*.json"):
        with open(file, "r") as f:
            data = json.load(f)
            listOfProblems = data.get("problems", [])
            
            for p in listOfProblems:
                # add the category to the each problem
                p["category"] = data.get("category", "Unknown Category")

                # get the solved and neetcode status
                isSolved = p.get("solved", False)
                isNeetcode = p.get("neetcode", False)

                # skip the problem if it is not solved or not neetcode
                if CONFIG["only_solved"] and not isSolved:
                    continue
                if CONFIG["only_neetcode"] and not isNeetcode:
                    continue

                # add to problems array
                problems.append(p)
    return problems


def get_random_problems(number_of_problems=10): 
    problems = load_problems() # load all the problems
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



# start the process of opening problem links
opening_problem_links()
