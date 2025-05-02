
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User



#Create your models here.
SELECT_CATEGORY_CHOICES = [
    ("Food","Food"),
    ("Travel","Travel"),
    ("Shopping","Shopping"),
    ("Necessities","Necessities"),
    ("Entertainment","Entertainment"),
    ("Other","Other")
 ]
ADD_EXPENSE_CHOICES = [
     ("Expense","Expense"),
     ("Income","Incomet")
 ]



class Expenses(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,)
    addmoney_category=models.CharField(max_length = 10 , choices = ADD_EXPENSE_CHOICES )
    expense_category = models.CharField( max_length = 20, choices = SELECT_CATEGORY_CHOICES,null=True,blank=True )
    amount = models.FloatField(max_length=20,null=True)
    Date = models.DateField(default = now)
    
        
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    Savings = models.IntegerField( null=True, blank=True)
    income = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
       return self.user.username
   



