// Petite Musique de Nuit - A gentle evening melody in Faust
// Inspired by classical serenade forms

import("stdfaust.lib");

// Golden ratio for harmonic intervals
phi = 1.618033988749;

// Gentle evening tempo
tempo = 72;
beat = 60.0/tempo;

// Simple envelope
env(gate, a, r) = gate : si.smooth(ba.tau2pole(select2(gate, r, a)));

// Soft pad voice with detuned oscillators
pad(freq, gate) = sum(i, 3, os.osc(freq * (1 + (i-1)*0.003))) / 3 * env(gate, 0.3, 0.8);

// Plucked string voice (Karplus-Strong style)
pluck(freq, gate) = gate : ba.impulsify : fi.fb_fcomb(1024, del, 1, -0.995) * env(gate, 0.01, 0.5)
with {
    del = ma.SR/freq;
};

// Bell-like tone
bell(freq, gate) = os.osc(freq) * env(gate, 0.01, 1.5) * 0.3 +
                   os.osc(freq*2.4) * env(gate, 0.005, 0.8) * 0.15 +
                   os.osc(freq*5.95) * env(gate, 0.001, 0.3) * 0.08;

// Simple arpeggiator using phasor
arp_step = int(os.phasor(8, tempo/60/2)) % 8;

// G major chord tones (serenade key)
note_freqs = waveform{392, 494, 587, 784, 587, 494, 392, 330};  // G4 B4 D5 G5...
current_freq = note_freqs, arp_step : rdtable;

// The gentle night music
melody = pluck(current_freq, 1) * 0.4;
harmony = pad(196, 1) * 0.15 + pad(247, 1) * 0.1;  // G3 + B3 pad

// Soft reverb tail
reverbed = melody + harmony : re.mono_freeverb(0.8, 0.6, 0.5, 1);

// Final mix with stereo spread
process = reverbed <: _, @(int(ma.SR*0.02));  // Slight stereo delay
