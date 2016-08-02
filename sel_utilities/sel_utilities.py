# -*- coding: utf-8 -*-

import text_data_cards as tdc
import math
import cmath


def _mag_ang_to_complex(q, d):
    """ Combines magnitude and angle of quantity to a complex number and adds
        to the dict.
        Parameters:
            q - String of quantity to be combined.
            d - Dict of quantities

        Example:
            Given d = {'VA_MAG': 1.0, 'VA_ANG': 180}
            mag_ang_to_complex('VA', d)
            will compute the complex number of 1.0 at an angle of 180 degrees
            and add new key value pair 'VA': -1 to d if 'VA' does not exist or
            update it if it does exist.
    """
    d[q] = cmath.rect(d[q+'_MAG'], math.radians(d[q+'_ANG']))


def _strip_string(q, d):
    """ Strips whitespace from string and saves back to the dict. """
    d[q] = d[q].strip()


class RelaySEL311C:
    """ Class for SEL-311C relay types. """
    def __init__(self):
        cl = [tdc.DataCard('A30, A10, A8, A10, A12',
                           ['RID', '    Date: ', 'DATE', '    Time: ', 'TIME'],
                           fixed_fields=(1, 3)),
              tdc.DataCard('A30',
                           ['TID']),
              tdc.DataCardFixedText('                 A         B         C   '
                                    '      P         G'),
              tdc.DataCard('A12, F10.3, F10.3, F10.3, F10.3, F10.3',
                           ['I MAG (A)   ', 'IA_MAG', 'IB_MAG', 'IC_MAG',
                            'IP_MAG', 'IG_MAG'],
                           fixed_fields=(0,)),
              tdc.DataCard('A11, F10.2, F10.2, F10.2, F10.2, F10.2',
                           ['I ANG (DEG)', 'IA_ANG', 'IB_ANG', 'IC_ANG',
                            'IP_ANG', 'IG_ANG'],
                           fixed_fields=(0,)),
              tdc.DataCardFixedText(''),
              tdc.DataCardFixedText('                 A         B         C   '
                                    '      S'),
              tdc.DataCard('A12, F10.3, F10.3, F10.3, F10.3',
                           ['V MAG (KV)  ', 'VA_MAG', 'VB_MAG', 'VC_MAG',
                            'VS_MAG'],
                           fixed_fields=(0,)),
              tdc.DataCard('A11, F10.2, F10.2, F10.2, F10.2',
                           ['V ANG (DEG)', 'VA_ANG', 'VB_ANG', 'VC_ANG',
                            'VS_ANG'],
                           fixed_fields=(0,)),
              tdc.DataCardFixedText(''),
              tdc.DataCardFixedText('                 A         B         C   '
                                    '      3P'),
              tdc.DataCard('A12, F10.3, F10.3, F10.3, F10.3',
                           ['MW          ', 'MW_A', 'MW_B', 'MW_C', 'MW_3P'],
                           fixed_fields=(0,)),
              tdc.DataCard('A12, F10.3, F10.3, F10.3, F10.3',
                           ['MVAR        ', 'MVAR_A', 'MVAR_B', 'MVAR_C',
                            'MVAR_3P'],
                           fixed_fields=(0,)),
              tdc.DataCard('A12, F10.3, F10.3, F10.3, F10.3',
                           ['PF          ', 'PF_A', 'PF_B', 'PF_C', 'PF_3P'],
                           fixed_fields=(0,)),
              tdc.DataCard('A12, A10, A10, A10, A10',
                           ['            ', 'PF_LEADLAG_A', 'PF_LEADLAG_B',
                            'PF_LEADLAG_C', 'PF_LEADLAG_3P'],
                           fixed_fields=(0,)),
              tdc.DataCardFixedText(''),
              tdc.DataCardFixedText('                 I1       3I2       3I0  '
                                    '      V1        V2       3V0'),
              tdc.DataCard('A12, F10.3, F10.3, F10.3, F10.3, F10.3, F10.3',
                           ['MAG         ', 'I1_MAG', '3I2_MAG', '3I0_MAG',
                            'V1_MAG', 'V2_MAG', '3V0_MAG'],
                           fixed_fields=(0,)),
              tdc.DataCard('A11, F10.2, F10.2, F10.2, F10.2, F10.2, F10.2',
                           ['ANG   (DEG)', 'I1_ANG', '3I2_ANG', '3I0_ANG',
                            'V1_ANG', 'V2_ANG', '3V0_ANG'],
                           fixed_fields=(0,)),
              tdc.DataCardFixedText(''),
              tdc.DataCard('A12, F8.2, A24, F10.1',
                           ['FREQ (Hz)   ', 'FREQ',
                            '                VDC (V) ', 'VDC'],
                           fixed_fields=(0, 2))
              ]
        self.met = tdc.DataCardStack(cl,
                                     post_read_hook=self._met_post_read_hook)

    @staticmethod
    def _met_post_read_hook(met_card):
        #  Populate V0, I2, and I0 from 3V0, 3I2, and 3I0
        #  This will help provide a standardized interface among different
        #  relays that may vary in whether they provide V0 or 3V0, etc.
        met_card.data['V0_MAG'] = met_card.data['3V0_MAG'] / 3.
        met_card.data['V0_ANG'] = met_card.data['3V0_ANG']
        met_card.data['I2_MAG'] = met_card.data['3I2_MAG'] / 3.
        met_card.data['I2_ANG'] = met_card.data['3I2_ANG']
        met_card.data['I0_MAG'] = met_card.data['3I0_MAG'] / 3.
        met_card.data['I0_ANG'] = met_card.data['3I0_ANG']

        #  Add complex quantities to data dict. This will be a convenience for
        #  functions that use this class as the basis for computations.
        quantities = ['IA', 'IB', 'IC', 'IP', 'IG',
                      'VA', 'VB', 'VC', 'VS',
                      'V1', 'V2', '3V0', 'I1', '3I2', '3I0',
                      'V0', 'I2', 'I0']

        for q in quantities:
            _mag_ang_to_complex(q, met_card.data)

        for ph in ['A', 'B', 'C', '3P']:
            met_card.data['S_' + ph] = complex(met_card.data['MW_' + ph],
                                               met_card.data['MVAR_' + ph])

        # Trim whitespace from lead/lag
        for ph in ['A', 'B', 'C', '3P']:
            _strip_string('PF_LEADLAG_' + ph, met_card.data)

        # Trim whitespace from RID and TID
        _strip_string('RID', met_card.data)
        _strip_string('TID', met_card.data)
