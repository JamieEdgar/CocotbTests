// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vtop.h for the primary calling header

#ifndef VERILATED_VTOP___024ROOT_H_
#define VERILATED_VTOP___024ROOT_H_  // guard

#include "verilated.h"


class Vtop__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vtop___024root final : public VerilatedModule {
  public:

    // DESIGN SPECIFIC STATE
    VL_IN8(clk,0,0);
    VL_IN8(f,7,0);
    VL_OUT8(dn,2,0);
    CData/*0:0*/ second_order__DOT__clk;
    CData/*7:0*/ second_order__DOT__f;
    CData/*2:0*/ second_order__DOT__dn;
    CData/*0:0*/ second_order__DOT__stage1__DOT__clk;
    CData/*7:0*/ second_order__DOT__stage1__DOT__a;
    CData/*0:0*/ second_order__DOT__stage1__DOT__c;
    CData/*7:0*/ second_order__DOT__stage1__DOT__ab;
    CData/*7:0*/ second_order__DOT__stage1__DOT__b;
    CData/*0:0*/ second_order__DOT__stage2__DOT__clk;
    CData/*7:0*/ second_order__DOT__stage2__DOT__a;
    CData/*0:0*/ second_order__DOT__stage2__DOT__c;
    CData/*7:0*/ second_order__DOT__stage2__DOT__ab;
    CData/*7:0*/ second_order__DOT__stage2__DOT__b;
    CData/*0:0*/ __VstlFirstIteration;
    CData/*0:0*/ __VicoFirstIteration;
    CData/*0:0*/ __Vtrigprevexpr___TOP__clk__0;
    CData/*0:0*/ __VactContinue;
    IData/*31:0*/ __VactIterCount;
    VlUnpacked<CData/*0:0*/, 2> second_order__DOT__c;
    VlUnpacked<CData/*7:0*/, 2> second_order__DOT__ab;
    VlUnpacked<CData/*0:0*/, 2> second_order__DOT__c_d;
    VlTriggerVec<1> __VstlTriggered;
    VlTriggerVec<1> __VicoTriggered;
    VlTriggerVec<1> __VactTriggered;
    VlTriggerVec<1> __VnbaTriggered;

    // INTERNAL VARIABLES
    Vtop__Syms* const vlSymsp;

    // PARAMETERS
    static constexpr IData/*31:0*/ second_order__DOT__BITS = 8U;
    static constexpr IData/*31:0*/ second_order__DOT__stage1__DOT__BITS = 8U;
    static constexpr IData/*31:0*/ second_order__DOT__stage2__DOT__BITS = 8U;

    // CONSTRUCTORS
    Vtop___024root(Vtop__Syms* symsp, const char* v__name);
    ~Vtop___024root();
    VL_UNCOPYABLE(Vtop___024root);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


#endif  // guard
