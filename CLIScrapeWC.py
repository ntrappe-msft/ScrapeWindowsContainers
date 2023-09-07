import requests, datetime, pytz

# ANSI escape codes for text colors
GREY = '\033[90m'
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
PURPLE = '\033[95m'
TEAL = '\033[96m'
RESET = '\033[0m'

# HTTP responses
UNATHORIZED = 401
FORBIDDEN = 403

# GitHub API Info
OWNER = 'microsoft'
REPO = 'Windows-Containers'
PARAMS = {'per_page': 100}


def fetch(token):
    """
    Fetch all the Issues from a GitHub repo.

    Args:
        token (string): GitHub Personal Access Token

    Returns:
        1: Encountered an issue
        list: Set of issues
    
    The URL endpoint will scrape ONLY issue information. We first make an API request to get
    the number of total issues (closed or open) then we'll have to fetch multiple times 
    because, by default, the API only gives 30 issues at a time from a single page.
    """
    # URL endpoint to scrape ONLY issues information
    headers = {'Authorization': f'Bearer {token}'}
    url = f'https://api.github.com/repos/{OWNER}/{REPO}/issues?state=all'

    # Make the API request and retrieve the JSON response for querying issues
    response = requests.get(url.format(owner=OWNER, repo=REPO), headers=headers, params=PARAMS)
    
    if response.status_code == UNATHORIZED:
        print(RED + 'ERROR: Invalid token. You do not have permission to access this repo.' + RESET)
        return 1;
    elif response.status_code == FORBIDDEN:
        print(RED + 'ERROR: Valid token but do not have permission to fetch.' + RESET)
        return 1;
    else:
        data = response.json()
        # Go through each page of Issues, pulling all of them
        while 'next' in response.links:
            response = requests.get(response.links["next"]["url"], headers=headers)
            data += response.json()
        
        print(GREEN + f'Fetched {len(data)} Issues from the repo.' + RESET)
        return data

def printIssueTitles(issues):
    """
    Because of order of fetching, the first issue in issues is the most recently added
    issue to GitHub (highest issue #)
    """
    numIssues = len(issues)
    if (numIssues < 1):
        print(RED + 'ERROR: No issues to print.' + RESET)
    else:
        print(GREEN + '\nPrinting ' + str(numIssues) + ' issues.' + RESET + '\n')
        for issue in issues:
            print(PURPLE, 'Issue', issue['number'], RESET, '\t', issue['title'])
        print('\n')

def pipeIssuesToFile(filename, issues, token):
    """
    Pipes each issue #, title, creation data/time, body, and comments to a specified file
    
    Args:
        filename (string): File to pipe to (including extension)
        issues (list): Set of issues
        token (string): GitHub Personal Access Token

    Returns:
        0: success
        1: failure  
    """
    try:
        with open(filename, 'w') as file:
            for issue in issues:
                comments = fetchComments(issue, token)
                file.write('-----------------------------------ISSUE #'+ str(issue['number']) + '----------------------------------\n')
                file.write('Created At: ' + issue['created_at'] + '\n')
                file.write('\nDESCRIPTION:\n')
                file.write(issue['body'])
                file.write('\n\nCOMMENTS:\n')
                if comments == []:
                    file.write('No comments.\n')
                else:
                    for comment in comments:
                        file.write(comment['body'] + '\n')
            
                file.write('--------------------------------------END-------------------------------------\n\n')
        
        rint(GREEN + f"File '{filename}' has been created and written to successfully." + RESET + '\n\n')
        return 0
    except Exception as e:
        print(f"An error occurred: {e}")
        return 1

def fetchComments(issue, token):
    """
    Fetch all the comments from a single issue.

    Args:
        issue (list): Single GitHub Issue
        token (string): GitHub Personal Access Token

    Returns:
        []: No comments
        list: Set of comments
    """
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(issue['comments_url'], headers=headers, params=PARAMS)

    if response.status_code == UNATHORIZED:
        print(RED + 'ERROR: Invalid token. You do not have permission to access this repo.' + RESET)
        return 1;
    elif response.status_code == FORBIDDEN:
        print(RED + 'ERROR: Valid token but do not have permission to fetch.' + RESET)
        return 1;
    else:
        # Fetch the comments for the issue and return if we have any
        comments = response.json()
        if len(comments) < 1:
            return []
        else:
            return comments

def imageBreakdown():
    print('tbd')

def issueLifecycles():
    print('tbd')


# Entry point to the program
try:
    user_token = input(GREY + 'Please provide your GitHub token: ' + RESET)
    issues = fetch(user_token)
    
    print(GREY + '\nActions you can perform:' + RESET)
    print(PURPLE + 'A. Print GitHub Issue Titles' + RESET)
    print(BLUE + 'B. Pipe All Issues to a File' + RESET)
    print(TEAL + 'C. Get Total Number of Issues' + RESET)
    choice = input(GREY + '\nEnter the letter of your choice: ' + RESET)

    if choice.upper() == 'C':
        print(GREEN + f'There are {len(issues)} GitHub Issues' + RESET + '\n\n')
    elif choice.upper() == 'B':
        filename = input(GREY + '\nPlease provide the name for the file to pipe to (include the extension): ' + RESET)
        pipeIssuesToFile(filename, issues, user_token)
    elif choice.upper() == 'A':
        printIssueTitles(issues)
    else:
        print(RED + f"ERROR: '{choice}' was not a valid option" + RESET + '\n\n') 

except (EOFError, KeyboardInterrupt):
    print(YELLOW + '\nExiting program.' + RESET)

