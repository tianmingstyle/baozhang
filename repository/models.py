# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class User_Article(models.Model):
    uid = models.ForeignKey(to="User", to_field='id')
    aid = models.ForeignKey(to="Article", to_field='id')
    user_feels = [(1, 'yes'), (0, 'no')]
    feels = models.IntegerField(verbose_name='Ding or Cai', choices=user_feels)

    class Meta:
        db_table = 'user_article'
        verbose_name_plural = 'user_article'
        unique_together = (('uid', 'aid'),)



class Article(models.Model):
    user = models.ForeignKey(to="User")
    title = models.CharField(verbose_name='标题',max_length=64)
    summary = models.CharField(verbose_name='简介',max_length=128)
    detail = models.TextField(verbose_name='详细内容')
    ctime = models.DateField(verbose_name='ctetime',auto_now_add=True)
    readnum = models.IntegerField(default=0)
    commentnum = models.IntegerField(default=0)
    upcount = models.IntegerField(default=0)
    downcount = models.IntegerField(default=0)
    cls = models.ForeignKey("Classification")
    tag = models.ManyToManyField("Tag")
    blog = models.ForeignKey("Blog", default=1)
    type_choices = [
        (1, 'Python'),
        (2, 'Linux'),
        (3, 'Openstack'),
        (4, 'GoLang'),
    ]
    article_type_id = models.IntegerField(choices=type_choices, default=None)

    class Meta:
        db_table='Article'
        verbose_name_plural = '文章表'

    def __unicode__(self):
        return self.title


class Classification(models.Model):
    title = models.CharField(verbose_name='分类', max_length=32)
    blog = models.ForeignKey("Blog")
    # tag = models.ForeignKey("Tag")

    class Meta:
        db_table = 'classification'
        verbose_name_plural = '分类表'

    def __unicode__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(verbose_name='标签名', max_length=32)
    blog = models.ForeignKey("Blog")

    class Meta:
        db_table = 'tag'
        verbose_name_plural = '标签表'

    def __unicode__(self):
        return self.title


class User(models.Model):
    username = models.CharField(verbose_name='用户', max_length=32)
    pwd = models.CharField(verbose_name='密码', max_length=64)
    email = models.EmailField(verbose_name='email')
    img = models.ImageField(verbose_name='用户图像', upload_to='./static/imgs')
    fans = models.ManyToManyField('self', symmetrical=False, null=True, blank=True)

    class Meta:
        db_table = 'all_user'
        verbose_name_plural = 'all_user'

    def __unicode__(self):
        return self.username


class Baozhang(models.Model):
    UUID = models.UUIDField(verbose_name='UUID', primary_key=True)
    title = models.CharField(verbose_name='biaoti', max_length=32)
    detail = models.TextField(verbose_name='xiangxineirong')
    uid = models.ForeignKey("User", related_name='bzd')
    processor = models.ForeignKey("User", related_name='pbzd')
    my_choices = [(1,'wait_to_process'),(2,'processing'),(3,'finish to process')]
    status = models.IntegerField(verbose_name='zhuangtai', choices=my_choices)
    ctime = models.DateField(verbose_name='create_time', auto_now_add=True)
    process_time = models.DateField(verbose_name='process time', auto_now_add=True)

    class Meta:
        db_table = 'baozhangbiao'
        verbose_name_plural = 'baozhangbiao'

    def __unicode__(self):
        return self.title


class Blog(models.Model):
    title = models.CharField(verbose_name='biaoti', max_length=32)
    suffix = models.CharField(verbose_name='houzui', max_length=32, unique=True)
    theme = models.CharField(verbose_name='zhuti', max_length=32)
    summary = models.CharField(verbose_name='jitang', max_length=128)
    uid = models.OneToOneField("User")

    class Meta:
        db_table = 'blog'
        verbose_name_plural = 'blog'

    def __unicode__(self):
        return self.title


class Comment(models.Model):
    content = models.CharField(verbose_name='pinglun', max_length=256)
    ctime = models.DateField(verbose_name='crete time', auto_now_add=True)
    pcomment = models.ForeignKey(to='self', null=True, blank=True)
    article = models.ForeignKey("Article", default=1)
    class Meta:
        db_table = 'comment'
        verbose_name_plural = 'comment'

    def __unicode__(self):
        return self.content
