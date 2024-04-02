import json
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from street.models import TextDataset


class Command(BaseCommand):
    help = "Import Data from jsonl file to TextDataset"

    def add_arguments(self, parser):
        parser.add_argument("jsonl_file", type=str, help="Path to the JSONL file")

    
    def handle(self, **options):
        jsonl_file = options["jsonl_file"]
        self.import_jsonl_data(jsonl_file)
    

    def import_jsonl_data(self, jsonl_file):
        with open(jsonl_file, 'r') as file:
            for line in file:
                data = json.loads(line)
                text = data.get('text', '')
                if len(text) < 100:
                    continue
                while len(text) > 2500:
                    text1 = text[:2500]
                    try:
                        TextDataset.objects.get(text=text1)
                        text = text[2000:]
                        continue
                    except ObjectDoesNotExist:
                        model_instance = TextDataset(text=text1)
                        model_instance.save()
                        self.stdout.write(self.style.NOTICE(f"ADDED {model_instance}"))
                    text = text[2000:]
                if text:
                    try:
                        TextDataset.objects.get(text=text)
                        continue
                    except ObjectDoesNotExist:
                        model_instance = TextDataset(text=text)
                        model_instance.save()
                        self.stdout.write(self.style.SUCCESS(f"ADDED {model_instance}"))
        self.stdout.write(self.style.SUCCESS("JSONL data imported successfully"))