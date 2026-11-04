import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date de publication")

    def __str__(self):
        """
        Affiche les 20 premiers caractères de la question
        ainsi que sa date de publication.
        """
        return f"{self.question_text[:20]} - {self.pub_date}"

    def was_published_recently(self):
        """
        Retourne True si la question a été publiée
        durant les dernières 24 heures.
        """
        now = timezone.now()

        return (
            now - datetime.timedelta(days=1)
            <= self.pub_date
            <= now
        )

    def age(self):
        """
        Calcule l'âge de la question depuis sa publication.
        """
        return timezone.now() - self.pub_date

    def get_choices(self):
        """
        Retourne une liste contenant :
        - le texte du choix,
        - son nombre de votes,
        - sa proportion de votes en pourcentage.
        """
        choices = self.choice_set.all()

        total_votes = sum(
            choice.votes
            for choice in choices
        )

        result = []

        for choice in choices:

            if total_votes > 0:
                proportion = (
                    choice.votes / total_votes
                ) * 100
            else:
                proportion = 0

            result.append(
                (
                    choice.choice_text,
                    choice.votes,
                    proportion
                )
            )

        return result

    def get_max_choice(self):
        """
        Retourne le choix ayant obtenu le plus de votes
        ainsi que son nombre de votes et sa proportion.
        """
        choices = list(self.choice_set.all())

        if not choices:
            return None

        max_choice = max(
            choices,
            key=lambda choice: choice.votes
        )

        total_votes = sum(
            choice.votes
            for choice in choices
        )

        if total_votes > 0:
            proportion = (
                max_choice.votes / total_votes
            ) * 100
        else:
            proportion = 0

        return (
            max_choice.choice_text,
            max_choice.votes,
            proportion
        )


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )

    choice_text = models.CharField(
        max_length=200
    )

    votes = models.IntegerField(
        default=0
    )

    def __str__(self):
        """
        Affiche uniquement les 20 premiers caractères
        du texte du choix.
        """
        return self.choice_text[:20]