#!/bin/bash
# Build RosettaVM from phi-core submodule
cd specs/phi-core
make rust  # Or whatever build command builds rosettavm
cd ../..
cp specs/phi-core/target/release/rosettavm .  # Copy binary to root
chmod +x rosettavm