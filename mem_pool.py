from cacheout import Cache
from collections import deque
from replica import Replica
class MemPool:
    transaction_queue:deque
    pending_transaction:set
    queue_cntr:int
    req_cache=Cache() 
    def __init__(self):
        pass
    @classmethod
    def get_transactions(cls):
        txn = cls.transaction_queue.popleft()
        txn_id=txn[:txn.index(':')]
        cls.req_cache.add(txn_id,"processing")
        return txn

    @classmethod
    def push_transaction(cls,txn):
        txn_id = txn[:txn.index(':')]
        if(not cls.req_cache.has(txn_id)):
            cls.pending_transaction.add(txn_id)
            cls.transaction_queue.append(txn)
            cls.req_cache.add(txn_id,"In queue, not processed")
        else:
            Replica.send_response(txn_id,cls.req_cache.get(txn_id))

    @classmethod
    def processed_txns(cls,txns):
        for txn in txns:
            txn_id=txn[:txn.index(':')]
            cls.req_cache.set(txn_id,"processed")
            cls.pending_transaction.discard(txn_id)
            Replica.send_response(txn_id,cls.req_cache.get(txn_id))

   
        


