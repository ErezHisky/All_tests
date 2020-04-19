
class TheBuffer():
    def __init__(self):
        self.outSeqNum = 5

    def getHeader(self):

        list = []
        list.append('DE')
        list.append('AD')
        list.append('BE')
        list.append('EF')
        list.append(hex(self.outSeqNum))
        list.append(hex(self.outSeqNum >> 8))

        buffer = [int(element, 16) for element in list]
        return buffer
    
    def getDataHeader(self):

        list = []
        list.append('DE')
        list.append('AD')
        list.append('BE')
        list.append('EF')
        
        buffer = [int(element, 16) for element in list]
        return buffer

    def int_to_bytes(x: int) -> bytes:
        return x.to_bytes((x.bit_length() + 7) // 8, 'big')

    def test(self):
        print(hex(self.outSeqNum))
        print(hex(self.outSeqNum >> 8))
        print(self.int_to_bytes(222) )

if __name__ == "__main__":
    tb = TheBuffer()
    print(tb.getHeader())
    tb.test()
