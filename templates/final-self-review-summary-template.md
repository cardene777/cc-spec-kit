# Self Review Summary - All Phases

**Date**: {YYYY-MM-DD HH:MM:SS}
**Agent**: {AI Agent Name}
**Phases Completed**: {Phase 1, Phase 2, Phase 3, ...}

---

## Overall Summary

| Item               | Value        |
| ------------------ | ------------ |
| Total Phases       | {phase_count} |
| Total Tasks        | {total}      |
| TDD Complete       | {total} / {total} (100%) |
| Self Review PASS   | {pass_count} / {total} ({percent}%) |
| Self Review FAIL   | {fail_count} / {total} ({percent}%) |
| Overall Status     | **{✓ PASS / ✗ FAIL}** |

### Issues by Severity (All Phases)

| Severity | Count       |
| -------- | ----------- |
| Critical | {total_critical} |
| High     | {total_high}     |
| Medium   | {total_medium}   |
| Low      | {total_low}      |

---

## Phase Breakdown

| Phase   | Tasks | PASS | FAIL | Status |
| ------- | ----- | ---- | ---- | ------ |
| Phase 1 | {count} | {pass} | {fail} | {✓/✗} |
| Phase 2 | {count} | {pass} | {fail} | {✓/✗} |
| Phase 3 | {count} | {pass} | {fail} | {✓/✗} |
...

Detailed phase reports:
- Phase 1: `reports/self-review/self-review-phase-1.md`
- Phase 2: `reports/self-review/self-review-phase-2.md`
- Phase 3: `reports/self-review/self-review-phase-3.md`
...

---

## Failed Tasks Summary (if any)

| Task ID | Phase | Type | Score | Issues | Description |
| ------- | ----- | ---- | ----- | ------ | ----------- |
| {ID}    | {phase} | {type} | {score}/100 | {count} | {brief_desc} |

(List all tasks with Self Review FAIL across all phases)

For detailed issue information, see individual phase reports above.

---

## Success Metrics

- **Task Completion Rate**: {total - fail_count} / {total} ({percent}%)
- **Self Review Pass Rate**: {pass_count} / {total} ({percent}%)
- **Average Score**: {avg_score}/100
- **Critical Issues**: {critical_count} (target: 0)
- **High Issues**: {high_count} (target: 0)

---

## Next Steps

**{If any failed tasks}**:
1. Review failed tasks in tasks.md
2. Review detailed issues in phase reports: `reports/self-review/self-review-phase-*.md`
3. Run `/grove.review` for cross-review by another AI agent
4. After cross-review, run `/grove.fix` to address identified issues
5. Priority: Address Critical and High severity issues first

**{If all passed}**:
- ✓ All {total} tasks passed Self Review
- ✓ Implementation quality verified
- Next: Consider running `/grove.review` for additional cross-review
- Ready for: Integration testing, deployment, or next feature

---

## Implementation Timeline

- Feature implementation started: {start_timestamp}
- Feature implementation completed: {end_timestamp}
- Total implementation time: {duration}
- Average time per task: {avg_time}
- Phases completed: {phase_count}

---

## Quality Indicators

**Strengths** (if all or most tasks passed):
- ✓ Specification compliance maintained
- ✓ Tech stack adherence verified
- ✓ Test coverage adequate
- ✓ Code quality standards met

**Areas for Improvement** (if failures exist):
- ⚠️ {fail_count} tasks require attention
- ⚠️ {critical_count + high_count} high-priority issues
- ⚠️ Review phase reports for specific improvements
