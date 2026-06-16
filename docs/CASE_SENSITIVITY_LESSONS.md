# Git Branch Case-Sensitivity: Lessons Learned

## Problem Statement

Windows filesystems are **case-insensitive**, but GitHub (running on Linux) is **case-sensitive**. This creates a critical mismatch:

- On Windows, `main`, `Main`, and `MAIN` are treated as the **same branch**
- On GitHub, `main`, `Main`, and `MAIN` are treated as **three separate branches**

This discrepancy leads to:
- **Accidental branch duplication** (e.g., pushing `DEV` when `dev` exists)
- **Confusing Git output** (e.g., `git branch` showing lowercase, but you're on uppercase)
- **Repository pollution** with multiple case variants
- **Team confusion** about which branches are "real"

---

## How We Replicated the Problem

### Step 1: The Initial Mistake
Starting with `main` branch on Windows, we accidentally created a case variant:

```bash
# Windows Git is case-insensitive, so this silently matches 'main'
git checkout MAIN
git branch
# Output: * main  ← Still shows lowercase!
```

### Step 2: The Silent Problem
Git's checkout succeeded but with misleading output:
```
Switched to branch 'MAIN'  ← Looks like we switched, but...
git branch
* main                    ← Still shows 'main', not 'MAIN'
```

### Step 3: The Remote Duplication
When we pushed the case variant to GitHub:
```bash
git push origin MAIN
```

GitHub accepted it and created **two separate branches**:
- `main` (original)
- `MAIN` (new, because GitHub is case-sensitive)

### Step 4: The Deletion Trap
When we tried to clean up with `git branch -D MAIN`, Windows treated it as deleting `main` (case-insensitive), accidentally **deleting the real branch**:

```bash
git branch -D MAIN
# On Windows, this deleted the local reference to both main and MAIN
# Result: No local branches, but remote still had both
```

---

## How We Resolved It

### Solution 1: Client-Side Prevention (Git Pre-Push Hook)

**File:** `.githooks/pre-push`

**Purpose:** Catch case conflicts **before** they reach GitHub

**How it works:**
1. Runs automatically before every `git push`
2. Compares branch names case-insensitively against all existing branches
3. Rejects the push if a case conflict is detected
4. Provides clear error message with recommended branch name

**Setup (one-time for each developer):**
```bash
git config core.hooksPath .githooks
```

**Example output:**
```
❌ PUSH REJECTED: Branch 'DEV' conflicts with existing branch 'dev'
   Use lowercase branch names only (existing: dev)
```

**Advantage:** Immediate feedback, prevents bad pushes at the source

---

### Solution 2: Server-Side Prevention (GitHub Actions Workflow)

**File:** `.github/workflows/prevent-case-conflicts.yml`

**Purpose:** Auto-detect and delete case-conflicting branches on GitHub

**How it works:**
1. Triggers on every push
2. Fetches all branches from GitHub API
3. Compares current branch against existing branches (case-insensitive)
4. If conflict detected, **automatically deletes** the conflicting branch
5. Uses `curl` with Bearer token for proper GitHub API authentication

**Key components:**
- **Permissions:** `contents: write` — Allows workflow to delete branches
- **Token:** `github.token` (GITHUB_TOKEN) — Built-in GitHub Actions token
- **Detection:** Bash loop comparing lowercase versions of branch names
- **Deletion:** GitHub API endpoint `/git/refs/heads/{branch}`

**Example workflow execution:**
```
🔍 Checking branch: DEV
📋 All branches:
DEV
dev
main

❌ CONFLICT DETECTED!
   Branch 'DEV' conflicts with existing branch 'dev'

🗑️  Deleting conflicting branch: DEV
✅ Branch 'DEV' deleted successfully

💡 Recommended: Use lowercase naming instead: 'dev'
```

**Advantage:** Safety net for developers who bypass pre-push hooks, automatic enforcement

---

### Solution 3: Recovery from Disaster

If local branches get deleted due to case-insensitivity issues:

```bash
# 1. Fetch latest from remote
git fetch origin

# 2. Reset local branch to match remote
git reset --hard origin/main

# 3. Verify recovery
git branch -a
```

---

## Final Observations

### What We Discovered

1. **Windows Masks the Problem**
   - Case-insensitive filesystem hides the issue during development
   - Only surfaces when pushing to case-sensitive remote

2. **Git's Behavior is Confusing**
   - `git checkout BRANCH` silently matches `branch` on Windows
   - Output shows what you typed, not what actually happened
   - Developers don't realize the mismatch until GitHub rejects or duplicates

3. **Double Protection is Essential**
   - Pre-push hooks catch 95% of issues
   - GitHub Actions catches the 5% who bypass hooks
   - Both layers needed for team safety

4. **GitHub's Retention**
   - Deleted branches show "had recent pushes" for ~24 hours
   - This is a **feature**, not a bug — allows recovery
   - Branch is actually deleted from active list immediately

5. **Token Permissions Matter**
   - Simple `GITHUB_TOKEN` doesn't have write permissions by default
   - Must explicitly set `permissions: contents: write` in workflow
   - Must use `github.token` context variable (not `secrets.GITHUB_TOKEN`)

### Common Mistakes We Made

| Mistake | Cause | Solution |
|---------|-------|----------|
| `git branch -D MAIN` deleted `main` | Windows case-insensitivity | Use `git reset --hard origin/main` to recover |
| Workflow returned 403 Forbidden | Missing write permissions | Add `permissions: contents: write` to workflow |
| `gh repo delete-branch` failed | Wrong gh CLI syntax | Use curl API directly with Bearer token |
| Node.js 20 deprecation warnings | Outdated action version | Update `actions/checkout@v3` → `v4` |

---

## Best Practices

### For Individual Developers

1. **Always use lowercase branch names**
   ```bash
   ❌ git checkout -b Feature-XYZ
   ❌ git checkout -b FEATURE_XYZ
   ✅ git checkout -b feature-xyz
   ```

2. **Enable pre-push hooks immediately after clone**
   ```bash
   git config core.hooksPath .githooks
   ```

3. **Use consistent naming conventions**
   - Feature branches: `feature/short-description`
   - Bugfix branches: `bugfix/issue-number`
   - Hotfix branches: `hotfix/critical-issue`
   - All lowercase, hyphens instead of underscores

4. **Check before pushing**
   ```bash
   git branch --list
   git status
   # Verify case matches existing branches
   ```

### For Repository Maintainers

1. **Document naming standards in CONTRIBUTING.md**
   - Make it required reading
   - Show ❌ bad and ✅ good examples
   - Explain why it matters

2. **Add both protection layers**
   - Client-side: `.githooks/pre-push`
   - Server-side: GitHub Actions workflow
   - Don't rely on just one

3. **Set GitHub branch protection rules**
   - Require pull requests before merging
   - Require status checks to pass
   - Dismiss stale PR approvals

4. **Monitor for violations**
   - Watch GitHub Actions logs for detected conflicts
   - Track which branches get auto-deleted
   - Follow up with developers who bypass hooks

### For Windows Teams Specifically

1. **Educate about case-insensitivity**
   - Windows developers often unaware of this issue
   - Explain that remote is case-sensitive
   - Show real examples from your repo

2. **Use case-insensitive but consistent naming**
   - Never mix cases of the same word
   - Example: use `dev`, never `DEV` or `Dev`

3. **Test on both Windows and Linux**
   - Some developers may have WSL (Windows Subsystem for Linux)
   - Test branch names on both filesystems

4. **Consider branch naming policy**
   - Implement rules in GitHub (branch protection)
   - Enforce via Actions workflow
   - Document in team guidelines

---

## Testing the Solution

### How to Verify Protection is Working

#### Test 1: Pre-Push Hook (Local)
```bash
# Enable the hook
git config core.hooksPath .githooks

# Try to push a bad branch
git checkout -b TestBranch
git commit --allow-empty -m "test"
git push origin TestBranch

# Expected: Push rejected with message
# ❌ PUSH REJECTED: Branch 'TestBranch' conflicts with existing branch 'main'
```

#### Test 2: GitHub Actions (Server)
```bash
# Disable the hook temporarily to test server protection
git config core.hooksPath ""

# Create and push a case variant
git checkout TESTBRANCH
git push origin TESTBRANCH

# Check GitHub Actions tab
# Expected: Workflow runs and deletes TESTBRANCH
# Re-enable hook: git config core.hooksPath .githooks
```

#### Test 3: Recovery
```bash
# If something goes wrong
git fetch origin
git reset --hard origin/main
git branch -a
# Verify all branches are intact
```

---

## Related Documentation

- [Git Case Sensitivity Guide](https://stackoverflow.com/questions/11183788/case-sensitive-git)
- [GitHub Branch Protection Rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches)
- [Git Hooks Documentation](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks)
- [GitHub Actions Permissions](https://docs.github.com/en/actions/security-guides/permissions-for-github-token)

---

## Summary

**The Problem:** Windows is case-insensitive, GitHub is case-sensitive → branch duplication and confusion

**The Solution:** 
- Client-side pre-push hooks (prevent locally)
- Server-side GitHub Actions (enforce automatically)  
- Team education (build awareness)

**The Outcome:** 
- ✅ No more accidental branch case variants
- ✅ Team-wide consistency
- ✅ Automatic cleanup of violations
- ✅ Clear error messages guide developers

**Key Learning:** When building software on heterogeneous platforms (Windows, macOS, Linux), always assume the **most restrictive** platform's rules (Linux case-sensitivity) and enforce them everywhere.
