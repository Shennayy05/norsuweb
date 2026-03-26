from django.db import models
from django.utils import timezone

# Create your models here.

class Alumni(models.Model):
    LATIN_HONORS_CHOICES = [
        ('', 'No Latin Honor'),
        ('Summa Cum Laude', 'Summa Cum Laude'),
        ('Magna Cum Laude', 'Magna Cum Laude'),
        ('Cum Laude', 'Cum Laude'),
    ]
    name = models.CharField(max_length=255)
    latin_honors = models.CharField(max_length=50, choices=LATIN_HONORS_CHOICES, blank=True, default='')
    batch = models.CharField(max_length=10)
    course = models.CharField(max_length=255)
    position = models.CharField(max_length=255, blank=True)
    company = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='alumni/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Alumni'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.batch}"


class Announcement(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    title = models.CharField(max_length=255)
    content = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    image = models.ImageField(upload_to='announcements/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class AlumniNews(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='alumni/news/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, default='published', choices=[('draft', 'Draft'), ('published', 'Published')])

    class Meta:
        verbose_name_plural = 'Alumni News'

    def __str__(self):
        return self.title


class AlumniEvent(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='alumni/events/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='published', choices=[('draft', 'Draft'), ('published', 'Published')])

    class Meta:
        verbose_name_plural = 'Alumni Events'

    def __str__(self):
        return self.title


class AlumniAbout(models.Model):
    title = models.CharField(max_length=255, default='The NORSU-BSC Alumni Association')
    content = models.TextField()
    vision = models.TextField(default='A globally recognized state university.')
    mission = models.TextField()
    image = models.ImageField(upload_to='alumni/about/', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Alumni About'

    def __str__(self):
        return self.title


class College(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=20)
    dean = models.CharField(max_length=255)
    total_students = models.IntegerField(default=0)
    programs_offered = models.IntegerField(default=0)
    qualified_instructors = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    description = models.TextField(blank=True, help_text="List of colleges/departments under this college")
    image = models.ImageField(upload_to='colleges/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.abbreviation})"


class Faculty(models.Model):
    COLLEGE_CHOICES = [
        ('cas', 'College of Arts & Sciences'),
        ('cit', 'College of Industrial Technology'),
        ('cted', 'College of Teacher Education'),
        ('ccje', 'College of Criminal Justice Education'),
        ('cba', 'College of Business Administration'),
        ('caf', 'College of Agriculture & Forestry'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('onleave', 'On Leave'),
        ('retired', 'Retired'),
    ]

    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    college = models.CharField(max_length=50, choices=COLLEGE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    image = models.ImageField(upload_to='faculty/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Faculty'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.college}"


class Facility(models.Model):
    COLLEGE_CHOICES = [
        ('cas', 'College of Arts & Sciences'),
        ('cit', 'College of Industrial Technology'),
        ('cted', 'College of Teacher Education'),
        ('ccje', 'College of Criminal Justice Education'),
        ('cba', 'College of Business Administration'),
        ('caf', 'College of Agriculture & Forestry'),
    ]

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('maintenance', 'Under Maintenance'),
        ('reserved', 'Reserved'),
    ]

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=100, blank=True)
    capacity = models.CharField(max_length=100, blank=True)
    college = models.CharField(max_length=50, choices=COLLEGE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    image = models.ImageField(upload_to='facilities/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Facilities'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.college}"


class News(models.Model):
    CATEGORY_CHOICES = [
        ('general', 'General'),
        ('event', 'Event'),
        ('academic', 'Academic'),
        ('sports', 'Sports'),
    ]

    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='general')
    image = models.ImageField(upload_to='news/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class AcademicCalendar(models.Model):
    title = models.CharField(max_length=255, default='Academic Calendar')
    academic_year = models.CharField(max_length=50, default='2025-2026')
    description = models.TextField(blank=True)
    images = models.JSONField(default=list, blank=True)  # List of image URLs
    pdf_file = models.FileField(upload_to='calendar/pdf/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Academic Calendar'

    def __str__(self):
        return f"{self.title} ({self.academic_year})"


class Post(models.Model):
    POST_TYPE_CHOICES = [
        ('announcement', 'Announcement'),
        ('news', 'News'),
        ('update', 'Update'),
        ('alumni', 'Alumni'),
        ('award', 'Award'),
        ('general', 'General Post'),
    ]

    CATEGORY_CHOICES = [
        ('general', 'General'),
        ('event', 'Event'),
        ('academic', 'Academic'),
        ('sports', 'Sports'),
    ]

    COLLEGE_CHOICES = [
        ('all', 'All Colleges'),
        ('cas', 'College of Arts & Sciences'),
        ('cit', 'College of Industrial Technology'),
        ('cted', 'College of Teacher Education'),
        ('ccje', 'College of Criminal Justice Education'),
        ('cba', 'College of Business Administration'),
        ('caf', 'College of Agriculture & Forestry'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    title = models.CharField(max_length=255)
    content = models.TextField()
    post_type = models.CharField(max_length=20, choices=POST_TYPE_CHOICES, default='general')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='general')
    college = models.CharField(max_length=50, choices=COLLEGE_CHOICES, default='all')
    target_audience = models.CharField(max_length=50, choices=COLLEGE_CHOICES, default='all')
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='published')
    author = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.post_type})"


class Achievement(models.Model):
    CATEGORY_CHOICES = [
        ('academic', 'Academic'),
        ('sports', 'Sports'),
        ('research', 'Research'),
        ('community', 'Community Service'),
        ('arts', 'Arts & Culture'),
        ('leadership', 'Leadership'),
        ('international', 'International'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    recipient = models.CharField(max_length=255, blank=True, null=True)
    achievement_date = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to='achievements/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='published')
    is_highlighted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class AlumniSuccessStory(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    alumni_name = models.CharField(max_length=255)
    achievement = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='alumni/success_stories/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='published')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Alumni Success Stories'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.alumni_name} - {self.achievement}"


class MediaUpload(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('photo', 'Photo'),
        ('video', 'Video'),
    ]
    
    APPROVAL_STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    file = models.FileField(upload_to='alumni_media/')
    year = models.IntegerField()
    college = models.CharField(max_length=255)
    uploaded_by = models.CharField(max_length=255, blank=True, null=True)  # Alumni name
    approval_status = models.CharField(max_length=20, choices=APPROVAL_STATUS_CHOICES, default='pending')
    rejection_reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Media Uploads'

    def __str__(self):
        return f"{self.title} - {self.approval_status}"


class Program(models.Model):
    LEVEL_CHOICES = [
        ('undergraduate', 'Undergraduate'),
        ('graduate', 'Graduate'),
        ('certificate', 'Certificate'),
    ]

    COLLEGE_CHOICES = [
        ('cas', 'College of Arts & Sciences'),
        ('cit', 'College of Industrial Technology'),
        ('cted', 'College of Teacher Education'),
        ('ccje', 'College of Criminal Justice Education'),
        ('cba', 'College of Business Administration'),
        ('caf', 'College of Agriculture & Forestry'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES, default='undergraduate')
    college = models.CharField(max_length=50, choices=COLLEGE_CHOICES)
    duration = models.CharField(max_length=100, blank=True)
    objectives = models.TextField(blank=True, null=True)  # kept for backward compat
    dresscode_schedule = models.TextField(blank=True, null=True)
    dresscode_images = models.JSONField(blank=True, null=True, default=list)  # list of image paths
    vision = models.TextField(blank=True, null=True)
    mission = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='programs/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='published')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
