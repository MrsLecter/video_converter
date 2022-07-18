## DESCRIPTION
<p>Converts the downloaded file to .mp3. Forms task queue in Celery, it is possible to track task statu</p>

### Avaliable endpoints
<p><code>/convert</code> - accepts the file and returns the task ID</p>
<p><code>/check/<task_id></code> - shows the task status</p>

### HOW TO USE
<ul>
<li>1)start RabbitMQ container: sudo docker run -d -p 5672:5672 rabbitmq</li>
<li>2)start celery: celery -A celery_worker worker -Q hipri</li>
<li>3)start main.py</li>
</ul>
