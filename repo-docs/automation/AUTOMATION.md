# System Prompt Library Automation

This document describes the automated update system for the System Prompt Library.

## Overview

The library now includes automated workflows that periodically update the consolidated prompts, generate the index, and update the README without manual intervention.

## Automation Components

### 1. GitHub Actions Workflows

#### Daily Automatic Updates
- **File**: `.github/workflows/auto-update-library.yml`
- **Schedule**: Daily at 3:00 AM UTC
- **Function**: Runs the complete update process automatically
- **Triggers**: 
  - Scheduled (daily)
  - Manual dispatch with optional force rebuild

#### Manual Updates
- **File**: `.github/workflows/manual-update-library.yml`
- **Function**: Allows manual triggering with specific options
- **Options**:
  - Update type: full, consolidate-only, index-only, readme-only
  - Force rebuild: true/false

### 2. Core Update Script

- **File**: `update_library_unified.py`
- **Function**: Single script that handles all update tasks:
  1. Consolidates JSON files → `consolidated_prompts.json`
  2. Generates index → `index.md`
  3. Updates README with index content

### 3. Test Script

- **File**: `test_automation.sh`
- **Function**: Local testing of the automation process
- **Usage**: `./test_automation.sh`

## How It Works

### Automatic Process Flow

1. **Trigger**: GitHub Actions runs daily at 3:00 AM UTC
2. **Setup**: Checks out repository, sets up Python 3.11
3. **Update**: Runs `python3 update_library_unified.py`
4. **Detection**: Checks for file changes using `git status`
5. **Commit**: If changes detected, commits with detailed message
6. **Push**: Pushes changes back to repository

### Incremental Updates

The system uses file hashing to detect changes:
- Only processes modified JSON files
- Maintains metadata about file states
- Skips unchanged files for efficiency
- Can be forced to rebuild everything with `--force-rebuild`

## Files Generated/Updated

### Primary Files
- `consolidated_prompts.json` - All prompts in single JSON array
- `index.md` - Formatted index with growth tracking
- `README.md` - Updated with current index content

### Metadata Files
- `consolidated_prompts.metadata.json` - Processing statistics
- `index_metadata.json` - Index generation metadata
- `growth_history.json` - Historical prompt count tracking

## Usage

### Automatic Operation
No action required - runs daily automatically.

### Manual Triggering

#### Via GitHub Actions
1. Go to repository → Actions tab
2. Select "Manual Update System Prompt Library"
3. Click "Run workflow"
4. Choose options and run

#### Local Testing
```bash
# Test the automation locally
./test_automation.sh

# Run update manually
python3 update_library_unified.py

# Force rebuild everything
python3 update_library_unified.py --force-rebuild
```

## Monitoring

### GitHub Actions
- Check Actions tab for workflow status
- View logs for detailed execution information
- Receive notifications for failed runs

### Commit History
- Automated commits include detailed metadata
- Commit messages show prompt counts and processing stats
- Easy to track when updates occurred

## Configuration

### Scheduling
To change the schedule, edit the cron expression in `auto-update-library.yml`:
```yaml
schedule:
  - cron: '0 3 * * *'  # Daily at 3:00 AM UTC
```

### Git Configuration
The workflows use:
- Email: `action@github.com`
- Name: `GitHub Action`
- Token: `GITHUB_TOKEN` (automatic)

## Troubleshooting

### Common Issues

1. **No changes committed**: Normal if no JSON files were modified
2. **Python errors**: Check that all required files exist
3. **Git push failures**: Usually permission issues (rare with GITHUB_TOKEN)

### Manual Recovery
If automation fails, you can always run updates manually:
```bash
python3 update_library_unified.py --force-rebuild
```

### Logs and Debugging
- GitHub Actions logs show detailed execution
- Local testing with `test_automation.sh` helps diagnose issues
- Metadata files contain processing statistics
 