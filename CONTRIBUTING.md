## CONTRIBUTION
Hi, contributor!

Thanks for supporting this project - your contribution means a lot!
This guide will help you during the entire contribution proccess.
We are together on it!

Here I'll provide you with all necessary instructions on how to:
* 🔧 Install required tools
* ▶️ Run the application locally
* 📄 Read application outputs
* 👨‍💻 Change source code dynamically
* 🧪 Test and debug your changes
* 📝 **Name your branches propperlly**
* 📝 **Commit your updates correctly**
* 📬 Send acceptable pull requests

I recommend keeping this file open as you go through each step.
I also encourage you to copy and run any code snippets I’ve included to make your work easier.

Have fun!

### 🔧 Installing Developer Tools
#### 🐳 Docker

This application uses **Docker Compose** to run locally, which means you'll need both **Docker Engine** and **Docker Compose** installed on your system.

If you haven't installed Docker yet, follow the official installation guides:

* [Docker Desktop for Windows & macOS](https://docs.docker.com/desktop/)
* [Docker Engine for Linux](https://docs.docker.com/engine/install/)
* [Docker Compose Installation (Standalone or Plugin)](https://docs.docker.com/compose/install/)

💡 Make sure to start Docker after installation and verify it's working by running:

```bash
docker --version
docker compose version
```

#### 🤖 Commitizen (CLI tool)
In order to have your Pull Requests accepted, your commit messages must match an specific pattern.
Commitizen is a CLI automation that helps you create commit messages that fit into this pattern.

I'll explain how to use this automation later in this file.

For now, choose one of the following instructions (at your taste) to install Commitizen.

- [JavaScript's npn instructions](https://www.npmjs.com/package/commitizen)
- [Python`s pip instructions](https://commitizen-tools.github.io/commitizen/)

### ▶️ Runing the application iteractivelly
In order to access the container iteractive shell, you may choose between one of the following options:

1. **Use Docker Compose to build the images**
Open the **Docker Desktop** application.
Then open a terminal in the project root directory and execute:
```bash
docker compose up --build
```

2. **To rebuild the images, run:**
```bash
docker compose down; docker compose up --build
```
Execute interactive commands using Docker Desktop

3. **To rebuild images and db volume, run:**
```bash
docker compose down; docker volume rm cyclobot_api_db_cyclobots; docker compose up --build
```

4. **Iteractively run a single container**
On a new terminal, run the following:
```bash
docker run -p 8080:8080 -iteractive cyclobots_api_image:latest
```

1. **Accessing Docker container after running it**
On a new terminal, run the following:
```bash
docker exec -it cyclobots_api_container /bin/sh
```

### 🛠️ Reading, Updating and Debugging
Understand and manipulate the application using one (or a combination) of the following options:

1. **Reading logs**
Inside the container, all logs will be written to `/var/log/cyclobots_api`.
This directory is bound to `\logs`, outside the container.

[Tip]: If docker compose is being used, iteractive shell is not necessary.
Due to mount bindings on docker compose.yml, you should be able to read from `./cyclobots_api/logs/purePython.log` directly on your OS file system.

If you are inside the container (iteractive shell),
use the following command to read log updates in real time:
```bash
tail -f /var/log/cyclobots_api/purePython.log
```

2. **Editing files** 
If docker compose is being used, iteractive shell is not necessary.
Due to mount bindings on docker compose.yml, you should be able to update files at `./src` directly on your OS file system.

By default, the docker image does not have any editor installed.
To apply any experimental change without having to rebuild the app,
Run the iteractive shell (option 1 or 2), and then run:
```bash
apt update
apt install vim
```

3. **Debugging with logging**
No need for breakpoints or complex debugging tools.

Just use `logging.debug()` to expose application details directly in the same log file described above.

It’s the simplest and fastest way to capture specific information about the application's state at any point in time.

🚨 **DO NOT** use `logging.info()` for debugging.
Using it for temporary debug messages increases the risk of exposing sensitive or unnecessary information in external logs.

4. **Connecting to DB**
Once connected to the database container, run:
```bash
mysql -u cyclobots_api -p -h localhost -P 8080
```
(mysql -u [username] -p -h [hostname] -P [port])

### 🧪 Testing the application
Here are some options on how to test the application routes:

1. **Unit tests**
Run the iteractive shell (option 1 or 2), and then run:
```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

2. **Testing routes and methods** 
Usin **Bruno API Client**:
Bruno is a local-first, git-native and open source API Client.
No login required, no cloud dependency, unlimited (and free) requests.

Learn about the tool: https://www.usebruno.com

After installing VSCode extention,
use it to select the 'collections' directory,
then and have fun.

----
Using **Bash** or **CMD**:
```bash
curl -v -X OPTIONS http://localhost:9999/api
```

----
Using **PowerShell**, use native method:
```bash
Invoke-WebRequest -Uri http://localhost:9999/api -Method OPTIONS -Verbose -UseBasicParsing
```
or run the actual curl file:
```bash
& "C:\path\to\curl.exe" -v -X OPTIONS http://localhost:9999/api
```

----
Using **Wsl**:
```bash
sudo apt update && sudo apt install curl
curl -v -X OPTIONS http://localhost:9999/api
```

### ✅ Branch Naming Guidelines

All branch names in this project **must follow the [Conventional Branch](https://conventionalbranch.org/) specification**. This ensures consistent, readable branch history and enables automated tooling like Continuous Integration/Continuous Deployment pipelines.

#### Prefixes
- feature/ (or feat/): For new features (e.g., feature/add-login-page, feat/add-login-page)
- bugfix/ (or fix/): For bug fixes (e.g., bugfix/fix-header-bug, fix/header-bug)
- hotfix/: For urgent fixes (e.g., hotfix/security-patch)
- release/: For branches preparing a release (e.g., release/v1.2.0)
- chore/: For non-code tasks like dependency, docs updates (e.g., chore/update-dependencies)


#### Formatting Rules
- Use lowercase: Write all letters in lower case.
- Use hyphens: Separate words with a hyphen (-) instead of spaces or underscores.
- Keep it short: Limit descriptions to 3 to 5 clear words.
- No special characters.

#### Tools to adopt and enforce Conventional Branch in your project:

- commit-check: Check branch names, commit messages, and related Git metadata locally.
- commit-check-action: Validate branch names automatically in GitHub Actions.
- VSCode Conventional Branch: Create Conventional Branch names from Visual Studio Code.
- Conventional Branch Skill: Teach AI coding assistants how to create valid Conventional Branch names.



### ✅ Commit Message Guidelines

All commits in this project **must follow the [Conventional Commits](https://www.conventionalcommits.org/) specification**. This ensures consistent, readable commit history and enables automated tooling like changelogs and semantic versioning.

#### 🚫 Avoid using `git commit`

Instead, use **Commitizen** to create structured and meaningful commit messages.
Once you are very confident with commit message structure and it's options,
you may use TODO file to both log your actions and create your commit messages.

#### 🔧 Installing Commitizen
If you haven't installed it yet, please check the section "Installing Developer Tools" at the beginning of this file.

#### 📝 Using Commitizen
Once your Commitizen is installed and you have added your changes to be commited, run the following command to commit your changes:

```bash
cz commit
```

* Use the arrow keys to select the type of change you’re committing.
* Answer the prompted questions using the "Commit pattern references" bellow.
* Press `Enter` after each answer.
* Your commit will be formatted correctly and automatically checked against project rules.

> 💡 Tip: To view your previous commits, run `git log` in your terminal.


**Commit pattern reference**
Our commits follow this structure:

* **`fix:`** — Patches a bug (maps to **PATCH** in Semantic Versioning).
* **`feat:`** — Introduces a new feature (maps to **MINOR**).
* **`BREAKING CHANGE:`** — Introduces a breaking API change (maps to **MAJOR**). This can be included in any commit type using a `BREAKING CHANGE:` footer or by adding a `!` after the type/scope (e.g., `feat!:`, `refactor!:`, etc.).

Other allowed types include:

* `build:` — Changes to build system or dependencies
* `chore:` — Routine maintenance tasks
* `ci:` — Continuous integration-related changes
* `docs:` — Documentation updates
* `style:` — Code style changes (formatting, etc.)
* `refactor:` — Code changes that neither fix a bug nor add a feature
* `perf:` — Performance improvements
* `test:` — Adding or updating tests

For more details, see the [Conventional Commits documentation](https://www.conventionalcommits.org/en/v1.0.0/).


### 📬 Send acceptable pull requests
Make sure that:
1. The application runs as expected
2. Your commit messages follow the Conventional Commit guidelines
3. Your branch name follows the Conventional Branch guidelines

Then:
You’re ready to open your pull request 🥳
Thank you for contributing!