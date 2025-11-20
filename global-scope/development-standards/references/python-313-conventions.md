# Python Code Review Guide - Beyond Automated Checks (Python 3.13)

This guide defines higher-level review responsibilities for modern Python code. Ruff already enforces syntax, style, and basic modernization. Your task is to evaluate **design, semantics, and intent** - what automation cannot check.

## 1. Typing Design

| Watch For | Better Practice |
|-----------|----------------|
| Misuse of `Any` or overly-broad types | Constrain with `object`, `Protocol`, or proper generics |
| Missing or misleading type hints | Ensure function signatures reflect actual contracts |
| Overuse of `TypedDict` or `dataclass` where `Protocol` fits | Use constructs aligned with semantics (record vs behavior) |
| Complex nested generics that harm readability | Alias intermediate types for clarity, e.g. `type UserMap = dict[int, User]` |

## 2. API and Function Design

| Watch For | Better Practice |
|-----------|----------------|
| Functions mixing concerns (I/O, logic, formatting) | Separate pure logic from side effects |
| Too many positional arguments or hidden defaults | Use keyword-only arguments, dataclasses, or config objects |
| Implicit resource lifecycles (e.g. open/close across calls) | Manage resources explicitly with context managers |
| Leaky abstractions (e.g. returning raw DB rows, OS paths) | Return domain objects or sanitized values |

## 3. Error Handling and Contracts

| Watch For | Better Practice |
|-----------|----------------|
| Bare or over-broad `except Exception` | Catch only the expected errors |
| Swallowing exceptions silently | Log or re-raise with context |
| Assertions in production code | Replace with explicit validation (`ValueError`, `TypeError`) |
| Returning sentinel values to indicate failure | Raise exceptions or use `Result`-style returns |

## 4. Asynchronous and Concurrency Logic

| Watch For | Better Practice |
|-----------|----------------|
| Blocking I/O inside async functions | Use non-blocking libraries (`aiofiles`, `httpx`, etc.) |
| Detached tasks or missing `await` | Ensure tasks are tracked via `TaskGroup` or explicit `await` |
| Unbounded concurrency or parallelism | Use semaphores or bounded executors |

## 5. Control Flow and Readability

| Watch For | Better Practice |
|-----------|----------------|
| Deeply nested `if`/`else`/`try` structures | Flatten with early returns or guard clauses |
| Flag variables acting as implicit state machines | Use `Enum` or `match` statements for clarity |
| Side effects inside comprehensions | Keep comprehensions pure and move side effects out |

## 6. Data and Collection Semantics

| Watch For | Better Practice |
|-----------|----------------|
| Mutating a collection while iterating | Iterate over a copy or collect changes separately |
| Relying on implicit ordering in sets/dicts | Sort explicitly or use `OrderedDict` |
| Manual caching or memoization | Use `functools.cache` or `lru_cache` decorators |

## 7. Architectural Cohesion

| Watch For | Better Practice |
|-----------|----------------|
| Functions or classes with too many responsibilities | Apply the single-responsibility principle |
| Hidden global state or implicit singletons | Pass dependencies explicitly |
| Tight coupling between modules | Use interfaces or dependency injection |
| Reimplementing stdlib behavior | Prefer standard modules like `itertools`, `functools`, `contextlib` |

## 8. Testing and Contracts

| Watch For | Better Practice |
|-----------|----------------|
| Non-deterministic tests (time, randomness, I/O) | Seed randomness or mock external dependencies |
| Missing failure-path tests | Include negative and edge cases |
| Assertions with unclear messages | Use explicit messages or `pytest.raises` for clarity |

## 9. Maintainability and Clarity

| Watch For | Better Practice |
|-----------|----------------|
| Comments explaining *what* the code does | Explain *why* decisions were made |
| Clever or overly compressed one-liners | Prefer explicit and readable constructs |
| Undocumented module or function purpose | Add concise docstrings summarizing intent |

## 10. Ethical and Safety Considerations

| Watch For | Better Practice |
|-----------|----------------|
| Misleading variable or function names | Use accurate, intention-revealing naming |
| Hidden side effects (network, subprocess, filesystem) | Document all external interactions |
| Serialization or deserialization without validation | Validate data before use (`pydantic`, `dataclasses`, schema libraries) |

## Reviewer Checklist

- Function and class boundaries make logical sense
- Exceptions are explicit and meaningful
- Async code never blocks or leaks tasks
- No hidden global state or circular dependencies
- Comments describe intent, not implementation
- Typing reflects true contracts
- No magical or surprising behavior left unexplained

---

Last updated for Python 3.13 / Ruff 0.6
