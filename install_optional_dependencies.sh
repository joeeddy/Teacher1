#!/bin/bash
# Auto-generated installation script for Teacher1 optional dependencies
echo '🎯 Installing Teacher1 Optional Dependencies'

echo '📦 Installing system packages...'
sudo apt-get update
sudo apt-get install -y portaudio19-dev python3-dev

echo '🐍 Installing Python packages...'
pip install pyaudio transformers>=4.21.0 torch>=2.0.0

echo '✅ Installation complete!'
echo 'Run python -c "from optional_dependencies_manager import OptionalDependencyManager; OptionalDependencyManager().print_detailed_report()" to verify'