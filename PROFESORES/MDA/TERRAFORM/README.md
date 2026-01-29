# Creating a GitHub Repository Using `gh` CLI on macOS

This guide walks you through installing the GitHub CLI (`gh`), authenticating, creating a new repository, **and** generating a Personal Access Token (PAT) for use with Terraform or other CLI tools.

---

## 1. Install GitHub CLI

Open Terminal and run:

```sh
brew install gh
```

---

## 2. Authenticate with GitHub

Authenticate the CLI tool with your GitHub account:

```sh
gh auth login
```

- Select **GitHub.com**
- Choose **HTTPS** for authentication
- Follow the prompts to authenticate in your web browser

---

## 3. Create a New Repository

Navigate to or create a folder for your project:

```sh
mkdir my-new-repo
cd my-new-repo
```

(Optional): Initialize a new git repository and add a README:

```sh
git init
echo "# My Project" > README.md
git add README.md
git commit -m "Initial commit"
```

Create a repository on GitHub and push your code:

```sh
gh repo create my-new-repo --public --source=. --remote=origin --push
```

- Select public or private as needed.

---

## 4. View Your Repository in the Browser

```sh
gh repo view my-new-repo --web
```

---

## 5. (Optional) Create a GitHub Personal Access Token (PAT)

If you want to use Terraform (or other tools) to access GitHub via API, you need a Personal Access Token (PAT). Follow these steps:

### a. Generate a GitHub Token

1. Go to [https://github.com/settings/tokens](https://github.com/settings/tokens)
2. Click **"Generate new token"** (classic) or **"Fine-grained token"** if using the newer version.
3. Enter a **name**, and select **expiration** (choose "No expiration" for long-term use).
4. **Select scopes/permissions:**  
   - For Terraform, you typically need:
     - `repo` (Full control of private repositories)
     - `admin:repo_hook`
     - `delete_repo` (if needed)
     - `workflow` (if using actions)
     - (Adjust based on your needs)
5. Click **"Generate token"**.
6. **Copy the generated token once displayed**. You will not be able to retrieve it again.

### b. Set the Token as an Environment Variable

In your terminal, run:

```sh
export GITHUB_TOKEN=your_generated_token_here
```

You can add this line to your `~/.zshrc`, `~/.bash_profile`, or `~/.bashrc` to persist it:

```sh
echo 'export GITHUB_TOKEN=your_generated_token_here' >> ~/.zshrc
# Or use ~/.bash_profile or ~/.bashrc for other shells
```

Reload your shell config (if you added it):

```sh
source ~/.zshrc
```

---

## 6. (Optional) Use the Token with Terraform

Terraform and many other CLI tools will automatically use the `GITHUB_TOKEN` environment variable for authentication.  
You do **not** need to put the token in your Terraform code.

Example in a Terraform provider configuration:

```hcl
provider "github" {
  token = var.github_token  # Or rely on the GITHUB_TOKEN environment variable
  owner = "your_github_username"
}
```
If `token` is not specified, Terraform will use the `GITHUB_TOKEN` environment variable by default.

---

You’re done! You have installed `gh`, authenticated, created a repository, **and** set up a GitHub token for Terraform or API access.
