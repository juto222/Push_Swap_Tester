# Push Swap Tester

A lightweight, terminal-based Python tester for the **42 `push_swap`** project.

It generates random stacks of unique 32-bit signed integers, runs `push_swap` in adaptive mode, checks the resulting instructions with a checker, and reports sorting correctness and operation counts.

> **Status:** Personal project / work in progress. The tester requires your own `push_swap` executable and a compatible checker; neither is included here.

## Features

- Generates random lists of **10, 20, 100, and 500** distinct integers (configurable in the script).
- Lets you choose the number of tests per stack size.
- Runs `push_swap` with the `--adaptive` option.
- Selects `checker_Mac` on macOS or `checker_linux` on Linux.
- Counts successful (`OK`) and unsuccessful (`KO`) checks for each size.
- Displays the minimum, maximum, and average operation counts for successful tests.
- Runs argument-validation tests through `testerr.py` before the randomized tests.

## Requirements

- Python 3 (uses only standard-library modules).
- A compiled `push_swap` executable supporting `--adaptive`.
- A compatible `checker_Mac` or `checker_linux` executable, depending on your OS.
- The `testerr.py` module containing the `argerr()` function.

The script expects executable paths such as `./push_swap` to resolve **relative to your current terminal directory**, not necessarily the script's directory.

## Suggested project layout

```text
Push_swap/
├── push_swap             # Your compiled push_swap binary
├── checker_Mac           # Checker on macOS (if available)
├── checker_linux         # Checker on Linux (if available)
└── pushswaptester/
    ├── generator.py      # Main stress tester
    ├── testerr.py        # Argument tests (argerr)
    ├── README.md
    └── docs/
        └── GUIDE_FR.md
```

The diagram is a **suggested layout**. If you put the README elsewhere, adjust the paths accordingly.

## Run

From the folder containing the executable files (for example, `Push_swap/`):

```bash
python3 pushswaptester/generator.py
```

Enter the number of repetitions **per stack size** when prompted:

```text
How many test per size : 100
```

With four stack sizes and 100 repetitions, the script attempts **400 random sorting tests** after running its argument tests.

### Example output

The following numbers are illustrative and **not measured results**:

```text
How many test per size : 3

[Number 10]
OK : 3
KO : 0
Min ops : 21
Max ops : 38
Avg ops : 30.0

[Number 20]
OK : 3
KO : 0
Min ops : 79
Max ops : 110
Avg ops : 96.0
```

Additional sections are printed for 100 and 500 numbers.

## How it works

1. For each size in `NB_ARG`, generate a new set of unique random integers for each repetition.
2. Build the command arguments for `./push_swap --adaptive`.
3. Run `push_swap` using Python's `subprocess.run()` and capture its output.
4. Pass its standard output (the sorting instructions) to the checker via standard input, with the same starting numbers as checker arguments.
5. Record `OK` / `KO` results and aggregate operation counts for successful tests.

The tester uses `platform.system()` to identify the OS. On macOS it reports `Darwin` and selects `checker_Mac`; on Linux it selects `checker_linux`.

## Configuration

You can edit the constants in `generator.py`:

| Setting | Default | Purpose |
| --- | --- | --- |
| `NB_ARG` | `[10, 20, 100, 500]` | Stack sizes to test |
| `INT_MIN` | `-2147483648` | Minimum generated integer |
| `INT_MAX` | `2147483647` | Maximum generated integer |
| `nb_test` | Entered at runtime | Repetitions for each size |

The current script runs in `--adaptive` mode. Other sorting modes are not selectable through the interface yet.

## Interpretation

- **OK** means the checker reports a correctly sorted stack.
- **KO** means the checker does not confirm a correct sort (or reports an error).
- **Min / Max / Avg ops** are operation counts for successful sorting tests.
- These counts evaluate **operation volume**, not execution time.

## Known limitations

- Input validation for the number of repetitions is basic: a non-integer input can raise `ValueError`.
- The current test runner has **no timeout** for `push_swap` or the checker; a hanging process can hang the test.
- Externally supplied executables must exist and be executable at the expected paths.
- The code selects `checker_linux` for all Linux distributions; the fallback checker name does **not** specifically detect Fedora.
- OS and file-path handling is based on the original script, rather than a packaged installable CLI.
- No reproducible random seed or automatic saving of failed inputs is implemented.

## Development

Suggested next steps: improve input validation, add subprocess timeouts, preserve failed inputs for reproduction, and make executable paths configurable.

## Documentation

See [the French user and developer guide](docs/GUIDE_FR.md) for an explanation of each function, the test flow, and troubleshooting.
