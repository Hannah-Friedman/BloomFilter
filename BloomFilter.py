from BitHash import BitHash
from BitVector import BitVector

class BloomFilter(object):
    
    # calculate the estiamted bymber of bits needed for the bloom filter 
    def __bitsNeeded(self, numKeys, numHashes, maxFalsePositive):
        phi = 1 - ( maxFalsePositive ** (1/numHashes) )
        return int ( numHashes / ( 1 - ( phi**(1/numKeys) ) ) ) 
    
  
    def __init__(self, numKeys, numHashes, maxFalsePositive):
        self.__numKeys = numKeys
        self.__numHashes = numHashes
        self.__maxFalsePositive = maxFalsePositive
        
        self.__size = self.__bitsNeeded(numKeys, numHashes, maxFalsePositive)
        self.__bitVector = BitVector(size=self.__size )
        self.__numBits = 0
        
        
    
    # insert the key
    def insert(self, key):
        
        for i in range(1, self.__numHashes+1):
            
            # hash the key 
            k = BitHash(key, i) % self.__size
            
            # if the data is set to 0, set it to 1
            if self.__bitVector[k] == 0:
                self.__bitVector[k] = 1
                self.__numBits += 1
    
   
    # returns true if the key is likely in the bloom filter
    def find(self, key):
        for i in range(1, self.__numHashes+1):
            k = BitHash(key, i) % self.__size
            
            # if false, the key is definitely not present 
            if self.__bitVector[k] == 0:
                return False
            
        return True
    
    # calculates the projected rate of keys incorrectly found 
    def falsePositiveRate(self):
        phi = ( self.__size -  self.__numBits ) / self.__size
        return (1 - phi) ** self.__numHashes


    # returns the actual rate of keys incorrectly found 
    def numBitsSet(self):
        return self.__numBits
       

def __main():
    numKeys = 100000
    numHashes = 4
    maxFalse = .05  
    
    b = BloomFilter(numKeys, numHashes, maxFalse)  
    
    fin = open("wordlist.txt") 
    # create a list of all the words in the text file
    bank = []
    for line in fin:
        bank.append(line)
    
    # for the first numKeys of words, add the words to the BloomFilter
    for i in range(numKeys):
        b.insert(bank[i])
    fin.close()
    print("The theoretical false positive rate is", b.falsePositiveRate())
    
    # for the first numKeys of words, count the words which can't be found in the BloomFilter
    countMissing = 0
    for i in range(numKeys):
        if not b.find(bank[i]):
            countMissing += 1
    print("The amount of words found missing in the Bloom Filter is", countMissing)
        
    # for the next numKeys of words, count the words, falsely, found in the BloomFilter
    countFound = 0
    for i in range(numKeys, numKeys*2):
        if b.find(bank[i]):
            countFound += 1
    print("The actual false positive rate is", countFound / numKeys)    


    # Printed results:
    
    # The theoretical false positive rate is 0.05012067788662986
    # The amount of words found missing in the Bloom Filter is 0
    # The actual false positive rate is 0.05022
    
if __name__ == '__main__':
    __main()       

