import re
from apps.accounts.models import Account

c=0
for a in Account.objects.exclude(status='ignored').filter(bio__icontains='denver').filter(bio__icontains='@'):
    if "denver" in a.bio.lower():
        matches = re.findall(r'[\w\.-]+@[\w\.-]+', a.bio)
        for m in matches:
            print m
            c += 1

print "Emails: ",c




# Calculate percent finished
print "%.4f" % (1.0*len(Account.objects.filter(status='done')) / (len(Account.objects.filter(status='pending'))+len(Account.objects.filter(status='done'))) * 100)