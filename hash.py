'''
Created on Jun 27, 2012

@author: Saber
'''
class xxhash(object):
    '''
    classdocs
    '''
    def __init__(self):
        self.prime1= int(2654435761L)
        self.prime2= int(2246822519L)
        self.prime3= int(3266489917L)
        self.prime4= 668265263
        self.prime5= 0x165667b1
    def mask(self,n):
        if n >= 0:return 2**n - 1
        else:return 0
    def _rotl(self,n, rotations=1, width=32):
        rotations %= width
        if rotations < 1:return n
        n &= self.mask(width) ## Should it be an error to truncate here?
        return ((n << rotations) & self.mask(width)) | (n >> (width - rotations))
    def _intLE(self,b,i): return (((b[i+3] & 255) << 24) + ((b[i+2] & 255) << 16) + ((b[i+1] & 255) << 8) + ((b[i+0] & 255) << 0))
    def digest_fast32(self, data, seed):
        length = len(data)
        bEnd = length
        limit = bEnd - 16
        v1 = seed + self.prime1
        v2 = v1 * self.prime2 + length
        v3 = v2 * self.prime3
        v4 = v3 * self.prime4
        i = 0
        crc = 0
        while i < limit:
            v1 = self._rotl(v1, 13) + self._intLE(data, i)
            i+= 4
            v2 = self._rotl(v2, 11) + self._intLE(data, i)
            i+= 4
            v3 = self._rotl(v3, 17) + self._intLE(data, i)
            i+= 4
            v4 = self._rotl(v4, 19) + self._intLE(data, i)
            i+=4
        
        i = bEnd - 16
        v1+= self._rotl(v1, 17)
        v2+= self._rotl(v2, 19)
        v3+= self._rotl(v3, 13)
        v4+= self._rotl(v4, 11)
        
        v1 *= self.prime1
        v2 *= self.prime1
        v3 *= self.prime1
        v4 *= self.prime1
        
        v1 += self._intLE(data, i)
        i+= 4
        v2 += self._intLE(data, i)
        i+= 4
        v3 += self._intLE(data, i)
        i+= 4
        v4 += self._intLE(data, i)
        
        v1 *= self.prime2
        v2 *= self.prime2
        v3 *= self.prime2
        v4 *= self.prime2
        
        v1+= self._rotl(v1, 11)
        v2+= self._rotl(v2, 17)
        v3+= self._rotl(v3, 19)
        v4+= self._rotl(v4, 13)
        
        v1 *= self.prime3
        v2 *= self.prime3
        v3 *= self.prime3
        v4 *= self.prime3
        
        crc = v1 + self._rotl(v2, 3) + self._rotl(v3,6) + self._rotl(v4,9)
        crc ^= crc >> 11
        crc += (self.prime4 + length) * self.prime1
        crc ^= crc >> 15
        crc *= self.prime2
        crc ^= crc >> 13
        return 0xffffffffL & crc
        
if __name__ == '__main__':
    hash = xxhash()
    b = bytearray('aaaaaaaaaaaaaaaa','utf-8')
    print hash.digest_fast32(b, 0)
    
        