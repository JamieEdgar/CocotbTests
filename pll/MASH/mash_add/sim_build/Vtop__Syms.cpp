// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table implementation internals

#include "Vtop__pch.h"
#include "Vtop.h"
#include "Vtop___024root.h"

// FUNCTIONS
Vtop__Syms::~Vtop__Syms()
{

    // Tear down scope hierarchy
    __Vhier.remove(0, &__Vscope_mash_add);

}

Vtop__Syms::Vtop__Syms(VerilatedContext* contextp, const char* namep, Vtop* modelp)
    : VerilatedSyms{contextp}
    // Setup internal state of the Syms class
    , __Vm_modelp{modelp}
    // Setup module instances
    , TOP{this, namep}
{
        // Check resources
        Verilated::stackCheck(25);
    // Configure time unit / time precision
    _vm_contextp__->timeunit(-12);
    _vm_contextp__->timeprecision(-12);
    // Setup each module's pointers to their submodules
    // Setup each module's pointer back to symbol table (for public functions)
    TOP.__Vconfigure(true);
    // Setup scopes
    __Vscope_TOP.configure(this, name(), "TOP", "TOP", "<null>", 0, VerilatedScope::SCOPE_OTHER);
    __Vscope_mash_add.configure(this, name(), "mash_add", "mash_add", "mash_add", -12, VerilatedScope::SCOPE_MODULE);

    // Set up scope hierarchy
    __Vhier.add(0, &__Vscope_mash_add);

    // Setup export functions
    for (int __Vfinal = 0; __Vfinal < 2; ++__Vfinal) {
        __Vscope_TOP.varInsert(__Vfinal,"c", &(TOP.c), false, VLVT_UINT8,VLVD_IN|VLVF_PUB_RW,0,0);
        __Vscope_TOP.varInsert(__Vfinal,"clk", &(TOP.clk), false, VLVT_UINT8,VLVD_IN|VLVF_PUB_RW,0,0);
        __Vscope_TOP.varInsert(__Vfinal,"dn", &(TOP.dn), false, VLVT_UINT8,VLVD_IN|VLVF_PUB_RW,0,1 ,2,0);
        __Vscope_TOP.varInsert(__Vfinal,"dn_d", &(TOP.dn_d), false, VLVT_UINT8,VLVD_IN|VLVF_PUB_RW,0,1 ,2,0);
        __Vscope_TOP.varInsert(__Vfinal,"result", &(TOP.result), false, VLVT_UINT8,VLVD_OUT|VLVF_PUB_RW,0,1 ,3,0);
        __Vscope_mash_add.varInsert(__Vfinal,"c", &(TOP.mash_add__DOT__c), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
        __Vscope_mash_add.varInsert(__Vfinal,"clk", &(TOP.mash_add__DOT__clk), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
        __Vscope_mash_add.varInsert(__Vfinal,"dn", &(TOP.mash_add__DOT__dn), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,2,0);
        __Vscope_mash_add.varInsert(__Vfinal,"dn_d", &(TOP.mash_add__DOT__dn_d), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,2,0);
        __Vscope_mash_add.varInsert(__Vfinal,"result", &(TOP.mash_add__DOT__result), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,3,0);
    }
}
