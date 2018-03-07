from django.core.management.base import BaseCommand, CommandError
from temperature.models import TempReading
import time

class Command(BaseCommand):
    help = 'Saves temprature every 15 minutes.'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--interval', 
            nargs='?', 
            type=int, 
            default=15
        )


    def handle(self, *args, **options):
        interval = options['interval']

        self.stdout.write(self.style.SUCCESS("Started to reading with interval %d." % interval))
        
        while True:
            tempfile = open("/sys/bus/w1/devices/28-00000698fc00/w1_slave")
            tempfile_text = tempfile.read()
            currentTime=time.strftime('%x %X %Z')
            tempfile.close()
            tempC=float(tempfile_text.split("\n")[1].split("t=")[1])/1000
            tempF=tempC*9.0/5.0+32.0
            
            new_entry = TempReading(reading=tempF)
            new_entry.save()
            
            self.stdout.write(self.style.SUCCESS("New temprature saved. %f." % new_entry.reading))
            
            time.sleep(interval*60)
