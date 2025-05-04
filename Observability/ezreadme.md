### Describe SLO/SLI
#### TODO: Describe, in your own words, what the SLIs are, based on an SLO of monthly uptime and request response time.

**SLIs (Service Level Indicators)** are the actual measurements used to track if we meet our goals.  
- For a monthly uptime SLO, the SLI is the percentage of time the service was available in a month.  
- For a response time SLO, the SLI is the percentage of requests answered within the target response time.


### Creating SLI metrics.
#### TODO: It is important to know why we want to measure certain metrics for our customer. Describe in detail 5 metrics to measure these SLIs.

**Important Metrics to Measure SLIs**

1. **Uptime Percentage**  - Availability  
   Measures the proportion of time the system is available and operational.It shows the reliability users experience.

2. **Resource Utilization** - Saturation  
   The degree to which system resources (CPU, memory, I/O) are utilized.

3. **Response Time** - Latency    
   Measures how fast the service responds to user requests. It ensures most requests are answered within the target time.

4. **Error Rate**  
   Calculates the percentage of requests that fail due to errors. A low error rate means the service is stable and reliable.

5. **Throughput**  
   Shows how many requests the service handles per second or minute, helping to monitor if the service can manage the load efficiently.



