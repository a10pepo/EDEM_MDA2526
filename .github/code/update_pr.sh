#!/bin/bash

# Script to update a specific pull request branch with main
# Usage: ./update_pr.sh <PR_NUMBER>

if [ -z "$1" ]; then
    echo "Error: Please provide a PR number"
    echo "Usage: ./update_pr.sh <PR_NUMBER>"
    exit 1
fi

PR_NUMBER=$1

echo "Fetching PR #${PR_NUMBER} information..."

# Get the branch name for the PR
BRANCH_NAME=$(gh pr view $PR_NUMBER --json headRefName --jq '.headRefName')

if [ -z "$BRANCH_NAME" ]; then
    echo "Error: Could not find PR #${PR_NUMBER}"
    exit 1
fi

echo "PR #${PR_NUMBER} branch: ${BRANCH_NAME}"

# Clean up any existing git operations
echo "Cleaning up git state..."
if [ -d ".git/rebase-merge" ] || [ -d ".git/rebase-apply" ]; then
    echo "Aborting existing rebase..."
    git rebase --abort 2>/dev/null || true
fi

if [ -f ".git/MERGE_HEAD" ]; then
    echo "Aborting existing merge..."
    git merge --abort 2>/dev/null || true
fi

# Reset any uncommitted changes
echo "Resetting uncommitted changes..."
git reset --hard HEAD
git clean -fd

# Update main branch first
echo "Updating main branch..."
git checkout main
git pull origin main

# Checkout the PR branch and update it
echo "Checking out branch ${BRANCH_NAME}..."
git checkout $BRANCH_NAME

echo "Rebasing with main..."
git rebase main

if [ $? -ne 0 ]; then
    echo "Error: Rebase failed. Please resolve conflicts manually."
    exit 1
fi

echo "Pushing updates to origin..."
git push origin $BRANCH_NAME --force-with-lease

if [ $? -eq 0 ]; then
    echo "✓ Successfully updated PR #${PR_NUMBER} (${BRANCH_NAME}) with main"
else
    echo "Error: Failed to push updates"
    exit 1
fi
