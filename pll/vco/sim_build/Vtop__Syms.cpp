// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table implementation internals

#include "Vtop__pch.h"
#include "Vtop.h"
#include "Vtop___024root.h"

// FUNCTIONS
Vtop__Syms::~Vtop__Syms()
{

    // Tear down scope hierarchy
    __Vhier.remove(0, &__Vscope_vco);

}

Vtop__Syms::Vtop__Syms(VerilatedContext* contextp, const char* namep, Vtop* modelp)
    : VerilatedSyms{contextp}
    // Setup internal state of the Syms class
    , __Vm_modelp{modelp}
    // Setup module instances
    , TOP{this, namep}
{
        // Check resources
        Verilated::stackCheck(27);
    // Configure time unit / time precision
    _vm_contextp__->timeunit(-12);
    _vm_contextp__->timeprecision(-12);
    // Setup each module's pointers to their submodules
    // Setup each module's pointer back to symbol table (for public functions)
    TOP.__Vconfigure(true);
    // Setup scopes
    __Vscope_TOP.configure(this, name(), "TOP", "TOP", "<null>", 0, VerilatedScope::SCOPE_OTHER);
    __Vscope_vco.configure(this, name(), "vco", "vco", "vco", -12, VerilatedScope::SCOPE_MODULE);

    // Set up scope hierarchy
    __Vhier.add(0, &__Vscope_vco);

    // Setup export functions
    for (int __Vfinal = 0; __Vfinal < 2; ++__Vfinal) {
        __Vscope_TOP.varInsert(__Vfinal,"clk", &(TOP.clk), false, VLVT_UINT8,VLVD_IN|VLVF_PUB_RW,0,0);
        __Vscope_TOP.varInsert(__Vfinal,"x", &(TOP.x), false, VLVT_UINT8,VLVD_IN|VLVF_PUB_RW,0,1 ,7,0);
        __Vscope_TOP.varInsert(__Vfinal,"y", &(TOP.y), false, VLVT_REAL,VLVD_OUT|VLVF_PUB_RW|VLVF_DPI_CLAY,0,0);
        __Vscope_vco.varInsert(__Vfinal,"BITS", const_cast<void*>(static_cast<const void*>(&(TOP.vco__DOT__BITS))), true, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW,0,1 ,31,0);
        __Vscope_vco.varInsert(__Vfinal,"angle", &(TOP.vco__DOT__angle), false, VLVT_REAL,VLVD_NODIR|VLVF_PUB_RW|VLVF_DPI_CLAY,0,0);
        __Vscope_vco.varInsert(__Vfinal,"clk", &(TOP.vco__DOT__clk), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
        __Vscope_vco.varInsert(__Vfinal,"offset", &(TOP.vco__DOT__offset), false, VLVT_REAL,VLVD_NODIR|VLVF_PUB_RW|VLVF_DPI_CLAY,0,0);
        __Vscope_vco.varInsert(__Vfinal,"x", &(TOP.vco__DOT__x), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,7,0);
        __Vscope_vco.varInsert(__Vfinal,"y", &(TOP.vco__DOT__y), false, VLVT_REAL,VLVD_NODIR|VLVF_PUB_RW|VLVF_DPI_CLAY,0,0);
    }
}
