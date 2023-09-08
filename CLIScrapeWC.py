import requests, datetime, pytz
from scrapeWCHeader import GREY, RED, GREEN, YELLOW, BLUE, PURPLE, TEAL, RESET
from scrapeWCHeader import HEADER, FOOTER, EXIT_FAILURE, EXIT_SUCCESS
from analysisWC import analyze_issues, analyze_images, get_unknown_images

# HTTP responses
UNATHORIZED = 401
FORBIDDEN = 403

# GitHub API Info
OWNER = 'microsoft'
REPO = 'Windows-Containers'
PARAMS = {'per_page': 100}


def fetch(token):
    """
    Fetch all the Issues from a GitHub repo. The URL endpoint for Issues actually scrapes both
    Issue and Pull Requests (closed or open) so we'll first have to fetch then filter out PRs.
    By default, the API only gives 30 Issues at a time from a single page so I've increased
    how many Issues it pulls in at a time and it reads from multiple pages

    Args:
        token (string): GitHub Personal Access Token

    Returns:
        1: Encountered an issue
        list: Set of issues
    """
    # URL endpoint to scrape ONLY issues information
    headers = {'Authorization': f'Bearer {token}'}
    url = f'https://api.github.com/repos/{OWNER}/{REPO}/issues?state=all'

    # Make the API request and retrieve the JSON response for querying issues
    response = requests.get(url.format(owner=OWNER, repo=REPO), headers=headers, params=PARAMS)
    
    if response.status_code == UNATHORIZED:
        print(RED + 'ERROR: Invalid token. You do not have permission to access this repo.' + RESET)
        return EXIT_FAILURE;
    elif response.status_code == FORBIDDEN:
        print(RED + 'ERROR: Valid token but do not have permission to fetch.' + RESET)
        return EXIT_FAILURE;
    else:
        issues = response.json()
        # Go through each page of Issues, pulling all of them
        while 'next' in response.links:
            response = requests.get(response.links["next"]["url"], headers=headers)
            issues += response.json()
        
        # Now filter out the PRs
        filtered_issues = [issue for issue in issues if 'pull_request' not in issue]
        print(f'\nFetched {len(issues)} Issues from the repo.')
        print(f'Filtered out {len(issues) - len(filtered_issues)} PRs.')

        return filtered_issues

def print_issue_titles(issues):
    """
    Because of order of fetching, the first issue in issues is the most recently added
    issue to GitHub (highest issue #)
    """
    numIssues = len(issues)
    if (numIssues < 1):
        print(RED + 'ERROR: No issues to print.' + RESET)
    else:
        print(GREY + '\nPrinting ' + str(numIssues) + ' issues.' + RESET + '\n')
        for issue in issues:
            print(PURPLE, 'Issue', issue['number'], RESET, '\t', issue['title'])
        print('\n')

def pipe_issues_to_file(filename, issues, token):
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
                file.write(HEADER)
                file.write('\nDETAILS:\nIssue #' + str(issue['number']) + ' created at ' + issue['created_at'] + '\n')
                if issue['body'] == None:
                    file.write('\nDESCRIPTION:\n\nNo question or description found.\n')
                else:
                    file.write('\nDESCRIPTION:\n\n' + issue['body'] + '\n')
                
                # Now fetch all the comments for this Issue then pipe each one
                comments = fetch_comments(issue, token)
                if (comments == EXIT_FAILURE):
                    print(f"{RED}File '{filename}' could not be written successfully.{RESET}\n\n")
                    return EXIT_FAILURE

                file.write('\nCOMMENTS:\n')
                if comments == []:
                    file.write('\nNo comments.\n')
                else:
                    for comment in comments:
                        file.write(comment['body'] + '\n')
                file.write('\n' + FOOTER)
        print(BLUE + f"File '{filename}' has been created and written to successfully." + RESET + '\n\n')
        return EXIT_SUCCESS
    except Exception as e:
        print(f"An error occurred: {e}")
        return EXIT_FAILURE

def fetch_comments(issue, token):
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
        return EXIT_FAILURE;
    elif response.status_code == FORBIDDEN:
        print(RED + 'ERROR: Valid token but do not have permission to fetch.' + RESET)
        return EXIT_FAILURE;
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
    user_token = input(GREY + '\nPlease provide your GitHub token: ' + RESET)
    issues = fetch(user_token)

    if issues == EXIT_FAILURE:
        print(GREY + '\nExiting program --->\n\n' + RESET)
    else:
        while True:
            print(GREY + '\nChoose an action to perform:' + RESET)
            print(RED + 'A. Quit' + RESET)
            print(PURPLE + 'B. Print GitHub Issue Titles' + RESET)
            print(BLUE + 'C. Pipe All Issues to a File' + RESET)
            print(TEAL + 'D. Get Total Number of Issues' + RESET)
            print(GREEN + 'E. Issue Lifecycle Statistics' + RESET)
            print(YELLOW + 'F. Breakdown of Image Usage' + RESET)
            choice = input(GREY + '\nEnter the letter of your choice: ' + RESET)

            # Depending on the letter, call the corresponding function/ask for input
            if choice.upper() == 'A':
                print(GREY + '\nExiting program --->\n\n' + RESET)
                break
            
            elif choice.upper() == 'B':
                print_issue_titles(issues)
            
            elif choice.upper() == 'C':
                filename = input(GREY + '\nPlease provide the name for the file to pipe to (include the extension): ' + RESET)
                pipe_issues_to_file(filename, issues, user_token)
            
            elif choice.upper() == 'D':
                print(TEAL + f'\nThere are {len(issues)} GitHub Issues' + RESET + '\n')
            
            elif choice.upper() == 'E':
                analyze_issues(issues)
            
            elif choice.upper() == 'F':
                analyze_images(issues)
                print(GREY + "Would you like to see all of the Issues with 'Unknown' image types?" + RESET)
                see_misc = input(GREY + "\nSelect 'Y' for YES or 'N' for NO: " + RESET)
                if see_misc.upper() == 'Y' or see_misc.upper() == 'YES':
                    get_unknown_images()
            
            else:
                print(RED + f"ERROR: '{choice}' was not a valid option" + RESET + '\n\n') 

except (EOFError, KeyboardInterrupt):
    print(GREY + '\nExiting program --->\n\n' + RESET)

