from .memorix_api import MemorixApi




def start() -> None :
    api = MemorixApi(redis_url="redis://localhost:6379/0")
    for msg in api.pubsub.record.subscribe():
        record_key = msg.payload
        api._redis.expire(f"iq_data_{record_key}", 60)
        
        record_data = api.cache.record_data.get(key=record_key)
        print (f"freq is {record_data.curr_detection_range.f_start_mhz}MHz,i is {record_data.iteration_num}")
    
        record = api._redis.get(f"iq_data_{record_key}")
        print(record)