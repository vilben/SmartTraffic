class JunctionControl:
    def __init__(self, tlsId):
        self.tlsId = tlsId
        self.activeFactors = {}
        self.acquiredBy = None

    def declareActive(self, factor, reason, edge, lane):
        self.activeFactors[factor] = {
            "reason": reason,
            "edge": edge,
            "lane": lane,
        }

    def declareInactive(self, factor):
        if factor in self.activeFactors:
            del self.activeFactors[factor]

    def getActiveFactors(self):
        return self.activeFactors

    def getAcquiredBy(self):
        return self.acquiredBy

    def isOwner(self, factor):
        return self.acquiredBy == factor

    def getFactorLength(self):
        return len(self.activeFactors)

    def acquireJunction(self, factor):
        if self.acquiredBy is None:
            self.acquiredBy = factor
            return True
        return False

    def releaseJunction(self, factor):
        if self.acquiredBy == factor:
            self.acquiredBy = None
            return True
        return False


class JunctionManager:
    def __init__(self):
        self.activelyControlledJunctions = {}

    def getJunctionControl(self, tlsId):
        if tlsId not in self.activelyControlledJunctions:
            self.activelyControlledJunctions[tlsId] = JunctionControl(tlsId)

        return self.activelyControlledJunctions[tlsId]

    def releaseJunctionControl(self, tlsId) -> JunctionControl:
        if tlsId in self.activelyControlledJunctions:
            del self.activelyControlledJunctions[tlsId]
