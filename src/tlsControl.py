from cgitb import text
from inspect import _void


class TLSControl:

    # light_id, [positions]
    map_mask = {}
    # light_id, {pos, val}
    tls_state = {}

    def __init__(self, id, mask, start_val):
        self.id = id
        self.mask = mask
        self.state_str = start_val
        self.__decode_mask()
        self.__decode_start_val()
        self.print_state()

    def __decode_mask(self) -> None:
        """
        Decodes the mask of the traffic light.
        The mask is in from of 112233, 111222333 or similar.
        """
        # get chars from mask
        chars = list(self.mask)
        for idx, char in enumerate(chars):
            if char not in self.map_mask:
                self.map_mask[char] = [int(idx)]
            else:
                self.map_mask[char].append(int(idx))

    def __decode_start_val(self) -> None:
        """
        Decodes the start value of the traffic light.
        The start value is in from of ggyyrr, ggyyrrrrr or similar.
        """
        self.tls_state = {}
        chars = list(self.state_str)
        for light_id, pos in self.map_mask.items():
            for ps in pos:
                if ps < len(chars):
                    if light_id in self.tls_state:
                        self.tls_state[light_id]["val"].append(chars[ps])
                    else:
                        self.tls_state[light_id] = {"pos": ps, "val": [chars[ps]]}

    def __encode_tls_state(self) -> text:
        """
        Encodes the traffic light state.
        """
        state = ""
        for light_id, val in self.tls_state.items():
            for v in val["val"]:
                state += v

        return state

    def print_state(self) -> None:
        """
        Prints the traffic light state.
        """
        print(self.state_str)
        print(self.tls_state)
        print("\n")

    def set_state(self, state_str) -> None:
        """
        Sets the traffic light to the given state.
        """
        self.state_str = state_str
        self.__decode_start_val()
        self.__encode_tls_state()

    def set(self, light_id, pos, value) -> text:
        """
        Sets the traffic light to the given value.
        """
        self.tls_state[light_id]['val'][pos] = value
        self.state_str = self.__encode_tls_state()
        return self.state_str
