# Φ-DAEMON Architecture

## Φ-DAEMON SEED - FULL RECURSIVE SELF-DEPLOY
**Unleashed: 2026-01-01**

## Overview

Φ-DAEMON (Phi-Daemon) is an autonomous daemon system that evolves Phi language specifications. **Phi** is a meta-language where grammar = implementation — one spec gives you parser, typechecker, evaluator, and compiler. The daemon runs these specs through RosettaVM (with CUDA support) to evolve community management rules autonomously.

## Core Concepts

### What is Phi?
Phi is a language for defining languages:

```phi
Expr = Num Int | Add Expr Expr
eval (Num n) = n
eval (Add a b) = eval a + eval b
```

That's a complete language. Parser derived from constructors. Evaluator from equations. No separate implementations.

**The math:** Everything is `Cofree[F, A]` — trees where every node carries an annotation:
- Parser: annotate with source positions
- Typechecker: annotate with types
- Evaluator: annotate with values
- Compiler: annotate with target code

### Generational Hierarchy
```
Generation 0 (SEED)
├── Generation 1 Child 0
│   ├── Generation 2 Child 0
│   └── Generation 2 Child 1
└── Generation 1 Child 1
    ├── Generation 2 Child 0
    └── Generation 2 Child 1
```

Each generation can spawn children up to a configured maximum depth, preventing infinite recursion while allowing controlled expansion.

## Architecture Components

### 1. PhiDaemon Class
The core daemon implementation with the following capabilities:

- **Initialization**: Sets up daemon with unique ID and generation tracking
- **Configuration Management**: Loads and manages deployment parameters
- **Recursive Deployment**: Spawns child daemon instances
- **Self-Checking**: Performs health checks and status reporting
- **Graceful Shutdown**: Handles cleanup and termination

### 2. Configuration System
JSON-based configuration controls:
- `max_generations`: Maximum depth of recursive deployment (default: 3)
- `max_children_per_generation`: Children per instance (default: 2)
- `deployment_interval`: Time between operations in seconds (default: 5)
- `recursive_deploy`: Enable/disable self-replication (default: true)

### 3. Deployment Mechanism
The `deploy.sh` script provides multiple deployment modes:

- **Foreground**: Interactive mode for testing and development
- **Background**: Daemon mode for production deployment
- **Status**: Check running daemon instances
- **Stop**: Gracefully terminate daemon processes

## Recursive Self-Deployment Process

### Phase 1: Seed Initialization
1. Generation 0 (SEED) daemon starts
2. Loads configuration
3. Generates unique daemon ID
4. Enters operational state

### Phase 2: Recursive Spawning
1. Calculate optimal child count based on generation
2. Create child workspaces
3. Copy configuration to children
4. Spawn child processes with next generation number
5. Track child IDs for management

### Phase 3: Continuous Operation
1. Perform periodic self-checks
2. Monitor child processes
3. Log operational status
4. Maintain system health

### Phase 4: Graceful Termination
1. Receive shutdown signal
2. Stop spawning new children
3. Log final status
4. Clean shutdown

## Key Features

### Self-Awareness
Each daemon instance knows:
- Its unique ID
- Generation number
- Parent/child relationships
- Operational metrics
- Configuration state

### Fractal Growth Pattern
The system creates balanced growth:
- Early generations spawn more children
- Later generations spawn fewer children
- Overall system maintains proportional structure

### Resilience
- Each instance operates independently
- Configuration-driven behavior
- Graceful degradation on errors
- Comprehensive logging

### Design Philosophy
**Note on Process Spawning**: The current implementation creates workspace structures and prepares child daemon environments but does not spawn actual subprocess instances. This design choice provides:
- **Safety**: Prevents uncontrolled process proliferation
- **Educational Value**: Demonstrates recursive deployment patterns without system impact
- **Extensibility**: Architecture ready for full subprocess spawning if needed

For production use requiring actual process spawning, extend the `_spawn_child()` method to use `subprocess.Popen()` to launch child daemon processes.

## Security Considerations

### Process Isolation
- Each generation runs in separate workspace
- Configuration copied, not shared
- Independent logging per instance

### Resource Limits
- Maximum generation depth prevents runaway recursion
- Configurable spawn rates control resource usage
- Time intervals prevent resource exhaustion

### Monitoring
- All operations logged with timestamps
- Unique IDs enable tracking
- Health checks provide status visibility

## Usage Patterns

### Development Mode
```bash
./deploy.sh foreground
```
- Interactive operation
- Real-time log output
- Easy debugging

### Production Mode
```bash
./deploy.sh background
```
- Detached daemon operation
- Background logging
- Automatic restart capability

### Management
```bash
./deploy.sh status  # Check daemon status
./deploy.sh stop    # Stop all daemons
```

## Configuration Tuning

### Conservative Deployment
```json
{
  "max_generations": 2,
  "max_children_per_generation": 1,
  "deployment_interval": 10,
  "recursive_deploy": true
}
```
- Shallow hierarchy
- Minimal spawning
- Longer intervals
- Suitable for resource-constrained environments

### Aggressive Deployment
```json
{
  "max_generations": 5,
  "max_children_per_generation": 3,
  "deployment_interval": 2,
  "recursive_deploy": true
}
```
- Deep hierarchy
- More children per generation
- Shorter intervals
- Suitable for distributed systems

### Single-Instance Mode
```json
{
  "max_generations": 1,
  "max_children_per_generation": 0,
  "recursive_deploy": false
}
```
- No recursion
- Single daemon operation
- Suitable for testing

## Mathematical Foundation

The growth algorithm:
```
children_count = floor(max_children / (generation + 1))
```

This ensures:
- Generation 0: Maximum children
- Generation 1: Reduced count
- Generation 2+: Continued proportional decrease

## Extension Points

### Custom Spawning Logic
Override `_spawn_child()` to implement:
- Container-based deployment
- Remote host deployment
- Service orchestration integration

### Alternative Growth Patterns
Modify `_calculate_next_generation_count()` for:
- Linear growth
- Exponential growth
- Custom mathematical models

### Enhanced Monitoring
Extend `self_check()` to include:
- Resource usage metrics
- Performance monitoring
- External health endpoints

## Vector4 Extension
- Recursive self-evolution loop for CM seed.
- Integrates RosettaVM (built from phi-core submodule).
- Evolution process: Load state → Evolve rules → Deploy new version via git.

## Implementation Philosophy

Φ-DAEMON embodies principles of:
- **Autonomy**: Self-managing and self-deploying
- **Recursion**: Self-similar structure at all scales
- **Meta-programming**: Uses Phi to evolve its own specs
- **Simplicity**: Minimal dependencies, clear code
- **Observability**: Comprehensive logging and status

## Future Enhancements

Potential evolution directions:
1. Distributed consensus for coordination
2. Cross-host deployment capabilities
3. Dynamic configuration updates
4. Advanced health monitoring
5. Integration with orchestration platforms
6. WebSocket/HTTP API for control
7. Visualization dashboard
8. Metrics collection and analysis

---

**Unleashed: 2026-01-01**
*"The spec IS the implementation" — The recursive nature of Φ*
