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

### Example

1. Run the script via `python3 CLIScrapeWC.py` (or whatever is compatible with your Python version)
2. It will then ask you for your GitHub token. Paste it (**no spaces**!).
3. It successfully fetched all the GitHub Issues.

![Image showing fetch success]('https://github.com/ntrappe-msft/ScrapeWindowsContainers/blob/main/media/token_success.png')

4. Now we can select an option. I wanted to pipe all the issues to a file called `broski.txt`.
5. **This can take up to 1 or 2 minutes to finish if there are many Issues**. It was successful.

![Image showing pipe success](https://github.com/ntrappe-msft/ScrapeWindowsContainers/blob/main/media/pipe_file.png')

6. It will continue to prompt you until you exit (`a`, `ctrl + c`, or `ctrl + d`).
7. I chose option E to get statistics.
8. It was successful and shows the avergae, median, min, and max times it takes for an Issue to be closed.

![Image showing stats success]('https://github.com/ntrappe-msft/ScrapeWindowsContainers/blob/main/media/usage_stats.png')
