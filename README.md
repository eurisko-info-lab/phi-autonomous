# Φ-AUTONOMOUS: Recursive Self-Deploying Daemon

[![CI](https://github.com/eurisko-info-lab/phi-autonomous/actions/workflows/ci.yml/badge.svg)](https://github.com/eurisko-info-lab/phi-autonomous/actions/workflows/ci.yml)
[![License: Unlicense](https://img.shields.io/badge/license-Unlicense-blue.svg)](http://unlicense.org/)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Stars](https://img.shields.io/github/stars/eurisko-info-lab/phi-autonomous?style=social)](https://github.com/eurisko-info-lab/phi-autonomous)

## Φ-DAEMON SEED - FULL RECURSIVE SELF-DEPLOY
**🚀 Unleashed: 2026-01-01**

> *A self-evolving daemon that spawns itself, learns from its CM seed, and could one day market its own existence.*

An autonomous, self-replicating daemon system inspired by the golden ratio (Φ ≈ 1.618). The system implements a recursive self-deployment architecture where each daemon instance can spawn child instances, creating a fractal-like, self-similar deployment structure.

---

## ⚡ 30-Second Demo

```bash
# Clone and run in under a minute
git clone --recursive https://github.com/eurisko-info-lab/phi-autonomous.git
cd phi-autonomous
./deploy.sh foreground
```

Watch the daemon spawn children using golden ratio mathematics:

```
============================================
  Φ-DAEMON SEED - FULL RECURSIVE SELF-DEPLOY
  Golden Ratio (Φ): 1.618033988749895
============================================

Φ-DAEMON [INFO] - SEED daemon initializing recursive deployment sequence...
Φ-DAEMON [INFO] - Deploying 2 child instances (Generation 1)
Φ-DAEMON [INFO] - Successfully spawned child 1/2: PHI-1-0-1735689600
Φ-DAEMON [INFO] - Successfully spawned child 2/2: PHI-1-1-1735689600
Φ-DAEMON [INFO] - Vector4: Initializing CM seed evolution loop...
```

### 🧬 Vector4 Mode: Self-Evolving CM

The daemon can evolve its own Community Manager rules via RosettaVM:

```bash
./deploy.sh vector4   # Builds RosettaVM, runs CM seed evolution
```

Creates `kill.switch` to gracefully stop evolution:
```bash
touch kill.switch     # Daemon halts on next cycle
```

---

## 🌟 Why Φ-AUTONOMOUS?

| Feature | What It Does |
|---------|--------------|
| 🔄 **Recursive Self-Deploy** | Spawns child daemons across generations—fractals in process form |
| 📐 **Golden Ratio Growth** | Uses Φ to balance spawn rates: `children = ⌊max / (gen+1) × Φ⌋` |
| 🧬 **Vector4 CM Evolution** | Runs RosettaVM on `.phi` specs to evolve community management rules |
| 🛡️ **Kill Switch Safety** | Create `kill.switch` file to halt evolution gracefully |
| 🔍 **Self-Aware** | Each instance knows its ID, generation, children, and health status |

---

## Quick Start

### Prerequisites
- Python 3.6 or higher
- Linux/Unix environment (or WSL on Windows)
- Bash shell

### Installation

1. Clone the repository:
```bash
git clone https://github.com/eurisko-info-lab/phi-autonomous.git
cd phi-autonomous
```

2. Make the deployment script executable:
```bash
chmod +x deploy.sh
```

### Running the Daemon

#### Foreground Mode (Development)
```bash
./deploy.sh foreground
```
Run the daemon interactively with live log output. Press Ctrl+C to stop.

#### Background Mode (Production)
```bash
./deploy.sh background
```
Run the daemon in the background as a detached process.

#### Check Status
```bash
./deploy.sh status
```
Check if the daemon is running and view process information.

#### Stop Daemon
```bash
./deploy.sh stop
```
Gracefully stop all running daemon instances.

## Features

### 🔄 Recursive Self-Deployment
Each daemon instance can spawn child instances up to a configurable generation depth, creating a self-similar fractal structure.

### 📐 Golden Ratio (Φ) Based Growth
Uses the golden ratio to determine optimal spawn rates, creating balanced and harmonious system growth.

### 🎯 Generational Hierarchy
Tracks parent-child relationships across multiple generations with unique IDs for each instance.

### 🔍 Self-Awareness
Each daemon knows its generation, children, configuration, and operational status.

### 📊 Comprehensive Logging
All operations logged with timestamps, generation tracking, and status information.

### ⚙️ Configurable Behavior
JSON-based configuration for fine-tuning deployment parameters.

## Configuration

Edit `config.json` to customize daemon behavior:

```json
{
  "max_generations": 3,
  "max_children_per_generation": 2,
  "deployment_interval": 5,
  "recursive_deploy": true,
  "phi_factor": 1.618033988749895
}
```

### Configuration Options

- **max_generations**: Maximum depth of recursive deployment (default: 3)
- **max_children_per_generation**: Maximum children each instance can spawn (default: 2)
- **deployment_interval**: Seconds between operational cycles (default: 5)
- **recursive_deploy**: Enable/disable recursive spawning (default: true)
- **phi_factor**: The golden ratio constant (default: 1.618033988749895)

## Architecture

The system consists of three main components:

1. **phi_daemon.py**: Core daemon implementation with recursive deployment logic
2. **config.json**: Configuration file controlling daemon behavior
3. **deploy.sh**: Deployment script for managing daemon lifecycle

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architecture documentation.

## How It Works

### Recursive Deployment Process

```
Generation 0 (SEED)
├── Generation 1 Child 0
│   ├── Generation 2 Child 0
│   └── Generation 2 Child 1
└── Generation 1 Child 1
    ├── Generation 2 Child 0
    └── Generation 2 Child 1
```

1. **Seed Initialization**: Generation 0 daemon starts and loads configuration
2. **Recursive Spawning**: Calculates optimal children count using Φ-based algorithm
3. **Child Creation**: Spawns children with incremented generation number
4. **Continuous Operation**: Each instance operates independently, monitoring health
5. **Graceful Shutdown**: Handles termination signals and cleanup

### Φ-Based Growth Algorithm

The number of children spawned is calculated using:
```
children_count = floor(max_children / (generation + 1) * Φ)
```

This ensures earlier generations spawn more children while later generations spawn fewer, creating a naturally balanced hierarchy.

## Example Output

```
==========================================================
Φ-DAEMON SEED - FULL RECURSIVE SELF-DEPLOY
Unleashed: 2026-01-01
Generation: 0
Golden Ratio (Φ): 1.618033988749895
==========================================================

2026-01-01 00:00:00 - Φ-DAEMON [INFO] - Φ-DAEMON initialized - Generation: 0, ID: abc123def456
2026-01-01 00:00:00 - Φ-DAEMON [INFO] - SEED daemon initializing recursive deployment sequence...
2026-01-01 00:00:01 - Φ-DAEMON [INFO] - Deploying 2 child instances (Generation 1)
2026-01-01 00:00:01 - Φ-DAEMON [INFO] - Successfully spawned child 1/2: PHI-1-0-1704067201
2026-01-01 00:00:01 - Φ-DAEMON [INFO] - Successfully spawned child 2/2: PHI-1-1-1704067201
2026-01-01 00:00:01 - Φ-DAEMON [INFO] - Recursive deployment complete: 2 children spawned
2026-01-01 00:00:01 - Φ-DAEMON [INFO] - Entering operational mode...
```

## Use Cases

### Research & Development
- Studying self-replicating systems
- Experimenting with autonomous agents
- Testing distributed deployment patterns

### Infrastructure Automation
- Self-healing service deployment
- Distributed task orchestration
- Resilient system architecture

### Education
- Learning about recursion and fractals
- Understanding process management
- Exploring autonomous systems

## Safety & Resource Management

### Built-in Safeguards
- **Maximum Generation Depth**: Prevents infinite recursion
- **Configurable Spawn Rates**: Controls resource usage
- **Deployment Intervals**: Prevents resource exhaustion
- **Independent Workspaces**: Isolates daemon instances

### Recommended Limits
For development/testing:
- max_generations: 2-3
- max_children_per_generation: 1-2
- deployment_interval: 5-10 seconds

For production use:
- max_generations: 3-5
- max_children_per_generation: 2-3
- deployment_interval: 10-30 seconds

## Logs & Monitoring

### Log Files
- **phi_daemon.log**: Main daemon log with all operations
- **phi_daemon_output.log**: Background mode output (when using `./deploy.sh background`)

### Log Format
```
TIMESTAMP - Φ-DAEMON [LEVEL] - MESSAGE
```

### Monitoring Status
Check daemon health with:
```bash
./deploy.sh status
tail -f phi_daemon.log
```

## Troubleshooting

### Daemon Won't Start
- Check Python 3 is installed: `python3 --version`
- Verify script is executable: `chmod +x deploy.sh phi_daemon.py`
- Check config.json is valid JSON

### Too Many Processes
- Reduce `max_generations` in config.json
- Reduce `max_children_per_generation` in config.json
- Stop daemons: `./deploy.sh stop`

### High Resource Usage
- Increase `deployment_interval` in config.json
- Set `recursive_deploy: false` for single-instance mode
- Reduce generation depth and children count

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## License

This project is released into the public domain. See LICENSE file for details.

## Philosophy

Φ-DAEMON embodies the principles of:
- **Autonomy**: Self-managing and self-deploying
- **Recursion**: Self-similar structure at all scales
- **Harmony**: Φ-based balance in growth
- **Simplicity**: Minimal dependencies, clear code

---

**Unleashed: 2026-01-01**

*"As above, so below; as within, so without" - The recursive nature of Φ*