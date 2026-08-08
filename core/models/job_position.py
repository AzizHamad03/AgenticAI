from django.db import models

class JobPosition(models.Model):
    title = models.CharField(max_length=100)
    department = models.ForeignKey('Department', on_delete=models.CASCADE, related_name='job_positions')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    required_skills = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.title