from cgitb import text
import logging


class TLSControl:

    # light_id, [positions]
    map_mask = {}
    # light_id, {pos, val}
    tls_state = {}

    def __init__(self, id, mask, start_val):
        self.id = id
        self.mask = mask
        self.state_str = start_val
        self.__decodeMask()
        self.__decodeStartValue()

    def __decodeMask(self) -> None:
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

    def __decodeStartValue(self) -> None:
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

    def __encodeTLSState(self) -> text:
        """
        Encodes the traffic light state.
        """
        state = ""
        for light_id, val in self.tls_state.items():
            for v in val["val"]:
                state += v

        return state

    def logState(self) -> None:
        """
        Prints the traffic light state.
        """
        logging.debug(self.state_str)
        logging.debug(self.tls_state)
        logging.debug("\n")

    def setState(self, state_str) -> None:
        """
        Sets the traffic light to the given state.
        """
        self.state_str = state_str
        self.__decodeStartValue()
        self.__encodeTLSState()

    def set(self, light_id, pos, value) -> text:
        """
        Sets the traffic light to the given value.
        """
        self.tls_state[light_id]['val'][pos] = value
        self.state_str = self.__encodeTLSState()
        return self.state_str
