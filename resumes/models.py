from django.contrib.auth.models import User
from django.db import models

class MatchResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resume_file = models.FileField(upload_to='resumes/', null=True)
    result_pdf = models.FileField(upload_to='match_reports/', null=True, blank=True)  # ✅ Add this line
    job_description = models.TextField()
    score = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)  # ✅ Add this line

    def __str__(self):
        return f"{self.user.username} - {self.score}%"
