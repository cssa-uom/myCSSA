from django.contrib.postgres import fields
from rest_framework import serializers
from django.db.transaction import atomic

from UserAuthAPI.models import UserProfile

from . import models

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ['id', 'title']

class FavouritePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FavouritePost
        fields = ['post']

    @atomic
    def create(self, validated_data):
        userProfile: UserProfile = self.context['request'].user

        favourite = models.FavouritePost.objects.create(
            user_id=userProfile.pk,
            post=validated_data['post']
        )

        return favourite
        
class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Content
        fields = ['title', 'text', 'imageUrls']
        read_only_fields = ['editedTime']

def resolve_username(profile: UserProfile) -> str:
    # 暂时用用户的全名来当作用户名
    return profile.firstNameEN + ' ' + profile.lastNameEN

class PostSerializerMixin:
    """
    提供一些主贴和评论都会用到的公共方法
    """

    def fill_representation(self, repr, instance: models.Post):
        """
        向返回的json填充以下数据：
        帖子正文
        发帖的用户名
        """

        contentModel = models.Content.objects.filter(post=instance).order_by('-editedTime').first()
        repr['content'] = self.fields['content'].to_representation(contentModel)

        repr['createdBy'] = resolve_username(instance.createdBy)

    def create_content(self, validated_data, post: models.Post):
        """
        从输入的json创建一个新的content版本
        """

        userProfile: UserProfile = self.context['request'].user

        # TODO: 上传图片之类的代码写在这里

        return models.Content.objects.create(
            post=post,
            editedBy_id=userProfile.pk,
            **validated_data['content']
        )


class ReadPostSerializer(PostSerializerMixin, serializers.ModelSerializer):
    """
    只用来处理文章的读取
    """

    SUMMARY_TEXT_LENGTH = 50 # 25个汉字

    content = ContentSerializer(read_only=True)

    createdBy = serializers.CharField()

    class Meta:
        model = models.Post
        fields = ['id', 'tag_id', 'createTime', 'viewCount', 'viewableToGuest',
            # 正常情况下我们不需要再声明下面两个field，但是不这么搞的话 drf_yasg 会报错
            'content', 'createdBy']

    def to_representation(self, instance: models.Post):
        repr = super().to_representation(instance)
        self.fill_representation(repr, instance)

        # 如果是读取文章列表，只保留正文的前25个汉字
        if not self.context['view'].detail:
            repr['content']['text'] = repr['content']['text'][:self.SUMMARY_TEXT_LENGTH]

        return repr

class EditPostSerializer(PostSerializerMixin, serializers.ModelSerializer):
    """
    处理帖子的添加和修改。
    对于主贴而言，只有在添加的时候 tag 和 viewableToGuest 有效。其他情况下这两个字段没有用。
    """
    content = ContentSerializer()

    class Meta:
        model = models.Post
        fields = ['tag', 'viewableToGuest',
            # 正常情况下我们不需要再声明下面的field，但是不这么搞的话 drf_yasg 会报错
            'content']

    @atomic
    def create(self, validated_data):

        userProfile: UserProfile = self.context['request'].user

        post = models.Post.objects.create(
            createdBy_id=userProfile.pk,
            tag=validated_data['tag'],
            viewableToGuest=validated_data['viewableToGuest']
        )

        self.create_content(validated_data, post)

        return post

    def update(self, instance, validated_data):

        # TODO: update tag and viewable to guest?

        self.create_content(validated_data, instance)

        return instance
