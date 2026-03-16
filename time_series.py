from collections import defaultdict
import math
class TimeSeries:
    def __init__(s, name=""): s.name=name; s.data=[]
    def add(s, timestamp, value): s.data.append((timestamp, value)); s.data.sort()
    def range(s, start, end): return [(t,v) for t,v in s.data if start<=t<=end]
    def last(s, n=1): return s.data[-n:]
    def moving_avg(s, window=3):
        result = []
        for i in range(len(s.data)):
            start = max(0, i-window+1)
            vals = [v for _,v in s.data[start:i+1]]
            result.append((s.data[i][0], sum(vals)/len(vals)))
        return result
    def resample(s, bucket_size):
        buckets = defaultdict(list)
        for t,v in s.data: buckets[t//bucket_size*bucket_size].append(v)
        return [(k, sum(v)/len(v)) for k,v in sorted(buckets.items())]
    def stats(s):
        vals = [v for _,v in s.data]
        if not vals: return {}
        mn, mx = min(vals), max(vals); avg = sum(vals)/len(vals)
        var = sum((v-avg)**2 for v in vals)/len(vals)
        return {"count":len(vals),"min":mn,"max":mx,"avg":round(avg,2),"std":round(math.sqrt(var),2)}
def demo():
    ts = TimeSeries("cpu")
    for i in range(20): ts.add(i*60, 30 + 20*math.sin(i*0.5) + (i%3)*5)
    print(f"Stats: {ts.stats()}")
    print(f"Last 3: {ts.last(3)}")
    ma = ts.moving_avg(5)
    print(f"Moving avg (last 3): {[(t,round(v,1)) for t,v in ma[-3:]]}")
    resampled = ts.resample(300)
    print(f"5min buckets: {len(resampled)} points")
if __name__ == "__main__": demo()
