daniil@daniil-HN-WX9X:~$ ab -n 1000 -c 10 http://localhost/sample.html
This is ApacheBench, Version 2.3 <$Revision: 1903618 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking localhost (be patient)
Completed 100 requests
Completed 200 requests
Completed 300 requests
Completed 400 requests
Completed 500 requests
Completed 600 requests
Completed 700 requests
Completed 800 requests
Completed 900 requests
Completed 1000 requests
Finished 1000 requests

Server Software: nginx/1.24.0
Server Hostname: localhost
Server Port: 80

Document Path: /sample.html
Document Length: 84712 bytes

Concurrency Level: 10
Time taken for tests: 0.103 seconds
Complete requests: 1000
Failed requests: 0
Total transferred: 85051000 bytes
HTML transferred: 84712000 bytes
Requests per second: 9753.05 [#/sec] (mean)
Time per request: 1.025 [ms] (mean)
Time per request: 0.103 [ms] (mean, across all concurrent requests)
Transfer rate: 810065.32 [Kbytes/sec] received

Connection Times (ms)
min mean[+/-sd] median max
Connect: 0 0 0.1 0 1
Processing: 0 1 0.1 1 2
Waiting: 0 0 0.1 0 1
Total: 0 1 0.1 1 2

Percentage of the requests served within a certain time (ms)
50% 1
66% 1
75% 1
80% 1
90% 1
95% 1
98% 1
99% 1
100% 2 (longest request)

==========================================================================

daniil@daniil-HN-WX9X:~$ ab -n 1000 -c 10 http://127.0.0.1:8000/static/sample.html
This is ApacheBench, Version 2.3 <$Revision: 1903618 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 127.0.0.1 (be patient)
Completed 100 requests
Completed 200 requests
Completed 300 requests
Completed 400 requests
Completed 500 requests
Completed 600 requests
Completed 700 requests
Completed 800 requests
Completed 900 requests
Completed 1000 requests
Finished 1000 requests

Server Software: gunicorn
Server Hostname: 127.0.0.1
Server Port: 8000

Document Path: /static/sample.html
Document Length: 84712 bytes

Concurrency Level: 10
Time taken for tests: 0.628 seconds
Complete requests: 1000
Failed requests: 0
Total transferred: 85079000 bytes
HTML transferred: 84712000 bytes
Requests per second: 1591.65 [#/sec] (mean)
Time per request: 6.283 [ms] (mean)
Time per request: 0.628 [ms] (mean, across all concurrent requests)
Transfer rate: 132242.56 [Kbytes/sec] received

Connection Times (ms)
min mean[+/-sd] median max
Connect: 0 0 0.1 0 1
Processing: 3 6 1.5 6 15
Waiting: 2 6 1.5 5 14
Total: 4 6 1.5 6 15

Percentage of the requests served within a certain time (ms)
50% 6
66% 6
75% 6
80% 6
90% 7
95% 8
98% 13
99% 14
100% 15 (longest request)

==========================================================================

daniil@daniil-HN-WX9X:~$ ab -n 1000 -c 10 http://127.0.0.1:8000/
This is ApacheBench, Version 2.3 <$Revision: 1903618 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 127.0.0.1 (be patient)
Completed 100 requests
Completed 200 requests
Completed 300 requests
Completed 400 requests
Completed 500 requests
Completed 600 requests
Completed 700 requests
Completed 800 requests
Completed 900 requests
Completed 1000 requests
Finished 1000 requests

Server Software: gunicorn
Server Hostname: 127.0.0.1
Server Port: 8000

Document Path: /
Document Length: 121542 bytes

Concurrency Level: 10
Time taken for tests: 125.459 seconds
Complete requests: 1000
Failed requests: 0
Total transferred: 121840000 bytes
HTML transferred: 121542000 bytes
Requests per second: 7.97 [#/sec] (mean)
Time per request: 1254.594 [ms] (mean)
Time per request: 125.459 [ms] (mean, across all concurrent requests)
Transfer rate: 948.39 [Kbytes/sec] received

Connection Times (ms)
min mean[+/-sd] median max
Connect: 0 0 0.1 0 1
Processing: 238 1247 83.8 1250 1490
Waiting: 237 1246 83.8 1249 1489
Total: 238 1247 83.8 1250 1490

Percentage of the requests served within a certain time (ms)
50% 1250
66% 1270
75% 1283
80% 1291
90% 1313
95% 1331
98% 1370
99% 1398
100% 1490 (longest request)

==========================================================================

daniil@daniil-HN-WX9X:~$ ab -n 1000 -c 10 http://localhost/
This is ApacheBench, Version 2.3 <$Revision: 1903618 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking localhost (be patient)
Completed 100 requests
Completed 200 requests
Completed 300 requests
Completed 400 requests
Completed 500 requests
Completed 600 requests
Completed 700 requests
Completed 800 requests
Completed 900 requests
Completed 1000 requests
Finished 1000 requests

Server Software: nginx/1.24.0
Server Hostname: localhost
Server Port: 80

Document Path: /
Document Length: 121542 bytes

Concurrency Level: 10
Time taken for tests: 1.487 seconds
Complete requests: 1000
Failed requests: 0
Total transferred: 121876000 bytes
HTML transferred: 121542000 bytes
Requests per second: 672.63 [#/sec] (mean)
Time per request: 14.867 [ms] (mean)
Time per request: 1.487 [ms] (mean, across all concurrent requests)
Transfer rate: 80055.81 [Kbytes/sec] received

Connection Times (ms)
min mean[+/-sd] median max
Connect: 0 0 0.1 0 1
Processing: 0 8 82.0 0 1250
Waiting: 0 8 81.9 0 1250
Total: 0 8 82.1 0 1250

Percentage of the requests served within a certain time (ms)
50% 0
66% 0
75% 0
80% 0
90% 0
95% 0
98% 0
99% 236
100% 1250 (longest request)

==========================================================================

daniil@daniil-HN-WX9X:~$ ab -n 1000 -c 10 http://localhost/
This is ApacheBench, Version 2.3 <$Revision: 1903618 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking localhost (be patient)
Completed 100 requests
Completed 200 requests
Completed 300 requests
Completed 400 requests
Completed 500 requests
Completed 600 requests
Completed 700 requests
Completed 800 requests
Completed 900 requests
Completed 1000 requests
Finished 1000 requests

Server Software: nginx/1.24.0
Server Hostname: localhost
Server Port: 80

Document Path: /
Document Length: 121542 bytes

Concurrency Level: 10
Time taken for tests: 0.120 seconds
Complete requests: 1000
Failed requests: 0
Total transferred: 121896000 bytes
HTML transferred: 121542000 bytes
Requests per second: 8299.72 [#/sec] (mean)
Time per request: 1.205 [ms] (mean)
Time per request: 0.120 [ms] (mean, across all concurrent requests)
Transfer rate: 987990.82 [Kbytes/sec] received

Connection Times (ms)
min mean[+/-sd] median max
Connect: 0 0 0.1 0 1
Processing: 0 1 0.2 1 3
Waiting: 0 0 0.1 0 1
Total: 1 1 0.3 1 3

Percentage of the requests served within a certain time (ms)
50% 1
66% 1
75% 1
80% 1
90% 1
95% 1
98% 2
99% 3
100% 3 (longest request)
