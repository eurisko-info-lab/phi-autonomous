# Contributing to Phi

Welcome! Phi is a community-driven project building the unified meta-language for formal verification, type theory, and high-performance computing.

## Ways to Contribute

### 🐛 Report Bugs & Issues
Found something broken? [Open an issue](https://github.com/eurisko-info-lab/phi/issues/new).

### 💡 Propose Features
Have an idea? Start a [Discussion](https://github.com/eurisko-info-lab/phi/discussions) first to gather feedback.

### 📝 Improve Documentation
- Fix typos, clarify explanations
- Add examples
- Translate docs

### 🔧 Code Contributions
1. Fork the repo
2. Create a feature branch: `git checkout -b feature/your-idea`
3. Make your changes
4. Test thoroughly
5. Submit a PR

## Areas We Need Help

| Area | Skills | Entry Point |
|------|--------|-------------|
| **RVM Optimizations** | Rust, VM internals | `ports/rust/tools/rvm/` |
| **Type Theory** | λ-calculus, CoC, HoTT | `specs/phi-core/examples/type-theory/` |
| **GPU Backend** | CUDA, parallel algorithms | `specs/phi-core/examples/cuda.phi` |
| **Haskell Port** | Haskell, parsers | `ports/haskell/` |
| **Scala Port** | Scala, FP | `ports/scala/` |
| **Category Theory** | Math, CT | `specs/phi-core/MATH.md` |

## Getting Started

```bash
# Clone
git clone https://github.com/eurisko-info-lab/phi.git
cd phi

# Build RVM (Rust VM)
cd specs/phi-core/ports/rust/tools/rvm
cargo build --release

# Run examples
cargo run -- ../../examples/rvm/factorial.rvm
```

## Code Style

- **Phi specs**: Follow existing conventions in `specs/`
- **Rust**: `cargo fmt && cargo clippy`
- **Haskell**: `hlint` + standard formatting
- **Scala**: `scalafmt`

## Communication

- **GitHub Discussions**: Questions, ideas, show & tell
- **Issues**: Bug reports, specific tasks
- **Twitter/X**: [@euriskoInfoLab](https://twitter.com/euriskoInfoLab)

## First-Time Contributors

Look for issues tagged `good first issue` or `help wanted`.

Not sure where to start? Post in Discussions - we'll help you find something that matches your interests and skills.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

*"The best way to understand Phi is to break it."* — Try something wild, see what happens.
