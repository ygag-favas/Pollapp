from django.contrib import admin
from django.http import HttpResponse
from django_otp.admin import OTPAdminSite
from django.urls import path, reverse
from django.utils.html import format_html
from django_otp.plugins.otp_email.models import EmailDevice
from django_otp.plugins.otp_static.models import StaticDevice, StaticToken
from django_otp.plugins.otp_totp.models import TOTPDevice

admin.site.__class__ = OTPAdminSite


class TOTPDevices(TOTPDevice):
    class Meta:
        proxy = True
        verbose_name = 'TOTPDevice'
        verbose_name_plural = 'TOTPDevices'


class StaticDevices(StaticDevice):
    class Meta:
        proxy = True
        verbose_name = 'StaticDevice'
        verbose_name_plural = 'StaticDevices'


class EmailDevices(EmailDevice):
    class Meta:
        proxy = True
        verbose_name = 'EmailDevice'
        verbose_name_plural = 'EmailDevices'


class StaticTokenInline(admin.TabularInline):
    model = StaticToken
    extra = 0


class StaticDeviceAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'confirmed']

    fieldsets = [
        ('Identity', {
            'classes': ('grp-collapse grp-open',),
            'fields': ['user', 'name', 'confirmed'],
        }),
    ]
    raw_id_fields = ['user']

    inlines = [
        StaticTokenInline,
    ]


class EmailDeviceAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'confirmed']
    fieldsets = [
        ('Identity', {
            'fields': ['user', 'name', 'confirmed'],
        }),
        ('Configuration', {
            'fields': ['email'],
        }),
    ]

    raw_id_fields = ['user']


class TOTPDeviceAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'confirmed', 'qrcode_link']

    fieldsets = [
        ('Identity', {
            'fields': ['user', 'name', 'confirmed'],
        }),
        ('Configuration', {
            'fields': ['key', 'step', 't0', 'digits', 'tolerance'],
        }),
        ('State', {
            'fields': ['drift'],
        }),
        ('Throttling', {
            'fields': ['throttling_failure_timestamp',
                       'throttling_failure_count'],
        }),
        (None, {
            'fields': ['qrcode_link'],
        }),
    ]
    raw_id_fields = ['user']
    readonly_fields = ['qrcode_link']
    radio_fields = {'digits': admin.HORIZONTAL}

    def qrcode_link(self, device):
        try:
            href = reverse('admin:otp_totp_totpdevice_config',
                           kwargs={'pk': device.pk})
            link = format_html('<a href="{}">qrcode</a>', href)
        except Exception:
            link = ''

        return link

    qrcode_link.short_description = "QR Code"

    def qrcode_view(self, request, pk):
        device = TOTPDevice.objects.get(pk=pk)
        try:
            import qrcode
            import qrcode.image.svg

            img = qrcode.make(device.config_url,
                              image_factory=qrcode.image.svg.SvgImage)
            response = HttpResponse(content_type='image/svg+xml')
            img.save(response)
        except ImportError:
            response = HttpResponse('', status=503)

        return response

admin.site.unregister(TOTPDevice)
admin.site.unregister(EmailDevice)
admin.site.unregister(StaticDevice)
admin.site.register(TOTPDevices, TOTPDeviceAdmin)
admin.site.register(EmailDevices, EmailDeviceAdmin)
admin.site.register(StaticDevices, StaticDeviceAdmin)

