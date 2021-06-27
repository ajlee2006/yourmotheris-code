# yourmotheris-code

## My settings
I am running this on Heroku with the Heroku Schedular add-on to run `python3 main.py` hourly at :0. In addition, the following config vars must be set: `API_KEY` for wordsapi, `GITHUB_TOKEN` to access and edit the [yourmotheris-data](https://github.com/ajlee2006/yourmotheris-data) repo (you will need to change references to the repo in the code if you are doing this yourself), `TWYTHON_A`, `B`, `C`, and `D` (four keys necessary for Twython), and `WEBHOOK` URL to post the data into a Discord channel.
