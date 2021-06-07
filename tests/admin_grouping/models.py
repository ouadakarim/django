from django.db import models


class Cat(models.Model):
    name = models.CharField(max_length=100)


class Dog(models.Model):
    name = models.CharField(max_length=100)


class CatFood(models.Model):
    name = models.CharField(max_length=100)


class DogFood(models.Model):
    name = models.CharField(max_length=100)
