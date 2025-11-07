# API Reference

## Module: ai_rename_tool.core

### Functions

#### `scan_paths(root: Path, include_hidden: bool = False) -> list[Path]`

Recursively scan directory for files.

**Parameters:**
- `root` (Path): Root directory to scan
- `include_hidden` (bool, optional): Include hidden files/directories. Defaults to False

**Returns:**
- `list[Path]`: List of file paths found

**Example:**
```python
from pathlib import Path
from ai_rename_tool.core import scan_paths

files = scan_paths(Path("."), include_hidden=False)
print(f"Found {len(files)} files")
```

**Behavior:**
- Uses `Path.rglob("*")` for recursive scanning
- Filters out directories, keeps only files
- Skips paths with parts starting with `.` unless `include_hidden=True`

---

#### `build_plan(root: Path, files: Sequence[Path], provider: ProviderFn = local_heuristic_provider, categorise: bool = False) -> list[PlanItem]`

Generate rename plan for files using provider suggestions.

**Parameters:**
- `root` (Path): Root directory for relative path resolution
- `files` (Sequence[Path]): Files to generate rename plan for
- `provider` (ProviderFn, optional): Suggestion provider function. Defaults to local_heuristic_provider
- `categorise` (bool, optional): Organize files into category subdirectories. Defaults to False

**Returns:**
- `list[PlanItem]`: List of rename operations (src → dst)

**Raises:**
- `ValueError`: If provider returns mismatched number of suggestions
- `RuntimeError`: If unable to resolve unique filename after 10k attempts

**Example:**
```python
from pathlib import Path
from ai_rename_tool.core import scan_paths, build_plan

root = Path(".")
files = scan_paths(root)
plan = build_plan(root, files, categorise=True)
print(f"Generated {len(plan)} rename operations")
```

**Behavior:**
1. Calls provider to get suggestions for all files
2. Sanitizes each suggestion
3. Falls back to original filename if suggestion is invalid
4. Resolves naming conflicts with `_1`, `_2`, etc.
5. Creates category subdirectories if `categorise=True`

---

#### `write_plan_json(plan: Sequence[PlanItem], path: Path) -> None`

Save rename plan to JSON file.

**Parameters:**
- `plan` (Sequence[PlanItem]): Rename plan to save
- `path` (Path): Output JSON file path

**Returns:**
- None

**Example:**
```python
from pathlib import Path
from ai_rename_tool.core import write_plan_json

write_plan_json(plan, Path("rename_plan.json"))
```

**JSON Format:**
```json
[
  {
    "src": "/path/to/source.txt",
    "dst": "/path/to/destination.txt"
  }
]
```

---

#### `write_plan_csv(plan: Sequence[PlanItem], path: Path) -> None`

Save rename plan to CSV file.

**Parameters:**
- `plan` (Sequence[PlanItem]): Rename plan to save
- `path` (Path): Output CSV file path

**Returns:**
- None

**Example:**
```python
from pathlib import Path
from ai_rename_tool.core import write_plan_csv

write_plan_csv(plan, Path("rename_plan.csv"))
```

**CSV Format:**
```csv
src,dst
/path/to/source.txt,/path/to/destination.txt
```

---

#### `read_plan_json(path: Path) -> list[PlanItem]`

Load rename plan from JSON file.

**Parameters:**
- `path` (Path): JSON file path to read

**Returns:**
- `list[PlanItem]`: Loaded rename plan

**Raises:**
- `json.JSONDecodeError`: If file contains invalid JSON
- `FileNotFoundError`: If file doesn't exist

**Example:**
```python
from pathlib import Path
from ai_rename_tool.core import read_plan_json

plan = read_plan_json(Path("rename_plan.json"))
print(f"Loaded {len(plan)} operations")
```

---

#### `apply_plan(plan: Sequence[PlanItem]) -> None`

Execute rename operations from plan.

**Parameters:**
- `plan` (Sequence[PlanItem]): Rename plan to execute

**Returns:**
- None

**Raises:**
- `FileNotFoundError`: If source file doesn't exist
- `OSError`: If file operation fails

**Example:**
```python
from pathlib import Path
from ai_rename_tool.core import read_plan_json, apply_plan

plan = read_plan_json(Path("rename_plan.json"))
apply_plan(plan)
print("Renames applied successfully")
```

**Behavior:**
- Creates destination directories if needed
- Uses `Path.replace()` for atomic rename
- Processes operations in plan order

---

#### `undo_plan(path: Path) -> None`

Undo renames using saved plan file.

**Parameters:**
- `path` (Path): JSON plan file path

**Returns:**
- None

**Raises:**
- `FileNotFoundError`: If plan file or destination files don't exist
- `json.JSONDecodeError`: If plan file is invalid

**Example:**
```python
from pathlib import Path
from ai_rename_tool.core import undo_plan

undo_plan(Path("rename_plan.json"))
print("Renames undone successfully")
```

**Behavior:**
- Reads plan from JSON
- Reverses operations in reverse order
- Only processes files that exist at destination

---

## Module: ai_rename_tool.naming

### Functions

#### `sanitize_filename(name: str) -> str`

Clean filename to be filesystem-safe.

**Parameters:**
- `name` (str): Filename to sanitize

**Returns:**
- `str`: Sanitized filename

**Example:**
```python
from ai_rename_tool.naming import sanitize_filename

clean = sanitize_filename("my file!@#.txt")
# Returns safe filename
```

---

#### `is_good_name(name: str) -> bool`

Check if filename meets quality criteria.

**Parameters:**
- `name` (str): Filename to validate

**Returns:**
- `bool`: True if name is acceptable

---

#### `default_category(path: Path) -> str`

Determine file category from extension.

**Parameters:**
- `path` (Path): File path

**Returns:**
- `str`: Category name (e.g., "documents", "images")

**Example:**
```python
from pathlib import Path
from ai_rename_tool.naming import default_category

cat = default_category(Path("photo.jpg"))
# Returns "images"
```

---

## Module: ai_rename_tool.provider

### Type Aliases

#### `ProviderFn = Callable[[Sequence[Path]], Sequence[str]]`

Function type for rename suggestion providers.

**Parameters:**
- Files to generate suggestions for

**Returns:**
- Suggested filenames (must match input length)

---

### Functions

#### `local_heuristic_provider(files: Sequence[Path]) -> Sequence[str]`

Generate filename suggestions using local heuristics.

**Parameters:**
- `files` (Sequence[Path]): Files to generate suggestions for

**Returns:**
- `Sequence[str]`: Suggested filenames

**Example:**
```python
from pathlib import Path
from ai_rename_tool.provider import local_heuristic_provider

files = [Path("IMG_1234.jpg"), Path("DSC_5678.jpg")]
suggestions = local_heuristic_provider(files)
# Returns improved filenames
```

---

## Data Classes

### `PlanItem`

Immutable rename operation descriptor.

**Attributes:**
- `src` (Path): Source file path
- `dst` (Path): Destination file path

**Example:**
```python
from pathlib import Path
from ai_rename_tool.core import PlanItem

item = PlanItem(
    src=Path("/old/name.txt"),
    dst=Path("/new/name.txt")
)
```

---

## CLI Usage

### Command-Line Interface

```bash
# Generate plan with categorization
ai-rename-tool . --categorise --json plan.json --csv plan.csv

# Apply renames
ai-rename-tool . --apply

# Undo renames
ai-rename-tool --undo plan.json

# Include hidden files
ai-rename-tool . --include-hidden --json plan.json
```

---

## Constants

### `__version__`

Package version string (from Git tags via setuptools-scm).

**Type:** `str`
**Example:** `"1.0.0"`

---

Author: Kris Armstrong
