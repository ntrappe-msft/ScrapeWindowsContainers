# ScrapeWindowsContainers

This is an interactive script that allows you to scrape the Windows Containers repo
and to pull the number of Issues, print Issues, and pipe Issues to a file.

### Prequesities

- [ ] Make sure you have a GitHub token.
- [ ] Make sure you have `python` installed

#### Get a Token

- Go to `Profile > Settings > Developer settings > Personal access tokens > Tokens (classic)`
- Generate a new token and make sure it provides repo access
- Save the token (COPY IT DOWN SOMEWHERE)
- Authorize it with Microsoft

#### Get Python

- if you have homebrew installed you can do:

```ruby
brew install python
```

### How to Use

Run the program by using the following command (I use `python3` not `python` because I have version `3.11.5`):

```ruby
python3 CLIScrapeWC.py
```

It will then ask for your GitHub token. Paste it (no spaces).

### Example

Provide the correct GitHub token. This was sucessful because it fetched 410 Issues.
![Image showing fetch success]('media/usage_stats.png')

Select option C: Pipe All Issues to a File. This was successful because of the message.
**Note: this can take a while to write all the Issues to 1 file.**
![Image showing pipe success]('media/pipe_file.png')

Select option E: Issue Lifecycle Statistics. Here, we can see the avergage, median,
min, and max times it takes for an Issue to be closed from opening.
![Image showing stats success]('media/token_success.png')
