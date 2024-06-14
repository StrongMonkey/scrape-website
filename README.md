# Scrape-website 

scrape-website is a python tool that scrapes all html files from a web

# Guide

Run the following command to scrape HTMLs from a website. You need to have python installed.

```commandline
python -m venv venv

source venv/bin/activate

pip install -r requirements.txt
 
# This command will scrape all html files from https://reefresilience.org/ into folder reefresilience. Takes up about 10 minutes.
python main.py https://reefresilience.org/ reefresilience

```

Run with knowledge tool to serve as a knowledge base

```commandline
# This will install the latest release from the knowledge repo and put it into /usr/local/bin
curl -sLf https://raw.githubusercontent.com/gptscript-ai/knowledge/main/install.sh | sudo sh -

# To create a knowledge base, we will need the OPENAI_API_KEY
export OPENAI_API_KEY="YOUR_API_KEY"

# Create a dataset with a name
knowledge create dataset dataset1

# Ingest all the html files
knowledge ingest -r -d dataset1 ./reefresilience

gptscript --ui ./query.gpt
```