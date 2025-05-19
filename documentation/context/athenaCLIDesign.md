# Athena CLI Interface Design Document

## 1. Overview

The Athena Command Line Interface (CLI) serves as the primary user interaction method for the MVP phase. It provides access to Athena's core functionality through a set of intuitive commands and subcommands, allowing users to manage their Obsidian notes, configure the system, and control the AI assistant's behavior.

This document outlines the CLI design, including command structure, interaction patterns, feedback mechanisms, and implementation approach.

## 2. Design Principles

The Athena CLI adheres to the following design principles:

1. **Simplicity First** - Commands follow intuitive patterns and provide helpful guidance
2. **Progressive Disclosure** - Common operations are simple, advanced features accessible but not obtrusive
3. **Informative Feedback** - Clear, concise output with appropriate detail level
4. **Consistency** - Predictable patterns for command structure and options
5. **Fail Gracefully** - Helpful error messages and recovery suggestions
6. **Performance Indication** - Feedback for long-running operations

## 3. Command Structure

Athena uses a git-style command structure with the pattern:

```
athena [global-options] <command> [subcommand] [command-options] [arguments]
```

### 3.1 Global Options

These options can be used with any command:

| Option | Short | Description |
|--------|-------|-------------|
| `--config <path>` | `-c` | Path to configuration file |
| `--api-key <key>` | `-k` | OpenAI/Anthropic API key |
| `--vault-path <path>` | `-p` | Path to Obsidian vault |
| `--verbose` | `-v` | Enable verbose output |
| `--quiet` | `-q` | Minimal output (errors only) |
| `--help` | `-h` | Show help message |
| `--version` | | Show version information |
| `--no-color` | | Disable colored output |

Example:
```
athena --vault-path ~/Documents/Obsidian/MainVault init
```

## 4. Core Commands

### 4.1 Setup and Configuration

#### 4.1.1 `init`

Initializes Athena for first use, creates configuration, and indexes notes.

```
athena init [--api-key <key>] [--vault-path <path>]
```

Example:
```
athena init --api-key sk-abcdef123456 --vault-path ~/Documents/Obsidian/Notes
```

Interaction flow:
1. If parameters are missing, prompt user for required information
2. Create configuration file in `~/.athena/config.yaml`
3. Run initial scan of vault and create database
4. Display summary of indexed notes
5. Provide next steps suggestions

#### 4.1.2 `config`

Manages Athena configuration settings.

```
athena config [get|set|list] [key] [value]
```

Examples:
```
athena config list                              # Show all settings
athena config get features.note_cleaning        # Get specific setting
athena config set llm.provider anthropic        # Set specific setting
athena config set notifications.frequency daily # Configure notification frequency
```

#### 4.1.3 `status`

Shows current system status, processing queue, and statistics.

```
athena status [--detailed]
```

Output includes:
- Vault location and size
- Notes count (total, processed, pending)
- Last run information
- Model configuration
- Current task queue

### 4.2 Note Management

#### 4.2.1 `process`

Processes notes with AI assistant. Can target specific notes or process in batch.

```
athena process [<path>...] [--recursive] [--force] [--dry-run] [--limit <n>] [--modified-since <date>]
```

Examples:
```
athena process                                    # Process all pending notes
athena process Projects/Athena/notes.md           # Process specific note
athena process Projects/ --recursive              # Process all notes in directory
athena process --modified-since 2023-05-10        # Process recently modified notes
athena process --dry-run                          # Show what would be processed without making changes
```

Interactive mode (when processing single note):
- Shows suggested changes
- Allows accepting/rejecting each change
- Provides explanations for suggestions

Batch mode (when processing multiple notes):
- Shows progress bar
- Summarizes changes made
- Allows reviewing detailed logs after completion

#### 4.2.2 `suggest`

Generates suggestions without applying changes.

```
athena suggest [<path>...] [--type <suggestion-type>] [--limit <n>]
```

Suggestion types:
- `clean` - Formatting and typo fixes
- `connect` - Connection and backlink suggestions
- `organize` - Folder and tag suggestions
- `content` - Content improvement suggestions
- `all` (default) - All suggestion types

Example:
```
athena suggest Projects/Research.md --type connect
```

Output example:
```
Suggestions for Projects/Research.md:

CONNECTIONS:
• This note appears related to "Projects/Methods.md" (85% confidence)
  Common concepts: experimental design, methodology, data collection
  Suggested action: Add backlink to Methods.md in Research.md

• "Books/Scientific-Writing.md" contains complementary information (73% confidence)
  Suggested action: Review Scientific-Writing.md for relevant techniques

BACKLINKS:
• "Projects/Results.md" references concepts in this note but lacks a direct link
  Suggested action: Add [[Projects/Research.md]] in Results.md line 42
```

#### 4.2.3 `search`

Searches notes using semantic or keyword search.

```
athena search <query> [--semantic] [--exact] [--path <path>] [--limit <n>]
```

Examples:
```
athena search "productivity techniques"                 # Keyword search
athena search "ways to improve focus" --semantic        # Semantic search
athena search "meeting notes" --path Projects/Athena/   # Scoped search
```

Output provides relevance-ranked results with context snippets.

#### 4.2.4 `connect`

Finds and displays connections between notes.

```
athena connect [<path>] [--strength <0-100>] [--type <connection-type>] [--visualize]
```

Connection types:
- `concept` - Shared concepts/topics
- `reference` - Direct references or backlinks
- `semantic` - General semantic similarity
- `temporal` - Time-based relationships
- `all` (default) - All connection types

Example:
```
athena connect Projects/Athena/architecture.md --strength 70
```

The `--visualize` option generates a visualization (ASCII art for CLI, exportable graph file).

### 4.3 Knowledge Management

#### 4.3.1 `graph`

Explores and manipulates the knowledge graph.

```
athena graph [concepts|entities|clusters] [--limit <n>] [--min-connections <n>]
```

Examples:
```
athena graph concepts                     # List top concepts in the vault
athena graph entities --limit 20          # List top 20 entities
athena graph clusters --min-connections 3 # Find concept clusters
```

#### 4.3.2 `summarize`

Generates summaries at various levels.

```
athena summarize [<path>] [--recursive] [--depth <1-3>]
```

Examples:
```
athena summarize Projects/Athena/          # Summarize a folder
athena summarize --recursive --depth 2     # Recursive summary with medium detail
```

Depth levels:
1. Brief overview (1-2 sentences)
2. Moderate detail (paragraph)
3. Comprehensive (multiple paragraphs)

### 4.4 System Management

#### 4.4.1 `update`

Updates the knowledge graph and internal database.

```
athena update [--full] [--reindex]
```

The `--full` option forces reprocessing of all notes, while `--reindex` rebuilds the search index.

#### 4.4.2 `log`

Displays and manages system logs.

```
athena log [show|clear] [--level <level>] [--limit <n>]
```

Example:
```
athena log show --level warning --limit 50
```

## 5. User Interaction Patterns

### 5.1 Progressive Command Discovery

Help is integrated throughout the CLI to guide users:

1. `athena` (without arguments) shows overview and common commands
2. `athena --help` shows detailed help with all commands
3. `athena <command> --help` shows specific command help
4. Command tab-completion (when installed) simplifies discovery

### 5.2 Interactive Prompts

For essential missing information, Athena uses interactive prompts:

```
$ athena init
No API key provided. Please enter your OpenAI or Anthropic API key:
> sk-abc123...

No vault path specified. Please enter the path to your Obsidian vault:
> ~/Documents/Obsidian/MainVault

Initializing Athena...
```

### 5.3 Confirmation for Destructive Actions

```
$ athena process --force
This will process all pending notes and may make changes to your files.
Are you sure you want to continue? [y/N]: 
```

### 5.4 Progress Indication

For long-running operations:

```
$ athena update --full
Updating knowledge graph and reprocessing all notes...
[████████████████████████▒▒▒▒▒▒] 67% (134/200 notes) ETA: 45s
```

### 5.5 Rich Output Formatting

Athena uses color and formatting for readability (with `--no-color` option available):

- Green for success messages
- Yellow for warnings
- Red for errors
- Bold for headings and important information
- Indentation and lists for structured data
- Tables for tabular data
- Progress bars for long-running tasks

## 6. Configuration File

Athena stores configuration in YAML format at `~/.athena/config.yaml`. Example:

```yaml
# Athena Configuration

system:
  data_directory: "~/.athena/data"
  log_level: "INFO"
  backup_enabled: true

llm:
  provider: "openai"  # openai, anthropic
  model: "gpt-4"
  api_key: "<encrypted-key>"

vault:
  path: "~/Documents/Obsidian/MainVault"
  exclude_folders:
    - "Private"
    - ".trash"

features:
  note_cleaning:
    enabled: true
    fix_typos: true
    format_markdown: true
    add_summaries: true
    suggest_backlinks: true
  
  connections:
    enabled: true
    discovery_threshold: 0.75
    max_suggestions_per_day: 5
  
  recommendations:
    enabled: true
    external_content: false
```

API keys are stored securely using the system's keychain/credential manager when available, or encrypted at rest.

## 7. Installation and Setup

### 7.1 Installation Methods

```
# Via pip
pip install athena-notes

# Direct download
curl -sSL https://get.athena-notes.app | bash
```

### 7.2 First-Run Experience

1. User installs Athena
2. User runs `athena init`
3. Athena guides through initial setup (API key, vault path)
4. Athena scans vault and builds initial knowledge graph
5. Athena suggests next steps:
   ```
   Setup complete! Here are some things you can try:
   
   • athena status                          - See system status
   • athena process                         - Process all notes
   • athena suggest Projects/important.md   - Get suggestions for a specific note
   • athena connect                         - Discover connections between notes
   
   Run athena --help for more commands and options.
   ```

## 8. Error Handling

Athena provides helpful error messages with context and recovery suggestions:

```
$ athena process nonexistent.md
Error: File not found: nonexistent.md
The file does not exist in your vault at ~/Documents/Obsidian/MainVault.

Suggestions:
• Check the file path and try again
• Use 'athena search' to find the correct file
• Use tab completion to avoid typos in filenames
```

## 9. Implementation Approach

### 9.1 Technologies

The CLI will be implemented using:

- **Python 3.11+** as the base language
- **Typer** for CLI interface (built on Click)
- **Rich** for terminal formatting and output
- **PyYAML** for configuration management
- **Keyring** for secure API key storage
- **Watchdog** for file system monitoring

### 9.2 Code Structure

```
athena/
├── cli/
│   ├── __init__.py
│   ├── main.py           # Entry point
│   ├── commands/         # Command implementations
│   │   ├── __init__.py
│   │   ├── init.py
│   │   ├── process.py
│   │   ├── suggest.py
│   │   └── ...
│   ├── utils/            # CLI utilities
│   │   ├── __init__.py
│   │   ├── formatting.py
│   │   ├── progress.py
│   │   └── interactive.py
│   └── config.py         # Configuration management
├── core/                 # Core functionality from architecture
│   ├── __init__.py
│   ├── orchestrator.py
│   ├── note_processor.py
│   └── ...
└── ...
```

### 9.3 Performance Considerations

The CLI is designed for responsiveness:

- Asynchronous processing for long-running tasks
- Background workers for indexing and processing
- Caching of common queries and results
- Incremental updates to minimize processing time

### 9.4 Testing Strategy

- Unit tests for all commands
- Integration tests for core workflows
- Mock LLM responses for deterministic testing
- Test coverage for error handling paths

## 10. User Experience Examples

### 10.1 Note Processing Workflow

```
$ athena process Projects/Research/methods.md

Analyzing methods.md...

Suggested changes:

1. Format heading hierarchy (line 12)
   - Original: #### Data Collection Methods
   - Suggested: ### Data Collection Methods
   [Accept/Reject/Next/View/Help] (a/r/n/v/h): a
   Applied change.

2. Fix typo (line 27)
   - Original: The experment will be conducted in two phases.
   - Suggested: The experiment will be conducted in two phases.
   [Accept/Reject/Next/View/Help] (a/r/n/v/h): a
   Applied change.

3. Add summary (beginning of document)
   - Suggested: Add a brief overview of research methods, including data collection approach, experimental design, and analysis techniques.
   [Accept/Reject/Next/View/Help] (a/r/n/v/h): v
   
   This will add the following at the top of your note:
   ```
   # Research Methods
   
   > [!summary]
   > This document outlines the research methodology, including qualitative and quantitative data collection approaches, the two-phase experimental design, and statistical analysis techniques planned for the project.
   ```
   [Accept/Reject/Next/View/Help] (a/r/n/v/h): a
   Applied change.

4. Suggest backlinks (line 45)
   - Suggested: Add reference to analysis.md
   [Accept/Reject/Next/View/Help] (a/r/n/v/h): v
   
   This will add the following link:
   Original: See data analysis approach for details.
   Suggested: See [[Projects/Research/analysis.md|data analysis approach]] for details.
   [Accept/Reject/Next/View/Help] (a/r/n/v/h): a
   Applied change.

Processing complete. 4 changes applied.

Discovered connections:
• Strong connection to Projects/Research/participants.md (90% similarity)
• Moderate connection to Projects/Research/analysis.md (75% similarity)
• Weak connection to Books/Research-Methods.md (60% similarity)

Run 'athena connect Projects/Research/methods.md' to explore these connections.
```

### 10.2 Knowledge Exploration Workflow

```
$ athena graph concepts --limit 5

Top concepts in your vault:
1. Product Management (37 notes)
2. Research Methods (24 notes)
3. Productivity Systems (19 notes)
4. Technical Architecture (15 notes)
5. Note Organization (12 notes)

$ athena graph entities --filter "person" --limit 3

Top people mentioned in your vault:
1. Andy Matuschak (8 notes)
2. Tiago Forte (6 notes)
3. Marty Cagan (5 notes)

$ athena connect Projects/PARA-Method.md

Connections for Projects/PARA-Method.md:

STRONG CONNECTIONS:
• Projects/Productivity-Systems.md (92% similarity)
  Shared concepts: organization, productivity, project management
  Direct reference: Referenced on line The PARA method (line 27)

• Books/Building-Second-Brain.md (87% similarity) 
  Shared concepts: note-taking, knowledge management
  Contextual: Both discuss personal knowledge management systems

MODERATE CONNECTIONS:
• Projects/Athena/requirements.md (70% similarity)
  Relevant section: "In Athena, we can apply PARA principles to..."
  Suggested action: Consider linking these notes

• Archive/Old-Notes-System.md (65% similarity)
  Historical context: Previous organization system
  Potential insight: Compare your evolution in note organization

Run 'athena suggest Projects/PARA-Method.md --type connect' for specific connection suggestions.
```

## 11. Future Enhancements

The CLI design accounts for future expansion:

### 11.1 Plugin System

Future versions will support plugins for custom commands and integrations.

```
athena plugin install github-notes
athena github sync --repo username/repo --path Projects/OpenSource/
```

### 11.2 Automation Rules

Custom automation rules for processing and organization.

```
athena automation add "Move meeting notes" --condition "contains:meeting notes" --action "move:Projects/Meetings/"
```

### 11.3 Integration with Web Dashboard

CLI will be able to launch the web dashboard (Phase 2).

```
athena dashboard --port 8080
```

## 12. Accessibility Considerations

- Screen reader compatibility with semantic text output
- High-contrast mode option
- Configurable output verbosity
- Support for different terminal sizes and capabilities

---

This CLI UI design document provides a comprehensive plan for Athena's command-line interface, focusing on intuitive commands, clear feedback, and efficient workflows that align with the product requirements and technical architecture.
