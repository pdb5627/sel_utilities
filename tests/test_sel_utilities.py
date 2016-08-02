#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_sel_utilities
----------------------------------

Tests for `sel_utilities` module.
"""

import pytest


from sel_utilities import sel_utilities as su


@pytest.fixture()
def sel311c_met():
    return """BROKEN BOW 11S-02                 Date: 07/21/16    Time: 16:51:54.489
L1140C, PCB1102, BRK BOW-CALWY
                 A         B         C         P         G
I MAG (A)      200.563   213.328   202.246     7.309     7.424
I ANG (DEG)   -153.23     83.14    -39.40    -68.75    -68.60

                 A         B         C         S
V MAG (KV)      68.819    69.061    69.014    68.758
V ANG (DEG)      0.00   -119.91    119.89   -119.69

                 A         B         C         3P
MW             -12.323   -13.556   -13.056   -38.935
MVAR             6.218     5.769     4.936    16.924
PF              -0.893    -0.920    -0.935    -0.917
                 LEAD      LEAD      LEAD      LEAD

                 I1       3I2       3I0        V1        V2       3V0
MAG            205.182    30.990     7.424    68.965     0.142     0.031
ANG   (DEG)   -156.51    -37.31    -68.60     -0.01    172.65   -120.98

FREQ (Hz)      59.99                VDC (V)      133.4""".split('\n')


@pytest.fixture()
def sel311c_met_values():
    return {'RID': 'BROKEN BOW 11S-02',
            'TID': 'L1140C, PCB1102, BRK BOW-CALWY',
            'DATE': '07/21/16',
            'TIME': '16:51:54.489',
            'IA_MAG': 200.563,
            'IB_MAG': 213.328,
            'IC_MAG': 202.246,
            'IP_MAG': 7.309,
            'IG_MAG': 7.424,
            'IA_ANG': -153.23,
            'IB_ANG': 83.14,
            'IC_ANG': -39.40,
            'IP_ANG': -68.75,
            'IG_ANG': -68.60,
            'VA_MAG': 68.819,
            'VB_MAG': 69.061,
            'VC_MAG': 69.014,
            'VS_MAG': 68.758,
            'VA_ANG': 0.00,
            'VB_ANG': -119.91,
            'VC_ANG': 119.89,
            'VS_ANG': -119.69,
            'MW_A': -12.323,
            'MW_B': -13.556,
            'MW_C': -13.056,
            'MW_3P': -38.935,
            'MVAR_A': 6.218,
            'MVAR_B': 5.769,
            'MVAR_C': 4.936,
            'MVAR_3P': 16.924,
            'PF_A': -0.893,
            'PF_B': -0.920,
            'PF_C': -0.935,
            'PF_3P': -0.917,
            'PF_LEADLAG_A': 'LEAD',
            'PF_LEADLAG_B': 'LEAD',
            'PF_LEADLAG_C': 'LEAD',
            'PF_LEADLAG_3P': 'LEAD',
            'I1_MAG': 205.182,
            '3I2_MAG': 30.990,
            '3I0_MAG': 7.424,
            'V1_MAG': 68.965,
            'V2_MAG': 0.142,
            '3V0_MAG': 0.031,
            'I1_ANG': -156.51,
            '3I2_ANG': -37.31,
            '3I0_ANG': -68.60,
            'V1_ANG': -0.01,
            'V2_ANG': 172.65,
            '3V0_ANG': -120.98,
            'FREQ': 59.99,
            'VDC': 133.4}


@pytest.fixture()
def sel421_met():
    return """BROKEN BOW 11S-08 SEL-421 NON-PILOT        Date: 07/21/2016  Time: 16:54:23.886
L1074 BROKEN BOW-CROOKED CREEK             Serial Number: 1111780371

                      Phase Currents
                 IA        IB        IC
I MAG (A)       199.332   207.757   203.639
I ANG (DEG)    -149.68     89.01    -34.45

                      Phase Voltages                Phase-Phase Voltages
                 VA        VB        VC           VAB       VBC       VCA
V MAG (kV)       68.818    69.048    69.016      119.320   119.726   119.284
V ANG (DEG)       0.00   -119.87    119.86        30.12    -90.00    149.89

                    Sequence Currents (A)          Sequence Voltages (kV)
                  I1        3I2       3I0         V1        3V2       3V0
MAG             203.452    22.266     8.077      68.961     0.503     0.077
ANG (DEG)      -151.71    -11.83    -93.84        0.00    175.88    -14.17

                   A           B           C             3P
P (MW)           -11.84      -12.56      -12.66         -37.07
Q (MVAR)           6.92        6.93        6.09          19.94
S (MVA)           13.72       14.35       14.05          42.09
POWER FACTOR       0.86        0.88        0.90           0.88
                   LEAD        LEAD        LEAD           LEAD

FREQ (Hz)       60.00       VDC1(V)   133.67""".split('\n')


@pytest.fixture()
def sel421_met_values():
    return {'RID': 'BROKEN BOW 11S-08 SEL-421 NON-PILOT',
            'TID': 'L1074 BROKEN BOW-CROOKED CREEK',
            'S_N': '1111780371',
            'DATE': '07/21/2016',
            'TIME': '16:54:23.886',
            'IA_MAG': 199.332,
            'IB_MAG': 207.757,
            'IC_MAG': 203.639,
            'IA_ANG': -149.68,
            'IB_ANG': 89.01,
            'IC_ANG': -34.45,
            'VA_MAG': 68.818,
            'VB_MAG': 69.048,
            'VC_MAG': 69.016,
            'VA_ANG': 0.00,
            'VB_ANG': -119.87,
            'VC_ANG': 119.86,
            'VAB_MAG': 119.320,
            'VBC_MAG': 119.726,
            'VCA_MAG': 119.284,
            'VAB_ANG': 30.12,
            'VBC_ANG': -90.00,
            'VCA_ANG': 149.89,
            'I1_MAG': 203.452,
            '3I2_MAG': 22.266,
            '3I0_MAG': 8.077,
            'V1_MAG': 68.961,
            '3V2_MAG': 0.503,
            '3V0_MAG': 0.077,
            'I1_ANG': -151.71,
            '3I2_ANG': -11.83,
            '3I0_ANG': -93.84,
            'V1_ANG': 0.00,
            '3V2_ANG': 175.88,
            '3V0_ANG': -14.17,
            'MW_A': -11.84,
            'MW_B': -12.56,
            'MW_C': -12.66,
            'MW_3P': -37.07,
            'MVAR_A': 6.92,
            'MVAR_B': 6.93,
            'MVAR_C': 6.09,
            'MVAR_3P': 19.94,
            'S_A_MAG': 13.72,
            'S_B_MAG': 14.35,
            'S_C_MAG': 14.05,
            'S_3P_MAG': 42.09,
            'PF_A': 0.86,
            'PF_B': 0.88,
            'PF_C': 0.90,
            'PF_3P': 0.88,
            'PF_LEADLAG_A': 'LEAD',
            'PF_LEADLAG_B': 'LEAD',
            'PF_LEADLAG_C': 'LEAD',
            'PF_LEADLAG_3P': 'LEAD',
            'FREQ': 60.00,
            'VDC1': 133.67}

def test_sel311c_parse_met(sel311c_met, sel311c_met_values):
    tc = su.RelaySEL311C().met
    assert tc.match(sel311c_met) is True
    tc.read(sel311c_met)
    for k, v in sel311c_met_values.items():
        assert tc.data[k] == v


def test_sel421_parse_met(sel421_met, sel421_met_values):
    tc = su.RelaySEL421().met
    #assert tc.match(sel421_met) is True
    tc.read(sel421_met)
    for k, v in sel421_met_values.items():
        assert tc.data[k] == v
