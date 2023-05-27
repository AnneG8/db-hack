from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from datetime import date
import random
from datacenter.models import (Chastisement, Commendation, Lesson, Mark,
                               Schoolkid, Subject)


def get_child(schoolkid):
	try:
		child = Schoolkid.objects.get(full_name__contains=schoolkid)
		return child
	except MultipleObjectsReturned:
		print('По вашему запросу найдено несколько учеников. ' \
			  'Попробуйте задать подробнее.')
	except ObjectDoesNotExist:
		print('По вашему запросу не найден ни один ученик.')
	return False


def fix_marks(schoolkid):
	child = get_child(schoolkid)
	if child:
		Mark.objects.filter(schoolkid=child, points__in=[2, 3]) \
					.update(points=5)


def remove_chastisements(schoolkid):
	child = get_child(schoolkid)
	if child:
		Chastisement.objects.filter(schoolkid=child).delete()


def create_commendation(schoolkid, subject, сommendation=None):
	child = get_child(schoolkid)
	if not child:
		return

	subject_commendations = Commendation.objects.filter(
		schoolkid=child, 
		subject__title=subject
	).order_by('-created')

	all_subject_lessons = Lesson.objects.filter(
		year_of_study=child.year_of_study,
		group_letter=child.group_letter,
		subject__title=subject,
		date__lte=date.today()
	).order_by('-date')

	if not all_subject_lessons.count():
		print('По данному предмету нет уроков. ' \
			  'Проверьте, корректно ли указан данный параметр')
		return
	if subject_commendations.count() == all_subject_lessons.count():
		print('По данному предмету ко всем урокам уже есть похвала')
		return

	commendation_texts = ['Молодец!', 'Отлично!', 'Хорошо!', 
	'Гораздо лучше, чем ожидалось!', 'Ты меня приятно удивил!', 
	'Великолепно!', 'Прекрасно!', 'Ты сегодня прыгнул выше головы!',
	'Именно этого я давно ждал от тебя!', 'Сказано здорово – просто и ясно!',
 	'Ты, как всегда, точен!', 'Очень хороший ответ!', 'Талантливо!', 
 	'Ты меня очень обрадовал!', 'Я поражен!', 'Уже существенно лучше!',
 	'Потрясающе!', 'Замечательно!', 'Прекрасное начало!', 'Так держать!']

	for lesson in all_subject_lessons:
		if not subject_commendations.filter(created=lesson.date, 
											teacher=lesson.teacher):
			if сommendation is None:
				сommendation = random.choice(commendation_texts)
			Commendation.objects.create(
				text=сommendation, 
				schoolkid=child, 
				teacher=lesson.teacher, 
				subject=lesson.subject, 
				created=lesson.date
			)
			break








