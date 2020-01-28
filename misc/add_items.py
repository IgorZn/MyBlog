import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MyBlog.settings')

import django
django.setup()

from blog.models import Post
from django.contrib.auth.models import User
from faker import Faker
from random import randint
from taggit.models import Tag
import pprint

fake = Faker()
users = User.objects.all()


def add_users(Num: int):
    # create N Users
    for i in range(Num):
        f = fake.profile()
        User.objects.create_user(f['username'], email=f['mail'], password='DemoUser')

    users = User.objects.all()
    pprint.pprint(users)



def add_posts(Num: int, users):

    tags = Tag.objects.all()
    users_count = len(users)-1

    # create N posts
    for i in range(Num):
        random_index_users = randint(0, users_count)
        random_index_tags = randint(0, len(tags)-1)

        title = fake.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None)
        slug = title.replace(' ', '-').replace('.', '').lower()
        author = users[random_index_users]
        body = ''.join(fake.texts(nb_texts=3, max_nb_chars=200, ext_word_list=None))
        status = 'published'
        tag = tags[random_index_tags]

        Post.objects.create(title=title,
                            slug=slug,
                            author=author,
                            body=body,
                            status=status,
                            )


def main():
    add_posts(50, users)
    # add_users(20)


if __name__ == '__main__':
    main()