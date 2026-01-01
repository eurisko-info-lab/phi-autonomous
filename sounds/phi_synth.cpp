/* ------------------------------------------------------------
name: "phi_synth"
Code generated with Faust 2.79.3 (https://faust.grame.fr)
Compilation options: -a minimal.cpp -lang cpp -ct 1 -es 1 -mcd 16 -mdd 1024 -mdy 33 -single -ftz 0
------------------------------------------------------------ */

#ifndef  __mydsp_H__
#define  __mydsp_H__

/************************************************************************
 IMPORTANT NOTE : this file contains two clearly delimited sections :
 the ARCHITECTURE section (in two parts) and the USER section. Each section
 is governed by its own copyright and license. Please check individually
 each section for license and copyright information.
 *************************************************************************/

/******************* BEGIN minimal.cpp ****************/
/************************************************************************
 FAUST Architecture File
 Copyright (C) 2003-2019 GRAME, Centre National de Creation Musicale
 ---------------------------------------------------------------------
 This Architecture section is free software; you can redistribute it
 and/or modify it under the terms of the GNU General Public License
 as published by the Free Software Foundation; either version 3 of
 the License, or (at your option) any later version.
 
 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 
 You should have received a copy of the GNU General Public License
 along with this program; If not, see <http://www.gnu.org/licenses/>.
 
 EXCEPTION : As a special exception, you may create a larger work
 that contains this FAUST architecture section and distribute
 that work under terms of your choice, so long as this FAUST
 architecture section is not modified.
 
 ************************************************************************
 ************************************************************************/

#include <iostream>

#include "faust/gui/PrintUI.h"
#include "faust/gui/MapUI.h"
#ifdef LAYOUT_UI
#include "faust/gui/LayoutUI.h"
#endif
#include "faust/gui/meta.h"
#include "faust/audio/dummy-audio.h"
#ifdef FIXED_POINT
#include "faust/dsp/fixed-point.h"
#endif

// faust -a minimal.cpp noise.dsp -o noise.cpp && c++ -std=c++11 noise.cpp -o noise && ./noise

/******************************************************************************
 *******************************************************************************
 
 VECTOR INTRINSICS
 
 *******************************************************************************
 *******************************************************************************/


/********************END ARCHITECTURE SECTION (part 1/2)****************/

/**************************BEGIN USER SECTION **************************/

#ifndef FAUSTFLOAT
#define FAUSTFLOAT float
#endif 

#include <algorithm>
#include <cmath>
#include <cstdint>
#include <math.h>

#ifndef FAUSTCLASS 
#define FAUSTCLASS mydsp
#endif

#ifdef __APPLE__ 
#define exp10f __exp10f
#define exp10 __exp10
#endif

#if defined(_WIN32)
#define RESTRICT __restrict
#else
#define RESTRICT __restrict__
#endif

class mydspSIG0 {
	
  private:
	
	int iVec2[2];
	int iRec12[2];
	
  public:
	
	int getNumInputsmydspSIG0() {
		return 0;
	}
	int getNumOutputsmydspSIG0() {
		return 1;
	}
	
	void instanceInitmydspSIG0(int sample_rate) {
		for (int l4 = 0; l4 < 2; l4 = l4 + 1) {
			iVec2[l4] = 0;
		}
		for (int l5 = 0; l5 < 2; l5 = l5 + 1) {
			iRec12[l5] = 0;
		}
	}
	
	void fillmydspSIG0(int count, float* table) {
		for (int i1 = 0; i1 < count; i1 = i1 + 1) {
			iVec2[0] = 1;
			iRec12[0] = (iVec2[1] + iRec12[1]) % 65536;
			table[i1] = std::sin(9.58738e-05f * float(iRec12[0]));
			iVec2[1] = iVec2[0];
			iRec12[1] = iRec12[0];
		}
	}

};

static mydspSIG0* newmydspSIG0() { return (mydspSIG0*)new mydspSIG0(); }
static void deletemydspSIG0(mydspSIG0* dsp) { delete dsp; }

static float mydsp_faustpower2_f(float value) {
	return value * value;
}
static float ftbl0mydspSIG0[65536];

class mydsp : public dsp {
	
 private:
	
	int iVec0[2];
	int fSampleRate;
	float fConst0;
	float fConst1;
	float fConst2;
	float fConst3;
	float fConst4;
	float fConst5;
	FAUSTFLOAT fButton0;
	float fVec1[2];
	int iRec10[2];
	float fConst6;
	float fRec11[2];
	float fConst7;
	float fConst8;
	float fConst9;
	FAUSTFLOAT fHslider0;
	float fConst10;
	float fRec13[2];
	float fConst11;
	float fRec14[2];
	float fConst12;
	float fRec15[2];
	float fConst13;
	float fRec16[2];
	float fRec9[3];
	float fRec17[2];
	int IOTA0;
	float fVec3[8192];
	int iConst14;
	float fRec8[2];
	float fRec19[2];
	float fVec4[8192];
	int iConst15;
	float fRec18[2];
	float fRec21[2];
	float fVec5[8192];
	int iConst16;
	float fRec20[2];
	float fRec23[2];
	float fVec6[8192];
	int iConst17;
	float fRec22[2];
	float fRec25[2];
	float fVec7[8192];
	int iConst18;
	float fRec24[2];
	float fRec27[2];
	float fVec8[8192];
	int iConst19;
	float fRec26[2];
	float fRec29[2];
	float fVec9[8192];
	int iConst20;
	float fRec28[2];
	float fRec31[2];
	float fVec10[8192];
	int iConst21;
	float fRec30[2];
	float fVec11[2048];
	int iConst22;
	float fRec6[2];
	float fVec12[2048];
	int iConst23;
	float fRec4[2];
	float fVec13[2048];
	int iConst24;
	float fRec2[2];
	float fVec14[1024];
	int iConst25;
	float fRec0[2];
	
 public:
	mydsp() {
	}
	
	void metadata(Meta* m) { 
		m->declare("basics.lib/name", "Faust Basic Element Library");
		m->declare("basics.lib/version", "1.21.0");
		m->declare("compile_options", "-a minimal.cpp -lang cpp -ct 1 -es 1 -mcd 16 -mdd 1024 -mdy 33 -single -ftz 0");
		m->declare("delays.lib/name", "Faust Delay Library");
		m->declare("delays.lib/version", "1.1.0");
		m->declare("envelopes.lib/adsr:author", "Yann Orlarey and Andrey Bundin");
		m->declare("envelopes.lib/author", "GRAME");
		m->declare("envelopes.lib/copyright", "GRAME");
		m->declare("envelopes.lib/license", "LGPL with exception");
		m->declare("envelopes.lib/name", "Faust Envelope Library");
		m->declare("envelopes.lib/version", "1.3.0");
		m->declare("filename", "phi_synth.dsp");
		m->declare("filters.lib/allpass_comb:author", "Julius O. Smith III");
		m->declare("filters.lib/allpass_comb:copyright", "Copyright (C) 2003-2019 by Julius O. Smith III <jos@ccrma.stanford.edu>");
		m->declare("filters.lib/allpass_comb:license", "MIT-style STK-4.3 license");
		m->declare("filters.lib/fir:author", "Julius O. Smith III");
		m->declare("filters.lib/fir:copyright", "Copyright (C) 2003-2019 by Julius O. Smith III <jos@ccrma.stanford.edu>");
		m->declare("filters.lib/fir:license", "MIT-style STK-4.3 license");
		m->declare("filters.lib/iir:author", "Julius O. Smith III");
		m->declare("filters.lib/iir:copyright", "Copyright (C) 2003-2019 by Julius O. Smith III <jos@ccrma.stanford.edu>");
		m->declare("filters.lib/iir:license", "MIT-style STK-4.3 license");
		m->declare("filters.lib/lowpass0_highpass1", "MIT-style STK-4.3 license");
		m->declare("filters.lib/lowpass0_highpass1:author", "Julius O. Smith III");
		m->declare("filters.lib/lowpass:author", "Julius O. Smith III");
		m->declare("filters.lib/lowpass:copyright", "Copyright (C) 2003-2019 by Julius O. Smith III <jos@ccrma.stanford.edu>");
		m->declare("filters.lib/lowpass:license", "MIT-style STK-4.3 license");
		m->declare("filters.lib/name", "Faust Filters Library");
		m->declare("filters.lib/tf2:author", "Julius O. Smith III");
		m->declare("filters.lib/tf2:copyright", "Copyright (C) 2003-2019 by Julius O. Smith III <jos@ccrma.stanford.edu>");
		m->declare("filters.lib/tf2:license", "MIT-style STK-4.3 license");
		m->declare("filters.lib/tf2s:author", "Julius O. Smith III");
		m->declare("filters.lib/tf2s:copyright", "Copyright (C) 2003-2019 by Julius O. Smith III <jos@ccrma.stanford.edu>");
		m->declare("filters.lib/tf2s:license", "MIT-style STK-4.3 license");
		m->declare("filters.lib/version", "1.7.1");
		m->declare("maths.lib/author", "GRAME");
		m->declare("maths.lib/copyright", "GRAME");
		m->declare("maths.lib/license", "LGPL with exception");
		m->declare("maths.lib/name", "Faust Math Library");
		m->declare("maths.lib/version", "2.8.1");
		m->declare("name", "phi_synth");
		m->declare("oscillators.lib/name", "Faust Oscillator Library");
		m->declare("oscillators.lib/version", "1.6.0");
		m->declare("platform.lib/name", "Generic Platform Library");
		m->declare("platform.lib/version", "1.3.0");
		m->declare("reverbs.lib/mono_freeverb:author", "Romain Michon");
		m->declare("reverbs.lib/name", "Faust Reverb Library");
		m->declare("reverbs.lib/version", "1.4.0");
	}

	virtual int getNumInputs() {
		return 0;
	}
	virtual int getNumOutputs() {
		return 2;
	}
	
	static void classInit(int sample_rate) {
		mydspSIG0* sig0 = newmydspSIG0();
		sig0->instanceInitmydspSIG0(sample_rate);
		sig0->fillmydspSIG0(65536, ftbl0mydspSIG0);
		deletemydspSIG0(sig0);
	}
	
	virtual void instanceConstants(int sample_rate) {
		fSampleRate = sample_rate;
		fConst0 = std::min<float>(1.92e+05f, std::max<float>(1.0f, float(fSampleRate)));
		fConst1 = std::tan(6283.1855f / fConst0);
		fConst2 = 2.0f * (1.0f - 1.0f / mydsp_faustpower2_f(fConst1));
		fConst3 = 1.0f / fConst1;
		fConst4 = (fConst3 + -1.4142135f) / fConst1 + 1.0f;
		fConst5 = 1.0f / ((fConst3 + 1.4142135f) / fConst1 + 1.0f);
		fConst6 = 1.0f / std::max<float>(1.0f, 0.5f * fConst0);
		fConst7 = std::max<float>(1.0f, 0.1f * fConst0);
		fConst8 = 1.0f / fConst7;
		fConst9 = 0.3f / std::max<float>(1.0f, 0.2f * fConst0);
		fConst10 = 0.618034f / fConst0;
		fConst11 = 2.618034f / fConst0;
		fConst12 = 1.618034f / fConst0;
		fConst13 = 1.0f / fConst0;
		iConst14 = std::max<int>(0, int(0.025306122f * fConst0));
		iConst15 = std::max<int>(0, int(0.026938776f * fConst0));
		iConst16 = std::max<int>(0, int(0.028956916f * fConst0));
		iConst17 = std::max<int>(0, int(0.030748298f * fConst0));
		iConst18 = std::max<int>(0, int(0.0322449f * fConst0));
		iConst19 = std::max<int>(0, int(0.033809524f * fConst0));
		iConst20 = std::max<int>(0, int(0.035306122f * fConst0));
		iConst21 = std::max<int>(0, int(0.036666665f * fConst0));
		iConst22 = std::min<int>(1024, std::max<int>(0, int(0.0126077095f * fConst0)));
		iConst23 = std::min<int>(1024, std::max<int>(0, int(0.01f * fConst0)));
		iConst24 = std::min<int>(1024, std::max<int>(0, int(0.0077324263f * fConst0)));
		iConst25 = std::min<int>(1024, std::max<int>(0, int(0.0051020407f * fConst0)));
	}
	
	virtual void instanceResetUserInterface() {
		fButton0 = FAUSTFLOAT(0.0f);
		fHslider0 = FAUSTFLOAT(432.0f);
	}
	
	virtual void instanceClear() {
		for (int l0 = 0; l0 < 2; l0 = l0 + 1) {
			iVec0[l0] = 0;
		}
		for (int l1 = 0; l1 < 2; l1 = l1 + 1) {
			fVec1[l1] = 0.0f;
		}
		for (int l2 = 0; l2 < 2; l2 = l2 + 1) {
			iRec10[l2] = 0;
		}
		for (int l3 = 0; l3 < 2; l3 = l3 + 1) {
			fRec11[l3] = 0.0f;
		}
		for (int l6 = 0; l6 < 2; l6 = l6 + 1) {
			fRec13[l6] = 0.0f;
		}
		for (int l7 = 0; l7 < 2; l7 = l7 + 1) {
			fRec14[l7] = 0.0f;
		}
		for (int l8 = 0; l8 < 2; l8 = l8 + 1) {
			fRec15[l8] = 0.0f;
		}
		for (int l9 = 0; l9 < 2; l9 = l9 + 1) {
			fRec16[l9] = 0.0f;
		}
		for (int l10 = 0; l10 < 3; l10 = l10 + 1) {
			fRec9[l10] = 0.0f;
		}
		for (int l11 = 0; l11 < 2; l11 = l11 + 1) {
			fRec17[l11] = 0.0f;
		}
		IOTA0 = 0;
		for (int l12 = 0; l12 < 8192; l12 = l12 + 1) {
			fVec3[l12] = 0.0f;
		}
		for (int l13 = 0; l13 < 2; l13 = l13 + 1) {
			fRec8[l13] = 0.0f;
		}
		for (int l14 = 0; l14 < 2; l14 = l14 + 1) {
			fRec19[l14] = 0.0f;
		}
		for (int l15 = 0; l15 < 8192; l15 = l15 + 1) {
			fVec4[l15] = 0.0f;
		}
		for (int l16 = 0; l16 < 2; l16 = l16 + 1) {
			fRec18[l16] = 0.0f;
		}
		for (int l17 = 0; l17 < 2; l17 = l17 + 1) {
			fRec21[l17] = 0.0f;
		}
		for (int l18 = 0; l18 < 8192; l18 = l18 + 1) {
			fVec5[l18] = 0.0f;
		}
		for (int l19 = 0; l19 < 2; l19 = l19 + 1) {
			fRec20[l19] = 0.0f;
		}
		for (int l20 = 0; l20 < 2; l20 = l20 + 1) {
			fRec23[l20] = 0.0f;
		}
		for (int l21 = 0; l21 < 8192; l21 = l21 + 1) {
			fVec6[l21] = 0.0f;
		}
		for (int l22 = 0; l22 < 2; l22 = l22 + 1) {
			fRec22[l22] = 0.0f;
		}
		for (int l23 = 0; l23 < 2; l23 = l23 + 1) {
			fRec25[l23] = 0.0f;
		}
		for (int l24 = 0; l24 < 8192; l24 = l24 + 1) {
			fVec7[l24] = 0.0f;
		}
		for (int l25 = 0; l25 < 2; l25 = l25 + 1) {
			fRec24[l25] = 0.0f;
		}
		for (int l26 = 0; l26 < 2; l26 = l26 + 1) {
			fRec27[l26] = 0.0f;
		}
		for (int l27 = 0; l27 < 8192; l27 = l27 + 1) {
			fVec8[l27] = 0.0f;
		}
		for (int l28 = 0; l28 < 2; l28 = l28 + 1) {
			fRec26[l28] = 0.0f;
		}
		for (int l29 = 0; l29 < 2; l29 = l29 + 1) {
			fRec29[l29] = 0.0f;
		}
		for (int l30 = 0; l30 < 8192; l30 = l30 + 1) {
			fVec9[l30] = 0.0f;
		}
		for (int l31 = 0; l31 < 2; l31 = l31 + 1) {
			fRec28[l31] = 0.0f;
		}
		for (int l32 = 0; l32 < 2; l32 = l32 + 1) {
			fRec31[l32] = 0.0f;
		}
		for (int l33 = 0; l33 < 8192; l33 = l33 + 1) {
			fVec10[l33] = 0.0f;
		}
		for (int l34 = 0; l34 < 2; l34 = l34 + 1) {
			fRec30[l34] = 0.0f;
		}
		for (int l35 = 0; l35 < 2048; l35 = l35 + 1) {
			fVec11[l35] = 0.0f;
		}
		for (int l36 = 0; l36 < 2; l36 = l36 + 1) {
			fRec6[l36] = 0.0f;
		}
		for (int l37 = 0; l37 < 2048; l37 = l37 + 1) {
			fVec12[l37] = 0.0f;
		}
		for (int l38 = 0; l38 < 2; l38 = l38 + 1) {
			fRec4[l38] = 0.0f;
		}
		for (int l39 = 0; l39 < 2048; l39 = l39 + 1) {
			fVec13[l39] = 0.0f;
		}
		for (int l40 = 0; l40 < 2; l40 = l40 + 1) {
			fRec2[l40] = 0.0f;
		}
		for (int l41 = 0; l41 < 1024; l41 = l41 + 1) {
			fVec14[l41] = 0.0f;
		}
		for (int l42 = 0; l42 < 2; l42 = l42 + 1) {
			fRec0[l42] = 0.0f;
		}
	}
	
	virtual void init(int sample_rate) {
		classInit(sample_rate);
		instanceInit(sample_rate);
	}
	
	virtual void instanceInit(int sample_rate) {
		instanceConstants(sample_rate);
		instanceResetUserInterface();
		instanceClear();
	}
	
	virtual mydsp* clone() {
		return new mydsp();
	}
	
	virtual int getSampleRate() {
		return fSampleRate;
	}
	
	virtual void buildUserInterface(UI* ui_interface) {
		ui_interface->openVerticalBox("phi_synth");
		ui_interface->addHorizontalSlider("freq", &fHslider0, FAUSTFLOAT(432.0f), FAUSTFLOAT(1e+02f), FAUSTFLOAT(1e+03f), FAUSTFLOAT(1.0f));
		ui_interface->addButton("gate", &fButton0);
		ui_interface->closeBox();
	}
	
	virtual void compute(int count, FAUSTFLOAT** RESTRICT inputs, FAUSTFLOAT** RESTRICT outputs) {
		FAUSTFLOAT* output0 = outputs[0];
		FAUSTFLOAT* output1 = outputs[1];
		float fSlow0 = float(fButton0);
		int iSlow1 = fSlow0 == 0.0f;
		float fSlow2 = float(fHslider0);
		float fSlow3 = fConst10 * fSlow2;
		float fSlow4 = fConst11 * fSlow2;
		float fSlow5 = fConst12 * fSlow2;
		float fSlow6 = fConst13 * fSlow2;
		for (int i0 = 0; i0 < count; i0 = i0 + 1) {
			iVec0[0] = 1;
			fVec1[0] = fSlow0;
			iRec10[0] = iSlow1 * (iRec10[1] + 1);
			fRec11[0] = fSlow0 + fRec11[1] * float(fVec1[1] >= fSlow0);
			int iTemp0 = 1 - iVec0[1];
			float fTemp1 = ((iTemp0) ? 0.0f : fSlow3 + fRec13[1]);
			fRec13[0] = fTemp1 - std::floor(fTemp1);
			float fTemp2 = ((iTemp0) ? 0.0f : fSlow4 + fRec14[1]);
			fRec14[0] = fTemp2 - std::floor(fTemp2);
			float fTemp3 = ((iTemp0) ? 0.0f : fSlow5 + fRec15[1]);
			fRec15[0] = fTemp3 - std::floor(fTemp3);
			float fTemp4 = ((iTemp0) ? 0.0f : fSlow6 + fRec16[1]);
			fRec16[0] = fTemp4 - std::floor(fTemp4);
			fRec9[0] = 0.25f * (ftbl0mydspSIG0[std::max<int>(0, std::min<int>(int(65536.0f * fRec16[0]), 65535))] + 0.5f * ftbl0mydspSIG0[std::max<int>(0, std::min<int>(int(65536.0f * fRec15[0]), 65535))] + 0.25f * ftbl0mydspSIG0[std::max<int>(0, std::min<int>(int(65536.0f * fRec14[0]), 65535))] + 0.3f * ftbl0mydspSIG0[std::max<int>(0, std::min<int>(int(65536.0f * fRec13[0]), 65535))]) * std::max<float>(0.0f, std::min<float>(fConst8 * fRec11[0], std::max<float>(fConst9 * (fConst7 - fRec11[0]) + 1.0f, 0.7f)) * (1.0f - fConst6 * float(iRec10[0]))) - fConst5 * (fConst4 * fRec9[2] + fConst2 * fRec9[1]);
			float fTemp5 = fConst5 * (fRec9[2] + fRec9[0] + 2.0f * fRec9[1]);
			fRec17[0] = 0.5f * (fRec17[1] + fRec8[1]);
			fVec3[IOTA0 & 8191] = 0.7f * fRec17[0] + fTemp5;
			fRec8[0] = fVec3[(IOTA0 - iConst14) & 8191];
			fRec19[0] = 0.5f * (fRec19[1] + fRec18[1]);
			fVec4[IOTA0 & 8191] = fTemp5 + 0.7f * fRec19[0];
			fRec18[0] = fVec4[(IOTA0 - iConst15) & 8191];
			fRec21[0] = 0.5f * (fRec21[1] + fRec20[1]);
			fVec5[IOTA0 & 8191] = fTemp5 + 0.7f * fRec21[0];
			fRec20[0] = fVec5[(IOTA0 - iConst16) & 8191];
			fRec23[0] = 0.5f * (fRec23[1] + fRec22[1]);
			fVec6[IOTA0 & 8191] = fTemp5 + 0.7f * fRec23[0];
			fRec22[0] = fVec6[(IOTA0 - iConst17) & 8191];
			fRec25[0] = 0.5f * (fRec25[1] + fRec24[1]);
			fVec7[IOTA0 & 8191] = fTemp5 + 0.7f * fRec25[0];
			fRec24[0] = fVec7[(IOTA0 - iConst18) & 8191];
			fRec27[0] = 0.5f * (fRec27[1] + fRec26[1]);
			fVec8[IOTA0 & 8191] = fTemp5 + 0.7f * fRec27[0];
			fRec26[0] = fVec8[(IOTA0 - iConst19) & 8191];
			fRec29[0] = 0.5f * (fRec29[1] + fRec28[1]);
			fVec9[IOTA0 & 8191] = fTemp5 + 0.7f * fRec29[0];
			fRec28[0] = fVec9[(IOTA0 - iConst20) & 8191];
			fRec31[0] = 0.5f * (fRec31[1] + fRec30[1]);
			fVec10[IOTA0 & 8191] = fTemp5 + 0.7f * fRec31[0];
			fRec30[0] = fVec10[(IOTA0 - iConst21) & 8191];
			float fTemp6 = fRec30[1] + fRec28[1] + fRec26[1] + fRec24[1] + fRec22[1] + fRec20[1] + fRec18[1] + 0.5f * fRec6[1] + fRec8[1];
			fVec11[IOTA0 & 2047] = fTemp6;
			fRec6[0] = fVec11[(IOTA0 - iConst22) & 2047];
			float fRec7 = -(0.5f * fTemp6);
			float fTemp7 = fRec6[1] + fRec7 + 0.5f * fRec4[1];
			fVec12[IOTA0 & 2047] = fTemp7;
			fRec4[0] = fVec12[(IOTA0 - iConst23) & 2047];
			float fRec5 = -(0.5f * fTemp7);
			float fTemp8 = fRec4[1] + fRec5 + 0.5f * fRec2[1];
			fVec13[IOTA0 & 2047] = fTemp8;
			fRec2[0] = fVec13[(IOTA0 - iConst24) & 2047];
			float fRec3 = -(0.5f * fTemp8);
			float fTemp9 = fRec2[1] + fRec3 + 0.5f * fRec0[1];
			fVec14[IOTA0 & 1023] = fTemp9;
			fRec0[0] = fVec14[(IOTA0 - iConst25) & 1023];
			float fRec1 = -(0.5f * fTemp9);
			float fTemp10 = fRec1 + fRec0[1];
			output0[i0] = FAUSTFLOAT(fTemp10);
			output1[i0] = FAUSTFLOAT(fTemp10);
			iVec0[1] = iVec0[0];
			fVec1[1] = fVec1[0];
			iRec10[1] = iRec10[0];
			fRec11[1] = fRec11[0];
			fRec13[1] = fRec13[0];
			fRec14[1] = fRec14[0];
			fRec15[1] = fRec15[0];
			fRec16[1] = fRec16[0];
			fRec9[2] = fRec9[1];
			fRec9[1] = fRec9[0];
			fRec17[1] = fRec17[0];
			IOTA0 = IOTA0 + 1;
			fRec8[1] = fRec8[0];
			fRec19[1] = fRec19[0];
			fRec18[1] = fRec18[0];
			fRec21[1] = fRec21[0];
			fRec20[1] = fRec20[0];
			fRec23[1] = fRec23[0];
			fRec22[1] = fRec22[0];
			fRec25[1] = fRec25[0];
			fRec24[1] = fRec24[0];
			fRec27[1] = fRec27[0];
			fRec26[1] = fRec26[0];
			fRec29[1] = fRec29[0];
			fRec28[1] = fRec28[0];
			fRec31[1] = fRec31[0];
			fRec30[1] = fRec30[0];
			fRec6[1] = fRec6[0];
			fRec4[1] = fRec4[0];
			fRec2[1] = fRec2[0];
			fRec0[1] = fRec0[0];
		}
	}

};

/***************************END USER SECTION ***************************/

/*******************BEGIN ARCHITECTURE SECTION (part 2/2)***************/

using namespace std;

#ifdef LAYOUT_UI
void getMinimumSize(dsp* dsp, LayoutUI* ui, float& width, float& height)
{
    // Prepare layout
    dsp->buildUserInterface(ui);
    
    cout << "==========================" << endl;
    for (const auto& it : ui->fPathItemMap) {
        cout << it.second << endl;
    }
    
    cout << "Width " << ui->getWidth() << endl;
    cout << "Height " << ui->getHeight() << endl;
    
    width = ui->getWidth();
    height = ui->getHeight();
}

void setPosAndSize(LayoutUI* ui, float x_pos, float y_pos, float width, float height)
{
    ui->setSize(width, height);
    ui->setPos(x_pos, y_pos);
    
    cout << "==========================" << endl;
    for (const auto& it : ui->fPathItemMap) {
        cout << it.second << endl;
    }
    
    cout << "Width " << ui->getWidth() << endl;
    cout << "Height " << ui->getHeight() << endl;
}
#endif

int main(int argc, char* argv[])
{
    mydsp DSP;
    cout << "DSP size: " << sizeof(DSP) << " bytes\n";
    
    // Activate the UI, here that only print the control paths
    PrintUI print_ui;
    DSP.buildUserInterface(&print_ui);
    
    /*
    MapUI map_ui;
    DSP.buildUserInterface(&map_ui);
    for (int i = 0; i < map_ui.getParamsCount(); i++) {
        cout << "getParamAddress " << map_ui.getParamAddress(i) << endl;
        cout << "getParamShortname " << map_ui.getParamShortname(i) << endl;
        cout << "getParamLabel " << map_ui.getParamLabel(i) << endl;
    }
    */
    
#ifdef LAYOUT_UI
    LayoutUI layout_ui;
    float width, height;
    getMinimumSize(&DSP, &layout_ui, width, height);
    cout << "minimal_width: " << width << "\n";
    cout << "minimal_height: " << height << "\n";
    setPosAndSize(&layout_ui, 0, 0, width*1.5, height*1.5);
#else
    // Allocate the audio driver to render 5 buffers of 512 frames
    dummyaudio audio(5);
    audio.init("Test", static_cast<dsp*>(&DSP));
    
    // Render buffers...
    audio.start();
    audio.stop();
#endif
}

/******************* END minimal.cpp ****************/


#endif
