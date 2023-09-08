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

#### Start Up

Run the script via `python3 CLIScrapeWC.py` or `python CLIScrapeWC.py` (depends on your Python version). When asked for your GitHub token, paste it (no spaces).

<img src="/media/token_success.png" alt="showing fetch success" width="800"/>

#### Option 1

We can select whatever action we want. I chose **'C'** to pipe all the Issue data to a file called `broski.txt`. It's recommended to use a textfile. **NOTE:** This can take up to 1 or 2 minutes to process as it's length to write 400+ Issues to a file.

<img src="/media/pipe_file.png" alt="showing pipe success" width="800"/>

<img src="/media/broski.png" alt="textfile with issue" width="800"/>

#### Option 2

The script will continue to prompt us for an action. To end, enter `a` or do `ctrl + c`/`ctrl + d`. Next, we'll gather some statistics on how long Issues stay open for.

<img src="/media/usage_stats.png" alt="showing lifecycle stats success" width="800"/>

#### Option 3

Let's also find out which are the most popular images on this GitHub by using option **'F'**.

<img src="/media/image_stats.png" alt="showing usage of images" width="800"/>

#### Option 4

To see what are all the Issues we've fetched from GitHub, we can print the titles out using option **'B'**.

<img src="/media/issue_titles.png" alt="showing a snapshot of some titles" width="800"/>
