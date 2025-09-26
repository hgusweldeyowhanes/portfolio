from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from dateutil.relativedelta import relativedelta
from django.utils import timezone


class Project(models.Model):
    PROJECT_TYPES = [
        ('web', 'Web Application'),
        ('mobile', 'Mobile Application'),
        ('ml', 'Machine Learning'),
        ('ai', 'Artificial Intelligence'),
        ('blockchain', 'Blockchain/Crypto'),
        ('data', 'Data Science'),
        ('iot', 'IoT'),
        ('desktop', 'Desktop Application'),
    ]
    
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50 , unique=True, blank=True)
    description = models.TextField()
    short_description = models.CharField(max_length=200, blank=True, null=True)
    image =  models.ImageField(upload_to='projects/')
    technologies = models.ManyToManyField('Skills',blank=True, help_text="Display separated by commas")
    project_type = models.CharField(max_length=20, choices=PROJECT_TYPES,default='web')
    url = models.URLField(null=True, blank=True, verbose_name="Project URL")
    github_url = models.URLField(null=True,blank=True, verbose_name="Github URL")
    featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0, help_text="Display order (higher numbers shows first)")
    model_accuracy = models.FloatField(null=True, blank=True, verbose_name="Model Accuracy (%)")
    algorithm = models.CharField(max_length=100, blank=True, help_text="ML Algorithm used")
    dataset_size = models.CharField(max_length=50, blank=True, help_text="Dataset size (e.g., 10GB, 1M records)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-featured', '-order', '-created_at']
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.short_description and self.description:
            self.short_description = self.description[:200] + "..." if len(self.description) > 200 else self.description
        return super().save(*args,**kwargs)
    def get_absolute_url(self): 
        return reverse("project_detail", kwargs={"slug": self.slug})

    def technologies_list(self):
        return [tech.strip() for tech in self.technologies.split(",") ]
    def is_project_ml(self):
        return self.project_type['ml','ai','data']
    def __str__(self):
        return self.title

class Skills(models.Model):
    SKILL_LEVELS = [
        (1, 'Beginner'),
        (2, 'Intermediate'),
        (3, 'Advanced'),
        (4, 'Expert'),
     ]
    
    CATEGORIES = [
        ('backend', 'Backend Development'),
        ('frontend', 'Frontend Development'),
        ('database', 'Database'),
        ('devops', 'DevOps & Tools'),
        ('ml', 'Machine Learning'),
        ('ai', 'Artificial Intelligence'),
        ('data_science', 'Data Science'),
        ('blockchain', 'Blockchain & Crypto'),
        ('cloud', 'Cloud & AI Services'),
        ('soft', 'Soft Skills'),
    ]
    ML_SUBCATEGORIES = [
        ('supervised', 'Supervised Learning'),
        ('unsupervised', 'Unsupervised Learning'),
        ('reinforcement', 'Reinforcement Learning'),
        ('deep_learning', 'Deep Learning'),
        ('nlp', 'Natural Language Processing'),
        ('computer_vision', 'Computer Vision'),
        ('time_series', 'Time Series Analysis'),
    ]

    name = models.CharField(max_length=50)
    level = models.IntegerField(choices=SKILL_LEVELS, default=1)
    category = models.CharField(max_length=20, choices=CATEGORIES,default='backend')
    subcategory = models.CharField(max_length=20, choices=ML_SUBCATEGORIES,blank=True,null=True, help_text="Specialized subcategory")
    icon = models.CharField(max_length=50, blank=True)
    order = models.IntegerField(default=0)
    framework = models.CharField(max_length=50, blank=True, help_text="pytorch,Django, etc")
    library = models.CharField(max_length=50, blank=True,help_text="comma separeted library names")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', '-level','order','name']
    def get_level_display(self):
        level_class = {
            'beginner': 'Beginner',
            'intermediate': 'Intermediate',
            'advanced': 'Advanced',
            "expert": "Expert"
        }
        return level_class.get(self.level,'beginner')
    def libraries_list(self):
        return [lib.strip() for lib in self.libraries.split(',')] if self.libraries else []

    def __str__(self):
        return f"{self.name}({self.get_level_display()})"
    
class Experience(models.Model):
    INDUSTRY_TYPES = [
        ('tech', 'Technology'),
        ('finance', 'Finance'),
        ('healthcare', 'Healthcare'),
        ('ai_ml', 'AI/ML Startup'),
        ('education', 'Education'),
    ]
    company = models.CharField(max_length=50)
    role = models.CharField(max_length=50)
    description = models.TextField()
    short_description = models.CharField(max_length=200, blank=True, null= True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    current = models.BooleanField(default=False)
    company_log = models.ImageField(upload_to='company_logos/' ,blank=True,null=True)
    industry = models.CharField(max_length=200, choices=INDUSTRY_TYPES, default='tech')
    ml_projects = models.TextField(blank=True, help_text="ML/AI projects worked on")
    algorithms_used = models.CharField(max_length=200, blank=True, help_text="Algorithms and techniques used")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']
    def save(self,*args, **kwargs):
        if not self.short_description and self.description:
            self.short_description = self.description[:200] + "..." if len(self.description) > 200 else self.description
        return super().save(*args,**kwargs)
    
    def duration(self):
        if self.current:
            end = timezone.now().date()
        else:
            end = self.end_date
        
        rd = relativedelta(end, self.start_date)
        years = rd.years
        months = rd.months
        if years > 0:
            return f"{years} year{'s' if years > 1 else ''} {months} month{'s' if months > 1 else ''}"
        return f"{months} month{'s' if months > 1 else ''}"
    def is_ai_ml_role(self):
        ai_ml_keywords = ['machine learning', 'ai', 'artificial intelligence', 'data scientist', 'ml engineer']
        return any(keyword in self.role.lower() for keyword in ai_ml_keywords)
    def __str__(self):
        return f"{self.role} at {self.company}"
    