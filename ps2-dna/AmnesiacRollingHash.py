class AmnesiacRollingHash:
    def  __init__(self, base=256, prime = 1009):
        self.hash_value = 0
        self.base = base
        self.prime = prime
        #self.inv_base = pow(base, prime - 2, prime)
        self.inv_base = 6950663
        self.skip_multiplier = 1

    def append(self, value):
        self.hash_value = (self.hash_value * self.base + value) % self.prime
        self.skip_multiplier = (self.skip_multiplier * self.base) % self.prime

    def skip(self, value):
        self.skip_multiplier = (self.skip_multiplier * self.inv_base) % self.prime
        self.hash_value = (self.hash_value + self.prime - (value * self.skip_multiplier) % self.prime) %self.prime


