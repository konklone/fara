
import reversion

from django.contrib import admin

from FaraData.models import *

class reg_admin(admin.ModelAdmin):
    search_fields=['reg_name']
admin.site.register(Registrant, reg_admin)
    
class client_admin(admin.ModelAdmin):
    search_fields=['client_name']
admin.site.register(Client, client_admin) 

class recip_admin(admin.ModelAdmin):
    search_fields=['name', 'crp_id']
admin.site.register(Recipient, recip_admin)

#this one look a but weird if you have time go back to it
class lobby_admin(admin.ModelAdmin):
    search_fields=['lobbyist_name', 'PAC_name']
admin.site.register(Lobbyist, lobby_admin)

class meta_admin(admin.ModelAdmin):
    search_fields=['link']
admin.site.register(MetaData, meta_admin)

#would be good to add reg but it doesn't work
class gift_admin(admin.ModelAdmin):
    search_fields=['description', 'link']
admin.site.register(Gift, gift_admin)

class location_admin(admin.ModelAdmin):
    search_fields=['location', 'country_grouping']
admin.site.register(Location, location_admin)



#class contact_admin(admin.ModelAdmin):
	#search_fields=['description']
admin.site.register(Contact) #, contact_admin)

admin.site.register(Payment)

admin.site.register(Disbursement)

admin.site.register(Contribution)

admin.site.register(ClientReg)





    