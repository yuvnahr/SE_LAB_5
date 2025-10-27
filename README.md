# Lab 5 — Static Code Analysis README

This project applies Python static analysis using Pylint, Bandit, and Flake8 to identify and fix security, correctness, and style issues in inventory_system.py, with a prioritized focus on high and medium severity findings first. The final state shows a clean Bandit run, a high Pylint score, and remaining Flake8 long-line items for wrapping or configuration as noted below.[12][13][14][11]

### Reports summary

- Bandit: No issues identified across all severities after removing eval and replacing unsafe error handling, confirming the security surface is clean in the updated code.[13]
- Pylint: Overall score 9.83/10 with one remaining W0603 global-statement note, which is an acceptable tradeoff for a small module but can be eliminated by encapsulating state in a class.[12]
- Flake8: Remaining E501 long lines indicate lines exceeding the default 79-character limit, which can be wrapped or configured via a project rule such as max-line-length in .flake8.[14]

### Known issues fixed (prioritized)

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| eval() usage | Security | 59 | eval() executes arbitrary code; major security risk (Bandit B307) [11][15] | Remove eval() line entirely [11] |
| Bare except | Security/Style | 19 | No exception type specified; silently catches all errors [11][15] | Replace with explicit logic or specific exception handling (e.g., KeyError) [11] |
| File not closed properly | Bug/Resource leak | 28, 33, 37, 42 | Files opened without context manager; risk of leaks on exceptions [11] | Use with open(...) and explicit encoding for robust I/O [11] |
| Mutable default arg | Bug | 10 | logs=[] shared across calls causes state retention across invocations [11] | Default to None and initialize logs inside function [11] |
| Invalid type handling | Bug | 53, 54 | main() passed invalid types without checks, risking runtime errors [11] | Add strict input validation and raise ValueError on bad inputs [11] |
| No input validation | Bug | 10, 15 | Functions accepted any type; latent errors possible [11] | Add isinstance checks and reject invalid values with clear errors [11] |
| Global variable modification | Code smell | 29 | Direct global mutation hurts testability and clarity [11] | Constrain mutations via function API; consider class encapsulation [11] |
| Old-style string formatting | Style | 12 | Used % formatting; less readable and consistent than f-strings [11] | Convert to f-strings for clarity and consistency [11] |
| Function names not snake_case | Style | 8, 14, 22, 25, 31, 36 | camelCase violated PEP 8 naming conventions [11] | Rename to snake_case (add_item, remove_item, get_qty, load_data, save_data, print_data, check_low_items) [11] |
| Expected 2 blank lines | Style | 8, 14, 22, 25, 31, 36, 41, 48, 61 | Missing required spacing between top-level definitions [11] | Ensure two blank lines between functions and at EOF [11] |
| Missing final newline | Style | 61 | File lacked terminating newline [11] | Add newline at end of file [11] |
| Missing module docstring | Documentation | 1 | No top-level description of module purpose [11] | Add concise module docstring [11] |
| Missing function docstrings | Documentation | 8, 14, 22, 25, 31, 36, 41, 48 | No per-function documentation [11] | Add docstrings summarizing behavior, parameters, and returns [11] |

### Reflection

- Which issues were the easiest to fix, and which were the hardest, and why?  
  The easiest were mechanical hygiene items such as removing the unused import, adding the missing newline, converting to f-strings, and inserting required blank lines because they are local, behavior-preserving changes with immediate linter feedback.[11][14][12]
  The hardest were security and correctness changes—removing eval, replacing bare except with explicit handling, adding strict validation, and repairing file I/O—because they required rethinking control flow and function contracts while keeping behavior intact and ensuring security tools and linters agree on the fixes.[13][11][12]

- Did the static analysis tools report any false positives?  
  No Bandit false positives were observed in the final run; it reported zero issues across all severities, indicating that prior risky patterns have been fully eliminated.[13]
  The remaining Pylint global-statement note reflects a design preference rather than a defect for a small, single-module script and can be eliminated by moving state to a class if desired, so it is better categorized as a warning to consider rather than a false positive.[12]

- How would static analysis be integrated into the workflow?  
  Treat Bandit as a security gate in CI, failing the pipeline on any new finding to preserve the current zero-issue baseline established by the latest scan.[13]
  Add thresholds for Pylint (for example, fail if score < 9.5/10) and keep Flake8 as a style gate, resolving or configuring long lines with a repo-level rule to avoid recurring E501 noise while maintaining consistent readability.[14][12]

- Tangible improvements in quality, readability, or robustness after fixes  
  Security posture improved substantially by eliminating code execution risks and masked errors, validated by Bandit’s clean report with zero findings after the fixes.[13]
  Robustness and maintainability improved via safe file I/O, explicit validation, clear naming, and documentation, reflected in the elevated Pylint score and clearer, more uniform code structure for future changes and reviews.[11][12]

### Notes on current state

- Security: Clean baseline maintained with Bandit reporting zero issues, suitable for enforcing as a hard CI gate.[13]
- Quality: High Pylint score suggests strong readability and maintainability; consider removing remaining global usage in a future refactor if desired.[12]
- Style: Wrap or configure long lines to eliminate E501 while balancing readability and team conventions going forward.[14]
s/attachments/82600393/7e65e123-42c9-4da5-b459-1fc2d87ca9d6/bandit_report.txt)
