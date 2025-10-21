---
name: cli-ux-colorful
description: Design colorful CLI output with ANSI colors, syntax highlighting, status indicators, and terminal formatting. Use libraries like rich (Python) or chalk (Node.js). Use when designing CLI output, formatting terminal messages, or building command-line interfaces.
---

# CLI UX: Colorful Output

People like colorful CLIs. Use color when it makes things clearer.

## Core Principle: Color Enhances Usability

**Colorful, informative output is excellent for CLI usability.**

- ANSI color codes and terminal formatting enhance readability
- Syntax highlighting for code excerpts makes a huge difference
- Status indicators in color provide instant visual feedback
- Well-formatted output is professional and user-friendly

**Important distinction:** This is about ANSI color codes and terminal formatting, NOT emoji presentation characters. See `no-emoji-for-developers` skill for the emoji rule.

## Standard Color Conventions

Use conventional color meanings for consistency with other CLI tools:

**Red:** Errors and failures
- Error messages
- Failed tests
- Critical warnings
- ✗ failure indicators

**Yellow:** Warnings and cautions
- Non-critical warnings
- Deprecation notices
- Things requiring attention

**Green:** Success and completion
- Success messages
- Passing tests
- Completion confirmations
- ✓ success indicators

**Blue:** Information and prompts
- Informational messages
- Section headers
- User prompts
- Progress indicators

**Cyan/Magenta:** Highlighting and emphasis
- Emphasized key information
- Filenames or paths
- Important values in output

## Good Uses of Color

**Syntax-highlighted code excerpts:**
```
Showing code from src/parser.ts:
  function parseConfig(options) {    [blue]
    return loadFile(options.path);   [green]
  }                                  [blue]
```

**Colored diff output:**
```
+ Added this line          [green]
- Removed this line        [red]
  Unchanged line           [default]
```

**Status indicators:**
```
✓ Tests passing            [green checkmark]
✗ Build failed             [red x]
⚠ 3 warnings              [yellow warning]
```

**Progress indicators and section headers:**
```
┌─ Running Analysis ─────────────────┐   [blue header]
│ Processing files...                │
│ [████████████          ] 60%       │   [progress bar]
└────────────────────────────────────┘
```

**Emphasized key information:**
```
Found 15 undocumented functions       [default]
Impact score: 87                      [cyan/emphasized]
File: src/core/analyzer.py            [blue]
```

## Implementation

**Python:**
Use libraries like `rich` or `colorama` for terminal colors:

```python
from rich.console import Console
from rich.syntax import Syntax

console = Console()

# Colored output
console.print("[green]✓[/green] Tests passed")
console.print("[red]✗[/red] Build failed")

# Syntax highlighting
code = Syntax(code_string, "python", theme="monokai")
console.print(code)

# Tables and structured output
from rich.table import Table
table = Table(title="Analysis Results")
table.add_column("Function", style="cyan")
table.add_column("Score", style="magenta")
console.print(table)
```

**Node.js/TypeScript:**
Use libraries like `chalk` for terminal colors:

```typescript
import chalk from 'chalk';

// Colored output
console.log(chalk.green('✓') + ' Tests passed');
console.log(chalk.red('✗') + ' Build failed');
console.log(chalk.yellow('⚠') + ' Warning message');

// Emphasized text
console.log(`Found ${chalk.cyan('15')} undocumented functions`);
console.log(`File: ${chalk.blue(filepath)}`);

// Combined styles
console.log(chalk.bold.red('ERROR:') + ' Failed to parse file');
```

## Compatibility and Degradation

**Respect NO_COLOR environment variable:**
```python
import os
from rich.console import Console

# Disable color if NO_COLOR is set
console = Console(force_terminal=not os.environ.get('NO_COLOR'))
```

**Ensure graceful degradation:**
- Colors should degrade gracefully in terminals that don't support them
- Output should still be readable without color
- Don't rely on color as the ONLY way to convey information

**Test in multiple environments:**
- Test output in both light and dark terminal themes
- Verify colors are readable in both cases
- Ensure contrast is sufficient

## Examples of Excellent CLI Output

**Analysis results with colors:**
```bash
$ docimp analyze ./src

┌─ Documentation Analysis ──────────────────────────┐
│ Total functions: 42                               │
│ Documented: 28 [green]✓[/green]                   │
│ Undocumented: 14 [yellow]⚠[/yellow]               │
│ Coverage: 66.7%                                   │
└───────────────────────────────────────────────────┘

[cyan]Top Priority Items:[/cyan]

  [yellow]1.[/yellow] [bold]calculate_impact_score[/bold]
     File: src/scoring.py:45
     Complexity: 15
     Score: [red]75[/red]

  [yellow]2.[/yellow] [bold]parse_typescript_file[/bold]
     File: src/parsers/typescript.py:123
     Complexity: 12
     Score: [red]60[/red]
```

**Test results with colors:**
```bash
$ pytest -v

tests/test_parser.py::test_simple_parse [green]✓[/green]
tests/test_parser.py::test_complex_code [green]✓[/green]
tests/test_scorer.py::test_impact_score [red]✗[/red]

[red]FAILED[/red] tests/test_scorer.py::test_impact_score
  Expected: 75
  Got: 77

[green]2 passed[/green], [red]1 failed[/red]
```

## What This Is NOT

**This is not about emoji presentation characters:**
- Using ANSI colors: ✓ Excellent
- Using colorful emoji: ✗ See `no-emoji-for-developers` skill

**Examples:**
- `chalk.green('✓')` - Green text checkmark: Good!
- `console.log('✅')` - Colorful emoji: Bad (developer-facing)

## Remember

- People like colorful CLIs
- Use standard color conventions (red=error, yellow=warning, green=success, blue=info)
- Syntax highlighting for code excerpts
- Status indicators with colored symbols
- Respect NO_COLOR environment variable
- Test in light and dark themes
- Ensure graceful degradation
- Use libraries: `rich` (Python) or `chalk` (Node.js)
- Color enhances, doesn't replace, information
