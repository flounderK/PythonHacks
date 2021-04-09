#!/usr/bin/python3


class BitfieldManipulator:
    """An interface for easily manipulating the values the compose bitfields
        Example:
        Input descriptor:
        {'field1': 3,
         'field2': 4,
         'field3': 2}
        field1: 00 0000 111
        field2: 00 1111 000
        field3: 11 0000 000
    """
    def __init__(self, descriptor: dict):
        assert isinstance(descriptor, dict)
        if all([isinstance(v, int) for v in descriptor.values()]):
            self._bitfield_mask_descriptor = self.make_bitfield_mask_descriptor(descriptor)
        elif all([isinstance(v, (list, tuple)) for v in descriptor.values()]):
            self._bitfield_mask_descriptor = descriptor.copy()
        else:
            raise Exception("Values of descriptor must be either all ints or all lists")

    @staticmethod
    def make_bitfield_mask_descriptor(bitmask_bit_descriptor):
        """In order from lowest (LE rightmost) values to highest values to create
        a mask
        returns a dictionary in the form {"field1": [bitmask, bit_shift]}.

        Example:
        Input descriptor:
        {'field1': 3,
         'field2': 4,
         'field3': 2}
        field1: 00 0000 111
        field2: 00 1111 000
        field3: 11 0000 000

        returns:
        {"field1": [7, 0],
         "field2": [56, 3],
         "field3": [196, 6]}

        """
        bitmask_descriptor = dict()
        mask_shift = 0
        for k, v in bitmask_bit_descriptor.items():
            mask = ((1 << v) - 1) << mask_shift
            bitmask_descriptor[k] = [mask, mask_shift]
            mask_shift += v
        return bitmask_descriptor

    def to_bitfield(self, **kwargs):
        """Given a descriptor of the form {"mode": [field_mask, field_bitshift]},
        and kwargs corresponding to the keys in the descriptor, create a
        bitfield"""

        bitfield = 0
        for k, v in kwargs.items():
            if k not in self._bitfield_mask_descriptor.keys():
                # skip if keyname doesn't exist
                continue
            mask, shift = self._bitfield_mask_descriptor[k]
            bitfield += (v << shift) & mask

        return bitfield

    def from_bitfield(self, bitfield):
        """Given a bitfield and a bitfield_mask_descriptor, separate the bitfield
        out to the fields that it is composed of"""
        fields = dict()
        for k, [mask, shift] in self._bitfield_mask_descriptor.items():
            fields[k] = (mask & bitfield) >> shift
        return fields

    def __repr__(self):
        # TODO: right align this
        return "\n".join(["%s: %s" % (k, bin(mask)) for k, [mask, shift] in
                          self._bitfield_mask_descriptor.items()])


if __name__ == "__main__":
    NTP_BITMASK_BIT_DESCRIPTOR = {"mode": 3,
                                  "version": 3,
                                  "leap_indicator": 2}
    bf = BitfieldManipulator(NTP_BITMASK_BIT_DESCRIPTOR)
    print(hex(bf.to_bitfield(mode=3, version=4)))

