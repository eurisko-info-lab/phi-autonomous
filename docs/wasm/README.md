# RosettaVM

A content-addressed virtual machine with CPU and GPU backends.

## What Is It?

RosettaVM is a stack-based VM where code is identified by its cryptographic hash, not by name or version. Same code = same hash. Always.

**Key Features:**
- **Content-addressed** — Functions identified by BLAKE3 hash
- **Multi-backend** — Runs on CPU interpreter or compiles to CUDA
- **Massively parallel** — 1M independent tasks in 0.3 seconds on GPU
- **Recursive** — Full recursion support on both CPU and GPU

## Quick Start

```bash
# Build
cargo build --release

# Run a program
rosettavm run program.rvm

# Compile to GPU
rosettavm cuda program.rvm
nvcc -o program program.cu
./program 1000000  # 1M parallel executions
```

## Example

```asm
fn factorial(n) {
    load 0
    push 2
    lt
    jumpif 8
    load 0
    load 0
    push 1
    sub
    call factorial
    mul
    ret
    push 1
    ret
}

fn main() {
    push 10
    call factorial
    halt
}
```

## Performance

| Workload | CPU | GPU | Speedup |
|----------|-----|-----|---------|
| 1 factorial | 2ms | 308ms | CPU wins |
| 1,000 factorials | 1.4s | 0.31s | **4.5x** |
| 1,000,000 factorials | ~23min | 0.32s | **4,375x** |

GPU has ~300ms overhead. After that, 1 task or 1 million takes the same time.

## Architecture

```
┌────────────────────────────────────────────────────┐
│                    RosettaVM                       │
├────────────┬─────────────┬─────────────────────────┤
│   Store    │  CPU VM     │      GPU Backend        │
│            │             │                         │
│ Hash→Code  │ Stack-based │ RVM→CUDA compilation    │
│ Name→Hash  │ interpreter │ Per-thread state        │
│            │ + Rayon     │ Recursive support       │
└────────────┴─────────────┴─────────────────────────┘
```

## Commands

| Command | Description |
|---------|-------------|
| `run <file>` | Execute on CPU |
| `cuda <file>` | Compile to CUDA |
| `par <bench>` | Parallel CPU benchmark |
| `repl` | Interactive mode |
| `hash <input>` | Compute BLAKE3 hash |
| `test` | Run test suite |

## Modules

| File | Purpose |
|------|---------|
| `vm.rs` | CPU interpreter |
| `cuda_codegen.rs` | RVM → CUDA compiler |
| `parallel.rs` | Multi-threaded CPU (Rayon) |
| `store.rs` | Content-addressed code storage |
| `hash.rs` | BLAKE3 hashing |
| `parse.rs` | Assembly parser |

## License

MIT
