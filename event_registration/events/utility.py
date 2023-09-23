import csv
import zipfile

from events.models import Participant, Events


class Utilities:
    """
    Class for Utility functions
    """

    @staticmethod
    def upload_from_csv(csv_file, image_files=None):
        """
        Upload events details from csv and zip file.
        :param csv_file : csv file containing events details.
        :param image_files : zip file containing images.
        """
        data = csv_file.file.read()
        csv_content = data.decode('UTF-8').split('\n')
        reader = csv.DictReader(csv_content)
        success = failed = 0
        if image_files and zipfile.is_zipfile(image_files):
            with zipfile.ZipFile(image_files) as images:
                for event in reader:
                    try:
                        if not event['Email Address']:
                            continue

                        participant_obj, _ = Participant.objects.update_or_create(
                            email=event['Email Address'],
                            defaults={
                                "first_name": event['First Name'],
                                "last_name": event['Last Name'],
                                "phone_number": event['Phone Number']
                            }
                        )

                        participant_obj.save()
                        for event_name in map(lambda x: x.strip().title(), event['Events'].split(",")):
                            event_obj = Events.objects.get(event_name__iexact=event_name)

                            participant_obj.events.add(event_obj)
                        participant_obj.save()
                        if event['Profile picture'] in images.namelist():
                            with images.open(event['Profile picture']) as profile_picture:
                                participant_obj.profile_picture.save(event['Profile picture'], profile_picture, True)
                        success += 1
                    except Exception as e:
                        print(e)
                        failed += 1
                return success, failed
