from django.db import models

# Create your models here.
class Comment(models.Model):
    comment = models.TextField()    
    user = models.ForeignKey("users.User", on_delete =models.CASCADE , related_name = "user_comments_publication")
    publication = models.ForeignKey("publications.Publication", on_delete =models.CASCADE , related_name = "publications_comment_user")
class Publication(models.Model):
    post_photo= models.CharField(null=True,max_length=500)
    text= models.TextField()
    user= models.ForeignKey("users.User", on_delete =models.CASCADE , related_name = "publications")
    comments= models.ManyToManyField("users.User" , through="Comment",related_name="comment")

class Like(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE , related_name="publication_likes_user")
    publication = models.ForeignKey("publications.Publication", on_delete=models.CASCADE , related_name="likes_users")