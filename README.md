# GitHub Post Data Gathering Tool

This is a Python script for gathering post data and comments from GitHub using the GitHub API. The script allows you to validate links, gather post data, and format the collected data for further analysis.

## Prerequisites

Before running the script, make sure you have the following dependencies installed:

- Python 3.x
- requests library (`pip install requests`)

## Usage

1. Clone the repository or download the script `app.py` to your local machine.
2. Navigate to the directory where the script is located.
3. Open a terminal or command prompt in that directory.
4. Install the required dependencies by running the command `pip install -r requirements.txt`.
5. Run the script using the following command: python app.py [OPTION]

Replace `[OPTION]` with one of the available options listed below.

## Options

- `-v, --validate`: Validate links by checking the number of comments on each GitHub post. Only posts with three or more comments will be considered valid. The valid links will be saved to the file `TextFiles/validLinks.txt`.
- `-g, --gather`: Gather post data and comments from the valid links saved in `TextFiles/validLinks.txt`. The data will be stored in JSON format in the `JSONFiles` directory.
- `-j, --jsonFormat`: Formats the gathered data into the needed JSON structure that is required by ConVoKit.
- `-f, --format`: Format the gathered data into a specific structure. The formatted data will be stored in the `FormattedData` directory.
- `-a, --all`: Perform all the steps: validate links, gather post data, and format the data.
- `-h, --help`: Show the help message and exit.

## File Structure

The script uses the following directory structure:

- `TextFiles`: Contains input and output text files.
  - `links.txt`: Input file that stores the GitHub post links.
  - `validLinks.txt`: Output file that stores the valid GitHub post links.
- `JSONFiles`: Stores the raw post data and comments in JSON format.
  - `<ID>`: Unique ID for each post (e.g., `Issue<USER_LOGIN><NUMBER>`).
    - `Post.json`: Raw post data.
    - `Comments.json`: Raw comment data.
- `FormattedData`: Contains the formatted data.
  - `COV<ID>`: Unique ID for each post (e.g., `COV0` for the first post).
    - `ReferenceData.txt`: Information about the post (URL and number of comments).
    - `Utterances.txt`: Formatted utterances in the following format: `ID +++$+++ Speaker ID +++$+++ Reply To +++$+++ Previous Utterance +++$+++ Time +++$+++ Body +++$+++ Positive Reactions +++ Negative Reactions`.
    - `Speakers.txt`: List of speakers with their IDs, names, and roles in the same format as above.
- `Corpuses`: Contains the data formatted into the specific JSON structure needed by ConvoKit.
  - `COR<ID>`: Unique ID for each coprus (e.g. `COR0` for the first corpus)
    - `conversations.json` : A dictionary where keys are conversation index, and values are conversational-level metadata
    - `corpus.json` : Metadata of the corpus is saved in corpus.json, as a dictionary where keys are names of the metadata, and values are the actual content of such metadata.
    - `index.json` : ConvoKit requires an index.json file that contains information about all available metadata and their expected types.
    - `speakers.json` :  The speakers.json file keeps a dictionary, where the keys are speaker names, and values are metadata associated with the speakers.
    - `utterances.jsonl` : Each utterance is stored on its own line and represented as a json object, with six mandatory fields:
      - `id`: index of the utterance

      - `speaker`: the speaker who authored the utterance

      - `conversation_id`: id of the first utterance in the conversation this utterance belongs to

      - `reply_to`: index of the utterance to which this utterance replies to (None if the utterance is not a reply)

      - `timestamp`: time of the utterance

      - `text`: textual content of the utterance

Note: The directories (`JSONFiles` and `FormattedData`) will be created automatically during the script execution.

## Authorization

The script requires an access token to authenticate with the GitHub API. The token should be provided in the `Authorization` header of the HTTP requests. Replace `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` in the script with your own access token.

Please make sure to keep your access token secure and do not share it with others.

---
