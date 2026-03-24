#!/usr/bin/env bash
# Extract readable strings from the Claude Code binary and cache by version.
# Usage: bash extract.sh
# Output: prints the path to the cached strings file

set -euo pipefail

# Find the real claude binary, resolving symlinks and skipping wrappers
find_real_binary() {
    local candidate

    # Try ~/.local/bin/claude first (standard install)
    candidate="$HOME/.local/bin/claude"
    if [[ -e "$candidate" ]]; then
        # Resolve symlinks to get the actual binary
        candidate="$(readlink -f "$candidate" 2>/dev/null || realpath "$candidate" 2>/dev/null || echo "$candidate")"
        if file "$candidate" 2>/dev/null | grep -q "Mach-O\|ELF"; then
            echo "$candidate"
            return 0
        fi
    fi

    # Try which claude, but skip shell script wrappers
    candidate="$(which claude 2>/dev/null || true)"
    if [[ -n "$candidate" ]]; then
        candidate="$(readlink -f "$candidate" 2>/dev/null || realpath "$candidate" 2>/dev/null || echo "$candidate")"
        if file "$candidate" 2>/dev/null | grep -q "Mach-O\|ELF"; then
            echo "$candidate"
            return 0
        fi
    fi

    # Search common locations
    for dir in "$HOME/.local/share/claude/versions" "/usr/local/bin" "/opt/homebrew/bin"; do
        if [[ -d "$dir" ]]; then
            # Find the newest binary in the directory
            candidate="$(find "$dir" -maxdepth 1 -type f -perm +111 2>/dev/null | sort -V | tail -1)"
            if [[ -n "$candidate" ]] && file "$candidate" 2>/dev/null | grep -q "Mach-O\|ELF"; then
                echo "$candidate"
                return 0
            fi
        fi
    done

    echo "ERROR: Could not find Claude Code binary" >&2
    return 1
}

BINARY="$(find_real_binary)"
VERSION="$(basename "$BINARY")"

# If the binary name isn't a version number, try to extract it
if ! [[ "$VERSION" =~ ^[0-9]+\.[0-9]+ ]]; then
    # Try running claude --version
    VERSION="$("$BINARY" --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1 || echo "unknown")"
fi

CACHE_DIR="$HOME/.claude/cache/binary-strings"
CACHE_FILE="$CACHE_DIR/$VERSION.txt"

if [[ -f "$CACHE_FILE" ]]; then
    echo "$CACHE_FILE"
    exit 0
fi

mkdir -p "$CACHE_DIR"

echo "Extracting strings from $BINARY (version $VERSION)..." >&2
strings "$BINARY" > "$CACHE_FILE" 2>/dev/null
LINES="$(wc -l < "$CACHE_FILE" | tr -d ' ')"
echo "Extracted $LINES lines to $CACHE_FILE" >&2

echo "$CACHE_FILE"
