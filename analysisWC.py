import requests, datetime, pytz
import statistics
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime as dt
from datetime import timezone
from scrapeWCHeader import image_mapping, engine_mapping
from scrapeWCHeader import GREY, RED, GREEN, YELLOW, BLUE, PURPLE, TEAL, RESET

# Data structures
open_durations = []
image_counts = {}
miscellaneous_images = []

# Constants
SEC_IN_DAY = 86400

def analyze_images(issues):
    for issue in issues:
        get_image_type(issue)

    numIssues = len(issues)
    print(GREEN + '\nImage Usage Statistics:' + RESET)
    print(GREY + "Note that many users will indicate generic images types like 'server core' instead of " + RESET)
    print(GREY + "'server core 2022' or something specific. We also have a number of Issues that relate to " + RESET)
    print(GREY + "needs beyond generic container issues which is why we have many 'Unknown' entries.\n" + RESET)
    for key in image_counts.keys():
        percent = '{:.1f}'.format((image_counts[key]/numIssues) * 100)
        print(YELLOW + f'{percent}%\t' + RESET + f'of Issues had {key}')
    print('\n')


def get_unknown_images():
    print(GREEN + "\nIssues with 'Unknown' Image Types:" + RESET)
    print(GREY + f'Note that we have {len(miscellaneous_images)} of these.\n' + RESET)
    for misc in miscellaneous_images:
        print(misc)
    print('\n\n')

def analyze_issues(issues):
    for issue in issues:
        open_durations.append(get_issue_open_time(issue))

    if open_durations:
        avg_open_time = round(sum(open_durations) / len(open_durations))
        median_open_time = round(statistics.median(open_durations))
        max_open_time = round(max(open_durations))
        min_open_time = round(min(open_durations))
        print(GREEN + '\nIssue Lifecycle Statistics:' + RESET)
        print(f'  - Issues are open for an {GREEN}average of {avg_open_time}{RESET} days.')
        print(f'  - Issues are open for a {TEAL}median of {median_open_time}{RESET} days.')
        print(f'  - Issues are open between {BLUE}{min_open_time} and {max_open_time}{RESET} days.\n')
    else:
        print(RED + '\nERROR: No closed issues found.\n' + RESET)


def get_image_type(issue):
    """
    Given the text content of an Issue, identify which image type is being discussed.
    Updates our internal count of each image type once we identify them

    Args:
        issue (JSON string): all the data for a single Issue
    
    """
    found_image = 1
    page_content = f"{issue['title']} {issue['body']}"
    for image_name in image_mapping.keys():
        # found a reference to an existing image type in the body
        if image_name.lower() in page_content.lower():
            # get the official image type (from reference)
            standardized_name = image_mapping[image_name]
            # if we already have an input for this image in data_counts, incr
            # otherwise, create new entry and set count to 1
            if standardized_name in image_counts:
                image_counts[standardized_name] += 1
                found_image = 0
            else:
                image_counts[standardized_name] = 1
                found_image = 0
            # then break once we have found a match bc dont overinflate it
            break
    if (found_image == 1):
        miscellaneous_images.append(f"Issue #{issue['number']}: {issue['title']}")
        if 'Unknown' in image_counts:
            image_counts['Unknown'] += 1
        else:
            image_counts['Unknown'] = 1


def get_issue_open_time(issue):
    """
    Calculates the time an issue was open for by using function to subtract time closed from 
    time open in the ISO 8601 format

    Args:
        issue (JSON string): all the data for a single Issue

    Return:
        number: how many days Issue was open for
    """
    time_open = 0
    created_at = dt.fromisoformat(issue['created_at'])

    if issue['state'] == 'closed':
        closed_at = dt.fromisoformat(issue['closed_at'])
        time_open = closed_at - created_at
    else:
        now = dt.now()
        utc = pytz.utc
        time_open = utc.localize(now) - created_at
    
    days_open, seconds_remaining = divmod(time_open.total_seconds(), SEC_IN_DAY)
    
    # round up a day if we have time remaining
    if seconds_remaining > 0:
        days_open += 1

    return days_open


