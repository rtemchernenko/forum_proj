import graphene
from graphene_django.types import DjangoObjectType
from .models import Forum, Thread, Post, Comment, UserProfile
from django.contrib.auth.models import User
from django.utils.text import slugify
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
import graphql_jwt
from unidecode import unidecode
from itertools import count
import django_filters
from graphene_django.filter import DjangoFilterConnectionField
from graphql_auth import mutations
from graphql_auth.schema import UserQuery, MeQuery


class ForumType(DjangoObjectType):
    class Meta:
        model = Forum


class ThreadType(DjangoObjectType):
    class Meta:
        model = Thread


class PostType(DjangoObjectType):
    class Meta:
        model = Post


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment


class UserType(DjangoObjectType):
    class Meta:
        model = User


class UserProfileType(DjangoObjectType):
    class Meta:
        model = UserProfile


class Query(UserQuery, MeQuery, graphene.ObjectType):
    all_forums = graphene.List(ForumType)
    all_threads = graphene.List(ThreadType, forum_id=graphene.Int())
    all_posts = graphene.List(PostType, thread_id=graphene.Int())
    all_comments = graphene.List(CommentType, post_id=graphene.Int())
    me = graphene.Field(UserType)

    @login_required
    def resolve_all_forums(self, info):
        return Forum.objects.all()

    def resolve_all_threads(self, info, forum_id=None):
        if forum_id:
            return Thread.objects.filter(forum_id=forum_id)
        return Thread.objects.all()

    def resolve_all_posts(self, info, thread_id=None):
        if thread_id:
            return Post.objects.filter(thread_id=thread_id)
        return Post.objects.all()

    def resolve_all_comments(self, info, post_id=None):
        if post_id:
            return Comment.objects.filter(post_id=post_id)
        return Comment.objects.all()

    @login_required
    def resolve_me(self, info):
        return info.context.user


class CreatePost(graphene.Mutation):
    class Arguments:
        thread_id = graphene.Int(required=True)
        title = graphene.String(required=True)
        content = graphene.String(required=True)

    post = graphene.Field(PostType)

    @login_required
    def mutate(self, info, thread_id, title, content):
        user = info.context.user
        try:
            thread = Thread.objects.get(id=thread_id)
        except Thread.DoesNotExist:
            raise GraphQLError("Тема не найдена.")

        base_slug = slugify(unidecode(title))[:50]
        slug = base_slug
        for i in count(1):
            if not Post.objects.filter(slug=slug).exists():
                break
            slug = f"{base_slug}-{i}"

        post = Post(thread=thread, created_by=user, title=title, content=content, slug=slug)
        post.save()
        return CreatePost(post=post)


class UpdatePost(graphene.Mutation):
    class Arguments:
        post_id = graphene.Int(required=True)
        title = graphene.String()
        content = graphene.String()

    post = graphene.Field(PostType)

    @login_required
    def mutate(self, info, post_id, title=None, content=None):
        user = info.context.user
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise GraphQLError("Пост не найден.")

        if post.created_by != user:
            raise GraphQLError("Вы не можете редактировать чужой пост.")

        if title:
            post.title = title
            post.slug = slugify(title)[:50]
        if content:
            post.content = content

        post.save()
        return UpdatePost(post=post)


class DeletePost(graphene.Mutation):
    class Arguments:
        post_id = graphene.Int(required=True)

    success = graphene.Boolean()

    @login_required
    def mutate(self, info, post_id):
        user = info.context.user
        try:
            post = Post.objects.get(id=post_id)
            if post.created_by != user:
                raise GraphQLError("Вы не можете удалить этот пост.")
            post.delete()
            return DeletePost(success=True)
        except Post.DoesNotExist:
            raise GraphQLError("Пост не найден.")


class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    token_auth = mutations.ObtainJSONWebToken.Field()
    update_account = mutations.UpdateAccount.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()
    password_change = mutations.PasswordChange.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
