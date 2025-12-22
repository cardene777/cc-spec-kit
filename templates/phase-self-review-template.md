# Phase {N} Self Review Report

**Date**: {YYYY-MM-DD HH:MM:SS}
**Agent**: {AI Agent Name from tasks.md metadata}
**Phase**: Phase {N}

---

## 1. Summary

| Item               | Value        |
| ------------------ | ------------ |
| Total Tasks        | {total}      |
| TDD Complete       | {total}      |
| Self Review PASS   | {pass_count} |
| Self Review FAIL   | {fail_count} |
| Phase Status       | **{PASS/FAIL}** |

### Issues by Severity

| Severity | Count       |
| -------- | ----------- |
| Critical | {count}     |
| High     | {count}     |
| Medium   | {count}     |
| Low      | {count}     |

---

## 2. Task Summary

| Task | Type | Score | Status | Issues | Auto-Fixed |
| ---- | ---- | ----- | ------ | ------ | ---------- |
| {task_id} | {type} | {score}/100 | {PASS/FAIL} | {count} | {count} |

(Add one row per task)

---

## 3. Detailed Task Reports

Individual task reports are available in the `reports/self-review/` directory:

| Task ID | Description | Score | Status | Report |
| ------- | ----------- | ----- | ------ | ------ |
| {task_id} | {brief_description} | {score}/100 | {PASS/FAIL} | [`task-{task_id}.md`](task-{task_id}.md) |

(Add one row per task)

**For detailed verification results, issues, and evidence, see individual task reports above.**

---

## 4. Conclusion

Phase {N} implementation and Self Review completed.

**{If all PASS}**:
- All tasks passed Self Review
- Phase ready for next stage
- Consider running `/grove.review` for cross-review by another AI agent

**{If any FAIL}**:
- {fail_count} tasks require attention
- Priority: Address Critical/High severity issues first
- Run `/grove.review` for cross-review
- After cross-review, run `/grove.fix` to address issues
