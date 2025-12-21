# Task Verification Template

Use this template to verify each task item during Self Review in non-Claude Code environments.

## Verification Workflow (per task item)

### Step 1: Read Task Context

1. Read the task description from tasks.md
2. Identify the requirement from spec.md
3. Check the implementation approach from plan.md
4. Note the file paths mentioned in the task

### Step 2: Verification Checklist

Review the implementation against these criteria:

- [ ] **Specification Compliance**: Does it meet the requirement in spec.md?
- [ ] **Tech Stack Adherence**: Does it follow the tech stack and architecture in plan.md?
- [ ] **Task Completeness**: Is the implementation content in tasks.md completed?
- [ ] **Test Coverage**: Do tests exist and pass? (if tests are required)
- [ ] **Error Handling**: Is error handling appropriate?
- [ ] **Security**: Are there any security vulnerabilities?
- [ ] **Performance**: Are there any performance issues?
- [ ] **Code Quality**: Is the code readable and maintainable?

### Step 3: Score Calculation

Calculate a score from 0-100 based on issues found:

**Severity Levels**:
- **Critical**: Specification violation preventing system from working / Security vulnerability / Data loss potential → -30 points each
- **High**: Specification violation preventing major features from working → -20 points each
- **Medium**: Specification violation but features work / Performance issues → -10 points each
- **Low**: Minor issues not in spec / Code style violations → -5 points each

**Scoring**:
- Start with 100 points
- Subtract points for each issue
- Minimum score: 0

### Step 4: Result Determination

- **Score ≥ 80**: PASS → Mark "Self Review" as `[x]` with ✓
- **Score < 80**: FAIL → Attempt to fix (up to 3 iterations)

### Step 5: Issue Report Format

If issues are found, document them using this format:

```markdown
#### Issue {N}

| Item     | Details        |
| -------- | -------------- |
| Severity | {Critical/High/Medium/Low} |
| Location | `{file:line}`  |

- **Description**
  {what is wrong}

- **Cause**
  {why it's wrong}

- **Recommended Fix**
  ```
  {fix code}
  ```

- **Evidence**
  ```
  {actual code snippet from file:line}
  ```
```

## Output Template

After verification, create a summary for the task:

```markdown
### Task {ID} Verification

**Score**: {score}/100
**Status**: {PASS/FAIL}
**Issues Found**: {count}

{If FAIL, include Issue reports here}
```

## Notes

- Focus on specification compliance first
- Evidence must include file:line references
- Be objective and specific in descriptions
- Recommended fixes should be actionable code snippets
