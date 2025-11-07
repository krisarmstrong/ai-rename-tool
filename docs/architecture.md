# Architecture

## Overview

AI Rename Tool is a Python 3.14+ command-line utility for safely renaming files using deterministic suggestions. The architecture emphasizes a functions-first design with a clean plan → apply → undo workflow.

## System Design

### Core Components

1. **Naming Module** (`ai_rename_tool.naming`)
   - Filename sanitization and validation
   - Category determination logic
   - Name quality assessment

2. **Provider System** (`ai_rename_tool.provider`)
   - Local heuristic-based naming suggestions
   - Pluggable AI provider interface
   - Deterministic suggestion generation

3. **Core Planning Engine** (`ai_rename_tool.core`)
   - File scanning with hidden file filtering
   - Rename plan generation with conflict resolution
   - Plan serialization (JSON/CSV formats)
   - Apply and undo operations

4. **CLI Interface** (`ai_rename_tool.cli`)
   - Command-line argument parsing
   - User workflow orchestration
   - Progress reporting and error handling

### Data Flow

```
User Input (CLI args)
    ↓
File Scanning (scan_paths)
    ↓
Suggestion Generation (provider)
    ↓
Plan Building (build_plan)
    ↓
Conflict Resolution (_resolve_conflict)
    ↓
Plan Serialization (JSON/CSV)
    ↓
Apply/Undo Operations
```

## Module Dependencies

### External Libraries
- **Python 3.14+**: Latest Python features and performance
- **pathlib**: Modern path handling (Python stdlib)
- **json**: Plan serialization (Python stdlib)
- **csv**: CSV export support (Python stdlib)
- **dataclasses**: Immutable data structures (Python stdlib)

### Internal Modules
- **src/ai_rename_tool/core.py**: Core planning and execution logic
- **src/ai_rename_tool/naming.py**: Filename validation and categorization
- **src/ai_rename_tool/provider.py**: Suggestion provider interface
- **src/ai_rename_tool/cli.py**: Command-line interface

## Core Data Structures

### PlanItem

```python
@dataclass(frozen=True)
class PlanItem:
    src: Path  # Source file path
    dst: Path  # Destination file path
```

Immutable data class representing a single rename operation. Frozen ensures plan integrity.

## Provider System

The provider system is pluggable and extensible:

```python
ProviderFn = Callable[[Sequence[Path]], Sequence[str]]
```

**Local Heuristic Provider:**
- Deterministic filename suggestions
- No network dependency
- Based on file extension and naming patterns

**Future AI Provider:**
- Network-based intelligent naming
- Context-aware suggestions
- Pluggable through same interface

## Conflict Resolution

The system handles naming conflicts automatically:

1. **Detection**: Checks if target path exists or is already used in plan
2. **Resolution**: Appends `_1`, `_2`, etc. to filename stem
3. **Limit**: Attempts up to 10,000 variations before failing

## Plan Workflow

### 1. Dry-Run (Plan Generation)
- Scans files in target directory
- Generates suggestions via provider
- Builds rename plan with conflict resolution
- Saves plan to JSON/CSV for review

### 2. Apply
- Reads plan from JSON file
- Creates destination directories as needed
- Executes renames atomically using `Path.replace()`

### 3. Undo
- Reads original plan from JSON
- Reverses operations in reverse order
- Restores original file paths

## Type System

Full Python 3.14+ type annotations:

- `Path`: pathlib.Path for all file system operations
- `Sequence[T]`: Immutable sequences for function parameters
- `list[T]`: Mutable lists for internal operations
- `set[Path]`: Conflict tracking
- `ProviderFn`: Type alias for provider functions

## Error Handling

**Validation Errors:**
- Provider suggestion count mismatch
- Invalid plan JSON format
- File operation failures

**Conflict Resolution:**
- Automatic handling up to 10,000 attempts
- RuntimeError if unable to resolve unique name

## File Operations

All file operations use `pathlib.Path` methods:
- `Path.rglob()`: Recursive file scanning
- `Path.exists()`: File existence checks
- `Path.replace()`: Atomic rename operations
- `Path.mkdir(parents=True, exist_ok=True)`: Safe directory creation

## Version Management

- Semantic Versioning (MAJOR.MINOR.PATCH)
- Git tag-based versioning (`vMAJOR.MINOR.PATCH`)
- `setuptools-scm` reads version from Git tags
- `__version__` exposed from package

## Security Considerations

- Hidden files excluded by default (configurable)
- No credential storage or network operations (local provider)
- Atomic file operations prevent partial state
- Plan files enable audit trails and rollback

## Testing Strategy

- **Unit Tests**: Individual function testing with pytest
- **Coverage**: High coverage requirement (>80%)
- **Dry-Run Safety**: All operations planned before execution
- **Undo Capability**: Every apply can be undone

---

Author: Kris Armstrong
