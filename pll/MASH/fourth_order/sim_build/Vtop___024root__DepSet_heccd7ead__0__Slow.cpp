// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vtop.h for the primary calling header

#include "Vtop__pch.h"
#include "Vtop___024root.h"

VL_ATTR_COLD void Vtop___024root___eval_static__TOP(Vtop___024root* vlSelf);

VL_ATTR_COLD void Vtop___024root___eval_static(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_static\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    Vtop___024root___eval_static__TOP(vlSelf);
}

VL_ATTR_COLD void Vtop___024root___eval_static__TOP(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_static__TOP\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.fourth_order__DOT__dn = 0U;
    vlSelfRef.fourth_order__DOT__s3_dn_d = 0U;
    vlSelfRef.fourth_order__DOT__third_order1__DOT__dn = 0U;
    vlSelfRef.fourth_order__DOT__third_order1__DOT__s2_dn_d = 0U;
    vlSelfRef.fourth_order__DOT__third_order1__DOT__second_order1__DOT__dn = 0U;
    vlSelfRef.fourth_order__DOT__third_order1__DOT__second_order1__DOT__c_d[0U] = 0U;
    vlSelfRef.fourth_order__DOT__third_order1__DOT__second_order1__DOT__c_d[1U] = 0U;
    vlSelfRef.fourth_order__DOT__third_order1__DOT__second_order1__DOT__stage1__DOT__c = 0U;
    vlSelfRef.fourth_order__DOT__third_order1__DOT__second_order1__DOT__stage1__DOT__ab = 0U;
    vlSelfRef.fourth_order__DOT__third_order1__DOT__second_order1__DOT__stage1__DOT__b = 0U;
    vlSelfRef.fourth_order__DOT__third_order1__DOT__second_order1__DOT__stage2__DOT__c = 0U;
    vlSelfRef.fourth_order__DOT__third_order1__DOT__second_order1__DOT__stage2__DOT__ab = 0U;
    vlSelfRef.fourth_order__DOT__third_order1__DOT__second_order1__DOT__stage2__DOT__b = 0U;
    vlSelfRef.fourth_order__DOT__third_order1__DOT__stage0__DOT__c = 0U;
    vlSelfRef.fourth_order__DOT__third_order1__DOT__stage0__DOT__ab = 0U;
    vlSelfRef.fourth_order__DOT__third_order1__DOT__stage0__DOT__b = 0U;
    vlSelfRef.fourth_order__DOT__stage0__DOT__c = 0U;
    vlSelfRef.fourth_order__DOT__stage0__DOT__ab = 0U;
    vlSelfRef.fourth_order__DOT__stage0__DOT__b = 0U;
}

VL_ATTR_COLD void Vtop___024root___eval_initial(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_initial\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__Vtrigprevexpr___TOP__clk__0 = vlSelfRef.clk;
}

VL_ATTR_COLD void Vtop___024root___eval_final(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_final\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__stl(Vtop___024root* vlSelf);
#endif  // VL_DEBUG
VL_ATTR_COLD bool Vtop___024root___eval_phase__stl(Vtop___024root* vlSelf);

VL_ATTR_COLD void Vtop___024root___eval_settle(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_settle\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    IData/*31:0*/ __VstlIterCount;
    CData/*0:0*/ __VstlContinue;
    // Body
    __VstlIterCount = 0U;
    vlSelfRef.__VstlFirstIteration = 1U;
    __VstlContinue = 1U;
    while (__VstlContinue) {
        if (VL_UNLIKELY(((0x64U < __VstlIterCount)))) {
#ifdef VL_DEBUG
            Vtop___024root___dump_triggers__stl(vlSelf);
#endif
            VL_FATAL_MT("/home/jamie/git/CocotbTests/pll/MASH/fourth_order/fourth_order.sv", 1, "", "Settle region did not converge.");
        }
        __VstlIterCount = ((IData)(1U) + __VstlIterCount);
        __VstlContinue = 0U;
        if (Vtop___024root___eval_phase__stl(vlSelf)) {
            __VstlContinue = 1U;
        }
        vlSelfRef.__VstlFirstIteration = 0U;
    }
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__stl(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___dump_triggers__stl\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1U & (~ vlSelfRef.__VstlTriggered.any()))) {
        VL_DBG_MSGF("         No triggers active\n");
    }
    if ((1ULL & vlSelfRef.__VstlTriggered.word(0U))) {
        VL_DBG_MSGF("         'stl' region trigger index 0 is active: Internal 'stl' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

void Vtop___024root___ico_sequent__TOP__0(Vtop___024root* vlSelf);

VL_ATTR_COLD void Vtop___024root___eval_stl(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_stl\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1ULL & vlSelfRef.__VstlTriggered.word(0U))) {
        Vtop___024root___ico_sequent__TOP__0(vlSelf);
    }
}

VL_ATTR_COLD void Vtop___024root___eval_triggers__stl(Vtop___024root* vlSelf);

VL_ATTR_COLD bool Vtop___024root___eval_phase__stl(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_phase__stl\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    CData/*0:0*/ __VstlExecute;
    // Body
    Vtop___024root___eval_triggers__stl(vlSelf);
    __VstlExecute = vlSelfRef.__VstlTriggered.any();
    if (__VstlExecute) {
        Vtop___024root___eval_stl(vlSelf);
    }
    return (__VstlExecute);
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__ico(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___dump_triggers__ico\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1U & (~ vlSelfRef.__VicoTriggered.any()))) {
        VL_DBG_MSGF("         No triggers active\n");
    }
    if ((1ULL & vlSelfRef.__VicoTriggered.word(0U))) {
        VL_DBG_MSGF("         'ico' region trigger index 0 is active: Internal 'ico' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__act(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___dump_triggers__act\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1U & (~ vlSelfRef.__VactTriggered.any()))) {
        VL_DBG_MSGF("         No triggers active\n");
    }
    if ((1ULL & vlSelfRef.__VactTriggered.word(0U))) {
        VL_DBG_MSGF("         'act' region trigger index 0 is active: @(posedge clk)\n");
    }
}
#endif  // VL_DEBUG

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__nba(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___dump_triggers__nba\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1U & (~ vlSelfRef.__VnbaTriggered.any()))) {
        VL_DBG_MSGF("         No triggers active\n");
    }
    if ((1ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        VL_DBG_MSGF("         'nba' region trigger index 0 is active: @(posedge clk)\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD void Vtop___024root___ctor_var_reset(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___ctor_var_reset\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelf->clk = VL_RAND_RESET_I(1);
    vlSelf->f = VL_RAND_RESET_I(8);
    vlSelf->dn = VL_RAND_RESET_I(5);
    vlSelf->fourth_order__DOT__clk = VL_RAND_RESET_I(1);
    vlSelf->fourth_order__DOT__f = VL_RAND_RESET_I(8);
    vlSelf->fourth_order__DOT__dn = VL_RAND_RESET_I(5);
    vlSelf->fourth_order__DOT__s0_c = VL_RAND_RESET_I(1);
    vlSelf->fourth_order__DOT__s0_ab = VL_RAND_RESET_I(8);
    vlSelf->fourth_order__DOT__s3_dn = VL_RAND_RESET_I(4);
    vlSelf->fourth_order__DOT__s3_dn_d = VL_RAND_RESET_I(4);
    vlSelf->fourth_order__DOT__third_order1__DOT__clk = VL_RAND_RESET_I(1);
    vlSelf->fourth_order__DOT__third_order1__DOT__f = VL_RAND_RESET_I(8);
    vlSelf->fourth_order__DOT__third_order1__DOT__dn = VL_RAND_RESET_I(4);
    vlSelf->fourth_order__DOT__third_order1__DOT__s0_c = VL_RAND_RESET_I(1);
    vlSelf->fourth_order__DOT__third_order1__DOT__s0_ab = VL_RAND_RESET_I(8);
    vlSelf->fourth_order__DOT__third_order1__DOT__s2_dn = VL_RAND_RESET_I(3);
    vlSelf->fourth_order__DOT__third_order1__DOT__s2_dn_d = VL_RAND_RESET_I(3);
    vlSelf->fourth_order__DOT__third_order1__DOT__second_order1__DOT__clk = VL_RAND_RESET_I(1);
    vlSelf->fourth_order__DOT__third_order1__DOT__second_order1__DOT__f = VL_RAND_RESET_I(8);
    vlSelf->fourth_order__DOT__third_order1__DOT__second_order1__DOT__dn = VL_RAND_RESET_I(3);
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        vlSelf->fourth_order__DOT__third_order1__DOT__second_order1__DOT__c[__Vi0] = VL_RAND_RESET_I(1);
    }
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        vlSelf->fourth_order__DOT__third_order1__DOT__second_order1__DOT__ab[__Vi0] = VL_RAND_RESET_I(8);
    }
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        vlSelf->fourth_order__DOT__third_order1__DOT__second_order1__DOT__c_d[__Vi0] = VL_RAND_RESET_I(1);
    }
    vlSelf->fourth_order__DOT__third_order1__DOT__second_order1__DOT__stage1__DOT__clk = VL_RAND_RESET_I(1);
    vlSelf->fourth_order__DOT__third_order1__DOT__second_order1__DOT__stage1__DOT__a = VL_RAND_RESET_I(8);
    vlSelf->fourth_order__DOT__third_order1__DOT__second_order1__DOT__stage1__DOT__c = VL_RAND_RESET_I(1);
    vlSelf->fourth_order__DOT__third_order1__DOT__second_order1__DOT__stage1__DOT__ab = VL_RAND_RESET_I(8);
    vlSelf->fourth_order__DOT__third_order1__DOT__second_order1__DOT__stage1__DOT__b = VL_RAND_RESET_I(8);
    vlSelf->fourth_order__DOT__third_order1__DOT__second_order1__DOT__stage2__DOT__clk = VL_RAND_RESET_I(1);
    vlSelf->fourth_order__DOT__third_order1__DOT__second_order1__DOT__stage2__DOT__a = VL_RAND_RESET_I(8);
    vlSelf->fourth_order__DOT__third_order1__DOT__second_order1__DOT__stage2__DOT__c = VL_RAND_RESET_I(1);
    vlSelf->fourth_order__DOT__third_order1__DOT__second_order1__DOT__stage2__DOT__ab = VL_RAND_RESET_I(8);
    vlSelf->fourth_order__DOT__third_order1__DOT__second_order1__DOT__stage2__DOT__b = VL_RAND_RESET_I(8);
    vlSelf->fourth_order__DOT__third_order1__DOT__stage0__DOT__clk = VL_RAND_RESET_I(1);
    vlSelf->fourth_order__DOT__third_order1__DOT__stage0__DOT__a = VL_RAND_RESET_I(8);
    vlSelf->fourth_order__DOT__third_order1__DOT__stage0__DOT__c = VL_RAND_RESET_I(1);
    vlSelf->fourth_order__DOT__third_order1__DOT__stage0__DOT__ab = VL_RAND_RESET_I(8);
    vlSelf->fourth_order__DOT__third_order1__DOT__stage0__DOT__b = VL_RAND_RESET_I(8);
    vlSelf->fourth_order__DOT__stage0__DOT__clk = VL_RAND_RESET_I(1);
    vlSelf->fourth_order__DOT__stage0__DOT__a = VL_RAND_RESET_I(8);
    vlSelf->fourth_order__DOT__stage0__DOT__c = VL_RAND_RESET_I(1);
    vlSelf->fourth_order__DOT__stage0__DOT__ab = VL_RAND_RESET_I(8);
    vlSelf->fourth_order__DOT__stage0__DOT__b = VL_RAND_RESET_I(8);
    vlSelf->__Vtrigprevexpr___TOP__clk__0 = VL_RAND_RESET_I(1);
}
