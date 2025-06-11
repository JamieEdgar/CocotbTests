class prescaler:
    def __init__(self, p=8):
        self.p=p
        self.count = 0
        self.output = 0

    def step(self):
        self.count = self.count + 1
        if self.count == self.p:
            self.output = (self.output + 1) % 2
            self.count = 0
        print(self.output)

pre = prescaler()
for i in range(50):
    pre.step()
