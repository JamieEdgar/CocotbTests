// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table implementation internals

#include "Vtop__pch.h"
#include "Vtop.h"
#include "Vtop___024root.h"

// FUNCTIONS
Vtop__Syms::~Vtop__Syms()
{

    // Tear down scope hierarchy
    __Vhier.remove(0, &__Vscope_second_order);
    __Vhier.remove(&__Vscope_second_order, &__Vscope_second_order__stage1);
    __Vhier.remove(&__Vscope_second_order, &__Vscope_second_order__stage2);

}

Vtop__Syms::Vtop__Syms(VerilatedContext* contextp, const char* namep, Vtop* modelp)
    : VerilatedSyms{contextp}
    // Setup internal state of the Syms class
    , __Vm_modelp{modelp}
    // Setup module instances
    , TOP{this, namep}
{
        // Check resources
        Verilated::stackCheck(31);
    // Configure time unit / time precision
    _vm_contextp__->timeunit(-12);
    _vm_contextp__->timeprecision(-12);
    // Setup each module's pointers to their submodules
    // Setup each module's pointer back to symbol table (for public functions)
    TOP.__Vconfigure(true);
    // Setup scopes
    __Vscope_TOP.configure(this, name(), "TOP", "TOP", "<null>", 0, VerilatedScope::SCOPE_OTHER);
    __Vscope_second_order.configure(this, name(), "second_order", "second_order", "second_order", -12, VerilatedScope::SCOPE_MODULE);
    __Vscope_second_order__stage1.configure(this, name(), "second_order.stage1", "stage1", "stage", -12, VerilatedScope::SCOPE_MODULE);
    __Vscope_second_order__stage2.configure(this, name(), "second_order.stage2", "stage2", "stage", -12, VerilatedScope::SCOPE_MODULE);

    // Set up scope hierarchy
    __Vhier.add(0, &__Vscope_second_order);
    __Vhier.add(&__Vscope_second_order, &__Vscope_second_order__stage1);
    __Vhier.add(&__Vscope_second_order, &__Vscope_second_order__stage2);

    // Setup export functions
    for (int __Vfinal = 0; __Vfinal < 2; ++__Vfinal) {
        __Vscope_TOP.varInsert(__Vfinal,"clk", &(TOP.clk), false, VLVT_UINT8,VLVD_IN|VLVF_PUB_RW,0,0);
        __Vscope_TOP.varInsert(__Vfinal,"dn", &(TOP.dn), false, VLVT_UINT8,VLVD_OUT|VLVF_PUB_RW,0,1 ,2,0);
        __Vscope_TOP.varInsert(__Vfinal,"f", &(TOP.f), false, VLVT_UINT8,VLVD_IN|VLVF_PUB_RW,0,1 ,7,0);
        __Vscope_second_order.varInsert(__Vfinal,"BITS", const_cast<void*>(static_cast<const void*>(&(TOP.second_order__DOT__BITS))), true, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW,0,1 ,31,0);
        __Vscope_second_order.varInsert(__Vfinal,"ab", &(TOP.second_order__DOT__ab), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,1,1 ,0,1 ,7,0);
        __Vscope_second_order.varInsert(__Vfinal,"c", &(TOP.second_order__DOT__c), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,1,0 ,0,1);
        __Vscope_second_order.varInsert(__Vfinal,"c_d", &(TOP.second_order__DOT__c_d), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,1,0 ,0,1);
        __Vscope_second_order.varInsert(__Vfinal,"clk", &(TOP.second_order__DOT__clk), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
        __Vscope_second_order.varInsert(__Vfinal,"dn", &(TOP.second_order__DOT__dn), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,2,0);
        __Vscope_second_order.varInsert(__Vfinal,"f", &(TOP.second_order__DOT__f), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,7,0);
        __Vscope_second_order__stage1.varInsert(__Vfinal,"BITS", const_cast<void*>(static_cast<const void*>(&(TOP.second_order__DOT__stage1__DOT__BITS))), true, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW,0,1 ,31,0);
        __Vscope_second_order__stage1.varInsert(__Vfinal,"a", &(TOP.second_order__DOT__stage1__DOT__a), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,7,0);
        __Vscope_second_order__stage1.varInsert(__Vfinal,"ab", &(TOP.second_order__DOT__stage1__DOT__ab), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,7,0);
        __Vscope_second_order__stage1.varInsert(__Vfinal,"b", &(TOP.second_order__DOT__stage1__DOT__b), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,7,0);
        __Vscope_second_order__stage1.varInsert(__Vfinal,"c", &(TOP.second_order__DOT__stage1__DOT__c), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
        __Vscope_second_order__stage1.varInsert(__Vfinal,"clk", &(TOP.second_order__DOT__stage1__DOT__clk), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
        __Vscope_second_order__stage2.varInsert(__Vfinal,"BITS", const_cast<void*>(static_cast<const void*>(&(TOP.second_order__DOT__stage2__DOT__BITS))), true, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW,0,1 ,31,0);
        __Vscope_second_order__stage2.varInsert(__Vfinal,"a", &(TOP.second_order__DOT__stage2__DOT__a), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,7,0);
        __Vscope_second_order__stage2.varInsert(__Vfinal,"ab", &(TOP.second_order__DOT__stage2__DOT__ab), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,7,0);
        __Vscope_second_order__stage2.varInsert(__Vfinal,"b", &(TOP.second_order__DOT__stage2__DOT__b), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,7,0);
        __Vscope_second_order__stage2.varInsert(__Vfinal,"c", &(TOP.second_order__DOT__stage2__DOT__c), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
        __Vscope_second_order__stage2.varInsert(__Vfinal,"clk", &(TOP.second_order__DOT__stage2__DOT__clk), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
    }
}
