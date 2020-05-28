import time
from collections import OrderedDict

class LRUCacheDict:
    def __init__(self,max_size=1024,expiration=60):

        self.max_size=max_size
        self.expiration=expiration

        self._cache={}
        self._access_records=OrderedDict()  #记录访问时间
        self._expiration_records=OrderedDict() #记录失效时间

    def __setitem__(self, key, value):
        now = int(time.time())
        self.__delete__(key)

        self._cache[key] = value
        self._expiration_records[key]=now+self.expiration
        self._access_records[key]=now

        self.cleanup()

    def __getitem__(self, key):
        now = int(time.time())
        del self._access_records[key]
        self._access_records[key]=now
        self.cleanup()

        return self._cache[key]

    def __contains__(self, key):
        self.cleanup()
        return key in self._cache

    def __delete__(self, key):
        if key in self._cache:
            del self._cache[key]
            del self._expiration_records[key]
            del self._access_records[key]

    def cleanup(self):
        if self.expiration is None:
            return None
        pending_delete_keys=[]
        now = int(time.time())
        for k,v in self._expiration_records.items():
            if v<now:
                pending_delete_keys.append(k)
        for del_k in pending_delete_keys:
            self.__delete__(del_k)
        while (len(self._cache)> self.max_size):
            for k in self._access_records:
                self.__delete__(k)
                break

if __name__ == '__main__':
    cache_dict=LRUCacheDict(max_size=2,expiration=10)
    cache_dict['name']='lance'
    cache_dict['age']=30
    cache_dict['addr']='beijing'

    print('name' in cache_dict)
    print('age' in cache_dict)
