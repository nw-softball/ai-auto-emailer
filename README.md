# ai-auto-emailer

## Scope

This is an example helper email to send conference sponsorship emails to prospective sponsors for an event. This can be edited for
your event easily with some changes around the HTML email and the "template email."

This is designed to help community driven events to ask for money from companies, this will **save hours of work** for community volunteers.

## Configuration and setup

### PreSteps

Have [ollama][ollama] and python installed.

#### AI Model Setup

1. Download your preferred model, if you don't already have it on your machine, for instance `granite3.2`:
```bash
ollama pull granite3.2
```

  - You can find a list of available models [here](https://ollama.com/library)


2. List available models:
```bash
ollama list
```

3. Have `ollama` running (either from application or cli)
```bash
ollama serve
```

### Clone and Setup

1. Clone and set up the working space.
```bash
git clone https://github.com/jjasghar/ai-auto-emailer.git
cd ai-auto-emailer
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Copy the `config.toml.example` and edit the `config.toml` in a text editor of your choice (`nano`, `vim`, `VSCode`, etc).
```bash
cp config.toml.example config.toml
vim config.toml
```
  - NOTE: the `EMAIL_TEMPLATE` is the email that you want the LLM to take inspiration from.
  - NOTE: make sure you update the `OLLAMA_AI_MODEL` to the specific model you're using.

1. Copy the `names.csv.example` to `names.csv` and edit the list you want to use
```bash
vim names.csv # might I suggest just your name only to start out with.
```

1. Run a test run. NOTE: use `DEBUG=True` before `python main.py` to get DEBUG
   output in the `log/main_logging.log`.
```bash
DEBUG=True python main.py
SMTP password: super_secret_p@ssw0rd!
>>>> email sent to billy@example.com <<<<<
>>>> email sent to mark@example.com <<<<<
>>>> email sent to YOUREMAIL@gmail.com <<<<<
This took 0:01:35.220344 to run
```

1. Verify in your inbox
2. If you like it, change the `names.csv` to the people you want to start emailing.

## Using Gmail as your SMTP server

Set the following settings for `Gmail` to work.
```
SMTP_SERVER="smtp.gmail.com"
SMTP_PORT=465
SMTP_SENDER_EMAIL="YOUREMAIL@gmail.com"
```
The password for `SMTP_PASSWORD` will need to be your Gmail password, but if
you have "[Application Password](https://myaccount.google.com/apppasswords)"
you'll need to create a password for this application.

## License & Authors

If you would like to see the detailed LICENSE click [here](./LICENSE).

- Author: JJ Asghar <awesome@ibm.com>

```text
Copyright:: 2025- IBM, Inc

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

[ollama]: https://ollama.com
