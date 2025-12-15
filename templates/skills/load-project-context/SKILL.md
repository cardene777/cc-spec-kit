---
name: load-project-context
description: Load existing project structure and conventions from .specify/docs/. This skill should be used when creating feature specifications, planning implementations, or implementing features to ensure consistency with existing architecture and patterns.
---

# Load Project Context

## Purpose

This skill loads project context from `.specify/docs/` to understand existing patterns and conventions, preventing context pollution by loading documentation only when explicitly needed.

## Instructions

When creating new features or implementations, follow these steps:

1. **Check for existing documentation**
   - Look for `.specify/docs/` directory in the project root
   - Verify documentation exists before proceeding

2. **Load project structure**
   - Read `.specify/docs/*/index.md` files to understand directory structures
   - Read `.specify/docs/*/README.md` files for architecture overviews

3. **Extract patterns and conventions**
   - Identify naming conventions used in the project
   - Recognize architectural patterns (MVC, microservices, etc.)
   - Understand code organization and file structure

4. **Apply to new implementations**
   - Ensure new code follows existing naming conventions
   - Maintain architectural consistency
   - Follow established patterns for similar features

## When to Use This Skill

This skill is automatically invoked by:
- `/speckit.specify` - When creating feature specifications
- `/speckit.plan` - When planning implementation
- `/speckit.implement` - When implementing features
- `/speckit.tasks` - When breaking down tasks

You can also invoke it manually when you need to understand the project structure before making changes.

## What This Skill Does

### 1. Read Project Documentation
- Loads `.specify/docs/*/index.md` - Directory structures and file organization
- Loads `.specify/docs/*/README.md` - Architecture overviews and design decisions

### 2. Extract Existing Patterns
- Identifies naming conventions (camelCase, snake_case, PascalCase)
- Recognizes architectural patterns (layered, hexagonal, etc.)
- Understands code organization (feature-based, layer-based, etc.)

### 3. Guide New Implementations
- Ensures consistency with existing codebase
- Suggests following established patterns
- Maintains architectural coherence across features

## Benefits

- **No automatic loading**: `.specify/docs/` is excluded from auto-read, preventing context pollution
- **On-demand context**: Load project information only when needed
- **Scalable**: Works efficiently even for large projects with extensive documentation
- **Consistent implementations**: Ensures all features follow the same patterns and conventions

## Documentation Structure

The skill expects documentation in this structure:

```
.specify/
└── docs/
    └── src/  (or app/, lib/, core/, etc.)
        ├── index.md      # Directory overview
        ├── README.md     # Architecture overview
        └── components/
            ├── index.md  # Component directory overview
            ├── README.md # Component architecture
            └── ...
```

## Best Practices

1. **Keep documentation up-to-date**: Use `specify-ex sync` regularly to update `.specify/docs/`
2. **Document patterns explicitly**: Include clear examples of naming conventions and architectural patterns in README.md files
3. **Read before implementing**: Always load project context before starting new feature work
4. **Verify consistency**: After implementation, verify that new code follows loaded patterns

## Notes

- This skill is read-only and does NOT modify any files
- It only reads and analyzes existing documentation
- Documentation should be synchronized with source code using the `specify-ex sync` command
- Works best when `.specify/docs/` is regularly maintained and updated
