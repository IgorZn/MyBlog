from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from .forms import CommentForm
from taggit.models import Tag
from django.db.models import Count


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


	# Формирование списка похожих статей.
	post_tags_ids = post.tags.values_list('id', flat=True)
	similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
	similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]


	context = {
		'post': post,
		'comments': comments,
		'new_comment': new_comment,
		'comment_form': comment_form,
		'similar_posts': similar_posts,
	}
	return render(request, 'blog/post/detail.html', context)
