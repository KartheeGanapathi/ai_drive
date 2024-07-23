AI DRIVE HACKATHON
High Performance GCS Downloader
- Kartheepan G (20pd11)

Optimization Done:

1. Multi-threading for Improved Performance:
Utilized ThreadPoolExecutor: To handle multiple download operations concurrently, I used the ThreadPoolExecutor from the concurrent.futures module. This allowed the script to initiate multiple threads, each managing a separate download task. This approach leverages parallelism to reduce the overall download time, particularly beneficial when handling numerous small to medium-sized files.

2. Error Handling and Retries:
Added Robust Error Handling: Included comprehensive error handling to manage exceptions during download operations. This ensures that issues such as network failures or access errors are gracefully handled and logged.

3. Optimized Concurrency:
Adjustable Thread Pool Size: Configured the thread pool size to balance between optimal performance and resource constraints. This adjustment helps in managing the number of concurrent downloads, avoiding overwhelming the system or network.
Used Pool size = 16

Learnings:

1. Concurrency vs. Asynchronous Programming:
Multi-threading using ThreadPoolExecutor can be highly effective for I/O-bound tasks such as file downloads. However, asynchronous programming with asyncio could offer even better scalability and efficiency, especially for handling a large number of simultaneous I/O operations.

2. Performance Profiling:
Profiling the script to identify bottlenecks and optimize critical sections is key to improving performance. Understanding the impact of various optimizations helps in making informed decisions about trade-offs between concurrency, resource usage, and overall efficiency.

Future Plan:

1. Tuning the hyperparameter, concurrency. I’ve set 16 as concurrency.


2. Batch Processing:Download files in batches to reduce overhead and manage large numbers of files more efficiently.
