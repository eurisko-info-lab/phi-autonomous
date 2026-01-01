// Phi Synth - A functional audio greeting
// Faust: Functional Audio Stream

import("stdfaust.lib");

// Phi frequency ratios (golden ratio vibes)
phi = 1.618033988749;

// Base frequency
freq = hslider("freq", 432, 100, 1000, 1);

// A chord based on phi ratios
fundamental = os.osc(freq);
golden1 = os.osc(freq * phi) * 0.5;
golden2 = os.osc(freq * phi * phi) * 0.25;
golden3 = os.osc(freq / phi) * 0.3;

// Combine voices
chord = (fundamental + golden1 + golden2 + golden3) / 4;

// Simple envelope 
gate = button("gate");
env = en.adsr(0.1, 0.2, 0.7, 0.5, gate);

// Add some reverb
wet = chord * env : fi.lowpass(2, 2000) : re.mono_freeverb(0.7, 0.5, 0.5, 1);

// Stereo output
process = wet <: _, _;
