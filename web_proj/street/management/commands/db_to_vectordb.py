from ...utils.functions import generate_embeddings_from_database
from django.core.management.base import BaseCommand
from street.models import TextDataset, VectorDataset



class Command(BaseCommand):
    help = "Create a VectorDataset from TextDataset"


    def handle(self, *args, **options):
        #getting a starting idx so it becomes more efficient
        #(not checking throw rows we know are vectorized already)
        num_of_vectorized_text_idx = VectorDataset.objects.all().count()

        #embeddings_generator will start from where it stopped no matter the pk, it is about count
        embeddings_generator = generate_embeddings_from_database(start_idx=num_of_vectorized_text_idx)

        for text_dataset in TextDataset.objects.all():
            embeddings = next(embeddings_generator)
            if VectorDataset.objects.filter(original_pk=text_dataset.pk).exists():
                self.stdout.write(self.style.ERROR(f"VectorDataset with original_pk {text_dataset.pk} exists."))
            else:
                vector_dataset_instance = VectorDataset(original_pk=text_dataset.pk)
                vector_dataset_instance.set_vector_data(embeddings)
                vector_dataset_instance.save()
                self.stdout.write(self.style.SUCCESS(f"VectorDataset with original_pk {text_dataset.pk} ADDED: {vector_dataset_instance} "))