from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from .forms import CommentForm
from taggit.models import Tag


def post_list(request, tag_slug=None):
	print(tag_slug)
	posts = Post.published.all()
	drafts = Post.draft.all()
	tag = None

	if tag_slug:
		tag = get_object_or_404(Tag, slug=tag_slug)
		posts = posts.filter(tags__in=[tag])

	context = {
		'posts': posts,
		'drafts': drafts,
		'tag': tag,
	}
	return render(request, 'blog/post/list.html', context)


def post_detail(request, year, month, day, post):
	post = get_object_or_404(
		Post,
		slug=post,
		status='published',
		publish__year=year,
		publish__month=month,
		publish__day=day,
	)

	# Список активных комментариев для этой статьи.
	comments = post.comments.filter(active=True)
	new_comment = None

	if request.method == 'POST':
		# Пользователь отправил комментарий.
		comment_form = CommentForm(data=request.POST)

		if comment_form.is_valid():
			# Создаем комментарий, но пока не сохраняем в базе данных.
			new_comment = comment_form.save(commit=False)

			# Привязываем комментарий к текущей статье.
			new_comment.post = post

			# Сохраняем комментарий в базе данных.
			new_comment.save()
	else:
		comment_form = CommentForm()

	context = {
		'post': post,
		'comments': comments,
		'new_comment': new_comment,
		'comment_form': comment_form,
	}

	return render(request, 'blog/post/detail.html', context)
