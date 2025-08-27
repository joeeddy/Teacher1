# Built-in Dependencies Guide for Teacher1

## Overview

Teacher1 requires certain Python built-in modules that should come with Python but may be missing on some systems, especially minimal Linux installations. This guide explains how to identify and resolve these issues.

## The Issue

Python's "built-in" modules are part of the standard library but may be packaged separately on some systems. The most common issue is `tkinter`, which is required for GUI functionality in Teacher1.

## Quick Test

Run our built-in dependency test:

```bash
python test_builtin_dependencies.py
```

## Common Built-in Dependencies

### tkinter (CRITICAL)
- **Purpose**: GUI framework for `big_text_gui.py`
- **Error**: `ModuleNotFoundError: No module named 'tkinter'`
- **Fix**: `sudo apt-get install python3-tk`

### Other Standard Library Modules
- `uuid` - Used in websocket communication
- `json` - Configuration and API handling
- `asyncio` - Asynchronous operations
- `threading` - Concurrent operations
- `urllib.parse` - URL parsing

## Platform-Specific Solutions

### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install python3-tk
```

### CentOS/RHEL
```bash
sudo yum install tkinter
# or on newer versions:
sudo dnf install python3-tkinter
```

### Alpine Linux
```bash
apk add py3-tkinter
```

### Docker/Container Environments
Add to your Dockerfile:
```dockerfile
RUN apt-get update && apt-get install -y python3-tk
```

## Verification

After installation, verify tkinter works:
```bash
python -c "import tkinter; print('tkinter available')"
```

Run the GUI test:
```bash
python big_text_gui.py
```

## Why This Happens

1. **Minimal Python installations** often exclude GUI components
2. **Container environments** may not include GUI libraries
3. **Package managers** sometimes split standard library components
4. **Security policies** in some environments disable GUI components

## Integration with Setup Script

The `setup.py` script now automatically checks for missing built-in dependencies and provides installation instructions when issues are detected.

## Related Files

- `test_builtin_dependencies.py` - Comprehensive testing
- `setup.py` - Includes built-in dependency checking
- `big_text_gui.py` - Requires tkinter
- `.devcontainer/test_setup.py` - Basic dependency testing