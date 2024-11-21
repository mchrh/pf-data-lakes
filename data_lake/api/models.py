from django.db import models

class Transaction(models.Model):
    transaction_id = models.CharField(max_length=100, primary_key=True)
    customer_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField()
    is_high_value = models.BooleanField(default=False)

    class Meta:
        ordering = ['-transaction_date']

    def __str__(self):
        return f"Transaction {self.transaction_id}"

    def save(self, *args, **kwargs):
        self.is_high_value = self.amount > 1000
        super().save(*args, **kwargs)

class WebLog(models.Model):
    timestamp = models.DateTimeField()
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    hour = models.IntegerField()
    request_count = models.IntegerField()
    error_count = models.IntegerField()
    total_bytes = models.BigIntegerField()

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['year', 'month', 'day', 'hour']),
        ]

    def __str__(self):
        return f"Log {self.timestamp}"

    def save(self, *args, **kwargs):
        self.year = self.timestamp.year
        self.month = self.timestamp.month
        self.day = self.timestamp.day
        self.hour = self.timestamp.hour
        super().save(*args, **kwargs)

class Campaign(models.Model):
    campaign_id = models.CharField(max_length=100, primary_key=True)
    total_clicks = models.IntegerField(default=0)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    unique_users = models.IntegerField(default=0)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"Campaign {self.campaign_id}"

    @property
    def duration_days(self):
        return (self.end_date - self.start_date).days

    @property
    def cost_per_click(self):
        if self.total_clicks > 0:
            return self.total_cost / self.total_clicks
        return 0